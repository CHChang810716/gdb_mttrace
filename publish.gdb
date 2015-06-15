python
import threading
import time
import re
import os
import gdb
import signal
from multiprocessing import Process

def tail(f, lines=1, _buffer=4098):
    """Tail a file and get X lines from the end"""
    # place holder for the lines found
    lines_found = []

    # block counter will be multiplied by buffer
    # to get the block size from the end
    block_counter = -1

    # loop until we find X lines
    while len(lines_found) < lines:
        try:
            f.seek(block_counter * _buffer, os.SEEK_END)
        except IOError:  # either file is too small, or too many lines requested
            f.seek(0)
            lines_found = f.readlines()
            break

        lines_found = f.readlines()

        # we found enough lines, get out
        if len(lines_found) > lines:
            break
        # decrement the block counter to get the
        # next X bytes
        block_counter -= 1
    return lines_found[-lines:]
def dbtimer(pid, trace_log, step_log):
    pidstr = str(pid)
#   gdb.write("pid : " + pidstr + " trace_log : " + str(trace_log) + '\n')
    f_size = -1;
    with open (trace_log, "r") as f:
        while(True):
            f.seek(0)
            gdb.flush()
        #if trace_log's last line is [Inferior 1 (process XXXX) exited normally] then break
            last = tail(f, 1)
            exit_pattern = "^\[.*exited normally.*\]$"
            prog = re.compile(exit_pattern)
            res = prog.match(last[0])
            if( res is not None ):
                break;
            #client program doesnt finish
            statinfo = os.stat(trace_log)
            if( f_size == statinfo.st_size ): #file dosen't bigger
            #set interrupt
                try:
                    os.kill(pid, signal.SIGINT)
                    step_log.write("SIGINT\n")
                except:
                    break
            else:
                f_size = statinfo.st_size
                time.sleep(0.3)
import random
def thread_switch(step_log):
    tids = gdb.selected_inferior().threads()
    this_thread = gdb.selected_thread ()
    if ( len(tids) >= 1 ):
        gdb_tid = tids[random.randrange(len(tids))].num
        if ( this_thread is None ):
            gdb.execute("thread " + str(gdb_tid))
            step_log.write("thread " + str(gdb_tid) + '\n')
        elif ( gdb_tid != this_thread.num ):
            gdb.execute("thread " + str(gdb_tid))
            step_log.write("thread " + str(gdb_tid) + '\n')
        return (True, gdb_tid)
    else:
        return (False, -1)
def mt_trace():
    step_log = open('step.log',  'a')
    gdb_log = 'gdb.log'
    gdb.execute("set logging file gdb.log")
    gdb.execute("set logging on")
    gdb.execute("start < undeterministic_input.dat 2> err.log 1> out.log")
    gdb.execute("set scheduler-locking on")
    inf = gdb.selected_inferior()
    pid = inf.pid
    p = Process(target=dbtimer, args=(pid, gdb_log, step_log))
    p.start()
    while True:
        if(thread_switch(step_log)[0] == False):
            break
        try:
            gdb.execute("si")
            step_log.write("si\n")
        except gdb.error as e:
            if(thread_switch(step_log)[0] == False):
                break
    step_log.close()
mt_trace()
