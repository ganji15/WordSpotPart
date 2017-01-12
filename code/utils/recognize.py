##!/usr/bin/env python
#coding=gbk

import os
import numpy

from keras.models import model_from_json
from utils.tools import formatSample, embdingWords, get_pred

model = None

if os.path.exists('model.json'):
    model =  model_from_json(open('model.json').read())  
    model.load_weights('model.h5')
    formatSample(u'初始化模型')

def recognize(sentence):
    x_str, x, _ = formatSample(sentence)
    X = numpy.asarray([embdingWords(x)])     
    pred = model.predict_on_batch(numpy.asarray(X)).argmax(2)[0]

    return get_pred(pred, x_str)