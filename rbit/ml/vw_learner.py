# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

import subprocess
from os import path

_vw_path = 'vw'

def _fixl(l):
    if l is None:
        return ""
    def fixs(s):
        return s.encode('utf-8').replace(':','_').replace('|','_')
    return ":1 ".join(map(fixs, l.split()))


def _output_message(output, message, label):
    print >>output, \
        label, \
        "|body", _fixl(message.body), \
        "|subject", _fixl(message.subject), \
        "|from", _fixl(message.from_), \
        "|to", _fixl(message.recipients)

class VWModel(object):
    def __init__(self, cache_file, model_file):
        self.cache_file = cache_file
        self.model_file = model_file

    def apply(self, message):
        proc = subprocess.Popen([_vw_path,
            '-t',
            '--initial_regressor', self.model_file,
            '-r', '/dev/stdout',
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
        _output_message(proc.stdin, message, 0)

        proc.stdin.close()
        res = proc.stdout.read()
        return float(res)


class VWLearner(object):
    def __init__(self, basedir):
        self.basedir = basedir
        self.passes = 2
        self.ngram = 3

    def train(self, mids, labels, name, normalisedlabels, create_session=None):
        from rbit import models
        assert normalisedlabels
        assert max(labels) == 1
        model_file = path.join(self.basedir, '%s.model' % name)
        cache_file = path.join(self.basedir, '%s.cache' % name)
        proc = subprocess.Popen([_vw_path,
            '--cache_file', cache_file,
            '--adaptive',
            '--final_regressor', model_file,
            '--ngram', str(self.ngram),
            '--passes', str(self.passes)
            ],
            stdin=subprocess.PIPE)
        for mid,ell in zip(mids,labels):
            message = models.Message.load_by_mid(mid, create_session)
            _output_message(proc.stdin, message, (1 if ell else -1))
        proc.stdin.close()
        proc.wait()
        return VWModel(cache_file, model_file)
