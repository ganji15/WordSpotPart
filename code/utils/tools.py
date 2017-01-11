##!/usr/bin/env python
## coding=utf-8

import random
import jieba
import word2vec
import numpy
from scipy import stats

word2vec_model = word2vec.load('corpusWord2Vec.bin')
label_dict = [ u'业务品种',   u'方向    ', u'期限    ', 
              u'利率    ', u'金额    ', u'类型    ', 
              u'交易对象',  u'评级', u'债券发性']


def shuffle(lol, seed):
    '''
    lol :: list of list as input
    seed :: seed the shuffling

    shuffle inplace each list in the same order
    '''
    for l in lol:
        random.seed(seed)
        random.shuffle(l)


def minibatch(l, bs):
    '''
    l :: list of word idxs
    return a list of minibatches of indexes
    which size is equal to bs
    border cases are treated as follow:
    eg: [0,1,2,3] and bs = 3
    will output:
    [[0],[0,1],[0,1,2],[1,2,3]]
    '''
    out  = [l[:i] for i in xrange(1, min(bs,len(l)+1) )]
    out += [l[i-bs:i] for i in xrange(bs,len(l)+1) ]
    assert len(l) == len(out)
    return out


def contextwin(l, win):
    '''
    win :: int corresponding to the size of the window
    given a list of indexes composing a sentence
    it will return a list of list of indexes corresponding
    to context windows surrounding each word in the sentence
    '''
    assert (win % 2) == 1
    assert win >=1
    l = list(l)

    lpadded = win/2 * [-1] + l + win/2 * [-1]
    out = [ lpadded[i:i+win] for i in range(len(l)) ]

    assert len(out) == len(l)
    return out


def isWordAllnum(word):
    for ch in word:
        if not (ch in [u'0', u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9', u'.', u'-']):
            return False

    return True


def embdingWords(idxs):
    num_word = len(idxs)
    vecmat = numpy.zeros((num_word, 100))
    for i, idx in enumerate(idxs):
        vecmat[i] = word2vec_model.vectors[idx]

    return vecmat


def preProcessSentence(sentence):
    sentence = sentence.replace(u'M', u'万')
    sentence = sentence.replace(u'Y', u'亿')
    sentence = sentence.replace(u'D', u'天')
    return sentence


def formatSample(sentence, labels=None):
    
    try:
        sentence = preProcessSentence(sentence.decode('utf-8'))
        print sentence.decode('utf-8')
    except UnicodeEncodeError, e:
        pass

    wordlist = jieba.cut(sentence, cut_all=False)
    words = [word for word in wordlist]
    idxs = []
    rt_labels = []
    start_id = 0
    for word in words:
        if labels:
            label = stats.mode(labels[start_id : start_id + len(word)])[0][0]
            start_id += len(word)
            try:
                print word, label
            except UnicodeEncodeError, e:
                print label
            
            rt_labels.append(label)


        if isWordAllnum(word):
            word = word2vec_model.vocab[4]
        
        try:
            idx =word2vec_model.ix(word)
        except KeyError, e:
            idx = 5 

        idxs.append(idx)
        

    return words, idxs, rt_labels


def formatDataset(path):
    import cPickle
    data = cPickle.load(open(path, 'rb'))
    data = data[:800]

    xs = []
    ys = []
    xstrs = []
    for sentence, labels in data:
        x_str, x, y = formatSample(sentence, labels)

        xstrs.append(x_str)
        xs.append(x)
        ys.append(y)

    cPickle.dump([xstrs, [xs], [ys]], open('data/zhdata.pkl', 'w'))
    print 'save model: data/zhdata.pkl'


def loadTestdata(path):
    import cPickle
    data = cPickle.load(open(path, 'rb'))
    data = data[800:]

    xs = []
    xstrs = []
    for sentence, labels in data:
        x_str, x, y = formatSample(sentence, labels)

        xstrs.append(x_str)
        xs.append(x)

    return xstrs, [xs]


def print_pred(pred, words):
    strs = []
    for j in xrange(len(words)):
        #print 'wj-i', words[j - 1]
                
        if (j > 0 and j <= (len(words) - 1)) and \
            isWordAllnum(words[j - 1]):
            pred[j - 1] = pred[j]
            #print 'set: ', words[j - 1], 'to: %s'%label_dict[pred[j]]


    for i in xrange(len(label_dict)):
        strs.append(''.join(words[j] for j in xrange(len(words)) if pred[j] == i))

    
    for i in xrange(len(label_dict)):
        print label_dict[i], ':', strs[i]