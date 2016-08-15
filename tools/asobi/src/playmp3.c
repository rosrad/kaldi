// playmp3.c: play an mp3 audio file.
// It read mp3 data from stdin.
//
// Compile:
// $ gcc -o playmp3 playmp3.c libplaypcm.c -lasound -lmad
//
// Usage:
// $ ./playmp3 < foo.mp3
//
// References:
// http://www.underbit.com/products/mad/
// http://www.bsd-dk.dk/~elrond/audio/madlld/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <unistd.h>
#include <mad.h>
#include <alsa/asoundlib.h>
#include "libplaypcm.h"

static signed short MadFixedToSshort(mad_fixed_t Fixed)
{
    if(Fixed>=MAD_F_ONE)
        return(SHRT_MAX);
    if(Fixed<=-MAD_F_ONE)
        return(-SHRT_MAX);

    Fixed=Fixed>>(MAD_F_FRACBITS-15);
    return((signed short)Fixed);
}

static int PrintFrameInfo(FILE *fp, struct mad_header *Header)
{
    const char *Layer, *Mode, *Emphasis;

    switch(Header->layer)
    {
        case MAD_LAYER_I:
            Layer="I";
            break;
        case MAD_LAYER_II:
            Layer="II";
            break;
        case MAD_LAYER_III:
            Layer="III";
            break;
        default:
            Layer="(unexpected layer value)";
            break;
    }

    switch(Header->mode)
    {
        case MAD_MODE_SINGLE_CHANNEL:
            Mode="single channel";
            break;
        case MAD_MODE_DUAL_CHANNEL:
            Mode="dual channel";
            break;
        case MAD_MODE_JOINT_STEREO:
            Mode="joint (MS/intensity) stereo";
            break;
        case MAD_MODE_STEREO:
            Mode="normal LR stereo";
            break;
        default:
            Mode="(unexpected mode value)";
            break;
    }

    /* Convert the emphasis to it's printed representation. Note that
     * the MAD_EMPHASIS_RESERVED enumeration value appeared in libmad
     * version 0.15.0b.
     */
    switch(Header->emphasis)
    {
        case MAD_EMPHASIS_NONE:
            Emphasis="no";
            break;
        case MAD_EMPHASIS_50_15_US:
            Emphasis="50/15 us";
            break;
        case MAD_EMPHASIS_CCITT_J_17:
            Emphasis="CCITT J.17";
            break;
#if (MAD_VERSION_MAJOR>=1) || \
    ((MAD_VERSION_MAJOR==0) && (MAD_VERSION_MINOR>=15))
        case MAD_EMPHASIS_RESERVED:
            Emphasis="reserved(!)";
            break;
#endif
        default:
            Emphasis="(unexpected emphasis value)";
            break;
    }

    fprintf(fp,"player: %lu kb/s audio MPEG layer %s stream %s CRC, "
            "%s with %s emphasis at %d Hz sample rate\n",
            Header->bitrate, Layer,
            Header->flags & MAD_FLAG_PROTECTION ? "with" : "without",
            Mode, Emphasis, Header->samplerate);
    return ferror(fp);
}

#define INPUT_BUFFER_SIZE   (5*8192)

static int MpegAudioDecode(FILE *InputFp)
{
    pcm_player          *player;

    struct mad_stream   Stream;
    struct mad_frame    Frame;
    struct mad_synth    Synth;

    unsigned char       InputBuffer[INPUT_BUFFER_SIZE + MAD_BUFFER_GUARD];

    unsigned char       *OutputBuffer = NULL;
    unsigned char       *OutputPtr = NULL;
    unsigned char       *OutputBufferEnd = NULL;

    int                 Status = 0, i;

    unsigned long       FrameCount = 0;

    // initialize libmad
    mad_stream_init(&Stream);
    mad_frame_init(&Frame);
    mad_synth_init(&Synth);

    do
    {
        if(Stream.buffer == NULL || Stream.error == MAD_ERROR_BUFLEN)
        {
            size_t ReadSize, Remaining;
            unsigned char *ReadStart;

            if(Stream.next_frame != NULL)  // there is data remaining
            {
                Remaining = Stream.bufend - Stream.next_frame;
                memmove(InputBuffer, Stream.next_frame, Remaining);
                ReadStart = InputBuffer + Remaining;
                ReadSize = INPUT_BUFFER_SIZE - Remaining;
            }
            else
            {
                ReadSize = INPUT_BUFFER_SIZE;
                ReadStart = InputBuffer;
                Remaining = 0;
            }

            ReadSize = fread(ReadStart, 1, ReadSize, InputFp);
            if(ReadSize <= 0)
            {
                if(ferror(InputFp))
                {
                    fprintf(stderr,"error: read error on bit-stream (%s)\n",
                            strerror(errno));
                    Status = 1;
                }
                if(feof(InputFp))
                    fprintf(stderr,"error: end of input stream\n");
                break;
            }

            mad_stream_buffer(&Stream, InputBuffer, ReadSize + Remaining);
            Stream.error = 0;
        }

        // decode one frame
        if(mad_frame_decode(&Frame, &Stream))
        {
            if(MAD_RECOVERABLE(Stream.error))
            {
                if(Stream.error != MAD_ERROR_LOSTSYNC)
                {
                    fprintf(stderr,"error: recoverable frame level error\n");
                    fflush(stderr);
                }
                continue;
            }
            else
            {
                if(Stream.error == MAD_ERROR_BUFLEN)
                    continue;
                else
                {
                    fprintf(stderr,"error: unrecoverable frame level error\n");
                    Status=1;
                    break;
                }
            }
        }

        // if it's the 0th frame, print some information
        if(FrameCount == 0) {
            if(PrintFrameInfo(stderr, &Frame.header))
            {
                Status = 1;
                break;
            }

            int framerate = Frame.header.samplerate;
            int nchannels = MAD_NCHANNELS(&Frame.header);
            int sampwidth = 2;

            player = pcm_player_init(framerate, nchannels, sampwidth);
            if(player == NULL) {
                fprintf(stderr, "error: can't init pcm_player\n");
                Status = 1;
                break;
            }

            OutputBuffer = player->buffer;
            OutputPtr = OutputBuffer;
            OutputBufferEnd = OutputBuffer + player->buffersize;
        }

        FrameCount++;

        mad_synth_frame(&Synth, &Frame);

        // output
        for(i = 0; i < Synth.pcm.length; i++)
        {
            signed short Sample;

            // left channel
            Sample = MadFixedToSshort(Synth.pcm.samples[0][i]);
            *(OutputPtr++) = Sample & 0xff;  // little endian
            *(OutputPtr++) = Sample >> 8;

            // right channel
            if(MAD_NCHANNELS(&Frame.header) == 2) {
                Sample = MadFixedToSshort(Synth.pcm.samples[1][i]);
                *(OutputPtr++) = Sample & 0xff;  // little endian
                *(OutputPtr++) = Sample >> 8;
            }

            // flush OutputBuffer if it is full
            if(OutputPtr == OutputBufferEnd)
            {
                int cnt = pcm_player_write(player, player->buffer);
                if(cnt == 0) {
                    Status = 2;
                    break;
                }
                OutputPtr = OutputBuffer;
            }
        }
    } while(1);

    // fixme: it's possible that OutputBuffer is not empty

    mad_synth_finish(&Synth);
    mad_frame_finish(&Frame);
    mad_stream_finish(&Stream);

    pcm_player_free(player);

    return Status;
}

int main(int argc, char *argv[])
{
    return MpegAudioDecode(stdin);
}
