#!/usr/bin/Python
from __future__ import division
import re
import sys
from operator import itemgetter
import codecs
import os
from math import fabs
directory = "/Users/danielbishop/Documents/Python/AltDetector/Testeveryone/"#this was hardcoded in as I was using my own private corpus. If interested in obtaining a copy of the corpus, please email me at lolologist@gmail.com

####README BEFORE LOOKING THROUGH THE CODE####
####README BEFORE LOOKING THROUGH THE CODE####
####README BEFORE LOOKING THROUGH THE CODE####
#Note by Daniel Bishop, 3/31/2012
#This was a project of mine for a short time ending in March 2011. I was attempting to de-obfuscate a single user having
#multiple accounts on the online game Skyrates (www.skyrates.net), of which I have a corpus of a lot of data from nearly every
#user. The code has been left as-is from when I last worked on it, with debugging and commented-out sections and notes to
#myself and others. As can be seen, this was very much a learning process. It worked to a degree and actually did find some
#unknown alternate accounts on the game but was far from perfect. No scholarly research was done into Automated
#Authorship Attribution beforehand, but rather this project was done entirely by what seemed nice at the time. My CL experience
# and programming experience were still limited and as such I am proud of what I made. I hope you, reader, at least find it
#interesting.
#This project is provided without the requisite corpora from which the data is gathered, nor the host program that iterated over
#each of the users in the corpus. This program is by far the meat of the project and is thus all I am sharing publicly.
#Feel free to contact me at lolologist@gmail.com for more information.
####README BEFORE LOOKING THROUGH THE CODE####
####README BEFORE LOOKING THROUGH THE CODE####
####README BEFORE LOOKING THROUGH THE CODE####

def tokenize(line):
	d = { ':)': '<HAPPY_SMILEY>', ':(': '<SAD_SMILEY>', ';)':'<WINK_SMILEY>', ':D': '<COLON_CAPD>', 'D:': '<CAPD_COLON>', ':3':'<COLON_3>', 'T.T':'<CAP_T_CRY>', '^.^':'<CARROTS_PD>', '^^':'<2CARROTS>', '^-^':'<CARROTS_MINUS>','^_^':'<CARROTS_UNDER>',"XD":'<CAP_XD>',"xD":'<LOW_XD>',"X3":'<CAPX3>',":U":'<COLON_U>', ";D":'<WINK_CAPD>', ":P":'<COLON_CAPP>', ";P":'<SEMI_CAPP>',"=P":"<EQUALSP>", ":-)":'<SMILEY_W_NOSE>', ":V":'<BIG_DUCK>', ":v":'<LITTLE_DUCK>' ,"=>":'<EQUALS_GREATER>', "=<":'<EQUALS_LESSER>', "O.O":'<BOPDBO>', "O.o":'<BOPDLO>', "o.O":'<LOPDBO>',"0.0":'<ZEROPDZERO>',"O.0":'<BOPDZERO>',"o.0":'<LOPDZERO>',"0.O":'<ZEROPDBO>',"0.o":'<ZERPPDLO>',"O_O":"<BOUNBO>","O_o":"<BOUNLO>","o_O":"<LOUNBO>","0_0":"<ZEROUNZERO>","O_0":"<BOUNZERO>","o_0":"<LOUNZERO>","0_O":"<ZEROUNBO>","0_o":"<ZEROUNLO>","X.X":"<BXPDBX>","X.x":"<BXPDLX>","x.x":"<LXPDLX>","X_X":"<BXUNBX>","X_x":"<BXUNLX>","x_X":"<LXUNBX>","x[":"<LXLB>","x]":"<LXRB>","X]":"<BXRB>","X[":"<BXLB>","x3":"<LX3>",":O":"<COLON_CAPO>",":0":"<COLON_ZERO>",":o":"<COLON_LO>",">:D":"<GRCOLCAPD>",":/":"<COLRSLASH>",":\\":"<COLLSLASH>"}
	for smiley, placeholder in d.iteritems():
		line = line.replace(smiley, placeholder)
	list1 = line.split()
	tokens = []
	for item in list1:
            while re.match ('<i>\(\(',item):
                tokens.append(item[0:5])
                item = item[5:]
            while re.match ('<i>',item):
                tokens.append(item[0:3])
                item = item[3:]
            while re.match ('<b>',item):
                tokens.append(item[0:3])
                item = item[3:]
            while re.match ('/em',item):
                tokens.append(item[0:3])
                item = item[3:]
            while re.match ('/me',item):
                tokens.append(item[0:3])
                item = item[3:]
            while re.match ('/emote',item):
                tokens.append(item[0:6])
                item = item[6:]
            #while re.match ("\\\\",item): #I keep getting \\ in the output and want just the one.
                #tokens.append(item[1])
                #item = item[1:]
            temp = [] #used for the end of word instances, to put them back on in order
            while re.search('\W$',item):
                if re.search ('\)\)</i>',item):
                    item = item[:-6]
		if re.search ('</i>$',item):
                    item = item[:-4]
                elif re.search ('</b>$',item):
                    item = item[:-4]
		elif re.search('<.+?>$',item):
			length = re.search('<(.+?)>$',item)
			length = length.group(0)
			temp.append(item[-len(length):])
			item = item[:-len(length)]
                else:
                    # non-alphnumeric item at end of item
		    if len(item) > 0:
			    temp.append(item[-1])
			    item = item[:-1]
            while re.match('\W',item):
                #non-alphnumeric item at beginning of item
                tokens.append(item[0])
                item = item[1:]
	    if len(item) != 0:
		    tokens.append(item)
	    tokens.extend(temp[::-1])
	for index,each in enumerate(tokens):
		for smiley, placeholder in d.iteritems():
			if each == placeholder: #there exists a bug in which a letter or something on either side, rather, both sides, results in the smiley not being replaced from the <WHATEVER> form. May need to include something like a re.search with a group to find exactly where it is. Seems very rare though.
				each = each.replace(placeholder, smiley)
				tokens[index] = each
	return tokens
