##!/usr/bin/env python
#coding=gbk

import cPickle
import numpy as np
import time
import sys
import os
import random

from utils.tools import embdingWords, loadTestdata, formatSample, get_pred
from utils.Wr_Excel import write_excel

from keras.models import Sequential, model_from_json
from keras.layers import (Input, Embedding, SimpleRNN, Dense, Activation,
                          TimeDistributed, Bidirectional, Input)


if __name__ == '__main__':

    model =  model_from_json(open('model.json').read())  
    model.load_weights('model.h5')  

    trainset = loadTestdata('w_a_t')
    train_str = trainset[0]
    [train_lex] = trainset[1] 
    nsentences = len(train_lex)

    results = []
    for i in xrange(nsentences):
        X = np.asarray([embdingWords(train_lex[i])])
        if X.shape[1] == 1:
            continue # bug with X, Y of len 1
        pred = model.predict_on_batch(np.asarray(X)).argmax(2)[0]
        #print ' '.join(train_str[i])

        strs = get_pred(pred, train_str[i])
        results.append([[''.join(train_str[i])], strs])

    print 'write over...'
    write_excel(results)
