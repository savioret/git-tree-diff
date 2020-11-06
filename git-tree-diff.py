#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import collections
import argparse
import re

class FileTreeDict:
    def __init__(self, tree, spaces, utf8):
        self.tree = tree
        self.spaces = spaces
        self.utf8 = utf8


    def line_symbol(self, last):
        if last:
            c = "└─" if self.utf8 else "\- ";
        else:
            c =  "├─" if self.utf8 else "|- ";

        return (" "*self.spaces) + c

    def indent_symbol(self, last):
        if last:
            c = "";
        else:
            c =  "│ " if self.utf8 else "| ";
        return (" "*self.spaces) + c

    def print_node(self, node, name, depth, indent, last = False):
        suffix = ''
        line = indent
        if depth:
            line += self.line_symbol(last)
            indent += self.indent_symbol(last)

        if not isinstance(node, int):
            suffix += '/'
        print(line+name+suffix);
        if not isinstance(node, int):
            treelen = len(node)
            i = 1
            for key, val in node.items():
                self.print_node(val, key, depth+1, indent, i == treelen)
                i += 1

    def show(self):
        for key, val in self.tree.items():
            self.print_node(val, key, 0, "", True);

def paths_to_dict(paths, add_status = False):
    paths.sort()
    if add_status:
        paths = append_file_status(paths)
        paths = encode_file_renames(paths)

    stack = []
    d = collections.OrderedDict()
    paths = filter(None, paths)
    for p in paths:
        path_arr = p.split('/')
        plen = len(path_arr)
        if add_status:
            path_arr[plen-1] = decode_file_rename(path_arr[plen-1])

        auxd = d
        depth = 0
        for tk in path_arr:
            if tk in auxd:
                pass
            else:
                if depth == plen-1:
                    auxd[tk] = 0
                else:
                    auxd[tk] = {}
            auxd = auxd[tk]
            parent_tk = tk
            depth += 1

    return d

def append_file_status(paths_list):
    return list(map(lambda n: re.sub(r'([A-Z])(?:[0-9]{0,3})([\t\s]+)([^\t\s]+(?:[\s\t]+[^\t\s]+)?)', r'\3[\1]', n), paths_list))

def encode_file_renames(paths_list):
    space = '#@@#';
    a = list(map(lambda n: re.sub(r'([^\t\s]+)([\s\t]+)([^\t\s]+)', '\\1'+space+'\\3', n), paths_list))
    for i in range(len(a)):
        p = a[i]
        if space in p:
            tk = p.split(space)
            rename = tk[1].replace('/', "#&&#");
            a[i] = tk[0]+space+rename

    return a

def decode_file_rename(path):
    sep = '#@@#';
    return path.replace(sep, " -> ").replace("#&&#", '/');

def get_head_revision():
    return subprocess.check_output(('git', 'rev-parse', 'HEAD')).decode().replace("\n", "")

def process_branch_diff(branch, fromrev, add_status, nspaces, utf8):

    if fromrev == 'HEAD':
        fromrev = get_head_revision()

    proc = subprocess.Popen(('git', 'rev-list', '--boundary', fromrev+'...'+branch), stdout=subprocess.PIPE)
    proc1 = subprocess.Popen(("grep", "^-"), stdin=proc.stdout, stdout=subprocess.PIPE)
    proc2 = subprocess.Popen(('cut', "-c2-"), stdin=proc1.stdout, stdout=subprocess.PIPE)
    output = subprocess.check_output(('head', "-n1"), stdin=proc2.stdout).decode()
    proc2.wait()

    lines = output.split('\n')
    if len(lines) and len(lines[0]):
        branchnode = lines[0]
        tilde = '~' if fromrev in branchnode else ''
        file_mode = '--name-status' if add_status else '--name-only'
        output = subprocess.check_output(('git', 'diff', file_mode, branchnode+tilde+'..'+fromrev)).decode()
        files = output.split('\n')
        arr = paths_to_dict(files, add_status)

        FileTreeDict(arr, nspaces, utf8).show()


def process_diff(revs, add_status, nspaces, utf8):

    rev0 = revs[0]
    if len(revs) > 1:
        rev1 = revs[1]
    else:
        rev1 = 'HEAD'

    if rev0 == 'HEAD':
        rev0 = get_head_revision()
    if rev1 == 'HEAD':
        rev1 = get_head_revision()

    file_mode = '--name-status' if add_status else '--name-only'
    tilde = '~' if (rev0 in rev1) or (rev1 in rev0) else ''
    output = subprocess.check_output(('git', 'diff', file_mode, rev0+tilde+'..'+rev1)).decode()
    files = output.split('\n')
    arr = paths_to_dict(files, add_status)
    FileTreeDict(arr, nspaces, utf8).show()



def main():
    parser = argparse.ArgumentParser(description = 'Shows a tree-form view of modified files in a branch or within a range of revisions')
    parser.add_argument('-s', '--status', help = 'Include file status occured in the diff', action='store_true')
    parser.add_argument('-u', '--utf8', help = 'Use utf8 characters for tree nodes', action='store_true', default=False)
    parser.add_argument('-n', '--nspaces', metavar='num', help = 'Number of spaces in each depth level', type=int, default=4)
    group1 = parser.add_argument_group('Ancestor mode', 'Show modified files in the current branch')
    group1.add_argument('-b', '--branch', help='Base branch or revision, must be an ancestor of <from>. It finds the oldest common ancestor between the branch and the HEAD of current branch')
    group1.add_argument('-f', '--from', metavar='rev', dest='revfrom', help='Revision from which to obtain the changes. If not provided, uses the HEAD of the current branch.', default='HEAD')
    group2 = parser.add_argument_group('Revision diff', 'Show modified files between two arbitrary revisions')
    group2.add_argument('-r', '--rev', metavar='rev', nargs='+', help='Revisions to compare with. If only one revision is specified then that revision is compared to the working directory, and, when no revisions are specified, the working directory files are compared to its first parent')

    args = parser.parse_args()
    # print(args)

    if args.rev is None:
        return process_branch_diff(args.branch, args.revfrom, args.status, args.nspaces, args.utf8)
    else:
        return process_diff(args.rev, args.status, args.nspaces, args.utf8)


if __name__ == "__main__":
    main()

