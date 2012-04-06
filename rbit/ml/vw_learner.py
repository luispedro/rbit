# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

import subprocess
from os import path

def _maybemkdir(dir):
    from os import makedirs
    try:
        makedirs(dir)
    except OSError:
        pass

_basedir = path.expanduser('~/.local/share/rbit/vw/')
_maybemkdir(_basedir)

def _fixl(l):
    if l is None:
        return ""
    def fixs(s):
        return s.encode('utf-8').replace(':','_').replace('|','_')
    return ":1 ".join(map(fixs, l.split()))

class VWModel(object):
    def __init__(self, cache_file, model_file):
        self.cache_file = cache_file
        self.model_file = model_file

    def apply(self, message):
        proc = subprocess.Popen(['./vw',
            '-t',
            '--initial_regressor', self.model_file,
            '-r', '/dev/stdout',
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
        print >>proc.stdin, "0", \
            "|body", _fixl(message.body), \
            "|subject", _fixl(message.subject)

        proc.stdin.close()
        res = proc.stdout.read()
        res = float(res)
        return res


class VWLearner(object):
    def __init__(self, basedir=_basedir):
        self.basedir = basedir
        self.passes = 2
        self.ngram = 3

    def train(self, messages, labels, name, normalisedlabels):
        assert normalisedlabels
        assert max(labels) == 1
        model_file = path.join(self.basedir, '%s.model' % name)
        cache_file = path.join(self.basedir, '%s.cache' % name)
        proc = subprocess.Popen(['./vw',
            '--cache_file', cache_file,
            '--adaptive',
            '--final_regressor', model_file,
            '--ngram', str(self.ngram),
            '--passes', str(self.passes)
            ],
            stdin=subprocess.PIPE)
        for message,ell in zip(messages,labels):
            print >>proc.stdin, \
                ("1" if ell else "-1"), \
                "|body", _fixl(message.body), \
                "|subject", _fixl(message.subject)
        proc.stdin.close()
        proc.wait()
        return VWModel(cache_file, model_file)
