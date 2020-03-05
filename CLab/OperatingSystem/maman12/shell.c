// Name: Yehonathan Jacob
// ID: 316304740
// Date: 29/12/2019
// Description: This library create a shell promot that can thred jobs and and control the process of them.
// TODO: - fill the missing parts
//       - write Makefile with 'shell' executable as a target
#include <ctype.h>
#include <errno.h>
#include <fcntl.h>
#include <glob.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/wait.h>
#include <unistd.h>

#define MAX_COMMAND_LEN 250     /* max length of a single command 
                                   string */
#define JOB_STATUS_FORMAT "[%d] %-22s %.40s\n"



struct jobSet {
    struct job * head;      /* head of list of running jobs */
    struct job * fg;        /* current foreground job */
};


struct childProgram {
    pid_t pid;              /* 0 if exited */
    char ** argv;           /* program name and arguments */
    int numRedirections;    /* elements in redirection array */

    glob_t globResult;      /* result of parameter globbing */
    int freeGlob;           /* should we globfree(&globResult)? */
    int isStopped;          /* is the program currently running? */
};

struct job {
    int jobId;              /* job number */
    int numProgs;           /* total number of programs in job */
    int runningProgs;       /* number of programs running */
    char * text;            /* name of job */
    char * cmdBuf;          /* buffer various argv's point into */
    pid_t pgrp;             /* process group ID for the job */
    struct childProgram * progs; /* array of programs in job */
    struct job * next;      /* to track background commands */
    int stoppedProgs;       /* number of programs alive, but stopped */
};

void freeJob(struct job * cmd) {
    int i;

    for (i = 0; i < cmd->numProgs; i++) {
        free(cmd->progs[i].argv);
//        if (cmd->progs[i].redirections) free(cmd->progs[i].redirections);
        if (cmd->progs[i].freeGlob) globfree(&cmd->progs[i].globResult);
    }
    free(cmd->progs);
    if (cmd->text) free(cmd->text);
    free(cmd->cmdBuf);
}

int getCommand(FILE * source, char * command) {
    if (source == stdin) {
        printf("# ");
        fflush(stdout);
    }

    if (!fgets(command, MAX_COMMAND_LEN, source)) {
        if (source == stdin) printf("\n");
        return 1;
    }

    /* remove trailing newline */
    command[strlen(command) - 1] = '\0';

    return 0;
}

void globLastArgument(struct childProgram * prog, int * argcPtr,
                        int * argcAllocedPtr) {
    int argc = *argcPtr;
    int argcAlloced = *argcAllocedPtr;
    int rc;
    int flags;
    int i;
    char * src, * dst;

    if (argc > 1) {             /* cmd->globResult is already initialized */
        flags = GLOB_APPEND;
        i = prog->globResult.gl_pathc;
    } else {
        prog->freeGlob = 1;
        flags = 0;
        i = 0;
    }

    rc = glob(prog->argv[argc - 1], flags, NULL, &prog->globResult);
    if (rc == GLOB_NOSPACE) {
        fprintf(stderr, "out of space during glob operation\n");
        return;
    } else if (rc == GLOB_NOMATCH || 
               (!rc && (prog->globResult.gl_pathc - i) == 1 && 
                !strcmp(prog->argv[argc - 1], 
                        prog->globResult.gl_pathv[i]))) {
        /* we need to remove whatever \ quoting is still present */
        src = dst = prog->argv[argc - 1];
        while (*src) {
            if (*src != '\\') *dst++ = *src;
            src++;
        }
        *dst = '\0';
    } else if (!rc) {
        argcAlloced += (prog->globResult.gl_pathc - i);
        prog->argv = realloc(prog->argv, argcAlloced * sizeof(*prog->argv));
        memcpy(prog->argv + (argc - 1), prog->globResult.gl_pathv + i,
                sizeof(*(prog->argv)) * (prog->globResult.gl_pathc - i));
        argc += (prog->globResult.gl_pathc - i - 1);
    }

    *argcAllocedPtr = argcAlloced;
    *argcPtr = argc;
}

