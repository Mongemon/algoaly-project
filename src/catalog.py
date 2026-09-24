import json
import sqlite3

from dataclasses import dataclass
from pathlib import Path

#getting the database location
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
db_path = project_root / "data" / "melody_catalog.db"

#A melody stored in the database
@dataclass(frozen = True)
class Melody:
	id: int
	title: str
	key: str | None
	note_count: int
	lowest_pitch: int
	highest_pitch: int
	pitches: tuple[int, ...]



class MelodyCatalog:
	def __init__(self, database_path):
		self.database_path = database_path

	#Opens a connection to the database
	def connect(self):
		connection = sqlite3.connect(self.database_path)

		connection.row_factory = sqlite3.Row

		return connection

	#converts one database row into a melody object
	def row_to_melody(self,row):
		pitches = tuple(json.loads(row["pitches"]))

		return Melody(
			id=row["id"],
			title=row["title"],
			key=row["key"],
			note_count=row["note_count"],
			lowest_pitch=row["lowest_pitch"],
			highest_pitch=row["highest_pitch"],
			pitches=pitches,
			)

	#returns all distinct keys found in the database
	def get_keys(self):
		connection = self.connect()

		try:
			rows = connection.execute(
				"""
				SELECT DISTINCT key
				FROM melodies
				WHERE key IS NOT NULL
				ORDER BY key
				"""
			).fetchall
		finally:
			connection.close()

		return [row["key"] for row in rows]


	#search melodies by title and/or key
	def search(self, title=None, key=None, limit=None):

		query = """
			SELECT
				id,
				title,
				key,
				note_count,
				lowest_pitch,
				highest_pitch,
				pitches
			FROM melodies
			"""

		conditions = []
		parameters = []

		if title is not None:
			conditions.append("title LIKE ?")
			parameters.append(f"%{title}%")

		if key is not None:
			conditions.append("key = ?")
			parameters.append(key)

		if conditions:
			query += " WHERE "
			query += " AND ".join(conditions)

		query += "ORDER BY title"

		if limit is not None:
			if limit <= 0:
				raise ValueError("limit must be grater than zero")

			query += " LIMIT ?"
			parameters.append(limit)

		connection = self.connect()

		try:
			rows = connection.execute(query, parameters).fetchall()
		finally:
			return [self.row_to_melody(row) for row in rows]

	#Returns one melody based on id
	def get_by_id(self, melody_id):
		connection = self.connect()

		try:
			row = connection.execute(
				"""
				SELECT
					id,
					title,
					key,
					note_count,
					lowest_pitch,
					highest_pitch,
					pitches
				FROM melodies
				WHERE id = ?
				""", (melody_id,),
				).fetchone()

		finally:
			connection.close()

		if row is None:
			return None

		return self.row_to_melody(row)

#removes duplicate melodies from given melodies
def remove_duplicate_melodies(melodies):
	unique = []
	seen_pitches = set()

	for melody in melodies:
		if melody.pitches in seen_pitches:
			continue
		seen_pitches.add(melody.pitches)
		unique.append(melody)

	return unique
