import wordfreq 
import re

lang='en'
words={}
Ndict = 20000



def is_5digit_lowercase(s):
        return re.match("^[a-z][a-z][a-z][a-z][a-z]$", s)



for w in wordfreq.iter_wordlist(lang):
    if is_5digit_lowercase(w):
        words[w] = wordfreq.word_frequency(w,lang)
        if len(words)>=Ndict:
            break


with open('wordlist.txt','w') as f:
    for w in words:
        f.write(w+'\n')

        
#probsum = 0


#for w in words:
#        probsum += words[w]

#for w in words:
#        words[w]/=probsum


#assume probability of a word being the answer 
#exponentially decays with the popularity rank
#for (k,w) in enumerate(words):
#        words[w] = math.exp(-k/3000)
#        probsum+=words[w]

#for w in words:
#    words[w]/=probsum

