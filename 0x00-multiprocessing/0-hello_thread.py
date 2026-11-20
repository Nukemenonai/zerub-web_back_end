#!/usr/bin/env python3
"""Task 0 — run a callable in a new thread and return the started Thread."""
import threading  # noqa: F401


def run_in_thread(target, args):
    """Start `target(*args)` in a new threading.Thread and return it.

    The returned Thread must already be started. The caller is responsible
    for joining it. The function must not block waiting for `target` to
    finish.
    """
    thread = threading.Thread(target=target, args=args)
    return thread