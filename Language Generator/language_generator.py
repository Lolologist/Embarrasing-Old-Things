#! /usr/bin/Python
# -*- coding: utf-8 -*-
import random
import sys
from operator import itemgetter
print
#Phonology Basics v.0.0.2

#After learning a method of setting values for each consonant and being able to check against them to better add neighboring sounds, I have decided to start more or less anew. Using lots of old code, though.

#Definitions for those reading, as well as to return english-language values when testing consonants

vl = "voiceless"
vd = "voiced"
bl = "bilabial"
ld = "labiodental"
dent = "dental"
alv = "alveolar"
postalv = "postalveolar"
retro = "retroflex"
pal = "palatal"
vel = "velar"
uv = "uvular"
phary = "pharyngeal"
glott = "glottal"
exp = "plosive"
nas = "nasal"
trill = "trill"
flap = "flap"
tap = "tap"
fric = "fricative"
latfric = "lateral fricative"
approx = "approximant"
latapprox = "lateral approximant"


#All of the consonants
consonantlist= {
u"p" : [vl, bl, exp],
u"b" : [vd, bl, exp],
u"m" : [vd, bl, nas],
u"ʙ" : [vd, bl, trill],
u"ɸ" : [vl, bl, fric],
u"β" : [vd, bl, fric],
u"ɱ" : [vd, ld, nas],
u"ⱱ" : [vd, ld, flap], #tremendously rare, only recently documented. Leave out? Not on official IPA chart but on my IPA pallete
u"f" : [vl, ld, fric],
u"v" : [vd, ld, fric],
u"ʋ" : [vd, ld, approx],
u"t" : [vl,alv,exp],
u"d":[vd, alv, exp],
u"n":[vd, alv, nas],
u"r":[vd, alv, trill],
u"ɾ":[vd, alv, tap],
u"θ":[vl, dent, fric],
u"ð":[vd, dent, fric],
u"s":[vl, alv, fric],
u"z":[vd, alv, fric],
u"ʃ":[vl, postalv, fric],
u"ʒ":[vd, postalv, fric],
u"ɬ":[vl, alv, latfric],
u"ɮ":[vd, alv, latfric],
u"ɹ":[vd, alv, approx],
u"l":[vd, alv, latapprox],
u"ʈ":[vl, retro, exp],
u"ɖ":[vd, retro, exp],
u"ɳ":[vd, retro, nas],
u"ɽ":[vd, retro, tap],
u"ʂ":[vl, retro, fric],
u"ʐ":[vd, retro, fric],
u"ɻ":[vd, retro, approx],
u"ɭ":[vd, retro, latapprox],
u"c":[vl, pal, exp],
u"ɟ":[vd, pal, exp],
u"ɲ":[vd, pal, nas],
u"ç":[vl, pal, fric],
u"ʝ":[vd, pal, fric],
u"j":[vd, pal, approx],
u"ʎ":[vd, pal, approx],
u"k":[vl, vel, exp],
u"g":[vd, vel, exp],
u"ŋ":[vd, vel, nas],
u"x":[vl, vel, fric],
u"ɣ":[vd, vel, fric],
u"ɰ":[vd, vel, approx],
u"ʟ":[vd, vel, latapprox],
u"q":[vl, uv,exp],
u"ɢ":[vd, uv, exp],
u"ɴ":[vd, uv, nas],
u"ʀ":[vd, uv, trill],
u"χ":[vl, uv, fric],
u"ʁ":[vd, uv, fric],
u"ħ":[vl, phary,fric],
u"ʕ":[vd, phary, fric],
u"ʔ":[vl, glott, exp],
u"h":[vl, glott, fric],
u"ɦ":[vd, glott, fric],
}


