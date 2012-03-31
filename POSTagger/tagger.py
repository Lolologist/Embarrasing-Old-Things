#POS Tagger
#Daniel Bishop
#Begun 11/26/2011
#V0.0.1
import os
import re
import time
import sys


##########################################################################################
##########################################################################################
##########################################################################################
########TRAINING###########################################################################
##########################################################################################
##########################################################################################
##########################################################################################

master_dict_pos = {}
master_dict_word = {}
master_dict_bigram_POS = {}
master_dict_bigram_words = {}
master_dict_bigram_combined = {}
def pos_extract(f, folder):#extracts word-pos pairs
    os.chdir(folder)
    all_f_words = []
    all_f_POS = []
    all_f_combined = []
    for line in f:
        find = re.findall('\([^(\)]+?\)',line)
        if len(find) > 0:
            for each in find:
                if not each.startswith("(-NONE-"):
                    each = each.lower()
                    each = each[1:-1]
                    all_f_combined.append(each)
                    each = each.split()
                    all_f_POS.append(each[0])
                    all_f_words.append(each[1])
                    
                    if each[0] not in master_dict_pos:
                        master_dict_pos[each[0]] = {}
                        master_dict_pos[each[0]][each[1]] = 1
                    elif each[1] not in master_dict_pos[each[0]]:
                        master_dict_pos[each[0]][each[1]] = 1
                    else:
                        master_dict_pos[each[0]][each[1]] += 1
                        
                    if each[1] not in master_dict_word:
                        master_dict_word[each[1]] = {}
                        master_dict_word[each[1]][each[0]] = 1
                    elif each[0] not in master_dict_word[each[1]]:
                        master_dict_word[each[1]][each[0]] = 1
                    else:
                        master_dict_word[each[1]][each[0]] += 1

    #now to make the bigrams of words and POSes and then add them as necessary to a master dictionary
    x = 0
    while x < (len(all_f_words)-1):
        if (all_f_words[x],all_f_words[x+1]) in master_dict_bigram_words:
            master_dict_bigram_words[all_f_words[x],all_f_words[x+1]] += 1
        else:
            master_dict_bigram_words[all_f_words[x],all_f_words[x+1]] = 1
        if (all_f_POS[x],all_f_POS[x+1]) in master_dict_bigram_POS:
            master_dict_bigram_POS[all_f_POS[x],all_f_POS[x+1]] += 1
        else:
            master_dict_bigram_POS[all_f_POS[x],all_f_POS[x+1]] = 1
        if (all_f_combined[x],all_f_combined[x+1]) in master_dict_bigram_combined:
            master_dict_bigram_combined[all_f_combined[x],all_f_combined[x+1]] += 1
        else:
            master_dict_bigram_combined[all_f_combined[x],all_f_combined[x+1]] = 1
        x +=1
    
##########################################################################################
#######BEGIN UNIGRAMS#######################################################################
##########################################################################################
def unigrams(folder, ambigToDefinite):
    print folder+"/training_data is where the files are going."
    if os.path.exists(folder+"/training_data") == False:
        print "NOTE: training_data did not exist. Creating it now."
        os.makedirs(folder+"/training_data")
    else:
        print "NOTE: training_data already existed. You may be making a copy of or adding to existing files."

    print ""
    if ambigToDefinite != "none":
        print "NOT IMPLEMENTED - Ambiguous->Definite tag feature."
        print "You specified that tags where one tag is more than "+str(ambigToDefinite)+"% of the tags for a given word to treat it as unambiguous."
        print "In time this feature will become available."
        
    definite = 0
    ambig = 0
    for k,v in master_dict_word.iteritems():
        #print k.upper()#the word
        loop = 0
        for k1, v1 in v.iteritems():
            if len(v) == 1: #if there's no question as to which POS tag a given word gets
                definite += 1
                try:
                    #o =open("/Users/danielbishop/Python/parser/training data/definite_1-grams.txt","a")
                    o =open(folder+"/training_data/definite_1-grams.txt","a")
                except:
                    #o =open("/Users/danielbishop/Python/parser/training data/definite_1-grams.txt","w")
                    o =open(folder+"/training_data/definite_1-grams.txt","w")
                o.write(k.upper()+" "+k1+"\n") #writing words in all-caps to avoid word ambiguity. It's my belief that, right now, we don't need to distinguish
                o.close()
            else:
                #print k,k1, v1#the POS and the count of the POS
                ambig += 1
                try:
                    o =open(folder+"/training_data/ambiguous_1-grams.txt","a")
                except:
                    o =open(folder+"/training_data/ambiguous_1-grams.txt","w")
                if loop == 0:  
                    o.write(k.upper()+" ("+str(k1)+" "+str(v1)+") ")
                else:
                    if loop == len(v)-1:
                        o.write("("+str(k1)+" "+ str(v1)+")\n")
                    else:
                        o.write("("+str(k1)+" "+str(v1)+") ")
                o.close()
                loop += 1
    print
    print ambig, "ambiguous words versus", definite, "1-grams with only one POS tag associated."