###############END TOKENIZER################

###Semi-Stupid bigram-ifier.###
def bigrammer(line,bigrams):
	for index,each in enumerate(line):
		#Replaces pronouns in some cases with more general terms to avoid overlooking different gender-based characters.
		if each.lower() in ["he","she","him","her","himself","herself","his","her","hers"]:
			line[index] = "3PS"
	x = 0
	while x < (len(line)-1):
		if (line[x].isalnum() == True) and (line[x+1].isalnum() == True):
			if (line[x],line[x+1]) in bigrams:
				bigrams[line[x],line[x+1]] += 1
			else:
				bigrams[line[x],line[x+1]] = 1
		x +=1
	return bigrams
###############FUNCTION WORDS, RETURN A DICT OF OCCURENCES OF THESE WORDS################
def functionwords(tokens):
	funcwords = {}
	FWords = ["the","a","if","that","then","well","however","thus","to","over","out","and","under","of","in","through","with","on","off","at","since","for","before","past","til","till","until","below","across","into","toward","towards","from","about","yes","no","ok","okay","however","i","you","he","she","it","him","her","me","they","we","us","y'all","yall","am","are","be","been","can","can't","could","couldn't","couldnt","dare","did","didn't","didnt","do","don't","dont","does","doesn't","doesnt","had","hadn't","hadnt","has","hasn't","hasnt","have","haven't","havent","is","isn't","isnt","may","maynt","mayn't","might","mightn't","mightnt","must","mustnt","mustn't","need","neednt","needn't","ought","oughtn't","oughtnt","shall","shant","shan't","should","shouldnt","shouldn't","was","wasn't","wasnt","were","weren't","werent","will","won't","wont","would","wouldn't","wouldnt"]
#of note: possibly might be worth it to figure out percentage of the time apostrophated words have apostrophes. Ex: list of all (many at least) words that end in n\'t or nt, and see what \% of the time words get apostrophed.
	for each in tokens.iteritems():
		if each[0].lower() in FWords:
			k = each[0]
			v = each[1]
			funcwords[k] = v
	return funcwords
#############################
def analyze(line):
###############number of commas in a line#######################
	numcommas = 0  # RETURN THIS
	for each in line:
		if each == ",":
			numcommas += 1
#######################################################