voiced = ["b","m","ʙ","β","ɱ","ð","v","ʋ","d","n","r","ɾ","z","ʒ","ɖ","ɳ","ɽ","ʐ","ɻ","ɭ","ɟ","ɲ","ʝ","j","ʎ","g","ŋ","ɣ","ɰ","ʟ","ɢ","ɴ","ʀ","ʁ","ʕ","ɦ"]
voiceless =["p","ɸ","f","t","θ","ɬ","s","ʃ","ʈ","ʂ","c","ç","k","x","q","χ","ħ","ʔ","h"]
allconsonants = ["p","ɸ","f","t","θ","ɬ","s","ʃ","ʈ","ʂ","c","ç","k","x","q","χ","ħ","ʔ","h","b","m","ʙ","β","ɱ","ð","v","ʋ","d","n","r","ɾ","z","ʒ","ɖ","ɳ","ɽ","ʐ","ɻ","ɭ","ɟ","ɲ","ʝ","j","ʎ","g","ŋ","ɣ","ɰ","ʟ","ɢ","ɴ","ʀ","ʁ","ʕ","ɦ"]


consplaces = {"bilabials":99,"labiodentals":95,"dentals":75,"alveolars":99,"postalveolars":70,"retroflexes":35,"palatals":70,"velars":90,"uvulars":20,"pharyngeals":15,"glottals":70} #weights for each place of articulation by what % of the time that shows up in languages... hopefully
# Places of Articulation with relative weights for each sound contained within, roughly by what percent of languages they show up in (my guesses anyways, and particularly rough ones so far)
bilabials ={u"p":99,u"b":93,u"m":99,u"ʙ":22,u"ɸ":23,u"β":23} 
labiodentals ={u"ɱ":15,u"f":99,u"v":95,u"ʋ":38}
dentals ={u"θ":85,u"ð":83}
alveolars ={u"t":99,u"d":96,u"n":99,u"r":70,u"ɾ":70,u"s":85,u"z":81,u"ɬ":5,u"ɮ":5,u"ɹ":10,u"l":80}
postalveolars ={u"ʃ":60,u"ʒ":55}
retroflexes = {u"ʈ":20,u"ɖ":17,u"ɳ":31,u"ɽ":19,u"ʂ":10,u"ʐ":8,u"ɻ":5,u"ɭ":5}
palatals = {u"c":30,u"ɟ":25,u"ɲ":25,u"ç":15,u"ʝ":10,u"j":99,u"ʎ":10}
velars ={u"k":99,u"g":93,u"ŋ":80,u"x":65,u"ɣ":60,u"ɰ":30,u"ʟ":10}
uvulars ={u"q":18,u"ɢ":15,u"ɴ":12,u"ʀ":10,u"χ":30,u"ʁ":25}
pharyngeals ={u"ħ":20,u"ʕ":16}
glottals ={u"ʔ":70,u"h":90,u"ɦ":20}

####DECIDING SORTS OF PHONEMIC DISTINCTIONS####
#Do we want just raw phonemes? Perhaps the language can make a distinction between labialized consonants? Or velarized?
#labialized, aspirated, valarized, glottalized, pharyngealized...









