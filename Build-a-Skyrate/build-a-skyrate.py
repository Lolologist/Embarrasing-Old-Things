#! /usr/bin/python
#Skyrate Approximator
#Takes a given player, takes their file of everything they've said.
#Takes all the bigrams and counts of the bigrams
#Calculates percentages of likelihood of any bigram following another
#Jams stuff together in a thoroughly scientific manner
import re
import sys
from operator import itemgetter
import random
import os
# Import modules for CGI handling

import cgi, cgitb 
cgitb.enable()
# Create instance of FieldStorage 
form = cgi.FieldStorage()
# Get data from fields
skyrate = form.getvalue('username')


allbigrams = {}
def Test(d): #This helps determine weighted choices
    r = random.uniform(0, sum(d.itervalues()))
    s = 0.0
    for k, w in d.iteritems():
        s += w
        if r < s: return k
    return k

def assembler(probs):
    sentence = skyrate+": " #start at a blank sentence
    word = Test(probs["SOL"]) #default start at Start of Line
    sentence += word #add that
    while word != "EOL": #until I hit EOL
      nextword = Test(probs[word]) #probs[word] is a dictionary- key is the word we're starting with, value is a dictionary of all words that follow that word and their counts. Test takes all those weights (counts) and finds one in that dictionary to choose, outputs the key from within there as the new word
      sentence += " "+nextword #adds that word that was picked
      word = nextword
    sentence = sentence[:-4] #this cuts out the "EOL" at the end.
    if re.search("<i>",sentence): #some lines start with italics, and if so I want to make sure it ends with it.
      sentence += "</i>"
    return sentence
  #		print each, probs["SOL"][each] #probs["SOL"][each] is the count

def extractbigrams(line):
	bigrams = {}
	x = 0
	while x < (len(line)-1):
                if (line[x],line[x+1]) in bigrams:
                    bigrams[line[x],line[x+1]] += 1
                else:
                    bigrams[line[x],line[x+1]] = 1
		x +=1
	return bigrams

def percentages(bigramsfinal): #this makes a dictionary, probs, which has keys of each of the first words in a bigram pair.
	probs = {}
	for k,v in bigramsfinal:
		if k in probs:
			probs[k][v] = bigramsfinal[k,v] #the value of the dict is the second word in the bigram pair and how many times it occurs.
		else:
			probs[k] = {v:bigramsfinal[k,v]}
	return probs

def main():
        directory = "/home/dabishop/lo.lologi.st/skyrates/Everyone/"#that's where all the individual users' text files are, a corpus of everything they've said.
        f= open(directory + "lines_"+skyrate)
        for line in f:
          line = "SOL "+line+" EOL" #so I can tell what kind of words start and end lines
          line = line.split()
          bigrams = extractbigrams(line)
          #make a list here where each entry is a 2-part list: the first thing and then all the second things. Use this in a loop in assembler to go much faster
          for key,val in bigrams:
            #print key, val, bigrams[(key, val)]
            if (key, val) in allbigrams:
              allbigrams[(key, val)] += 1
            else:
              allbigrams[(key, val)] = 1
        probs = percentages(allbigrams)
        print "Content-type:text/html\r\n\r\n" #So good at website building, aren't I? :P At least I got the damn thing to work considering I have no experience with such things.
        print
        print "<html><head>"
        print "<title>Sentence Generator</title>"
        print "</head><body>"
        sentences = 10 #This way you don't have to just get one at a time. 10 seems like a nice number, not too few nor too many.
        while sentences > 0:    
            sent = assembler(probs)
            print "<p>"+ sent + "<p>"
            sentences -= 1
        print "</body></html>"

if __name__ == '__main__': #I always found this odd.
  main()
