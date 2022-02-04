#! python3

import math
import wordfreq 
import re

def is_5digit_lowercase(s):
        return re.match("^[a-z][a-z][a-z][a-z][a-z]$", s)

words = {}
Ndict = 5000
probsum = 0
for w in wordfreq.iter_wordlist('en'):
    if is_5digit_lowercase(w):
        words[w] = wordfreq.word_frequency(w,'en')
        probsum += words[w]
        if len(words)>=Ndict:
            break


# read in the list of five letter words
#words = open('fiveletterwords','r').readlines()
#words = list(map(str.strip,words))

print()
print()

greenstring = input("Enter green letters. The ones you know for sure, put a dot for the ones you don't know (in form h.l..)\n> ");


if greenstring=='':
        greenstring='.....'


print()
print()
#priororange = []
#for k in range(5):
#    x = input("Enter the orange letters that have occured for letter number %d\n (just the letters, any order, no# spaces between them, just hit enter if there are none)\n> "%(k+1))
#    priororange.append(set(x))
orangestring = input('Enter orange letters for each of the five letters, separated by four spaces, dots ignored\n> ')
if orangestring=='':
        orangestring=". . . . ."


print()
print()
greystring = input('Enter letters not in word (the ones that appear grey, with no spaces between them, any order)\n just hit enter if there are none \n> ')


#what we know so far
priorgreen = list(greenstring)
priororange = list(map(set,orangestring.split(' ')))
priororange = [ s-set('.') for s in priororange]
priorgrey = set(greystring)


#priorgreen  = list('.i.es')
#priororange = list(map(set,"s,,,,n".split(',')))
#[set('sa'), set('a'), set(''), set(''), set('s')]
#priorgrey = set("lardtchpawfamd")


#workout list of compatible words

possiblewords = []

for w in words:
    wordletters = set(w) 
    contender = True
    
    for k in range(5):
        if priorgreen[k] != '.' and priorgreen[k] != w[k]:
            contender = False
            break

    if not contender:
         continue

    if not priorgrey.isdisjoint(set(w)):
         continue

    for k in range(5):
        for c in priororange[k]:
            if not c in wordletters - set( w[k] ):
                contender = False
                break
    
    if not contender:
        continue

    possiblewords.append(w)




N = len(possiblewords)

#initial entropy each of the N words equally likely so 
# Hinit = - \sum_{i=1}^N 1/N log 1/N
#       =   \sum_{i=1}^N 1/N log N
#       =    log(N)
#

if N!=0:
    Hinit = 0
    probsum=0
    for w in possiblewords:
        probsum+=words[w]
    for w in possiblewords:
        words[w] /= probsum
        Hinit = Hinit  - words[w] * math.log2 (words[w])
    print()
    print("Initial entropy = %g bits"%(Hinit,))

# normalise probabilites



if N==0:
    print('Couldn\'t find any compatible words?')
elif N==1:
    print("Done!")
    print(possiblewords)
else:
    Hvals = dict()
    Hbest = Hinit
    for guess in words:
        outcomes = dict()
        for mysteryword in possiblewords:
            green = ['.', '.', '.', '.', '.']
            orange = [set(), set(), set(), set(), set()]
            grey = set()
            for k in range(5):
                if mysteryword[k]==guess[k]:
                    green[k] = guess[k]
                elif guess[k] in mysteryword:
                    orange[k].add(guess[k])
                grey.add(guess[k])
            
            # green and orange into something that can be used
            # as an index in a dict
            green = "".join(green)
            orange = map(frozenset,orange)
            info = (green,tuple(map(tuple,orange)),frozenset(grey))

            #print(mysteryword,guess,info)
    
            if info in outcomes:
                outcomes[info].append(mysteryword)
            else:
                outcomes[info] = [mysteryword]
        
        #work out the entropy after the guess
        H=0

        for outcome in outcomes:
            #probability of a particular outcome
            #by summing the probabilities of the 
            #corresponding mysterywords
            poutcome=0
            Houtcome =0 # resulting entropy for if this is the outcome 
            for w in outcomes[outcome]:
                poutcome += words[w]
            for w in outcomes[outcome]:
                Houtcome += - words[w]/poutcome * math.log2( words[w] / poutcome) 
 

            H +=   poutcome*Houtcome
        Hvals[guess] = H
        if H < Hbest:
            #print("Best so far %s with entropy %g"%(guess,H))
            Hbest = H


    sorted_H = sorted(Hvals.items(), key = lambda item: item[1])

    print()
    print()
    print("Possible solutions")
    print(possiblewords)
    print()
    print()
    print("some possible words with resulting entropies if they are used as a guess")
    possible_Hvals = {w: Hvals[w] for w in possiblewords}
    sorted_possible_Hvals = sorted(possible_Hvals.items(), key = lambda item: item[1])
    print(sorted_possible_Hvals[:10])
    print ()
    print()
    print("Goodwords to try next and the corresponding entropy (if in doubt try first one of these)")
    print(sorted_H[:10])