##########################################################################################
#######END UNIGRAMS#########################################################################
##########################################################################################

##########################################################################################
#######BEGIN BIGRAMS#########################################################################
##########################################################################################
def bigrams(folder, ambigToDefinite):
    print "Now creating relevant bigram files."
    try:
        o =open(folder+"/training_data/bigram_words.txt","a")
    except:
        o =open(folder+"/training_data/bigram_words.txt","w")
    for k,v in master_dict_bigram_words.iteritems():
        o.write(str(k)+" "+str(v)+"\n")
    o.close()

    for k,v in master_dict_bigram_POS.iteritems():
        firstletterL =k[0].split()[0][0]#first letter of the left POS
        firstletterR = k[1].split()[0][0]#first letter of the right POS
        if not re.search('[a-zA-Z]',firstletterL):
            firstletterL = "XX"
        if not re.search('[a-zA-Z]',firstletterR):
            firstletterR = "XX"
        try:
            mR =open(folder+"/training_data/bigram_pos_R_"+str(firstletterR)+".txt","a")
        except:
            mR =open(folder+"/training_data/bigram_pos_R_"+str(firstletterR)+".txt","w")
        try:
            mL =open(folder+"/training_data/bigram_pos_L_"+str(firstletterL)+".txt","a")
        except:
            mL =open(folder+"/training_data/bigram_pos_L_"+str(firstletterL)+".txt","w")
        mR.write(str(k)+" "+str(v)+"\n")
        mL.write(str(k)+" "+str(v)+"\n")
        mR.close()
        mL.close()
    
    for k,v in master_dict_bigram_combined.iteritems():
        firstletterL =k[0].split()[1][0]#first letter of the left word
        firstletterR = k[1].split()[1][0]#first letter of the right word
        if not re.search('[a-zA-Z]',firstletterL):
            firstletterL = "XX"
        if not re.search('[a-zA-Z]',firstletterR):
            firstletterR = "XX"
        try:
            mR =open(folder+"/training_data/bigram_comb_R_"+str(firstletterR)+".txt","a")
        except:
            mR =open(folder+"/training_data/bigram_comb_R_"+str(firstletterR)+".txt","w")
        try:
            mL =open(folder+"/training_data/bigram_comb_L_"+str(firstletterL)+".txt","a")
        except:
            mL =open(folder+"/training_data/bigram_comb_L_"+str(firstletterL)+".txt","w")
        mR.write(str(k)+" "+str(v)+"\n")
        mL.write(str(k)+" "+str(v)+"\n")
        mR.close()
        mL.close()
    
    try:
        m =open(folder+"/training_data/bigram_combined.txt","a")
    except:
        m =open(folder+"/training_data/bigram_combined.txt","w")
    for k,v in master_dict_bigram_combined.iteritems():
        m.write(str(k)+" "+str(v)+"\n")
    m.close()    
##########################################################################################
#######END BIGRAMS##########################################################################
##########################################################################################
                        
