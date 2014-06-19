#!/usr/bin/env python

# Bootstrap script (python 2.x). Creates home symlinks for files with '.symlink'
# appended to them. Handles symlinked files, directories and symlinked 
# files inside non symlinked directories.

# TODO handle existing targets. (backup? overwrite?)
# TODO handle symlinked files inside symlinked directories. Right now, it
# does nothing for files that are under a symlinked directory. (Can you even
# symlink under a symlink?)

import sys, os
from argparse import ArgumentParser

def get_args():
    parser = ArgumentParser(description="bootstrap script for dotfiles")
    parser.add_argument("-d", "--dotfiles", help="dotfiles directory path")
    args = parser.parse_args()
    if not args.dotfiles:
        print "dotfiles is required argument"
        sys.exit()
    return args

def make_links(symlinks, int_dirs):
    if len(int_dirs) != 0:
        print "Found intermediate directories:"
        for dir in int_dirs:
            print 'Create', dir, '(y/n)?'
            ch = raw_input()
            if ch=='y':
                try:
                    os.makedirs(dir)
                except Exception as err:
                    print 'Couldn\'t create directory', dir, ';', err
                    continue
                print 'Created', dir
            else:
                print 'Directory not created.'
                continue

    print "Found", len(symlinks), "links to create; create all (y/n)?"
    ch = raw_input()
    if ch == 'y':
        for target, linkname in symlinks.iteritems():
            try:
                os.symlink(target, linkname)
            except Exception as err:
                print 'Couldn\'t create symlink for', target, ';', err
                continue
            else:
                print 'Created link', linkname, '-->', target
    else:
        print 'No links created.'


def main():
    args = get_args()
    HOMEDIR = os.path.expanduser('~')
    HOMEDIR = os.path.abspath(HOMEDIR)
    DOTFILES = os.path.abspath(args.dotfiles)
    try:
        listing = os.listdir(DOTFILES)
    except Exception as e:
        print e
        sys.exit()

    all_items = []
    for dirpath, dirnames, filenames in os.walk(DOTFILES):
        if '.symlink' in dirpath:
            # parent directory is itself is a symlink. Ignoring all files
            # underneath it.
            continue
        for name in filenames+dirnames:
            all_items.append(os.path.join(dirpath, name))

    symlink_destinations = [x for x in all_items if '.symlink' in x]
    home_links = [x.replace(DOTFILES, HOMEDIR) for x in symlink_destinations]

    # dict has key == target, value == link name
    symlink_dict = {}
    for x in symlink_destinations:
        link_dir, link_name = os.path.split(x)
        link_name = link_name.replace('.symlink', '')
        actual_link = os.path.join(link_dir, link_name)
        actual_link = actual_link.replace(DOTFILES, HOMEDIR)
        symlink_dict[x] = actual_link

    intermediate_directories = set([os.path.dirname(x) for x in home_links if os.path.dirname(x) != HOMEDIR])

    make_links(symlink_dict, intermediate_directories)

if __name__ == "__main__":
    main()
