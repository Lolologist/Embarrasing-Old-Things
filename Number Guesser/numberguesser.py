#!/usr/bin/Python
#Fun number-guessing program
import random

guessthis = random.randint(1,100000000000000000000000000)
x = random.randint(1,100000000000000000000000000)
minnum = 1
maxnum = 100000000000000000000000000
print x
numberofguesses = 1

while x != guessthis:
    if x < guessthis:
        minnum = x
        x = random.randint(minnum,maxnum)
        print x
    if x > guessthis:
        maxnum = x
        x = random.randint(minnum,maxnum)
        print x
    numberofguesses += 1
            
print "I got it in " + str(numberofguesses) + " guesses"
print x