/* Return cmd->numProgs as 0 if no command is present (e.g. an empty
   line). If a valid command is found, commandPtr is set to point to
   the beginning of the next command (if the original command had more 
   then one job associated with it) or NULL if no more commands are 
   present. */
int parseCommand(char ** commandPtr, struct job * job, int * isBg) {
    char * command;
    char * returnCommand = NULL;
    char * src, * buf, * chptr;
    int argc = 0;
    int done = 0;
    int argvAlloced;
    int i;
    char quote = '\0';  
    int count;
    struct childProgram * prog;

    /* skip leading white space */
    while (**commandPtr && isspace(**commandPtr)) (*commandPtr)++;

    /* this handles empty lines and leading '#' characters */
        if (!**commandPtr || (**commandPtr=='#')) {
        job->numProgs = 0;
        *commandPtr = NULL;
        return 0;
    }

    *isBg = 0;
    job->numProgs = 1;
    job->progs = malloc(sizeof(*job->progs));

    /* We set the argv elements to point inside of this string. The 
       memory is freed by freeJob(). 

       Getting clean memory relieves us of the task of NULL 
       terminating things and makes the rest of this look a bit 
       cleaner (though it is, admittedly, a tad less efficient) */
    job->cmdBuf = command = calloc(1, strlen(*commandPtr) + 1);
    job->text = NULL;

    prog = job->progs;
    prog->numRedirections = 0;
//    prog->redirections = NULL;
    prog->freeGlob = 0;
    prog->isStopped = 0;

    argvAlloced = 5;
    prog->argv = malloc(sizeof(*prog->argv) * argvAlloced);
    prog->argv[0] = job->cmdBuf;

    buf = command;
    src = *commandPtr;
    while (*src && !done) {
        if (quote == *src) {
            quote = '\0';
        } else if (quote) {
            if (*src == '\\') {
                src++;
                if (!*src) {
                    fprintf(stderr, "character expected after \\\n");
                    freeJob(job);
                    return 1;
                }

                /* in shell, "\'" should yield \' */
                if (*src != quote) *buf++ = '\\';
            } else if (*src == '*' || *src == '?' || *src == '[' || 
                       *src == ']')
                *buf++ = '\\';
            *buf++ = *src;
        } else if (isspace(*src)) {
            if (*prog->argv[argc]) {
                buf++, argc++;
                /* +1 here leaves room for the NULL which ends argv */
                if ((argc + 1) == argvAlloced) {
                    argvAlloced += 5;
                    prog->argv = realloc(prog->argv, 
				    sizeof(*prog->argv) * argvAlloced);
                }
                prog->argv[argc] = buf;

                globLastArgument(prog, &argc, &argvAlloced);
            }
        } else switch (*src) {


          case '|':                         /* pipe */
            /* finish this command */
            if (*prog->argv[argc]) argc++;
            if (!argc) {
                fprintf(stderr, "empty command in pipe\n");
                freeJob(job);
                return 1;
            }
            prog->argv[argc] = NULL;

            /* and start the next */
            job->numProgs++; 
            job->progs = realloc(job->progs, 
                                 sizeof(*job->progs) * job->numProgs);
            prog = job->progs + (job->numProgs - 1);
            prog->numRedirections = 0;
//            prog->redirections = NULL;
            prog->freeGlob = 0;
            argc = 0;

            argvAlloced = 5;
            prog->argv = malloc(sizeof(*prog->argv) * argvAlloced);
            prog->argv[0] = ++buf;

            src++;
            while (*src && isspace(*src)) src++;

            if (!*src) {
                fprintf(stderr, "empty command in pipe\n");
                return 1;
            }
            src--;              /* we'll ++ it at the end of the loop */

            break;

          case '&':                         /* background */
            *isBg = 1;
          case ';':                         /* multiple commands */
            done = 1;
            returnCommand = *commandPtr + (src - *commandPtr) + 1;
            break;


          default:
            *buf++ = *src;
        }

        src++;
    }

    if (*prog->argv[argc]) {
        argc++;
        globLastArgument(prog, &argc, &argvAlloced);
    }
    if (!argc) {
        freeJob(job);
        return 0;
    }
    prog->argv[argc] = NULL;

    if (!returnCommand) {
        job->text = malloc(strlen(*commandPtr) + 1);
        strcpy(job->text, *commandPtr);
    } else {
        /* This leaves any trailing spaces, which is a bit sloppy */

        count = returnCommand - *commandPtr;
        job->text = malloc(count + 1);
        strncpy(job->text, *commandPtr, count);
        job->text[count] = '\0';
    }

    *commandPtr = returnCommand;

    return 0;
}


