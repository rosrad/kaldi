// SCTP multi-stream server.
// gcc -o sctpsrvr sctpsrvr.c -lsctp
// Ref: http://www.ibm.com/developerworks/library/l-sctp/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <errno.h>
#include <signal.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netinet/sctp.h>

#define MAX_BUFFER       1024
#define MY_PORT_NUM      3000
#define LOCALTIME_STREAM 0
#define GMT_STREAM       1

int main()
{
    int listenSock, connSock, ret;
    struct sockaddr_in servaddr;
    struct sctp_initmsg initmsg;
    char buffer[MAX_BUFFER+1];
    time_t currentTime;

    // ignore SIGPIPE
    signal(SIGPIPE, SIG_IGN);

    // Create SCTP TCP-Style Socket
    listenSock = socket(AF_INET, SOCK_STREAM, IPPROTO_SCTP);

    // Accept connections from any interface
    bzero((void *)&servaddr, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    servaddr.sin_port = htons(MY_PORT_NUM);

    ret = bind(listenSock, (struct sockaddr *)&servaddr, sizeof(servaddr));

    // Specify that a maximum of 5 streams will be available per socket
    memset(&initmsg, 0, sizeof(initmsg));
    initmsg.sinit_num_ostreams = 5;
    initmsg.sinit_max_instreams = 5;
    initmsg.sinit_max_attempts = 4;
    ret = setsockopt(listenSock, IPPROTO_SCTP, SCTP_INITMSG,
                      &initmsg, sizeof(initmsg));

    // Place the server socket into the listening state
    listen(listenSock, 5);
    printf("Listening on 0.0.0.0:%d ...\n", MY_PORT_NUM);

    while(1) {
        connSock = accept(listenSock, (struct sockaddr *)NULL, (socklen_t *)NULL);
        printf("Accepted a new connection: %d\n", connSock);

        // Grab the current time
        currentTime = time(NULL);

        // Send local time on stream LOCALTIME_STREAM
        snprintf(buffer, MAX_BUFFER, "%s", ctime(&currentTime));
        ret = sctp_sendmsg(connSock, (void *)buffer, (size_t)strlen(buffer),
                            NULL, 0, 0, 0, LOCALTIME_STREAM, 0, 0);
        if(ret == -1) {
            printf("sctp_sendmsg error: %s\n", strerror(errno));
            close(connSock);
            continue;
        }

        // Send GMT on stream GMT_STREAM
        snprintf(buffer, MAX_BUFFER, "%s", asctime(gmtime(&currentTime)));
        ret = sctp_sendmsg(connSock, (void *)buffer, (size_t)strlen(buffer),
                            NULL, 0, 0, 0, GMT_STREAM, 0, 0);
        if(ret == -1) {
            printf("sctp_sendmsg error: %s\n", strerror(errno));
            close(connSock);
            continue;
        }

        close(connSock);
    }

    return 0;
}
