#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <alsa/asoundlib.h>

int main()
{
    int portid;
    snd_seq_t *seq_handle;
    snd_seq_event_t ev;
 
    if (snd_seq_open(&seq_handle, "hw", SND_SEQ_OPEN_DUPLEX, 0) < 0) {
        fprintf(stderr, "Error opening ALSA sequencer.\n");
        exit(1);
    }
 
    snd_seq_set_client_name(seq_handle, "Generated MIDI");
    
    portid = snd_seq_create_simple_port(seq_handle, "Generated MIDI Output",
          SND_SEQ_PORT_CAP_READ | SND_SEQ_PORT_CAP_SUBS_READ,
          SND_SEQ_PORT_TYPE_APPLICATION);
 
    if (portid < 0) {
        fprintf(stderr, "fatal error: could not open output port.\n");
        exit(1);
    }
 
    int i, ret;
    for(i = 0; i < 100; i++) {
        snd_seq_ev_clear(&ev);
        ret = snd_seq_event_output(seq_handle, &ev);
        printf("ret is %d\n", ret);
        sleep(1);
    }
 
    snd_seq_close(seq_handle);
 
    return 0;
}
