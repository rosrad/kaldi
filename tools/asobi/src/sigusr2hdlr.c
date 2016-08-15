
static void sigusr2_cb(struct ev_loop *loop, ev_signal *watcher, int revents)
{
    int pipefd[2], rpipe, wpipe;
    pid_t child;
    char *binfile;
    char fdbuf[16];
    static ev_io rpipe_watcher;

    PFatal("caught signal %s\n", strsignal(watcher->signum));

    // create a pair of pipes
    if (pipe(pipefd) == -1)
    {
        PError("failed to create pipes: %s\n", strerror(errno));
        return;
    }
    rpipe = pipefd[0];
    wpipe = pipefd[1];

    child = fork();
    if(child == -1)
    {
        PError("failed to fork: %s\n", strerror(errno));
    }
    else if(child == 0)
    {
        PDebug("In child: pid=%d, ppid=%d\n", getpid(), getppid());

        close(rpipe);

        // get executable file path
        binfile = program_path();
        if(binfile == NULL)
        {
            PError("failed to exec: %s\n", strerror(errno));
            exit(1);
        }

        // set environment variables
        sprintf(fdbuf, "%d", wpipe);
        setenv("INIT_ACK_PIPE", fdbuf, 1);

        sprintf(fdbuf, "%d", state.server.sockfd);
        setenv("SERVER_SOCKFD", fdbuf, 1);

        // exec
        if(execv(binfile, state.argv) == -1)
        {
            PError("failed to exec: %s\n", strerror(errno));

            write(wpipe, "F", 1);
            close(wpipe);

            _exit(1);
        }
    }
    else
    {
        PDebug("In parent: pid=%d, ppid=%d\n", getpid(), getppid());

        close(wpipe);

        if(set_nonblocking(rpipe, 1) == -1)
        {
            PError("set_nonblocking error: %s\n", strerror(errno));
            close(rpipe);
            return;
        }

        ev_io_init(&rpipe_watcher, rpipe_on_read, rpipe, EV_READ);
        ev_io_start(state.loop, &rpipe_watcher);
    }
}
