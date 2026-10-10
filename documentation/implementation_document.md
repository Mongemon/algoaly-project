# Implementation document
The main program itself consists of 4 files, trie.py, markov.py, catalog.py and main.py. trie.py consists of the backbone of the whole project; the generic trie (prefix tree) which markov.py uses to make the actual Markov chain. catalog.py has functions to query the database, stored in /data, which consists of all the monophonic melodies found in the music21 corpus. main.py is pretty self explanatory – it calls markov.py and catalog.py to make the main program. test.py has tests that test the functionalities of trie.py and markov.py. 

In /src there are still another 3 files which are not part of the main program: music_analysis.py, analyze_corpus.py, build_catalog.py. music_analysis and analyze_corpus were used to query music21 to gather information about how the corpus and music is displayed in the corpus to find a way to define “monophony” in a sensible way and to find a way to query the whole corpus. analyze_corpus.py can be ran and it will make an analysis of the whole corpus (running it takes around 15 min), build_catalog.py can also be ran and it will use analyze_corpus to scan the corpus and inserts all monophonic melodies to /data/melody_catalog.db (this will delete the old database and takes around 20 min). music_analysis.py has functions that analyze_corpus calls to analyze the corpus at the music / score level. 

The worst space complexity of the Markov chains (which are all stored in the trie) is O(Nm) where N is the total number of inserted notes and m is the Markov order. The time complexity to train the Markov chains i.e. function “fit(self, sequences)” is O(Nm). Generating the next note i.e. function "choose_next(self, context, rng)" takes around O(m) to O(N+m) in the worst scenario as the time complexity depends heavily on the trie made. Getting the whole trie i.e. "get_sequences(self)" (which __str__ calls) takes O(T) where T is the total number of trie nodes in the tree.

I think overall the project went well, but I spent a lot of the time analyzing the corpus and extracting data. I used probably 1 / 3 of the total time writing different tests to analyze the corpus and find a way to extract monophonic melodies from it and incorporate those melodies into the project in some type of sensible way. The algorithm itself, the trie and Markov are actually quite simple and easy to understand algorithms which didn’t take that much time to build. If I would do the course again I wouldn’t use that much time on data extraction as it is not really the core of the course. 

In this course I used LLM:s, precisely ChatGPT. ChatGPT was used to get a hang of music21, unittest and the music21 corpus structure analysis. 

Data sources
- music21 corpus

Learning sources
- https://music21.org/music21docs/ 
- https://www.youtube.com/watch?v=BZwdYmPS5f8 
- https://typing.python.org/en/latest/reference/generics.html 
- https://www.youtube.com/watch?v=KZeIEiBrT_w 
- https://docs.python.org/3/library/unittest.html 
- https://realpython.com/python-unittest/ 
