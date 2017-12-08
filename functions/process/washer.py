# !/usr/bin/env python2
# -*- coding: utf-8 -*-
from clear_data import filter_latex_html
import re
import jieba
def segment_sentence(x):
    """
    "\t".join(["\t".join(jieba.cut(sentence)) for sentence in x.split('\t')])
    """
    step1 = re.compile(' +')
    step2 = re.compile(' [0-9](?=[A-Z])')
    try:
        words = " ".join([" ".join(jieba.cut(sentence)) for sentence in x.split('\t')])
        words = step1.sub(' ', words)
        words = step2.sub(' ', words)
        return words
    except Exception, e:
        return x


def clear_words(words):
    words = filter_latex_html(words)
    words = segment_sentence(words)
    return words