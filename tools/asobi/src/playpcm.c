// playpcm.c: play raw PCM sound data.
// It reads PCM data from stdin.
//
// Compile:
// $ gcc -o playpcm playpcm.c libplaypcm.c -lasound
// 
// Usage:
// $ ./playpcm sample_rate channels seconds < file
// 
// Examples:
// $ ./playpcm 44100 2 5 < /dev/urandom
// $ ./playpcm 22050 1 8 < foo.pcm
//
// References:
// http://users.suse.com/~mana/alsa090_howto.html
// http://www.alsa-project.org/main/index.php/FramesPeriods
// https://gist.github.com/ghedo/963382

#include <stdio.h>
#include <unistd.h>
#include "libplaypcm.h"

int main(int argc, char **argv) {
    int framerate, nchannels, sampwidth;
    pcm_player *player;

    if (argc < 4) {
        printf("Usage: %s SampleRate Channels SampleWidth\n", argv[0]);
        return -1;
    }

    framerate = atoi(argv[1]);
    nchannels = atoi(argv[2]);
    sampwidth = atoi(argv[3]);

    // create a player
    player = pcm_player_init(framerate, nchannels, sampwidth);
    if(player == NULL) {
        fprintf(stderr, "error: can't init pcm_player\n");
        return 1;
    }

    // play
    pcm_player_play(player, STDIN_FILENO);

    // finish
    pcm_player_free(player);

    return 0;
}