###########check for distance between commas, if more than one############
	pos1 = 0
	pos2 = 0
	commadist = [] #positions of the commas
	distance = []
	for index,token in enumerate(line):
		if token == ",":
			pos1 = index
			for index,token in enumerate(line):
				if index > pos1:
					if token == ",":
						pos2 = index
						break
					else:
						continue
			if pos2 != 0:
				commadist.append(pos1)
	x = 0
	y = 1
	while y < len(commadist):
		distance.append(commadist[y]-commadist[x]-1)
		y+=1
		x+=1
	#print commadist, "positions of the commas in the sentence"


       	################################
	tokens = {} #a dict of all individual tokens in the line and the number of occurences, to go to a global list of all words and frequencies
	#RETURN THIS
	for index,token in enumerate(line): #tokens in a given line and how many times they show up
		if token not in tokens:
			tokens[token] = 1
		else:
			tokens[token] += 1
	#######################
	#find the number of semicolons total
	numsemis = 0 #RETURN THIS
	for token in line:
		if token == ";":
			numsemis += 1
	###############Capitalization of statement-initial stuff (short only, presuming RP ignored then)
	cap = 2
	try:
		if line[0][0].isalpha():	
			if (line[0][0] == line[0][0].capitalize()): #check initial  token for capitalization, store what percent of the time they do so
				cap = 1
			else:
				cap = 0
	except:
		meaningless = 0
	return numcommas, distance, tokens, numsemis, cap #this at the end of all parts		

######################################################
###################MAIN###############################
######################################################
def main(nametoopen):
	sys.stdout.flush()
	sys.stdout.write("|")#program can take a bit going through hundreds of users so it's nice to be sure it isn't hanging
	lines = []
	bigrams = {}
	alltokens = {} 
	funcwords = {}
	dossier = [] # all the outputs to be combined here, and written to a file (at the end. Probably of the form NAME[dossier] to be looked at by another program that either iterates over this for each name, or just looks at the final dossier file
	numcommas =[]
	distance =[]
	cap = []
	linetokens = []
	FWords = ["the","a","if","that","then","well","however","thus","to","over","out","and","under","of","in","through","with","on","off","at","since","for","before","past","til","till","until","below","across","into","toward","towards","from","about","yes","no","ok","okay","however","i","you","he","she","it","him","her","me","they","we","us","y'all","yall","am","are","be","been","can","can't","could","couldn't","couldnt","dare","did","didn't","didnt","do","don't","dont","does","doesn't","doesnt","had","hadn't","hadnt","has","hasn't","hasnt","have","haven't","havent","is","isn't","isnt","may","maynt","mayn't","might","mightn't","mightnt","must","mustnt","mustn't","need","neednt","needn't","ought","oughtn't","oughtnt","shall","shant","shan't","should","shouldnt","shouldn't","was","wasn't","wasnt","were","weren't","werent","will","won't","wont","would","wouldn't","wouldnt"]
	numsemicolons = []
	linelengths = []
	#nametoopen = raw_input()
	filetoopen = directory + nametoopen#"/"+"lines_"+ nametoopen
	f = open(filetoopen)
	#print nametoopen
#############ITERATE OVER THE LINES######################
	for line in f:
		line = line.rstrip()
		line = tokenize(line) #tokenize
		linebigrams = bigrammer(line,bigrams)
		bigrams.update(linebigrams)
		lines += line
		if len(line) < 40:
			part = analyze(line)
			linetokens.append(part[2])
			numsemicolons.append(part[3])
			cap.append(part[4])
		else: #for longer ones
			part = analyze(line)
			numcommas.append(part[0])
			distance.append(part[1])
			linetokens.append(part[2])
			numsemicolons.append(part[3])
			cap.append(part[4])
			linelengths.append(len(line))
###############ADD TOKENS TO ALLTOKENS###################
	for each in linetokens:
		for k, v in each.iteritems():
			if k in alltokens:
				alltokens[k] += v
			if k not in alltokens:
				alltokens[k] = v
		

################ZIPFESQUE TOKENS, AKA TOP 100 AND THEIR COUNTS#####
	sorted_tokens = sorted(alltokens.iteritems(), key=itemgetter(1), reverse=True) # sort tokens by values for easier reference, in reverse order from highest to lowest
	x = 0
	top_sorted_tokens = []
	while x < 100:
		top_sorted_tokens += sorted_tokens[x] #get the top hundred tokens and how many times they are shown
		x += 1
	#print top_sorted_tokens #top 100 commonest tokens and how often they were used

