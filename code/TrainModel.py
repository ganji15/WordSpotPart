import cPickle
import numpy as np
import time
import sys
import os
import random

from utils.tools import shuffle

from utils.tools import embdingWords

from keras.models import Sequential, Model
from keras.layers import (Input, Embedding, SimpleRNN, Dense, Activation, merge, 
                          TimeDistributed, Input)
from keras.optimizers import SGD
from keras.utils.np_utils import to_categorical


if __name__ == '__main__':

    s = {'fold':3, # 5 folds 0,1,2,3,4
         'lr':0.1,
         'verbose':1,
         'nhidden':100, # number of hidden units
         'seed':345,
         'emb_dimension':100, # dimension of word embedding
         'nepochs':200}

    trainset = cPickle.load(open('zhdata.pkl' , 'r'))
    
    train_str = trainset[0]
    [train_lex] = trainset[1] 
    [train_y] = trainset[2]

    nclasses = 11
    nsentences = len(train_lex)

    # instanciate the model
    np.random.seed(s['seed'])
    random.seed(s['seed'])

    l_in = Input(shape=(None, s['emb_dimension']))
    l_fw = SimpleRNN(s['nhidden'], activation='sigmoid',
                        return_sequences=True)(l_in)
    l_bk = SimpleRNN(s['nhidden'], activation='sigmoid',
                        return_sequences=True, go_backwards=True)(l_in)
    bi_rnn = merge([l_fw, l_bk], mode='concat')

    l_dense = TimeDistributed(Dense(output_dim=nclasses))(bi_rnn)
    l_softmax = Activation("softmax")(l_dense)
    model = Model(input=[l_in], output=[l_softmax])
    model.summary()

    sgd = SGD(lr=s['lr'], momentum=0.0, decay=0.0, nesterov=False)
    model.compile(loss='categorical_crossentropy', optimizer=sgd,
                metrics=['accuracy'])

    # train with early stopping on validation set
    best_f1 = -np.inf
    for e in xrange(s['nepochs']):
        # shuffle
        shuffle([train_str, train_lex, train_y], s['seed'])
        s['ce'] = e
        tic = time.time()
        for i in xrange(nsentences):
            X = np.asarray([embdingWords(train_lex[i])])
            Y = to_categorical(np.asarray(train_y[i])[:, np.newaxis],
                                          nclasses)[np.newaxis, :, :]
            if X.shape[1] == 1:
                continue # bug with X, Y of len 1
            model.train_on_batch(X, Y)

            if s['verbose']:
                print '[learning] epoch %i >> %2.2f%%'%(e,(i+1)*100./nsentences),'completed in %.2f (sec) <<\r'%(time.time()-tic),
                sys.stdout.flush()

        if e % 10 == 0 and e > 0:
            all_count = 0
            acc_count = 0
            for i in xrange(nsentences):
                X = np.asarray([embdingWords(train_lex[i])])
                if X.shape[1] == 1:
                    continue # bug with X, Y of len 1
                pred = model.predict_on_batch(np.asarray(X)).argmax(2)[0]
                true = train_y[i]
                all_count += len(true)
                acc_count += sum(1 for i in xrange(len(true)) if pred[i] == true[i])

            cur_acc = (acc_count * 100. / all_count)
            print '\ntrain acc: %.2f%%'%cur_acc

            if cur_acc > best_f1:
                best_f1 = cur_acc
                json_string = model.to_json()  
                open('model.json','w').write(json_string)  
                model.save_weights('model.h5')
                print 'bese model save: model.json'
    