def gold_training(program_folder, gold_standard_folder, gold_standard_type, ambigToDefinite):
    main_directory = os.listdir(gold_standard_folder)
    print "Building gold-standard files for POS tagging."
    for each_folder in main_directory:
        if not each_folder.startswith(".") and each_folder != "MERGE.LOG":
            folderdir = gold_standard_folder+"/"+each_folder+"/"
            for each_file in os.listdir(folderdir):
               file_to_open = folderdir+str(each_file)
               f = open(file_to_open)
               pass_folder = folderdir+"/"
               pos_extract(f, pass_folder)
               f.close()
    unigrams(program_folder, ambigToDefinite)
    bigrams(program_folder, ambigToDefinite)



##########################################################################################
##########################################################################################
##########################################################################################
########END TRAINING########################################################################
##########################################################################################
##########################################################################################
##########################################################################################

##########################################################################################
##########################################################################################
##########################################################################################
######BEGIN DEFINITE TAGGING###################################################################
##########################################################################################
##########################################################################################
##########################################################################################
def tag_unambiguous_words(train, test, out,cycle_type):
    #print train
    #print test
    #print out
    print "Tagging unambiguous words."
    starttime = time.clock()
    unambig = open(train+"definite_1-grams.txt","r")
    ambig = open(train+"ambiguous_1-grams.txt","r")
    unam = {}
    amb = {}
    wordlist = []
    unknown_wordlist = []
    for line in ambig:
        wordlist.append(line.split()[0])
    for line in unambig:
        line = line.split()
        wordlist.append(line[0])
        unam[line[0]] = line[1]
    testfile = open(test, "r")
    testfile2 = open(test, "r")
    len_of_testfile = len(testfile2.readlines())
    testfile2.close()
    outfilem = re.search(".+/(.+$)",test)
    outfile = outfilem.group(1)
    print "Outfile is: "+out+outfile[:-4]+"_tagged_unam.txt"
    tagged_output = open(out+outfile[:-4]+"_tagged_unam.txt", "w")
    replaced = 0
    total = 0
    unknown = 0
    for word in testfile:
        if (total % 5000) == 0 and (total != 0):
            taken = (time.clock()-starttime)
            seconds_per_line = taken/total
            total_time = seconds_per_line *len_of_testfile
            remaining = (total_time - taken)/60.0
            minutes = remaining % 60
            seconds = minutes - int(minutes)
            seconds = int(seconds * 60)
            minutes = int(minutes)
            hours = int(remaining / 60)
            #print "#|#|#|#|#|#|#|#|#|#|#|#"
            #print str(format(taken,'.2f')),"seconds taken so far"
            percent = 100*((total+0.0)/(len_of_testfile+0.0))
            percent = format(percent,'.2f')
            print str(percent)+"% done. About", str((int(remaining))), "m "+str(seconds)+" sec remaining."
            #print "#|#|#|#|#|#|#|#|#|#|#|#"
            
        if word[:-1].upper() not in wordlist:
            unknown += 1 #means that the word isn't known
            if word not in unknown_wordlist:
                unknown_wordlist.append(word) #a list of each unknown word
        total += 1
        word1 = word[:-1].upper()
        if word1 in unam.keys():
            #tagged_output.write(unam[word1]+" "+word[:-1]+"\n")
            tagged_output.write(word[:-1]+" "+unam[word1].upper()+"\n")
            replaced += 1
        else:
            tagged_output.write(word)
    tagged_output.close()
    
    print "Unambiguous words are now tagged."
    procent = format((100*replaced/(total+0.0)),'.2f')
    print str(replaced) +" tags were non-ambiguous, at "+ str(procent)+" percent of the test corpus."
    print str(unknown)+" unknown tokens. "+str(len(unknown_wordlist))+" unknown types (different words)."
    print str(total), "tokens total."
    endtime = time.clock()
    timetaken = endtime-starttime
    print str(timetaken/60.0)+" minutes taken."
    partially_tagged_file = out+outfile[:-4]+"_tagged_unam.txt"
    tag_ambiguous_words(train, out, partially_tagged_file, unknown_wordlist,replaced,1, procent, cycle_type)#the 1 at the end is the cycle - aka it'll be the first run through the ambiguous training. Keeps track of cycles

