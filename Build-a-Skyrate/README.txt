README for Daniel Bishop's Build-a-Skyrate
This was a project in my free time, unrelated to classes, in middle 2011.
Using what by a slight stretch could be considered Hidden Markov Modeling,
I take a given user from my private corpus of Skyrates users and text,
and approximate, one word at a time, a sentnece.
Beginning with a dummy start-of-line character and ending at an end-of-line
character, each word that follows is picked based solely on what the previous
word was and how often each word that can follow it does so.
As such, any two words in a row will make sense and certain longer strings
will, as well, but most sentences as a whole are fun gibberish.
This project is provided with the main portion of the project but cannot
be run due to missing the corpus and some supporting programming.
It is intact as I last left it, with debug info and notes to myself and the
public, to give you an idea of how I made it.
If you would like to see this program working, you can do so here:
http://lo.lologi.st/skyrates/build-a-skyrate.html

-Daniel Bishop
