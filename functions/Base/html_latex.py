#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import re
patten1 = re.compile(r'<span class="latex">')
patten2 = re.compile(r'</span>')
def show_latex(word):
    word = patten1.sub(u'<img src="http://latex.codecogs.com/gif.latex?', word)
    word = patten2.sub(u'" />', word)
    return word
