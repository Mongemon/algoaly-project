1. This week I did a tool for analyzing the music21 corpus for monophonic melodies and created a tool to take the monophonic melodies from the corpus into a database and created a database.
2. The program has it's first steps done, which is basically data extraction for the Markov Chains. I used first analyze_corpus.py to analyze the basic corpus structure and music_analysis.py to analyze the separate scores. analyze_corpus.py main() parses the whole corpus and goes through every single score and analyzes for monophonic scores. Monophony is defined in this case as a score which does not contain chords, which does not have more than 1 active parts (e.g. parts with musical content), which does not have more than 2 voices and which do not have overlapping notes. The rules for monophony are overly strict and it probably labels songs that truly are monophonic as polyphonic but it is better to mislabel too strict rather than too loose, as polyphonic songs could create huge problems for the Markov Chains while a slightly smaller pool of songs wont be a problems. After running the code I got:
```
round : 3193
round : 3194
printing summary...
CORPUS SUMMARY
--------------
Total scores:        15026
Usable melodies:     12281
Rejected:            2745
With chords:         325
Multiple parts:      1972
Overlapping notes:   638
```
12281 melodies is way more than enough for our uses, but the code took about 15 min to run, so querying songs directly from the corpus wont be possible in the application, therefore, I chose to move all the monophonic scores into a SQLite database where they could be queried way faster. I made build_catalog.py for making the database and got this after running it:
```
CATALOG COMPLETE
----------------
Files:    3194
Scores:   15026
Accepted: 12279
```
For some reason the analysis was a bit different than before, only 12279 accepted while before it was 12281, while analyzing in both instant there was some random problems while analyzing certain notes of some scores but the corpus handled the problems by itself and 2 lost scores does not matter in the big picture. Now with the database the user doesn't even need to download music21 to use the application as all the songs and melodies are already in the database.

3. I learned quite a lot about the music21 corpus structure and how information is stored in the corpus.  

4. Many things have gotten clearer not that I've gotten further in the project and there has not been anything too challenging, though it took a while to get a hang of the corpus.  

5. Next I'll start working on the trie and Markov chains.  

time used this week: 23h
