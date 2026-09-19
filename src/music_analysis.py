from music21.chord import Chord
from music21.note import Note
from music21.stream import Score, Voice

#returns true if note objects overlap
#elements are assumed to belong to the same container
def notes_overlap(notes):
	notes = list(notes)

	notes.sort(key=lambda note: note.offset)

	for previous, current in zip(notes, notes[1:]):
		previous_end = (previous.offset + previous.duration.quarterLength)

		if current.offset < previous_end:
			return True

	return False

#analyzes properties relevant to monophony
def analyze_structure(score):
	contains_chords = False
	active_part_count = 0
	overlapping_notes = False
	voices = []

	for element in score.recurse():
		if isinstance(element, Chord):
			contains_chords = True 
		elif isinstance(element, Voice):
			voices.append(element)

	voice_count = len(voices)

	for part in score.parts:
		has_musical_content = False
		measures = part.getElementsByClass("Measure")

		for measure in measures:
			notes = [element for element in measure.notes if isinstance(element, Note)]

			if notes:
				has_musical_content = True

				if notes_overlap(notes):
					overlapping_notes = True

		for voice in part.recurse().getElementsByClass("Voice"):
			notes = [element for element in voice.notes if isinstance(element, Note)]

			if notes:
				has_musical_content = True 

		if has_musical_content:
			active_part_count += 1

	monophonic = (
		not contains_chords 
		and active_part_count <= 1 
		and voice_count <= 1 
		and not overlapping_notes)

	return {
		"contains_chords": contains_chords,
		"voices": voice_count,
		"active_parts": active_part_count,
		"overlapping_notes": overlapping_notes,
		"monophonic": monophonic,
		}

#returns the MIDI pitches of the score given
def get_pitches(score):

	pitches = []

	for element in score.recurse().notes:
		if isinstance(element, Note):
			pitches.append(element.pitch.midi)

	return pitches

#returns the pitch range of the pitches given
def get_pitch_range(pitches):

	if not pitches:
		return None, None

	return min(pitches), max(pitches)

#asks music21 for the key of the score
def get_key(score):
	try:
		return score.analyze("key")
	except Exception:
		return None
