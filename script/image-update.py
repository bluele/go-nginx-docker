#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import print_function
from hashlib import md5
from os.path import join, exists, expanduser, basename
import commands
import sys

is_debug = False
cache_dir = expanduser('~/cache')


def check_digest(name):
    digest_path = join(cache_dir, basename(name) + '.digest')
    if not exists(digest_path):
        return True

    with open(name) as r:
        current = md5(r.read()).hexdigest()
        with open(digest_path) as f:
            digest = f.read()
            if current != digest:
                return True

    return False


def check_digests(names):
    for name in names:
        if check_digest(name):
            if is_debug:
                print("{}'s digest has changed.".format(name))
            sys.exit(1)

    if is_debug:
        print("All digests have not changed.")
    sys.exit(0)


def save_digest(name):
    with open(name) as r:
        current = md5(r.read()).hexdigest()
        with open(join(cache_dir, basename(name) + '.digest'), 'wb') as f:
            f.write(current)


def save_digests(names):
    for name in names:
        save_digest(name)


def main():
    global is_debug
    import argparse
    parser = argparse.ArgumentParser(description='docker image update manager.')

    subparsers = parser.add_subparsers()
    loader = subparsers.add_parser('check')
    loader.set_defaults(func=check_digests)

    saver = subparsers.add_parser('save')
    saver.set_defaults(func=save_digests)

    for p in (loader, saver):
        p.add_argument(
            '--files', nargs='+'
        )
        p.add_argument(
            '--debug', action='store_true'
        )

    args = parser.parse_args()
    is_debug = args.debug
    args.func(args.files)

if __name__ == '__main__':
    main()
