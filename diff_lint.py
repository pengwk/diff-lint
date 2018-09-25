# _*_ coding: utf-8 _*_

import json
import os
import sys
import time
from collections import defaultdict

import hglib
import unidiff
from pylint import epylint as lint


MERCURIAL = 'Mercurial'
GIT = 'Git'


def get_vcs_root(vcs_client):
    if isinstance(vcs_client, hglib.client.hgclient):
        return vcs_client.root()
    else:
        raise NotImplementedError


def initial_vcs_client(vcs_software, repo_root):
    if vcs_software == MERCURIAL:
        return hglib.open(repo_root)
    raise NotImplementedError


def get_diff(vcs_client, path_=None):
    # path is dir or file
    if isinstance(vcs_client, hglib.client.hgclient):
        return vcs_client.diff(files=[path_])
    else:
        raise NotImplementedError


def diff_lint(diff, repo_root):
    changed_files = defaultdict(set)
    patches = unidiff.PatchSet(diff)
    for patch in patches:
        # remove a, since patch.source_file == 'b/project/main.py'
        path = patch.target_file[1:]
        if path.endswith('.py'):
            for hunk in patch:
                end = hunk.target_start + hunk.target_length
                changed_files[path].update(
                    range(hunk.target_start, end))

    for file_, range_ in changed_files.items():
        start = time.time()
        cmd_tpl = '{file_name} --output-format=json'
        (pylint_stdout, __) = lint.py_run(
            cmd_tpl.format(file_name=repo_root + file_),
            return_std=True)
        for line in json.loads(pylint_stdout.buf):
            message_tpl = '{type_} -> {path}:{line} {message}.'
            if line['line'] in range_:
                print message_tpl.format(
                    type_=line['type'],
                    path=line['path'],
                    line=line['line'],
                    message=line['message'])
        seconds = time.time() - start
        print "Time spent: {seconds}s.\n".format(seconds=seconds)


def main():
    start_time = time.time()

    repo_root = os.popen('hg root').read().strip()
    if repo_root.startswith('abort'):
        print 'Not under a Mercurial Repository!'
        return

    if len(sys.argv) > 2:
        print "Only support one argument!"
        return
    
    arg = None
    if len(sys.argv) > 1:
        arg = sys.argv[1]
    
    vcs_client = initial_vcs_client(MERCURIAL, repo_root)
    diff = get_diff(vcs_client, arg)
    diff_lint(diff.decode('utf-8'), repo_root)
    end_time = time.time()
    print 'Time spent {}s.'.format(end_time - start_time)
