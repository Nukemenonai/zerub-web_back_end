#!/usr/bin/env python3
"""Driver for task 0 — hello from a thread."""
import threading

run_in_thread = __import__('0-hello_thread').run_in_thread


def worker(n, name):
    """Print a hello message identifying the thread and its argument."""
    print("worker: hello from thread {} with arg={}".format(name, n))


if __name__ == '__main__':
    print("main: before")
    t = run_in_thread(worker, (42, "MainWorker"))
    assert isinstance(t, threading.Thread), "must return a Thread"
    t.join()
    print("main: after")
