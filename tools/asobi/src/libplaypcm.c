#include "libplaypcm.h"

pcm_player *pcm_player_init(int framerate, int nchannels, int sampwidth)
{
    pcm_player *player;
    int retval, format, buffsz;
    char *buff, *devname;
    snd_pcm_t *pcm_handle;
    snd_pcm_stream_t stream;
    snd_pcm_hw_params_t *hwparams;
    snd_pcm_uframes_t periodsize;

    // check parameters
    if(nchannels != 1 && nchannels != 2) {
        fprintf(stderr, "error: unsupported channels: %d\n", nchannels);
        return NULL;
    }

    if(sampwidth == 1)
        format = SND_PCM_FORMAT_U8;
    else if(sampwidth == 2)
        format = SND_PCM_FORMAT_S16_LE;
    else if(sampwidth == 3)
        format = SND_PCM_FORMAT_S24_LE;
    else if(sampwidth == 4)
        format = SND_PCM_FORMAT_S32_LE;
    else {
        fprintf(stderr, "error: unsupported sample width: %d\n", sampwidth);
        return NULL;
    }

    // allocate the structure
    player = (pcm_player*)malloc(sizeof(pcm_player));
    if(player == NULL)
        return NULL;


    // open the PCM device in playback mode
    devname = "default";
    stream = SND_PCM_STREAM_PLAYBACK;
    if((retval = snd_pcm_open(&pcm_handle, devname, stream, 0)) < 0) {
        fprintf(stderr, "error: can't PCM device: %s\n", snd_strerror(retval));
        free(player);
        return NULL;
    }

    // allocate parameters object and fill it with default values
    snd_pcm_hw_params_alloca(&hwparams);
    snd_pcm_hw_params_any(pcm_handle, hwparams);

    // set parameters
    if((retval = snd_pcm_hw_params_set_access(pcm_handle, hwparams, SND_PCM_ACCESS_RW_INTERLEAVED)) < 0) {
        fprintf(stderr, "error: can't set interleaved mode: %s\n", snd_strerror(retval));
        snd_pcm_close(pcm_handle);
        free(player);
        return NULL;
    }

    if ((retval = snd_pcm_hw_params_set_format(pcm_handle, hwparams, format)) < 0) {
        fprintf(stderr, "error: can't set format: %s\n", snd_strerror(retval));
        snd_pcm_close(pcm_handle);
        free(player);
        return NULL;
    }

    if ((retval = snd_pcm_hw_params_set_channels(pcm_handle, hwparams, nchannels)) < 0) {
        fprintf(stderr, "error: can't set channels: %s\n", snd_strerror(retval));
        snd_pcm_close(pcm_handle);
        free(player);
        return NULL;
    }

    if ((retval = snd_pcm_hw_params_set_rate_near(pcm_handle, hwparams, &framerate, 0)) < 0) {
        fprintf(stderr, "error: can't set rate: %s\n", snd_strerror(retval));
        snd_pcm_close(pcm_handle);
        free(player);
        return NULL;
    }

    periodsize = framerate / 10;
    if((retval = snd_pcm_hw_params_set_period_size(pcm_handle, hwparams, periodsize, 0)) < 0) {
        fprintf(stderr, "error: can't set period size: %s\n", snd_strerror(retval));
        snd_pcm_close(pcm_handle);
        free(player);
        return NULL;
    }

    // write parameters
    if ((retval = snd_pcm_hw_params(pcm_handle, hwparams)) < 0) {
        fprintf(stderr, "error: can't set hardware parameters: %s\n", snd_strerror(retval));
        snd_pcm_close(pcm_handle);
        free(player);
        return NULL;
    }

    // resume information
    printf("PCM name: %s\n", snd_pcm_name(pcm_handle));

    snd_pcm_hw_params_get_channels(hwparams, &nchannels);
    printf("channels: %i ", nchannels);
    if (nchannels == 1)
        printf("(mono)\n");
    else if (nchannels == 2)
        printf("(stereo)\n");

    snd_pcm_hw_params_get_rate(hwparams, &framerate, 0);
    printf("framerate: %d Hz\n", framerate);

    // allocate buffer to hold single period
    snd_pcm_hw_params_get_period_size(hwparams, &periodsize, 0);
    printf("period size: %d\n", periodsize);

    buffsz = sampwidth * nchannels * periodsize;
    printf("buffer size: %d\n", buffsz);

    buff = (char*)malloc(buffsz);
    if(buff == NULL) {
        fprintf(stderr, "error: can't allocate pcm buffer\n");
        snd_pcm_close(pcm_handle);
        free(player);
        return NULL;
    }

    // set player attributes
    player->pcm_handle = pcm_handle;
    player->framerate = framerate;
    player->nchannels = nchannels;
    player->sampwidth = sampwidth;
    player->periodsize = periodsize;
    player->buffersize = buffsz;
    player->buffer = buff;

    return player;
}

int pcm_player_write(pcm_player *player, const char *buff)
{
    int retval;

    retval = snd_pcm_writei(player->pcm_handle, buff, player->periodsize);
    if (retval == -EPIPE) {  // buffer underrun
        snd_pcm_prepare(player->pcm_handle);
        return 1;
    } else if (retval < 0) {
        fprintf(stderr, "error: can't write to PCM device: %s\n",
            snd_strerror(retval));
        return 0;
    }
}

void pcm_player_play(pcm_player *player, int fd)
{
    int retval;

    while(1) {
        retval = read(fd, player->buffer, player->buffersize);
        if(retval <= 0)
            break;

        retval = pcm_player_write(player, player->buffer);
        if(retval == 0)
            break;
    }
}

void pcm_player_free(pcm_player *player)
{
    snd_pcm_drain(player->pcm_handle);
    snd_pcm_close(player->pcm_handle);

    free(player->buffer);
    free(player);
}
