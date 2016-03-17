#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import print_function
import os
import re
import commands
from os.path import join

is_debug = False


def debug(msg):
    if is_debug:
        print(msg)


def get_images():
    outputs = commands.getstatusoutput("docker images")
    if outputs[0] != 0:
        raise Exception(output)
    images = []
    pat = re.compile(r'^([^\s]+)')
    for line in outputs[1].split("\n")[1:]:
        ret = pat.search(line)
        if ret is not None:
            name = ret.groups()[0]
            if name != '<none>':
                images.append(name)
    return images


def save(base):
    for name in get_images():
        cmd = '''docker save "{}" > {}'''.format(name, join(base, name))
        if is_debug:
            debug(cmd)
        outputs = commands.getstatusoutput(cmd)
        if outputs[0] != 0:
            raise Exception(cmd, outputs)


def load(base):
    for fname in os.listdir(base):
        print(fname)
        cmd = '''docker load < "{}"'''.format(join(base, fname))
        if is_debug:
            debug(cmd)
        outputs = commands.getstatusoutput(cmd)
        if outputs[0] != 0:
            raise Exception(cmd, outputs)


def main():
    global is_debug
    import argparse
    parser = argparse.ArgumentParser(description='docker cache controller')

    subparsers = parser.add_subparsers()
    loader = subparsers.add_parser('load')
    loader.set_defaults(func=load)

    saver = subparsers.add_parser('save')
    saver.set_defaults(func=save)

    for p in (loader, saver):
        p.add_argument(
            '--cache', nargs=1, help='path to image cache directory'
        )
        p.add_argument(
            '--debug', action='store_true'
        )

    args = parser.parse_args()
    is_debug = args.debug
    args.func(args.cache[0])

if __name__ == '__main__':
    main()
