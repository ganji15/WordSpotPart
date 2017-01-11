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

    s = {'fold':3, # 5 folds 0,1,2,3,4
         'lr':0.1,
         'verbose':1,
         'nhidden':100, # number of hidden units
         'seed':345,
         'emb_dimension':100, # dimension of word embedding
         'nepochs':50}

    model =  model_from_json(open('model.json').read())  
    model.load_weights('model.h5')  

    #trainset = loadTestdata('E:/is13/E-DATA/w_a_t')
    #train_str = trainset[0]
    #[train_lex] = trainset[1] 
    #nsentences = len(train_lex)

    #for i in xrange(nsentences):
    #    X = np.asarray([embdingWords(train_lex[i])])
    #    if X.shape[1] == 1:
    #        continue # bug with X, Y of len 1
    #    pred = model.predict_on_batch(np.asarray(X)).argmax(2)[0]
    #    print ' '.join(train_str[i])

    #    print_pred(pred, train_str[i])
    #    raw_input()

    while True:
        str = raw_input(u'业务描述: '.encode('gb18030')).decode(sys.stdin.encoding or locale.getpreferredencoding(True))
        x_str, X, _ = formatSample(str)
        pred = model.predict_on_batch(np.asarray([embdingWords(X)])).argmax(2)[0]
        print '='*20
        print ' '.join(x_str)
        print '-'*20
        print_pred(pred, x_str)
        print '-'*20

