#User Guide
For now the project is divided into data and src. In data there's a database containing monophonic melodies from the music21 corpus and in src are all the python files. To run the main program one doesn't need to install any extra installation to python as the corpus files have been parsed into the database, so there's no need to install music21. But if one wants to see how the data analyzation and database building tools (music_analysis.py, analyze_corpus.py and build_catalog.py) function one has to install music 21. To get the main program running run:
```
python3 -m venv venv
source venv/bin/activate
cd src
python3 main.py
```
The first thing the main program does is to ask the user a title and a key to query the database for melodies. The query will give max 500 melodies to train with. Then it will ask the user how many queries should be used in training, all, a random set or some set of specific songs. Lastly it'll ask which Markov order to generate in and how many notes should be generated and then starts generating sequences until the user stops it.

If you wish to test the corpus analyzation tools you can download music21 by running:
```
pip install music21   
```
Take into account that analyze_corpus.py takes around 15 min to run and build_catalog.py will take around 20 min to run because of the corpus size. If you run build_catalog.py all of the database data will be deleted and redone, which takes around 20 min. 