int runCommand(struct job newJob, struct jobSet * jobList, 
               int inBg) {
    struct job * job;
    char * newdir, * buf;
    int i, len;
    int nextin, nextout;
    int pipefds[2];             /* pipefd[0] is for reading */
    char * statusString;
    int jobNum;

    /* handle built-ins here -- we don't fork() so we can't background
       these very easily */
    if (!strcmp(newJob.progs[0].argv[0], "exit")) {
        /* this should return a real exit code */
        exit(0);
    } else if (!strcmp(newJob.progs[0].argv[0], "pwd")) {
        len = 50;
        buf = malloc(len);
        while (!getcwd(buf, len) && errno == ERANGE) {
            len += 50;
            buf = realloc(buf, len);
        }
        printf("%s\n", buf);
        free(buf);
        return 0;
    } else if (!strcmp(newJob.progs[0].argv[0], "cd")) {
        if (!newJob.progs[0].argv[1] == 1) 
            newdir = getenv("HOME");
        else 
            newdir = newJob.progs[0].argv[1];
        if (chdir(newdir)) 
            printf("failed to change current directory: %s\n",
                    strerror(errno));
        return 0;
    } else if (!strcmp(newJob.progs[0].argv[0], "jobs")) {
        // FILL IN HERE
        //For each job, check if it is running or not
        for(job = jobList->head; job!= NULL; job=job->next) {
            // while statusString is one of the {Stopped, Running}
            statusString = (job->runningProgs == job->stoppedProgs)? "Stopped" : "Running";
            printf(JOB_STATUS_FORMAT, job->jobId, statusString, job->text);
        }
        return 0;
    } else if (!strcmp(newJob.progs[0].argv[0], "fg") ||
               !strcmp(newJob.progs[0].argv[0], "bg")) {
 
        // FILL IN HERE
        int i,jobID,isTooBig = newJob.progs[0].argv[1] == NULL || newJob.progs[0].argv[2] != NULL;
        int ;
        char *arg1;
        char * expected;

        // First of all do some syntax checking. 
        // If the syntax check fails return 1
        if (isTooBig)
        {
            fprintf(stderr, "%s: Required only one argument.\n", newJob.progs[0].argv[0]);
            return 1;
        }
        arg1 = newJob.progs[0].argv[1];
        for(i=0;arg1[i];i++)
        {
            if ((i==0 && arg1[i] != '%') || (i!=0 && !isdigit(arg1[i])))
            {
                expected = (i==0 && arg1[i] != '%')? "%":"digit";
                fprintf(stderr, "%s: Wrong char at index: %d,expected: '%s' got: '%c'\n", newJob.progs[0].argv[0],i,expected,arg1[i]);
                return 1;
            }
        }
        
    	// else find the job in the job list 
        jobID = atoi(arg1+1);
        for(job=jobList->head; job && job->jobId!=jobID; job=job->next);
        // If job not found return 1
        if(!(job))
        {
            fprintf(stderr, "%s: Error in getting job number: %d.\n", newJob.progs[0].argv[0], jobID);
            return 1;
        }
    	// If strcmp(newJob.progs[0].argv[0] == "f"
        if(strcmp(newJob.progs[0].argv[0] , "fg"))
        {
            // Don't forget to update the fg field in jobList
            jobList->fg=job;
            // then put the job you found in the foreground (use tcsetpgrp)
            if (tcsetpgrp(0, job->pgrp))
            {
                fprintf(stderr, "Error in tcsetpgrp function.\n");
                perror("Error tcsetpgrp");
                return 1;
            }
        }
    	
    	// In any case restart the processes in the job by calling kill(-job->pgrp, SIGCONT).
        if(kill(job->pgrp, SIGCONT)) {
            fprintf(stderr, "Error in trying to continue job number %d.\n", jobID);
            perror('Error kill');
            return 1;
        }
    	// Don't forget to set isStopped = 0 in every proicess
        for(i=0; i<job->numProgs; i++)
            job->progs[i].isStopped=0;
        // and stoppedProgs = 0 in the job
        job->stoppedProgs=0;

        return 0;
    }

    nextin = 0, nextout = 1;
    for (i = 0; i < newJob.numProgs; i++) {
        if ((i + 1) < newJob.numProgs) {
            pipe(pipefds);
            nextout = pipefds[1];
        } else {
            nextout = 1;
        }

        if (!(newJob.progs[i].pid = fork())) {
            signal(SIGTTOU, SIG_DFL);

            if (nextin != 0) {
                dup2(nextin, 0);
                close(nextin);
            }

            if (nextout != 1) {
                dup2(nextout, 1);
                close(nextout);
            }


	    signal (SIGINT, SIG_DFL);
	    signal (SIGQUIT, SIG_DFL);
	    signal (SIGTSTP, SIG_DFL);
	    signal (SIGTTIN, SIG_DFL);
	    signal (SIGTTOU, SIG_DFL);
	    signal (SIGCHLD, SIG_DFL);
            
	    setpgid(newJob.progs[i].pid, newJob.progs[0].pid);
            
	    execvp(newJob.progs[i].argv[0], newJob.progs[i].argv);
            fprintf(stderr, "exec() of %s failed: %s\n", 
                    newJob.progs[i].argv[0], 
                    strerror(errno));
            exit(1);
        }

        /* put our child in the process group whose leader is the
           first process in this pipe */
        setpgid(newJob.progs[i].pid, newJob.progs[0].pid);

        if (nextin != 0) close(nextin);
        if (nextout != 1) close(nextout);

        /* If there isn't another process, nextin is garbage 
           but it doesn't matter */
        nextin = pipefds[0];
    }

    newJob.pgrp = newJob.progs[0].pid;

    /* find the ID for the job to use */
    newJob.jobId = 1;
    for (job = jobList->head; job; job = job->next)
        if (job->jobId >= newJob.jobId)
            newJob.jobId = job->jobId + 1;

    /* add the job to the list of running jobs */
    if (!jobList->head) {
        job = jobList->head = malloc(sizeof(*job));
    } else {
        for (job = jobList->head; job->next; job = job->next);
        job->next = malloc(sizeof(*job));
        job = job->next;
    }

    *job = newJob;
    job->next = NULL;
    job->runningProgs = job->numProgs;
    job->stoppedProgs = 0;

    if (inBg) {
        /* we don't wait for background jobs to return -- append it 
           to the list of backgrounded jobs and leave it alone */

        printf("[%d] %d\n", job->jobId, 
               newJob.progs[newJob.numProgs - 1].pid);
    } else {
        jobList->fg = job;

        /* move the new process group into the foreground */
        
        if (tcsetpgrp(0, newJob.pgrp))
            perror("tcsetpgrp");
    }

    return 0;
}

