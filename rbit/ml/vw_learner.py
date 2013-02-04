# Copyright (C) 2012-2013 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

import subprocess
from os import path
from rbit.decode import decode_unicode
import logging

_vw_path = 'vw'
log = logging

def _as_features(l):
    '''
    features = _as_features(str)

    Format as features.
    '''
    if l is None:
        return ""
    def fixs(s):
        assert type(s) == unicode
        return s.replace(':','_').replace('|','_')
    tokens = map(fixs, l.split())
    tokens.append('')
    single = u":1 ".join(tokens)
    return single.encode('utf-8')


def _formatted_headers(headers):
    keys = headers.keys()
    keys.sort()
    res = []
    for k in keys:
        v = headers[k]
        k = decode_unicode(k)
        v = map(decode_unicode, v)
        v = u' '.join(v)
        res.append(k.decode('utf-8'))
        res.append(v)
    return _as_features(u" ".join(res))

def _output_message(output, message, label):
    from rbit.html2text import html2text
    output.write('{0} |subject {1} |from {2} |to {3} |headers {4}|body {5}\n'.format(
                label,
                _as_features(message.subject),
                _as_features(message.from_),
                _as_features(message.recipients),
                _formatted_headers(message.headers),
                _as_features(html2text(message.body)),
                ))

def _parse_label(s):
    s = s.strip()
    return int(float(s)), 1.0

class VWModel(object):
    def __init__(self, cache_file, model_file, names):
        self.cache_file = cache_file
        self.model_file = model_file
        self.names = names

    def apply(self, message):
        args = [_vw_path,
            '-t',
            '--initial_regressor', self.model_file,
            '-p', '/dev/stdout',
            '--quiet',
            ]
        log.info('Executing {}'.format(' '.join(args)))
        proc = subprocess.Popen(args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
        _output_message(proc.stdin, message, 1)

        proc.stdin.close()
        label,strength = _parse_label(proc.stdout.read())
        return strength, self.names[label-1]


class VWLearner(object):
    def __init__(self, basedir):
        self.basedir = basedir
        self.passes = 2
        self.ngram = 3

    def train(self, mids, labels, create_session=None):
        from rbit import models
        names = list(set(labels))
        names.sort()
        labels = [names.index(ell) for ell in labels]

        model_file = path.join(self.basedir, 'model')
        cache_file = path.join(self.basedir, 'cache')
        args = [_vw_path,
            '--cache_file', cache_file,
            '--adaptive',
            '--ect',
            str(len(names)),
            '--final_regressor', model_file,
            '--ngram', str(self.ngram),
            '--passes', str(self.passes)
            ]
        log.info('Calling {}'.format(' '.join(args)))
        proc = subprocess.Popen(args, stdin=subprocess.PIPE)
        for mid,ell in zip(mids,labels):
            message = models.Message.load_by_mid(mid, create_session)
            _output_message(proc.stdin, message, ell + 1)
        proc.stdin.close()
        proc.wait()
        return VWModel(cache_file, model_file, names)
