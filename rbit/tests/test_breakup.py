from rbit.imap import breakup
import random
from itertools import chain

def test_breakup():
    random.seed(34)
    for i in xrange(16):
        for n in [2,3,9,23,45,102]:
            values = [random.random() for i in xrange(n)]
            for b in [1,4,7,8]:
                assert list(chain(*breakup(values, b))) == values