#Going to start picking characters here
consonants = []
finalconsonants = {}
numberofcons1 =0
numberofcons = 0
def chooseconsonants():
    consonants = [] #filled by each consonant to be added to the 'language'
    #choosing the number of consonants
    numberofcons1 = random.randint(1,100) #this is to approximate a bell-curve distribution for the number of consonants
    if 1<= numberofcons1 <= 5:
        numberofcons = random.randint(6,12)
    if 6 <= numberofcons1 <= 15:
        numberofcons = random.randint(13,20)
    if 16 <= numberofcons1 <= 84:
        numberofcons = random.randint(20,28) # each of these represents the range of a standard deviation from the middle, assuming a bell curve for percentage and distribution but not for the number of consonants. Wikipedia says 22-26 is normal, hench this range for the middle
    if 84 <= numberofcons1 <= 95:
         numberofcons = random.randint(29,50)
    if 96 <= numberofcons1 <= 100:
        numberofcons = random.randint(39,51) #placeholder, I'm having trouble with the larger number of consonants since I don't have labialization and whatever
         #numberofcons = random.randint(51,81) #since I'm not doing labialized or anything right now, might wanna forego above 50 or so, but am keeping it in for now. I think it ran once and tried to do 81 and didn't break or anything, running out of consonants or anything, so I suppose it can stay
         
    print numberofcons, "is the number of consonants we want to end up with."

    while int(numberofcons) >= len(consonants):
        whichplace = Test(consplaces) #test which place of articulation to use, using the weights above
        if whichplace == "bilabials":
            whichconsonant = Test(bilabials) #I hope there's a way to cut all of this out here, and somehow get the string outputted from Test to be interpreted as the list it is, but I don't know how
        if whichplace == "labiodentals":
            whichconsonant = Test(labiodentals)
        if whichplace == "dentals":
            whichconsonant = Test(dentals)
        if whichplace == "alveolars":
            whichconsonant = Test(alveolars)
        if whichplace == "postalveolars":
            whichconsonant = Test(postalveolars)
        if whichplace == "palatals":
            whichconsonant = Test(palatals)
        if whichplace == "velars":
            whichconsonant = Test(velars)
        if whichplace == "retroflexes":
            whichconsonant = Test(retroflexes)
        if whichplace == "uvulars":
            whichconsonant = Test(uvulars)
        if whichplace == "pharyngeals":
            whichconsonant = Test(pharyngeals)
        if whichplace == "glottals":
            whichconsonant = Test(glottals)            
        #for now, it's ok, but make sure to include a test for if it's voiced, and if the voiceless version is included as will be necessary (mentioned above, as well)

        if whichconsonant not in consonants: #if the randomly selected consonant is not yet in the list of consonants gathered so far,
            consonants += whichconsonant #add it
    #print "Here are the consonants, in no particular order, but eventually will be in a nice chart I hope."
    for each in consonants:
        #print each.encode('utf-8')
        finalconsonants[each] = consonantlist[each]
    #for k,v in finalconsonants.iteritems():
       # print k.encode("utf-8"), " ".join(v)

def Test(d): #This helps determine weighted choices, rather clever really. I found it online.
    r = random.uniform(0, sum(d.itervalues()))
    s = 0.0
    for k, w in d.iteritems():
        s += w
        if r < s: return k
    return k
chooseconsonants()


def prettyprintvowels(): #IN PROGRESS
    collumns = ["Close","Near-Close","Close-Mid","Mid","Open-Mid","Near-Open","Open"]
    rows = ["Front","Near-Front","Central","Near-Back","Back"]
    vchart = [
        ["\tF\t", "NF\t", "C\t", "NB\t", "B"],
        ["Close"," "," ","  ------------"," "," ", "--------"," "," "],
        ["Near-Close","\\"," "," ","  \\","\t"," ","|"],
        ["Close-Mid"]
        ]

    x = 0
    y = 0
    while y < 2:
        print " ".join(vchart[y]).encode('utf-8')
        y += 1