#############B-B-B-BIGRAMS###############################
	sorted_bigrams = sorted(bigrams.iteritems(), key=itemgetter(1), reverse=True) # sort tokens by values for easier reference, in reverse order from highest to lowest
	#print sorted_bigrams
	x = 0
	top_sorted_bigrams = {}
	punct = ["\"", "'", ",", ";", "!", "?", ";",":", ".", "","[","]"]
	#print nametoopen
	while len(top_sorted_bigrams) < 100:
		if (sorted_bigrams[x][0][0] not in punct):
			if (sorted_bigrams[x][0][1] not in punct):
				if ((sorted_bigrams[x][0][0].lower() not in FWords) and (sorted_bigrams[x][0][1].lower() not in FWords)):
					#print sorted_bigrams[x][0][0],sorted_bigrams[x][0][1], sorted_bigrams[x][1]
					if sorted_bigrams[x][0] in top_sorted_bigrams:
						top_sorted_bigrams[sorted_bigrams[x][0]] += sorted_bigrams[x][1]
					else:
						top_sorted_bigrams[sorted_bigrams[x][0]] = sorted_bigrams[x][1]
			#top_sorted_bigrams += sorted_bigrams[x] #get the top hundred tokens and how many times they are shown
		x += 1
	#print sorted(top_sorted_bigrams.iteritems(), key=itemgetter(1), reverse=True), nametoopen, "TOP BIGRAMS" #top 10 commonest bigrams and how often they were used #this seems to be a shit method of determining... maybe look through all bigrams, find unusual bigrams, see if anyone else has em... I think that's probably not a bad idea
	
###############AVERAGE COMMAS PER SENTENCE#################
	avgcommas = 0 
	average_commas = 0
	for each in numcommas:
		avgcommas += each
	average_commas = avgcommas / len(numcommas)
	#print average_commas, "Average commas per sentence"
################AVERAGE DISTANCE BETWEEN COMMAS##############
	avg_distance_list = []
	avg_distance = 0
	for thelist in distance:
		for each in thelist:
			avg_distance_list.append(each)
	for each in avg_distance_list:
		avg_distance += each
	#print avg_distance_list
	try:
		avg_distance = avg_distance / len(avg_distance_list)
	except:
		avg_distance = "DERP"
		print "PROBLEM"
	#print avg_distance, "Average distance between commas (sentences over 30 tokens, 2+ commas)"
##############NUMBER SEMICOLONS PER TEN THOUSAND TOKENS
	totalsemis = 0
	average_semicolons = 0
	for each in numsemicolons:
		totalsemis += each

	average_semicolons = totalsemis / (len(lines)/10000)
	if average_semicolons == 0:
		average_semicolons = 10
	#print len(lines), "length of all tokens"
	#print average_semicolons, "Semicolons per ten thousand tokens"
###################PERCENTAGE OF SHORTER STATEMENTS BEGINNING WITH A CAPITAL LETTER (IF A LETTER)
	totalcaps = 0
	totalcapstocount = 0
	for each in cap:
		if each == 1:
			totalcaps +=1
			totalcapstocount += 1
		elif each == 0:
			totalcapstocount += 1
	percentcap = 100*(totalcaps/totalcapstocount)
	#print percentcap, "is the percent of line-initial capitals, given a letter."

##################AVERAGE LINE LENGTH IN NUMBER OF TOKENS###################
	averagelinelength = 0
	for each in linelengths:
		averagelinelength += each
	averagelinelength = averagelinelength/len(linelengths)
	#print averagelinelength, "tokens is the average length of a line."

##############FIND FUNCTION WORD FREQUENCIES##############
	funcwords = functionwords(alltokens)
	funcfreqs = {}
	for k,v in funcwords.iteritems():
		funcfreqs[k] = v/len(alltokens)
	#print funcfreqs
#####################################################
		
		#add to the dossier here
	dossier = [len(lines), sorted_tokens, top_sorted_tokens, sorted_bigrams, top_sorted_bigrams, average_commas, avg_distance, average_semicolons, percentcap, averagelinelength, funcfreqs]
	#print dossier
	return dossier #I like this name for the variable or matrix or whatever it ends up as. It'll be a whole big list of all of the tests and their outcomes, and the individual parts of it will be able to be checked against other people's dossiers



def tbigramcompare(persona, personb):
	difference = 0
	similar = {}
	for ka,va in sorted(persona.iteritems(), key=itemgetter(1), reverse=True):
		if ka in personb:
			#print ka, personb[ka]
			similar[ka] = fabs(va-personb[ka])
	#print similar, "SIMILAR"
	#for kb,vb in  sorted(personb.iteritems(), key=itemgetter(1), reverse=True):

	#print len(similar), "overlapping top bigrams"
	#for k,v in similar.iteritems():
		#print k,v
	return similar




