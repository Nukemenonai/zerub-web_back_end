#!/usr/bin/env python3
"""Task 0 driver: prints the facts of 0-Dockerfile that the spec fixes.

Run ./0-main.py from this folder. It prints your file, then a Dockerfile text built into
the driver (shell-form CMD, an unpinned image, a backslash continuation), then a file that
does not exist (only the exception name).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = """\
FROM python
# comment lines are not instructions
RUN pip install \\
    --no-cache-dir -r requirements.txt
CMD python app/main.py
"""


def instructions(text):
    """Return [(NAME, args)] with comments dropped and backslash lines joined."""
    out, buf = [], ''
    for line in text.splitlines():
        line = line.strip()
        if not buf and (not line or line.startswith('#')):
            continue
        if line.endswith('\\'):
            buf += line[:-1].rstrip() + ' '
            continue
        name, _, args = (buf + line).partition(' ')
        out.append((name.upper(), args.strip()))
        buf = ''
    return out


def show(text):
    """Print the facts of the Dockerfile `text`."""
    ins = instructions(text)
    names = [n for n, _ in ins]
    print('stages: %d' % names.count('FROM'))
    for name, args in ins:
        if name == 'FROM':
            print('from: ' + args.split()[0])
        elif name == 'WORKDIR':
            print('workdir: ' + args)
        elif name == 'ENV':
            print('env: ' + args)
        elif name == 'EXPOSE':
            print('expose: ' + args)
        elif name == 'RUN' and 'pip install' in args:
            print('pip install: --no-cache-dir ' + ('yes' if '--no-cache-dir' in args else 'no'))
        elif name == 'CMD':
            try:
                print('cmd: %s (exec form)' % json.loads(args))
            except ValueError:
                print('cmd: %s (shell form)' % args)
    order = []
    for name, args in ins:
        if name == 'COPY' and 'requirements.txt' in args:
            order.append('COPY requirements.txt')
        elif name == 'RUN' and 'pip install' in args:
            order.append('RUN pip install')
        elif name == 'COPY':
            order.append('COPY ' + args.split()[0])
    print('order: ' + ', '.join(order))


def run(path):
    """Show the Dockerfile at `path`; print the exception name if it cannot be read."""
    try:
        with open(path, encoding='utf-8') as f:
            show(f.read())
    except OSError as err:
        print(type(err).__name__)


if __name__ == '__main__':
    run(os.path.join(HERE, '0-Dockerfile'))
    show(EDGE)
    run(os.path.join(HERE, 'no-such-file'))
