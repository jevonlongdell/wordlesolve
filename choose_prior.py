#!/usr/bin/env python

import math
import wordfreq 
import re
from multiprocessing import Pool, cpu_count
import os

from matplotlib.pyplot import *
import numpy as n
import wordle_lists


def is_5digit_lowercase(s):
        return re.match("^[a-z][a-z][a-z][a-z][a-z]$", s)



if __name__ == "__main__":
    words = {}
    Ndict = 100000
    probsum = 0

    for w in wordfreq.iter_wordlist('en'):
        if is_5digit_lowercase(w):
            words[w] = wordfreq.word_frequency(w,'en')
            probsum += words[w]
            if len(words)>=Ndict:
                break


    for (k,w) in enumerate(words):
            words[w] = k
            
    mystery_ranks = [words[w] for w in wordle_lists.mysterywords]
    
    figure(1)
    ion()
    hist(mystery_ranks,100)
   # figure(2)
    x = n.linspace(0,30000)
    plot(x,220*n.exp(-x/3000))
    show()

