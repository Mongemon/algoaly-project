import json
import sqlite3

from pathlib import Path

from music21 import corpus
from music21.stream import Opus, Score

from music_analysis import analyze_structure, get_pitches, get_key
from analyze_corpus import get_scores

#getting the database location
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
db_path = project_root / "data" / "melody_catalog.db"

#Deletes an old table and creates a new one
def create_database(connection):

	connection.execute("DROP TABLE IF EXISTS melodies")

	connection.execute(
	"""
	CREATE TABLE melodies (
		id INTEGER PRIMARY KEY,
		title TEXT NOT NULL,
		key TEXT,
		note_count INTEGER NOT NULL, 
		lowest_pitch INTEGER NOT NULL,
		highest_pitch INTEGER NOT NULL,
		pitches TEXT NOT NULL
		)
		"""
	)
	connection.commit()

#Analyzes one accepted meody and inserts it into the database
def add_melody(connection, score):
	pitches = get_pitches(score)

	if not pitches:
		return False

	title = None

	if score.metadata:
		title = score.metadata.title

	if not title:
		return False

	key = get_key(score)

	lowest_pitch = min(pitches)
	highest_pitch = max(pitches)

	connection.execute(
		"""
		INSERT INTO melodies (
	 		title,
	 		key,
	 		note_count,
	 		lowest_pitch,
	 		highest_pitch,
	 		pitches
	 		)
	 	VALUES (?, ?, ?, ?, ?, ?)
	 	""",
	 	(
	 		title,
	 		str(key),
	 		len(pitches),
	 		lowest_pitch,
	 		highest_pitch,
	 		json.dumps(pitches),
	 		)
	 	)
	return True

#Goes through the corpus and stores all accepted melodies
def build_catalog(paths, connection):
	total_files = 0
	total_scores = 0
	accepted_scores = 0

	for path in paths:
		total_files += 1
		print(f"round: {total_files}")

		try:
			parsed = corpus.parse(path)
		except Exception as error:
			print(
				f"Could not parse {path}: " 
				f"{error}"
				)

			continue

		scores = get_scores(parsed)

		total_scores += len(scores)

		for score in scores:
			structure = analyze_structure(score)

			if not structure["monophonic"]:
				continue

			if add_melody(connection, score):
				accepted_scores += 1

		connection.commit()

		if total_files % 25 == 0:
			print(
				f"Processed {total_files} files\n"
				f"Scores: {total_scores}\n"
				f"Accepted: {accepted_scores}\n"
				)

	return {
	"files": total_files,
	"scores": total_scores,
	"accepted": accepted_scores,
	}

def main():
	paths = corpus.getCorePaths()

	#paths = paths[:4]
	print(f"Found {len(paths)} corpus files.")
	connection = sqlite3.connect(db_path)

	try:
		create_database(connection)
		results = build_catalog(paths, connection)
	finally:
		connection.close()

	print(
		f"CATALOG COMPLETE\n"
		f"----------------\n"
		f"Files:    {results['files']}\n"
		f"Scores:   {results['scores']}\n"
		f"Accepted: {results['accepted']}\n")


if __name__ == "__main__":
	main()