void removeJob(struct jobSet * jobList, struct job * job) {
    struct job * prevJob;

    freeJob(job); 
    if (job == jobList->head) {
        jobList->head = job->next;
    } else {
        prevJob = jobList->head;
        while (prevJob->next != job) prevJob = prevJob->next;
        prevJob->next = job->next;
    }

    free(job);
}

/* Checks to see if any background processes have exited -- if they 
   have, figure out why and see if a job has completed */
void checkJobs(struct jobSet * jobList) {
    struct job * job;
    pid_t childpid;
    int status;
    int progNum;
   
    while ((childpid = waitpid(-1, &status, WNOHANG | WUNTRACED)) > 0) {
        for (job = jobList->head; job; job = job->next) {
            progNum = 0;
            while (progNum < job->numProgs && 
                        job->progs[progNum].pid != childpid)
                progNum++;
            if (progNum < job->numProgs) break;
        }

        if (WIFEXITED(status) || WIFSIGNALED(status)) {
            /* child exited */
            job->runningProgs--;
            job->progs[progNum].pid = 0;

            if (!job->runningProgs) {
                printf(JOB_STATUS_FORMAT, job->jobId, "Done", job->text);
                removeJob(jobList, job);
            }
        } else {
            /* child stopped */
            job->stoppedProgs++;
            job->progs[progNum].isStopped = 1;

            if (job->stoppedProgs == job->numProgs) {
                printf(JOB_STATUS_FORMAT, job->jobId, "Stopped", job->text);
            }
        }
    }

    if (childpid == -1 && errno != ECHILD)
        perror("waitpid");
}

