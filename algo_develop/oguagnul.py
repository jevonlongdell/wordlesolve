#!/usr/bin/env python

import math
import wordfreq 
import re
from multiprocessing import Pool, cpu_count
import os

def translate(intxt):
    words = intxt.split()
    outtxt = ""
    for inword in words: 
        outword = ''
        for ch in list(inword):
            if ch=='a':
                outword+='u'
            elif ch=='e':
                outword+='o'
            elif ch=='o':
                outword+='e'
            elif ch=='u':
                outword+='a'
            elif ch=='A':
                outword+='U'
            elif ch=='E':
                outword+='O'
            elif ch=='O':
                outword+='E'
            elif ch=='U':   
                outword+='A'
            else:
                outword+=(ch)
        outtxt += outword[::-1] + " "
    return outtxt.strip()
        
        
lang='en'



if __name__ == "__main__":
    words = {}
    
    #for w in wordfreq.iter_wordlist(lang):
    for w in map(lambda x: x.strip(), open('/usr/share/dict/words','r').readlines()):
        translated = translate(w)
        if w==translated:
            print("%s  <-> %s"%(w,w))
        words[w] = translate(w)
    

    print()
    print()
    print("Pairs:")
    for w in words:
        if translate(w) in words:
            print(w,' <-> ', translate(w))

    while True:
        w = input("Enter txt: ")
        print("-> ",translate(w))
 