def prettyprintIPAchart():
    collumns = ["bilabial","labiodental","dental","alveolar","postalveolar","retroflex","palatal","velar","uvular","pharyngeal","glottal"]
    rows = ["plosive","nasal","trill","tap","flap","fricative","lateral fricative","approximant","lateral approximant"]
    IPAchart = [
        ["\t\t", " BL\t"," LD\t"," DN\t"," AV\t"," PA\t"," RT\t"," PL\t"," VL\t"," UV\t"," PH\t"," GL\t"],
        ["Plosive\t\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","  \t"," "," ","\t"," "," ","\t"," "," "],
        ["Nasal\t\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","  \t"," "," ","\t"," "," ","\t"," "," "],
        ["Trill\t\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","  \t"," "," ","\t"," "," ","\t"," "," "],
        ["Tap or Flap\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","  \t"," "," ","\t"," "," ","\t"," "," "],
        ["Fricative\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","  \t"," "," ","\t"," "," "],
        ["Lateral Fricative\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","  \t"," "," ","\t"," "," ","\t"," "," "],
        ["Approximant\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," "],
        ["Lateral Approximant\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," ","\t"," "," "],
        ]
    

    therow = 0
    thecollumn = 0
    for pos in collumns:
        for man in rows:
            for k, v in finalconsonants.iteritems():
                if pos in v and man in v:
                    if pos == "bilabial":
                        thecollumn = 1
                    if pos == "labiodental":
                        thecollumn = 4
                    if pos == "dental":
                        thecollumn = 7
                    if pos == "alveolar":
                        thecollumn = 10
                    if pos == "postalveolar":
                        thecollumn = 13
                    if pos == "retroflex":
                        thecollumn = 16
                    if pos == "palatal":
                        thecollumn = 19
                    if pos == "velar":
                        thecollumn = 22
                    if pos == "uvular":
                        thecollumn = 25
                    if pos == "pharyngeal":
                        thecollumn = 28
                    if pos == "glottal":
                        thecollumn = 31
                    if man == "plosive":
                        therow = 1
                    if man == "nasal":
                        therow = 2
                    if man == "trill":
                        therow = 3
                    if man == "tap":
                        therow = 4
                    if man == "flap":
                        therow = 4
                    if man == "fricative":
                        therow = 5
                    if man == "lateral fricative":
                        therow = 6
                    if man == "approximant":
                        therow = 7
                    if man == "lateral approximant":
                        therow = 8
                    if v[0] == "voiced":
                        thecollumn += 1
                    IPAchart[therow][thecollumn] = k
                    #print v[0], pos, man, k.encode('utf-8')

    #print IPAchart
    x = 0
    y = 0
    while y < 9:
        print " ".join(IPAchart[y]).encode('utf-8')
        y += 1
#This area has room to improve the chart display. But it's close enough to see what's going on!!!!

    
prettyprintIPAchart()










print

###VOWELS TIME###

vowellist = {
u"i" : ["close","front","unrounded"], #add ATR values later so we have choice of differentiating by them 
u"ɪ" : ["near-close","near-front","unrounded"],
u"e" : ["close-mid","front","unrounded"],
u"ɛ" : ["open-mid","front","unrounded"],
u"æ" : ["near-open","front","unrounded"],
u"a" : ["open","front","unrounded"],
u"y" : ["close","front","rounded"],
u"ʏ" : ["near-close","near-front","rounded"],
u"ø" : ["close-mid","front","rounded"],
u"œ" : ["open-mid","front","rounded"],
u"ɶ" : ["open","front","rounded"],
u"ɨ" : ["close","central","unrounded"],
u"ɘ" : ["close-mid","central","unrounded"],
u"ə" : ["mid","central","neither"], #neither! What do I do?
u"ɜ" : ["open-mid","central","unrounded"],
u"ɐ" : ["near-open","central","neither"],
u"ʉ" : ["close","central","rounded"],
u"ɵ" : ["close-mid","central","rounded"],
u"ɞ" : ["open-mid","central","rounded"],
u"ʊ" : ["near-close","near-back","rounded"],
u"ɯ" : ["close","back","unrounded"],
u"ɤ" : ["close-mid","back","unrounded"],
u"ʌ" : ["open-mid","back","unrounded"],
u"ɑ" : ["open","back","unrounded"],
u"u" : ["close","back","rounded"],
u"o" : ["close-mid","back","rounded"],
u"ɔ" : ["open-mid","back","rounded"],
u"ɒ" : ["open","back","rounded"],                                        
}
numberofvows = 0
numberofvows = 0
vowels = [] #filled by each vowel to be added to the 'language'
    #choosing the number of vowels
numberofvows1 = random.randint(1,100) #this is to approximate a bell-curve distribution for the number of vowels
if 1<= numberofvows1 <= 5:
    numberofvows = random.randint(2,4)
if 6 <= numberofvows1 <= 15:
    numberofvows = random.randint(5,10)
if 16 <= numberofvows1 <= 84:
    numberofvows = random.randint(11,15) # each of these represents the range of a standard deviation from the middle, assuming a bell curve for percentage and distribution but not for the number of vowels. Wikipedia says 13-21 is kinda high, hence this range for the middle
if 84 <= numberofvows1 <= 95:
    numberofvows = random.randint(13,16)
#    numberofvows = random.randint(16,23)
if 96 <= numberofvows1 <= 100:
    numberofvows = random.randint(13,16)
#    numberofvows = random.randint(24,32) #I don\'t have the ability to add nasalized as a property, right now, I\'ll just allow a slightly less realistic /sort/ of vowels but allowing the rightish /number/ of them. May be a stupid approach.
         
print numberofvows, "is the number of vowels we want to end up with."

#How do I choose which vowels? Probably want to try and make them as spread apart as possible, but there are languages with a bunch just mashed up together. Maybe just like the consonants one? Just weighted vowels?
#vowelmatrix = [
#50,[40,20,40], #close
#20,[50,50], #near-close
#50,[48,6,48], #close-mid
#60,[100], #mid
#50,[48,6,48], #open-mid
#30,[90,10], #near-open
#50,[50,50],
#]

round1vowels = [u'i',u'e',u'a',u'o',u'u']
round2vowels = [u'ə',u'ɛ',u'æ',u'ɑ',u'ɔ',u'ɯ']
round3vowels = [u'ʌ',u'ɒ',u'ʊ',u'y',u'ɪ',u'œ',u'ɤ']
round4vowels = [u'ʏ',u'ɨ',u'ɘ',u'ɶ',u'ø',u'ɵ',u'ɜ',u'ɞ',u'ɐ',u'ʉ']
x = 0
while x < numberofvows:
    y=random.randint(1,100)
    if y <=30:
        z = random.randint(0,4)
        if round1vowels[z] not in vowels:
            vowels.append(round1vowels[z])
            x += 1
    elif 31<=y<=55:
        z = random.randint(0,5)
        if round2vowels[z] not in vowels:
            vowels.append(round2vowels[z])
            x += 1
    elif 56<=y<=84:
        z = random.randint(0,6)
        if round3vowels[z] not in vowels:
            vowels.append(round3vowels[z])
            x += 1
    elif 85<=y<=100:
        z = random.randint(0,9)
        if round4vowels[z] not in vowels:
            vowels.append(round4vowels[z])
            x += 1

for each in vowels:
    print each,

###### SYLLABLES#######
#print 
#print
#print "Holy cow, so those are the consonants and vowels we're working with! What say you we do something with 'em now,"
#print "like come up with a syllable structure? That way we can start combining them together."
#print "First up is the Sonority Scale."
scale = []
#I probably ought add in a way to add any two bits together, maybe. And definitely need to... something. Damn. I forget.
#KEY:
#Voiceless stops = 1, voiced stops = 2, voiceless affricates = 3, voiced affricated = 4, voiceless fricatives = 5, voiced fricatives =6, nasals = 7, taps/flaps = 8, trills = 9, laterals = 10, approximants = 11
#KEY, PLACES
#bilabial = 1, labiodental = 2, dental = 3, alveolar = 4, p.alveolar = 5, retro = 6, palatal = 7, velar=8, uvular = 9, pharyngeal = 10, glottal = 11
#KEY, MANNERS (mind them, lol)
#plosive = 1, nasal = 2, trill=3,tap/flap=4,fricative=5,latfric=6,approx=7,latapprox=8
sonorityconstlist= [[u"p",1],[u"b",2],[u"m",7],[u"ʙ",9],[u"ɸ",5],[u"β",6],[u"ɱ",7],[u"ⱱ",8],[u"f",5],[u"v",6],[u"ʋ",11],[u"t",1],[u"d",2],[u"n",7],[u"r",9],[u"ɾ",8],[u"θ",5],[u"ð",6],[u"s",5],[u"z",6],[u"ʃ",5],[u"ʒ",6],[u"ɬ",10],[u"ɮ",10],[u"ɹ",11],[u"l",10],[u"ʈ",1],[u"ɖ",2],[u"ɳ",7],[u"ɽ",8],[u"ʂ",5],[u"ʐ",6],[u"ɻ",11],[u"ɭ",10],[u"c",1],[u"ɟ",2],[u"ɲ",7],[u"ç",5],[u"ʝ",6],[u"j",11],[u"ʎ",10],[u"k",1],[u"g",2],[u"ŋ",7],[u"x",5],[u"ɣ",6],[u"ɰ",11],[u"ʟ",10],[u"q",1],[u"ɢ",2],[u"ɴ",7],[u"ʀ",9],[u"χ",5],[u"ʁ",6],[u"ħ",5],[u"ʕ",6],[u"ʔ",1],[u"h",5],[u"ɦ",6]]
fsc = [] #final sonorant-scale consonant list

for each in sonorityconstlist:
    if each[0] in finalconsonants:
        fsc.append(each)
#according to the sonority scale, done below, alter the numbers in fsc to eliminate differences. AKA if 1.2.3 then make all of then 2 or something.



##OBSTRUENTS
#stops
a = random.randint(1,30)
if a <15:
    scale.append("1")
    scale.append("2")
else:
    scale.append("1.2")

#affricates
b = random.randint(1,30)
if b <14:
    scale.append("3")
    scale.append("4")
elif 15<b<24:
    scale.append("3.4")
elif 25<b<=30:
    scale[-1] = scale[-1]+".3.4"

#fricatives
c = random.randint(1,30)
if c <14:
    scale.append("5")
    scale.append("6")
elif 15<c<22:
    scale.append("5.6")
elif 23<c<=30:
    scale[-1] = scale[-1]+".5.6"

##SONORANTS
#nasals
scale.append("7") #Oh, I probably need a way to add in the actual consonants after all this...
#flap/tap
c = random.randint(1,30)
if c < 21:
    scale.append("8")
else:
    scale[-1] = scale[-1]+".8"
#liquids, rhotics, etc
d = random.randint(1,30)
if d<13:
    scale.append("9")
    scale.append("10")
elif 14<d<24:
    scale.append("9.10")
elif 25<d<=30:
    scale[-1] = scale[-1]+".9.10"
d = random.randint(1,30)
if d > 22:
    scale[-1] = scale[-1]+".11"
else:
    scale.append("11")
#vowels
sonv = random.randint(1,30)
if sonv <15:
    scale.append("13")
    scale.append("14")
    scale.append("15")
else:
    scale.append("13.14.15")

print
print
print " ".join(scale)
print "Came up with a Sonority Scale successfully."

########SYLLABLE STRUCTURE#########
print
print "Time now to come up with a syllable structure."


####ONSET####
ons = random.randint(1,10)
if ons<=4:
    onset = "R" #onset required
else:
    onset = "O" #optional onset
    onsprob = random.randint(3,7)#a 40% range of the time
    onset += str(onsprob)
onsnum = random.randint(1,10)
if onsnum <= 3:
    onset +="s" #single consonant only
else:
    onset +="c" #clusters allowed
    lenon = random.randint(1,30)
    if lenon <10:
        onset += "s"#short, 2cons max
    elif 10<=lenon<=22:
        onset += "m"#medium, 2-3 cons
    else:
        onset += "l"#large, 2-4cons

#####NUCLEUS       
#Decide if vowel clusters are allowed
vc = random.randint(1,10)
if vc <= 8:
    nucleus = "C"#complex, aka 2 or 3 vowels
else:
    nucleus = "S"#simple, aka 1 vowel

#####CODA
neccoda = random.randint(1,40)
if neccoda <=25:
    coda = "U" #unnecessary, unrestricted
elif 26<=neccoda <=37:
    coda = "N" #necessary, unrestricted
else:
    coda = "R" #unnecessary, restricted
syllable = onset + nucleus + coda
print "Successfully came up with a syllable structure. Debug code:", syllable
print

def wordmake(syllablesneeded,ons,nuc,cod):
    print syllablesneeded, ons, nuc, cod
    syllablessofar = 0
    syllables = []
    onset = []
    nucleus = []
    coda = []
    #print len(fsc) #shows up as 1 too many consonants. WHY?
    if ons[0] == "O":
        if ons[1] >5:
            if ons[2] == "c":
                if ons[3] == "s":
                    pick1 = random.randint(0,len(fsc)-1)
                    pick2 = random.randint(0,len(fsc)-1)
                    while fsc[pick1][1] == fsc[pick2][1]:
                        pick2 = random.randint(0,len(fsc)-1)
                    addthese = [pick1,pick2] #the number in fsc relating to which consonant is picked at random
                    addthese2 = [fsc[addthese[0]],fsc[addthese[1]]] #adds both consonants
                    addthese2 = sorted(addthese2, key=itemgetter(1)) #sorts them by sonority
                    
                    print addthese2[0][0].encode('utf-8'),addthese2[1][0].encode('utf-8')
# to add: if consonantlist[pick1[0]] == consonantlist[pick2[0]] or something like that to make sure you dont get like a [pb] cluster, and something to avoid wacky shit like [ʔχ], maybe a weight to avoid farther-back consonants clustering
#                    print fsc[addthese[0]][0].encode('utf-8'),
#                    print fsc[addthese[1]][0].encode('utf-8')
                    #sorted_addthese = sorted(addthese, key=itemgetter(1), reverse=False)
                    #print sorted_addthese
###NUCLEUS
    #if nuc == "S":
    nucleus.append(vowels[random.randint(1,len(vowels)-1)])
    print nucleus[0]
        
        
    #else: #if nuc = "c", aka a complex nucleus of 2 or 3 vowels (dipthong or tripthong)
      #  pass
    coda = ["p"]

    return onset, nucleus, coda

'''
    if ons[0] =="O":
        if random.randint(1,10)<int(ons[1]): #pick if option onset shows up
            print "shows up"
            if ons[2] == "s": #simple onset, one consonant allowed
                pick = random.randint(0,len(fsc)-1)
                onset.append(fsc[pick][0])
            else: #ons[2] == "c"
                if ons[3] == "s":
                    onsets = 2
                    pick1 = random.randint(0,len(fsc)-1)
                    pick2 = random.randint(0,len(fsc)-1)
                    if fsc[pick1][1] <= fsc[pick2][1]:
                        onset.append(fsc[pick1][0])
                        onset.append(fsc[pick2][0])
                    
                    else:
                        onset.append(fsc[pick2][0])
                        onset.append(fsc[pick1][0])
                        print onset
                elif ons[3] == "m":
                    onsets = random.randint(2,3)
                    if onsets == 2:
                        pick1 = random.randint(0,len(fsc)-1)
                        pick2 = random.randint(0,len(fsc)-1)
                        addthese = [pick1,pick2]
                        sorted_addthese = sorted(addthese, key=itemgetter(1), reverse=False)
                        print sorted_addthese
                    else:
                        pick1 = random.randint(0,len(fsc)-1)
                        pick2 = random.randint(0,len(fsc)-1)
                        pick3 = random.randint(0,len(fsc)-1)
                        addthese = [pick1,pick2,pick3]
                        sorted_addthese = sorted(addthese, key=itemgetter(1), reverse=False)
                        print sorted_addthese
                elif ons[3] == "l":
                    onsets= random.randint(2,4)
                    pick1 = random.randint(0,len(fsc)-1)
                    pick2 = random.randint(0,len(fsc)-1)
                    pick3 = random.randint(0,len(fsc)-1)
                    pick4 = random.randint(0,len(fsc)-1)
                    addthese = [pick1,pick2,pick3,pick4]
                    sorted_addthese = sorted(addthese, key=itemgetter(1), reverse=False)
                    #print sorted_addthese
        else:
            print "no onset"
            coda.append("")
    else:
        print "required onset"
        if ons[1] == "s": #simple onset, one consonant allowed
                pick = random.randint(0,len(fsc)-1)
                onset.append(fsc[pick][0])
        else:
            if ons[2] == "s":
                onsets = 2
                pick1 = random.randint(0,len(fsc)-1)
                pick2 = random.randint(0,len(fsc)-1)
                if fsc[pick1[1]] <= fsc[pick2[1]]:
                    onset.append(fsc[pick1][0])
                    onset.append(fsc[pick2][0])
                else:
                    onset.append(fsc[pick2][0])
                    onset.append(fsc[pick1][0])                        
            elif ons[2] == "m":
                onsets = random.randint(2,3)
                if onsets == 2:
                    pick1 = random.randint(0,len(fsc)-1)
                    pick2 = random.randint(0,len(fsc)-1)
                    addthese = [pick1,pick2]
                    sorted_addthese = sorted(addthese, key=itemgetter(1), reverse=False)
                    print sorted_addthese
                else:
                    pick1 = random.randint(0,len(fsc)-1)
                    pick2 = random.randint(0,len(fsc)-1)
                    pick3 = random.randint(0,len(fsc)-1)
                    addthese = [pick1,pick2,pick3]
                    sorted_addthese = sorted(addthese, key=itemgetter(1), reverse=False)
                    print sorted_addthese
            elif ons[2] == "l":
                onsets= random.randint(2,4)
                pick1 = random.randint(0,len(fsc)-1)
                pick2 = random.randint(0,len(fsc)-1)
                pick3 = random.randint(0,len(fsc)-1)
                pick4 = random.randint(0,len(fsc)-1)
                if onsets == 2:    
                    addthese = [pick1,pick2]
                if onsets == 3:    
                    addthese = [pick1,pick2,pick3]
                if onsets == 4:    
                    addthese = [pick1,pick2,pick3,pick4]
                sorted_addthese = sorted(addthese, key=itemgetter(1), reverse=False)
                print sorted_addthese
    #print "".join(coda).encode('utf-8')
    return coda
'''
            
####WORDS
print "That ought be everything we need for now. Time to make some words!"
print "we are going to spit out 15 random words. 5 single-syllable, 5 bisyllabic, and 5 trisyllabic words."
sylwords1 = []
sylwords2 = []
sylwords3 = []
x = 0
while x <5:
    onset = "O6cs"
    word = wordmake(1,onset,nucleus,coda)
    sylwords1.append(word)
    x += 1
x = 0
while x <5:
    word = wordmake(2,onset,nucleus,coda)
    sylwords2.append(word)
    x += 1
x = 0
while x <5:
    word = wordmake(3,onset,nucleus,coda)
    sylwords3.append(word)
    x += 1




#Notes from Wikipedia

#Phonological extremes: Ubyx and Arrernte have 2 phonemic vowels, but Ngwe has 14, 12 of which are long or short, making 26 oral vowels, plus 6 nasalized vowels, long and short, meaning 38 vowels.
#Rotokas has only 6 consonants whereas Ubyx has 81.
#The most common vowel system consists of the five vowels /i/, /e/, /a/, /o/, /u/. The most common consonants are /p/, /t/, /k/, /m/, /n/. Very few languages lack any of these: Arabic lacks /p/, standard Hawaiian lacks /t/, Mohawk and Tlingit lack /p/ and /m/, Hupa lacks both /p/ and a simple /k/, colloquial Samoan lacks /t/ and /n/, while Rotokas and Quileute lack /m/ and /n/.
#22-26 consonants are average, and English's 13-21 vowels (including dipthongs) is somewhat high.
#Tones are 0-9, won't be messing with them for a while
#phonemic unvoiced sonorants occur in about 5% of world's languages
#Obstruents are prototypically voiceless, though voiced obstruents are common. This contrasts with sonorants, which are much more rarely voiceless.

#All the vowels, so far not used
rawvowels = ["i","y","ɨ","ʉ","ɯ","u","ɪ","ʏ","e","ø","ɘ","ɵ","ʊ","ɤ","o","ə","ɛ","œ","ɜ","ɞ","ʌ","ɔ","æ","ɐ","a","ɶ","ɑ","ɒ"]
frontvowelsU =["i","e","ɛ","æ","a"]
frontvowelsR = ["y","ø","œ","ɶ"]
nearfrontvowelsU =["ɪ"]
nearfrontvowelsR = ["ʏ"]
centralvowelsU =["ɨ","ɘ","ɜ"]
centralvowelsR = ["ʉ","ɵ","ɞ"]
nearbackvowelsR = ["ʊ"]
backvowelsU = ["ɯ","ɤ","ʌ","ɑ"]
backvowelsR = ["u","o","ɔ","ɒ"]
closevowelsR =["y","ʉ","u"]
closevowelsU = ["i","ɨ","ɯ"]
nearclosevowelsU =["ɪ"]
nearclosevowelsR =["ʏ","ʊ"]
closemidvowelsU =["e","ɘ","ɤ"]
closemidvowelsR =["ø","ɵ","o"]
midvowel =["ə"]
openmidvowelsU =["ɛ","ɜ","ʌ"]
openmidvowelsR =["œ","ɞ","ɔ"]
nearopenvowelsU = ["æ"]
nearopenvowel = ["ɐ"]
openvowelsU =["a","ɑ"]
openvowelsR =["ɶ","ɒ"]
