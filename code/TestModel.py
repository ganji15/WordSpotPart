##!/usr/bin/env python
#coding=gbk

import cPickle
import numpy as np
import time
import sys
import os
import random


from recurrentshop.engine import RecurrentContainer
from recurrentshop.cells import SimpleRNNCell

from utils.tools import embdingWords, print_pred, loadTestdata, formatSample


from keras.models import Sequential, model_from_json
from keras.layers import (Input, Embedding, SimpleRNN, Dense, Activation,
                          TimeDistributed, Bidirectional, Input)


if __name__ == '__main__':

    model =  model_from_json(open('model.json').read())  
    model.load_weights('model.h5')  

    while True:
        str = raw_input(u'业务描述: '.encode('gb18030')).decode(sys.stdin.encoding or locale.getpreferredencoding(True))
        x_str, X, _ = formatSample(str)
        pred = model.predict_on_batch(np.asarray([embdingWords(X)])).argmax(2)[0]
        print '='*20
        print ' '.join(x_str)
        print '-'*20
        print_pred(pred, x_str)
        print '-'*20

