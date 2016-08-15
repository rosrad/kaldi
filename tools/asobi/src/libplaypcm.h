#ifndef __LIBPLAYPCM_H__
#define __LIBPLAYPCM_H__

#include <alsa/asoundlib.h>

typedef struct {
    snd_pcm_t *pcm_handle;
    int framerate;
    int nchannels;
    int sampwidth;
    int periodsize;
    int buffersize;
    char *buffer;
} pcm_player;

pcm_player *pcm_player_init(int framerate, int nchannels, int sampwidth);

int pcm_player_write(pcm_player *player, const char *buff);

void pcm_player_play(pcm_player *player, int fd);

void pcm_player_free(pcm_player *player);

#endif