############################################################
############################################################
############################################################
#######END DEFINITE TAGGING######################################
############################################################
############################################################
############################################################


######UNKNOWN WORD HANDLER######
def handle_unknown_words(train, this_word):
    #load_pickle = open(train+"unknown_word_properties.derp","rb")
    return this_word



############################################################
############################################################
############################################################
#######BEGIN AMBIGUOUS TAGGING##################################
############################################################
############################################################
############################################################
def tag_ambiguous_words(train, out, partially_tagged_file, unknown_wordlist,replaced_before,cycle, procent, cycle_type):
    replaced = 0
    tagged_total = 0
    f = open(partially_tagged_file, "r")
    lines = f.readlines() #LINES is the partially-tagged file as a list.
    f.close()
    g = open(partially_tagged_file[:-10]+"_"+str(cycle)+"ambig.txt","w")
    partially_tagged_file = partially_tagged_file[:-10]+"_"+str(cycle)+"ambig.txt"
    #print partially_tagged_file
    
    starttime = time.clock()
    
    #THIS GETS ALL OF THE UNIGRAMS FROM THE 1-GRAMS FILE
    ambig_unigrams_file = open(train+"ambiguous_1-grams.txt","r")
    ambig_unigrams_readlines = ambig_unigrams_file.readlines()
    ambig_unigrams_file.close()
    ambig_unigrams = {} #this dict is each entry in ambiguous-1-grams and its values
    for line in ambig_unigrams_readlines:
        line = line.split()#line[0] is the word - all caps. line[1:] are the options.
        c = 1
        #print line[0],
        while c < len(line):
            #print line[c][1:], line[c+1][:-1],#line[c][1:] is the tag, line[c+1][:-1] is the count
            if line[0] in ambig_unigrams:
                ambig_unigrams[line[0]][line[c][1:]] = line[c+1][:-1]
            else:
                ambig_unigrams[line[0]] = {}
                ambig_unigrams[line[0]][line[c][1:]] = line[c+1][:-1]
            c +=2
            #for each in ambig_unigrams:
               # print "!:",each, ambig_unigrams[each]
    

    
    for index, this_word in enumerate(lines): #Example: "nnp SOL" sans quotes, with a \n presumably, as saying (incorrectly) that SOL (start if line) is NNS
        ####KEEPING TRACK OF TIME AND REPORTING ESTIMATES OF TIME REMAINING
        this_word = this_word[:-1]
        if (index % 5000) == 0 and (index != 0):
            taken = (time.clock()-starttime)
            seconds_per_line = taken/index
            total_time = seconds_per_line *len(lines)
            remaining = (total_time - taken)/60.0
            if remaining > 60:
                minutes = remaining % 60
                seconds = minutes - int(minutes)
                seconds = int(seconds * 60)
                minutes = int(minutes)
                hours = int(remaining / 60)
                print "#|#|#|#|#|#|#|#|#|#|#|#"
                print taken,"seconds taken so far"
                print "token "+str(index)+":", str(hours), "hours and "+str(minutes)+" remaining, best guess."
                print"#|#|#|#|#|#|#|#|#|#|#|#"
            else:
                minutes = remaining % 60
                seconds = minutes - int(minutes)
                seconds = int(seconds * 60)
                minutes = int(minutes)
                hours = int(remaining / 60)
                print taken,"seconds taken so far"
                percent = 100*((index+0.0)/(len(lines)+0.0))
                percent = format(percent,'.2f')
                print str(percent)+"% done. About", str((int(remaining))), "m "+str(seconds)+" sec remaining."
                print "#|#|#|#|#|#|#|#|#|#|#|#"
        ####END KEEPING TRACK OF TIME AND REPORTING ESTIMATES OF TIME REMAINING



        if -1 < index < len(lines):
            try:
                left_word = lines[index-1]
            except: left_word = ""
            try:
                right_word = lines[index+1]
            except:
                right_word = ""
            #print left_word, this_word, right_word
            if " " not in this_word: # if the word we're at now hasn't yet been tagged
                possibilities_for_this_word = {} #each possibility will be a dict of the choice and a value (score)
                #look for an existing WORD WORD combo
                if " " in left_word: #if the word left of this word is already tagged, and we can look for a match
                    left_word_split = left_word.split()
                    left_word_pos = left_word_split[1]
                    left_word_word = left_word_split[0]
                    if not re.search('[a-zA-Z]',left_word_word[0]):#if the first letter of the left word isn't a letter, aka it's punctuation or some such
                        left_word_split_file_letter = "XX"
                    else:
                        left_word_split_file_letter = left_word_word[0]
                    left_word_file = open(train+"bigram_comb_L_"+left_word_split_file_letter.lower()+".txt","r")#things like this are HORRIBLY INEFFICIENT, I know
                    left_word_readlines = left_word_file.readlines()
                    left_word_file.close()
                    for line in left_word_readlines:
                        if (left_word_word == line.split()[1][:-2]) and (this_word == line.split()[3][:-2]):#this grabs the "ever" and "setting" from ('rb ever', 'vbg setting') 1 to see if the word combo matches
                            if (left_word_pos != line.split()[0][2:]):
                                pass
                                #print "POS mismatch - left word's ["+left_word_word+"] already given tag ["+left_word_pos+"] is not same for this word-word combo's left word's tag ["+line.split()[0][2:]+"]. Word sequence "+left_word_word,this_word,right_word_word
                                #print line
                            if line.split()[2][1:] in possibilities_for_this_word.keys():# if the possibilities for this word already include this POS tag (though I don't think it ought be able to at this point)
                                possibilities_for_this_word[line.split()[2][1:]] += int(line.split()[4])
                                #print "Shouldn't have happened: possibility for left tag already existed"
                            else:
                                possibilities_for_this_word[line.split()[2][1:]] = int(line.split()[4])
                    ###Add in the search for POS tag combos
                    if not re.search('[a-zA-Z]',left_word_pos[0]):
                        left_pos_file = open(train+"bigram_pos_L_XX.txt","r")
                    else:
                        left_pos_file = open(train+"bigram_pos_L_"+left_word_pos[0].lower()+".txt","r")
                    left_pos_readlines = left_pos_file.readlines()
                    left_pos_file.close()
                    for line in left_pos_readlines:
                        if(left_word_pos == line.split()[0][2:-2]): #if the left POS from the POS-POS combo, and the left_word's POS are the same
                            #print left_word_pos, "match.", line.split()[1][1:-2],"shows up",line.split()[2], "times."
                            if line.split()[1][1:-2] in possibilities_for_this_word:                                
                                possibilities_for_this_word[line.split()[1][1:-2]] += int(line.split()[2])
                            else:
                                possibilities_for_this_word[line.split()[1][1:-2]] = int(line.split()[2])


                                
                    ###We now have a possibility entry for the left word if the word, word combo existed. Now for the right word!
                ####################################################################
                if " " in right_word: #if the word left of this word is already tagged, and we can look for a match
                    right_word_split = right_word.split()
                    right_word_pos = right_word_split[1]
                    right_word_word = right_word_split[0]
                    if not re.search('[a-zA-Z]',right_word_word[0]):#if the first letter of the left word isn't a letter, aka it's punctuation or some such
                        right_word_split_file_letter = "XX"
                    else:
                        right_word_split_file_letter = right_word_word[0]
                    right_word_file = open(train+"bigram_comb_R_"+right_word_split_file_letter.lower()+".txt","r")
                    right_word_readlines = right_word_file.readlines()
                    right_word_file.close()
                    for line in right_word_readlines:
                        if (right_word_word == line.split()[3][:-2]) and (this_word == line.split()[1][:-2]):#this grabs the "ever" and "setting" from ('rb ever', 'vbg setting') 1 to see if the word combo matches
                            if (right_word_pos != line.split()[2][1:]):
                                pass
                                #print "POS mismatch - right word's ["+right_word_word+"] already given tag ["+right_word_pos+"] is not same for this word-word combo's right word's tag ["+line.split()[2][1:]+"]. Word sequence "+left_word_word,this_word,right_word_word
                                #print line
                            if line.split()[0][2:] in possibilities_for_this_word.keys():# if the possibilities for this word already include this POS tag (plenty reasonable here since left went first
                                possibilities_for_this_word[line.split()[0][2:]] += int(line.split()[4])#as with above, I believe word-word combo is stronger than POS probabilities so it gets a higher weight
                            else:
                                possibilities_for_this_word[line.split()[0][2:]] = int(line.split()[4])
                    ###Add in the search for POS tag combos
                    if not re.search('[a-zA-Z]',right_word_pos[0]):
                        right_pos_file = open(train+"bigram_pos_R_XX.txt","r")
                    else:
                        right_pos_file = open(train+"bigram_pos_R_"+right_word_pos[0].lower()+".txt","r")
                    right_pos_readlines = right_pos_file.readlines()
                    right_pos_file.close()
                    for line in right_pos_readlines:
                        if(right_word_pos == line.split()[1][1:-2]):
                            if line.split()[0][2:-2] in possibilities_for_this_word:
                                #print right_word_pos, "match.", line.split()[0][2:-2],"shows up",line.split()[2], "times."
                                possibilities_for_this_word[line.split()[0][2:-2]] += int(line.split()[2])
                            else:
                                possibilities_for_this_word[line.split()[0][2:-2]] = int(line.split()[2])



                ###Now that we have all of those, adjust weights for how often these possible tags show up for the actual word.
                if this_word.upper() in ambig_unigrams.keys():
                    #print "Word["+this_word+"] WAS found in ambiguous unigrams file."
                    for pos in ambig_unigrams[this_word.upper()]:
                        if pos in possibilities_for_this_word:#Need to have it check the ambiguous file first because stuff like "it" isn't getting tagged right
                            #When the ambig file is overwhelming it needs to just tag it. Right now the stuff below here is fucking that up.
                            
                            #print "MULTIPLIER",
                            #print this_word, pos, ambig_unigrams[this_word.upper()][pos]
                            possibilities_for_this_word[pos] += int(ambig_unigrams[this_word.upper()][pos])*50 #50 is an arbitrary number but I do want it to be sorta gigantic as an affirmation. Probably will need or want to tone that down though.
                            possibilities_for_this_word[pos] = possibilities_for_this_word[pos]
                        #else:
                            #print this_word+": No match between possibilities_for_this_word and the unigrams file."
                            #print "\t P_F_T_W:"+str(possibilities_for_this_word), " - A_U: "+str(ambig_unigrams[this_word.upper()])
                         
                
                        ##Go through each entry in this and check if it's in the ambig_unigrams[each]. Multiply possibilities_for_this_word values if there's a match.
                else: #if the word isn't in the ambiguous unigrams keys. This means it's an unknown word! This is actual unknown word handling.
                    #probably ought do unknown word handling passing along the possibility dict here.
                    if len(this_word) != 0:   #so as to skip blank words   
                        #print "Word["+this_word+"] not found in ambiguous unigrams file."
                        pass
                    

                if len(possibilities_for_this_word.keys()) > 0:
                    #print this_word+":", possibilities_for_this_word
                    highestnum = 0
                    highestpos = ""
                    total = 0
                    for pos in possibilities_for_this_word:
                        total += possibilities_for_this_word[pos]
                        if possibilities_for_this_word[pos] > highestnum:
                            highestnum+=possibilities_for_this_word[pos]
                            highestpos = pos
                    if highestnum > .9*total: #90% accuracy
                        #print "writing ["+highestpos+" "+this_word+"] since over 90% sure of that combo."
                        #print str(possibilities_for_this_word)
                        #g.write(highestpos+" "+this_word+"\n")
                        g.write(this_word+" "+highestpos.upper()+"\n")
                        replaced += 1
                        tagged_total += 1
                    else:
                        #print "not assigning ["+this_word+"] a POS tag at this time. Only "+str(format(float(100*(highestnum/(0.0+total))),'.2f'))+"% sure."
                        #print str(possibilities_for_this_word)
                        g.write(this_word+"\n")
                        
                else: #given an empty possibilities_for_this_word. 
                    highestnum = 0
                    highestpos = ""
                    total = 0
                    try:
                        for each in ambig_unigrams[this_word.upper()]:
                            #print each
                            #print ambig_unigrams[this_word.upper()][each], type(ambig_unigrams[this_word.upper()][each])
                            total+= int(ambig_unigrams[this_word.upper()][each])
                            if int(ambig_unigrams[this_word.upper()][each]) > highestnum:
                                highestnum = int(ambig_unigrams[this_word.upper()][each])
                                highestpos = each
                        if highestnum > .95*total:
                            #print "no entry for p_f_t_w, but the ambiguous_1-grams file is rather sure about ["+this_word+"] getting the tag ["+highestpos+"] at over 95%."
                            #WRITE TO FILE SINCE CONFIDENT
                            #g.write(highestpos+" "+this_word+"\n")
                            g.write(this_word+" "+highestpos.upper()+"\n")
                            replaced +=1
                            tagged_total += 1
                        else:
                            #WRITE TO FILE JUST THE WORD SINCE NOT CONFIDENT
                            g.write(this_word+"\n")
                            #print "["+this_word+"] getting no tag due to highest tag ["+highestpos+"] only being "+str(format(float(100*(highestnum/(0.0+total))),'.2f'))+"%."
                    except:
                        #print "["+each+"] wasn't in the ambiguous_1-grams file. Oh my! Length of pftw is "+str(len(possibilities_for_this_word))
                        #WRITE TO FILE JUST THE WORD SINCE WACKY
                        #g.write(this_word+"\n")#commented out since unknown word handler is now handling it
                        ###UNKNOWN WORD HANDLING GOES HERE
                        g.write(handle_unknown_words(train, this_word)+"\n")#Unknown word handler has to write SOMETHING.
                        #right now just returns the word.
                        
            else: #if the word was already tagged in an earlier stage
                #WRITE TO FILE
                g.write(this_word+"\n")
                tagged_total += 1
                #print this_word
        #right here - tally up how many new words got tags and if greater than 0, or greater than a percentage specified or a number of cycles, then redo this stage.
    new_procent = format(float(100*(tagged_total/(0.0+len(lines)))),'.2f')#the new percentage of the corpus that is tagged
    change_procent = format(float(new_procent) - float(procent),'.2f')#the amount the percent changed
    print "Added "+str(replaced)+" new tags, of "+str(len(lines))+" tokens. Now at "+str(new_procent)+"% tagged. +"+str(change_procent)+"% (of total) improvement."
    total_time_stage2 = time.clock()-starttime
    seconds_stage2 = int(total_time_stage2 % 60)
    minutes_stage2 = int(total_time_stage2 / 60)
    hours_stage2 = int(total_time_stage2 / 3600)
    print "Time taken: "+str(minutes_stage2)+" minutes "+str(seconds_stage2)+" seconds."
    partially_tagged_file = partially_tagged_file[:-11]+"_"+str(cycle)+"ambig.txt"
    cycle+=1
    g.close()
    if (cycle_type[0] == "n") and (int(cycle_type[1]) < cycle):
        tag_ambiguous_words(train, out, partially_tagged_file, unknown_wordlist,tagged_total,cycle, new_procent, cycle_type)
    elif (cycle_type[0] == "p") and (int(cycle_type[1]) < change_procent):
        tag_ambiguous_words(train, out, partially_tagged_file, unknown_wordlist,tagged_total,cycle, new_procent, cycle_type)
    elif (cycle_type[0] == "p") and (int(cycle_type[1]) >= change_procent):
        quit()
    elif (cycle_type[0] == "n") and (int(cycle_type[1]) >= cycle):
        quit()
    elif replaced >= 1:
        tag_ambiguous_words(train, out, partially_tagged_file, unknown_wordlist,tagged_total,cycle, new_procent, cycle_type)
    else:
        quit()
        
    

                    
