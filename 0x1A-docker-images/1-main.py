#!/usr/bin/env python3
"""Task 1 driver: prints the facts of 1-Dockerfile and .dockerignore that the spec fixes
(for .dockerignore, which of the four required patterns it lists).

Run ./1-main.py from this folder. It prints your files, then a single-stage Dockerfile
built into the driver, then a file that does not exist (only the exception name).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = """\
FROM python:3.12-slim
RUN pip install -r requirements.txt
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
    """Print the facts of each stage of the Dockerfile `text`."""
    stage = 0
    for name, args in instructions(text):
        if name == 'FROM':
            stage += 1
            print('stage %d: %s' % (stage, ' '.join(args.split())))
        elif name == 'COPY' and args.startswith('--from='):
            print('  copy from %s' % args.split(None, 1)[0][len('--from='):] + ': ' +
                  args.split(None, 1)[1])
        elif name == 'RUN' and 'pip install' in args:
            print('  pip install: yes')
        elif name == 'USER':
            print('  user: ' + args)
        elif name == 'HEALTHCHECK':
            print('  healthcheck: yes')
        elif name == 'EXPOSE':
            print('  expose: ' + args)
        elif name == 'CMD':
            try:
                print('  cmd: %s (exec form)' % json.loads(args))
            except ValueError:
                print('  cmd: %s (shell form)' % args)


def run(path):
    """Show the Dockerfile at `path`; print the exception name if it cannot be read."""
    try:
        with open(path, encoding='utf-8') as f:
            show(f.read())
    except OSError as err:
        print(type(err).__name__)


def ignored(path):
    """Print the patterns of the .dockerignore at `path`, sorted."""
    try:
        with open(path, encoding='utf-8') as f:
            lines = [x.strip() for x in f.read().splitlines()]
    except OSError as err:
        print(type(err).__name__)
        return
    wanted = ('.git', '.venv', '__pycache__', '.env')
    print('.dockerignore has: ' + (' '.join(sorted(x for x in wanted if x in lines)) or 'none'))


if __name__ == '__main__':
    run(os.path.join(HERE, '1-Dockerfile'))
    ignored(os.path.join(HERE, '.dockerignore'))
    show(EDGE)
    run(os.path.join(HERE, 'no-such-file'))