int main(int argc, char ** argv) {
    char command[MAX_COMMAND_LEN + 1];
    char * nextCommand = NULL;
    struct jobSet jobList = { NULL, NULL };
    struct job newJob;
    FILE * input = stdin;
    int i;
    int status;
    int inBg;

    if (argc > 2) {
        fprintf(stderr, "unexpected arguments; usage: "
                        "<commands>\n");
        exit(1);
    } else if (argc == 2) {
        input = fopen(argv[1], "r");
        if (!input) {
            perror("fopen");
            exit(1);
        }
    }


    signal (SIGINT, SIG_IGN);
    signal (SIGQUIT, SIG_IGN);
    signal (SIGTSTP, SIG_IGN);
    signal (SIGTTIN, SIG_IGN);
    signal (SIGTTOU, SIG_IGN);  
 
    while (1) {
        if (!jobList.fg) {
            /* no job is in the foreground */

            /* see if any background processes have exited */
            checkJobs(&jobList);

            if (!nextCommand) {
                if (getCommand(input, command)) break;
                nextCommand = command;
            }

            if (!parseCommand(&nextCommand, &newJob, &inBg) &&
                              newJob.numProgs) {
                runCommand(newJob, &jobList, inBg);
            }
        } else {
            /* a job is running in the foreground; wait for it */
            i = 0;
            while (!jobList.fg->progs[i].pid ||
                   jobList.fg->progs[i].isStopped) i++;

            waitpid(jobList.fg->progs[i].pid, &status, WUNTRACED);

            if (WIFEXITED(status) || WIFSIGNALED(status)) {
                /* the child exited */
                jobList.fg->runningProgs--;
                jobList.fg->progs[i].pid = 0;
            
                if (!jobList.fg->runningProgs) {
                    /* child exited */

                    removeJob(&jobList, jobList.fg);
                    jobList.fg = NULL;

                    /* move the shell to the foreground */
                    if (tcsetpgrp(0, getpid()))
                        perror("tcsetpgrp");
                }
            } else {
                /* the child was stopped */
                jobList.fg->stoppedProgs++;
                jobList.fg->progs[i].isStopped = 1;

                if (jobList.fg->stoppedProgs == jobList.fg->runningProgs) {
                    printf("\n" JOB_STATUS_FORMAT, jobList.fg->jobId, 
                                "Stopped", jobList.fg->text);
                    jobList.fg = NULL;
                }
            }

            if (!jobList.fg) {
                /* move the shell to the foreground */
                if (tcsetpgrp(0, getpid()))
                    perror("tcsetpgrp");
            }
        }
    }

    return 0;
}
