import math

words = open('fiveletterwords','r').readlines()

words = list(map(str.strip,words))


#what we know so far
priorgreen  = ['.', 'o', 'u', 'n', 't']
priororange = [set(), set(), set(), set(), set()]
priorgrey = set("clares")


#workout list of compatible words

possiblewords = []

for w in words:
    print(w)
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



print("Possible words:")
print(possiblewords)


N = len(possiblewords)

#initial entropy each of the N words equally likely so 
# Hinit = - \sum_{i=1}^N 1/N log 1/N
#       =   \sum_{i=1}^N 1/N log N
#       =    log(N)
#

Hinit = math.log2(N)

print()
print("Initial entropy = %g bits"%(Hinit,))




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
            outcomes[info]+=1
        else:
            outcomes[info] = 1
    
    #work out the entropy after the guess
    H=0
    for k in outcomes:
        H +=   outcomes[k] / N * math.log2(outcomes[k])
    Hvals[guess] = H
    if H < Hbest:
        print("Best so far %s with entropy %g"%(guess,H))
        Hbest = H