##########################################################################################
##########################################################################################
##########################################################################################
######END AMBIGUOUS TAGGING###################################################################
##########################################################################################
##########################################################################################
##########################################################################################

















def main():
    x = 1
    arguments = sys.argv[1:] #everything separated by spaces in the command-line arguments will be in arguments
    
    ###TRAINING FROM A GOLD STANDARD###
    if "-GoldTraining" in arguments:
        gold_standard_folder = arguments[arguments.index("-GoldStandardFolder")+1]
        if "/" not in gold_standard_folder:
            gold_standard_folder = os.getcwd()+"/"+gold_standard_folder
        #print gold_standard_folder
        gold_standard_type = arguments[arguments.index("-GoldStandardType")+1]
        program_folder = os.getcwd()
        if "-AmbigToDefinite" in arguments: #Not implemented yet, but if "true" or something, it will treat unambiguous words with an overwhelming amount of one tag versus the others treated as unambiguous.
            ambigToDefinite = float(arguments[arguments.index("-AmbigToDefinite")+1])#I think this is the ratio that I am specifying? Check that. Or implement it.
            gold_training(program_folder, gold_standard_folder, gold_standard_type, ambigToDefinite)
        else:
            gold_training(program_folder, gold_standard_folder, gold_standard_type, "none")

    ###POS TAGGING###
    if "-POSTag" in arguments:
        output_folder = arguments[arguments.index("-OutputFolder")+1]#weirdly, you don't need to include the final / (works either way)
        if output_folder == "here":
            output_folder = os.getcwd()+"/"
            #CYCLE type. As in, do we do 5 cycles? Until no improvements? Until <x% improvement?
        try:
            cycle_type = arguments[arguments.index("-CycleType")+1]
            #acceptable cycle types: nx (n1 n5 etc, where the number is the number of cycles no matter what), px (p5) where the number is the amount of percentage increase in tagged percent at which the tagger will stop, and f where it goes until no more improvement. (f as in final)
        except:
            print "Default cyclic tagging: until no improvement"
            cycle_type = "f"

        if ("/" not in output_folder) and (output_folder != os.getcwd()):
            output_folder = os.getcwd()+"/"+output_folder+"/"
        training_folder = arguments[arguments.index("-TrainingFolder")+1]
        if "/" not in training_folder:
            training_folder = os.getcwd()+"/"+training_folder+"/"
        tokenized_file = arguments[arguments.index("-ParseThis")+1]#needs to be a file
        if "/" not in tokenized_file:
            tokenized_file = os.getcwd()+"/"+tokenized_file
        tag_unambiguous_words(training_folder, tokenized_file, output_folder, cycle_type)


    ###TOKENIZING###
    if "-tokenize" in arguments:
        to_tokenize = arguments[arguments.index("-tokenize")+1]
        print "NOT YET. In time, various tokenization schemes will be incorporated into this program. For now, no."

if __name__=="__main__":
    main()



###INSTRUCTIONS
    # Training: Right now, it's only equipped for PTB-style. A folder containing the 24 (or less, depending) folders each with their own .mrg files.
    # Sample command: python tagger.py -GoldTraining -GoldStandardFolder PTB -GoldStandardType PTB
    # The -GoldStandardType command is a dummy command for now but will be necessary in the future. Include anything there. PTB, derp, whatever.
    # The GoldStandardFolder can be an absolute path and it can be the name of a folder within the directory of this program. Either or.
    #
    # For tagging: 
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
###
