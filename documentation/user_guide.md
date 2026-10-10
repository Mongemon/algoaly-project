# User Guide
The project is divided into /data and /src. In data there's a database containing monophonic melodies from the music21 corpus and in src are all the python files. To run the main program one doesn't need to install any extra installations as the corpus files have been parsed into the database, so there's no need to install music21. But if one wants to see how the data analyzation and database building tools (music_analysis.py, analyze_corpus.py and build_catalog.py) function one has to install music 21. To get the main program running run:
```
python3 -m venv venv
source venv/bin/activate
cd src
python3 main.py
```
The first thing the main program does is to ask whether the user wants to use melodies from the corpus/database or the user's own melody. If the user chooses corpus data the program will ask for a title and key to query the database and after querying it will ask in which way queried melodies should be selected for training. If the user chooses own melody the program will ask for the melody. After choosing the training data the program will ask the Markov order of the generation and the number of generated notes to be generated. Then the program asks for a starting sequence, the user can choose to give a starting sequence or optionally the program will randomly choose a valid starting sequence. Then the program will generate as many sequences as the user wants until the user chooses to quit the program.

If you wish to test the corpus analyzation tools you can download music21 by running:
```
pip install music21   
```
Take into account that analyze_corpus.py takes around 15 min to run and build_catalog.py will take around 20 min to run because of the corpus size. If you run build_catalog.py all of the database data will be deleted and redone, which takes around 20 min. 