############################main part done, postprocessing here#############
def postprocess():
	dossier = {}
	lengthgood = 0
	numofpeople = 0
	everytbigram = {}
	everyttoken = {}
	everybigram = {}
	everytoken = {}
	directory = "/Users/danielbishop/Documents/Python/AltDetector/Testeveryone/"
	subdirectories = os.listdir(directory)
	for person in subdirectories:
		try:
			howlong = main(person)	
			if howlong[0] > 5000:
				dossier[person] = howlong
				numofpeople +=1
				lengthgood += howlong[0]
				#print person, "had",dossier[person][0],"tokens"
		except:
			continue
	print
	print numofpeople, "number of files being used right now"

        #[len(lines), sorted_tokens, top_sorted_tokens, sorted_bigrams, top_sorted_bigrams, average_commas, avg_distance, average_semicolons, percentcap, averagelinelength, funcfreqs]
	avgtokens = lengthgood / len(dossier)
	for person in dossier.iteritems(): #smooth the numbers to match averages, like for bigram counts
		multiplier = avgtokens / int(person[1][0])
		person[1][0]=person[1][0]*multiplier
		for k,v in person[1][4].iteritems():
			person[1][4][k] = person[1][4][k]*multiplier
	matches4 = {}
	matches5 = {}
	matches6 = {}
	matches7 = {}
	matches8 = {}
	matches9 = {}
	matchingtoptokens = {}
	matchingtopbigrams = {}
	confidences = {}

	for controlperson in dossier.iteritems(): #see if the numbers are close to anyone else's
		confidences[controlperson[0]] = {}
		for experiperson in dossier.iteritems():
			if controlperson[0] != experiperson[0]: 
				if controlperson[0] not in matches4:
					matches4[controlperson[0]] = {}
				matches4[controlperson[0]][experiperson[0]] = tbigramcompare(controlperson[1][4],experiperson[1][4])
			if controlperson[0] != experiperson[0]: 
				if controlperson[0] not in matches5:
					matches5[controlperson[0]] = {}
				matches5[controlperson[0]][experiperson[0]] = [fabs(1-(controlperson[1][5] / experiperson[1][5]))]
			if controlperson[0] != experiperson[0]:
				if controlperson[0] not in matches6:
					matches6[controlperson[0]] = {}
				matches6[controlperson[0]][experiperson[0]] = [fabs(1-(controlperson[1][6] / experiperson[1][6]))]
			if controlperson[0] != experiperson[0]:
				#shit gets crazy if someone doesn't have any semicolons
				#print controlperson[0], "vs", experiperson[0]
				#print controlperson[1][7]
				#print experiperson[1][7]
				if controlperson[0] not in matches7:
					matches7[controlperson[0]] = {}
				if experiperson[1][7] != 0 and controlperson[1][7] != 0:
					matches7[controlperson[0]][experiperson[0]] = [fabs(1-(controlperson[1][7] / experiperson[1][7]))]
				else: # HERE IS THE FIX. GIVEN SOMEONE WITH ZERO SEMICOLONS THIS FIXES IT.
					matches7[controlperson[0]][experiperson[0]] = [fabs(1-(controlperson[1][7] / .1))]
			if controlperson[0] != experiperson[0]:	
				if controlperson[0] not in matches8:
					matches8[controlperson[0]] = {}
				matches8[controlperson[0]][experiperson[0]] = [fabs(1-(controlperson[1][8] / experiperson[1][8]))]
			if controlperson[0] != experiperson[0]:	
				if controlperson[0] not in matches9:
					matches9[controlperson[0]] = {}
				matches9[controlperson[0]][experiperson[0]] = [fabs(1-(controlperson[1][9] / experiperson[1][9]))]


	print "Top Bigrams:" 
	sorted_matches4 = sorted(matches4.iteritems(), key=itemgetter(1), reverse=True)
	addtoconf4 = 0
	for tester,v in sorted_matches4:
		#print tester #person I'm testing
		confidences[tester]["topbigrams"] = {}
		for expper, vals in v.iteritems():
			confidences[tester]["topbigrams"][expper] = {}
			#print expper #person testing against
			for bik,biv in vals.iteritems():
				#print bik, biv
				confidences[tester]["topbigrams"][expper][bik] =biv
		for a,b in confidences[tester]["topbigrams"][expper].iteritems():
			#print a,b
			addtoconf4 += b
	addtoconf4 = addtoconf4/len(vals)
#	print addtoconf4, "ADD" #I don't think this is being used, actually
	
	
#	print "Avg Commas:" #bad as is. 
	sorted_matches5 = sorted(matches5.iteritems(), key=itemgetter(1), reverse=True)
	for each in sorted_matches5:
		confidences[each[0]]["commas"] = each[1]
	#	print each[0], each[1]
	#print

	#print "Avg Distance:" #ok metric - average distance between commas if more than one per sentence
	sorted_matches6 = sorted(matches6.iteritems(), key=itemgetter(1), reverse=True)
	for each in sorted_matches6:
		confidences[each[0]]["dist"] = each[1]
	#	print each[0],each[1]
	#print

	#print "Avg semicolons:" # great metric (or so I thought at first. This turned out to be a horrible one.)
	sorted_matches7 = sorted(matches7.iteritems(), key=itemgetter(1), reverse=True)
	for each in sorted_matches7:
		confidences[each[0]]["semis"] = each[1]
		#print each[0],each[1]
	#print

	#print "Avg Percentcap:" #Best metric I have oddly
	sorted_matches8 = sorted(matches8.iteritems(), key=itemgetter(1), reverse=True)
	for each in sorted_matches8:
		confidences[each[0]]["caps"] = each[1]
		#print each[0],each[1]
#	print
	
	#print "Avg line length" (meh)
	sorted_matches9 = sorted(matches9.iteritems(), key=itemgetter(1), reverse=True)
	for each in sorted_matches9:
		confidences[each[0]]["length"] = each[1]
		#print each[0],each[1]
	#print
	#print
	
	commaconfidence = 10
	distanceconfidence =25
	bigramconfidence = 2
	semisconfidence = 50
	capconfidence = 45
	lengthconfidence = 30
	
	finalconfidence = {}
	#print
	print "CONFIDENCES"
	for k,v in confidences.iteritems():
		finalconfidence[k] = {}
		for keys, vals in sorted(v.iteritems(), key=itemgetter(0), reverse=True):
			#print keys, "KEYS"
			for a, b in sorted(vals.iteritems(), key=itemgetter(1), reverse=False):
				#print a,b, "VALUES"
				if (a != k):
					if a not in finalconfidence[k]:
						finalconfidence[k][a] = 0
				#if keys == "topbigrams":
					#print len(b), "is the number of similar top bigrams for", k, "and", a
					#print "and they are"
					#finalconfidence[k][a] = 30-len(b)
					#for q,w in b.iteritems():
						#print w
						#finalconfidence[k][a] +=w
					#finalconfidence[k][a] = (finalconfidence[k][a]/(len(b)+.01))#/bigramconfidence
					#The above is commented out because it's a bad measure. Testing below for only number of similar top bigrams, not their values relative to each other
					#finalconfidence[k][a] = (1/len(b))/bigramconfidence
					#print "for a total influence of " + str(finalconfidence[k][a])
				if keys == "semis":
					print "adding ", str((b[0]*10)/semisconfidence), "because of ", keys, "for ", k, "re", a
					finalconfidence[k][a] += (b[0]*10)/semisconfidence
					print finalconfidence[k][a], keys
				elif keys == "length":
					print "adding ",str((b[0]*10)/lengthconfidence), "because of ", keys, "for ", k, "re:",a
					finalconfidence[k][a] += (b[0]*10)/lengthconfidence
					print finalconfidence[k][a], keys
				elif keys == "dist":
					print "adding ",str((b[0]*10)/distanceconfidence), "because of ", keys, "for ", k, "re:",a
					finalconfidence[k][a] += (b[0]*10)/distanceconfidence
					print finalconfidence[k][a], keys
				elif keys == "commas":
					print "adding ",str((b[0]*10)/commaconfidence), "because of ", keys, "for ", k, "re:",a
					finalconfidence[k][a] += (b[0]*10)/commaconfidence
					print finalconfidence[k][a], keys
				elif keys == "caps":
					print "adding ",str((b[0]*10)/capconfidence), "because of ", keys, "for ", k, "re:",a
					finalconfidence[k][a] += (b[0]*10)/capconfidence
					print finalconfidence[k][a], keys
	for k,v in finalconfidence.iteritems():
		print k[6:], "is most like:"
		for keys,vals in sorted(v.iteritems(), key=itemgetter(1), reverse=False):
			print keys, vals
		print
	

if __name__ == "__main__":
	postprocess()


#Look at information gain. Which features give how much information? Some might be better metrics than others.
