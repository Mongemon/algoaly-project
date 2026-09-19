from music21 import corpus
from music21.stream import Opus, Score

from music_analysis import analyze_structure

#Return paths to corpus files
def get_corpus_files():
	return corpus.getCorePaths()

#returns all score objects in a parsed music21 object
def get_scores(parsed):
	 if isinstance(parsed, Score):
	 	return [parsed]

	 if isinstance(parsed, Opus):
	 	return [work for work in parsed if isinstance(work, Score)]

	 return []

#analyzes individual scores in given corpus paths
#returns a structural analysis
def analyze_corpus(paths):

	results = []
	r = 0

	for path in paths:
		r += 1
		print(f"round: {r}")

		try: 
			parsed = corpus.parse(path)
		except Exception as error:
			print(f"Could not parse {path}: {error}")
			continue


		scores = get_scores(parsed)

		for score in scores:
			structure = analyze_structure(score)
			results.append(structure)

	return results

#prints a summary of analyzed corpus
def print_corpus_summary(results):
	total = len(results)
	usable = sum(result["monophonic"] for result in results)
	rejected = total - usable

	chord_count = sum(result["contains_chords"] for result in results)
	multi_part_count = sum(result["active_parts"] > 1 for result in results)
	overlap_count = sum(result["overlapping_notes"] for result in results)

	print(
		f"CORPUS SUMMARY\n"
		f"--------------\n"
		f"Total scores:        {total}\n"
		f"Usable melodies:     {usable}\n"
		f"Rejected:            {rejected}\n"
		f"With chords:         {chord_count}\n"
		f"Multiple parts:      {multi_part_count}\n"
		f"Overlapping notes:   {overlap_count}\n"
		)

def main():

	paths = get_corpus_files()

	print(f"Found {len(paths)} corpus files")

	print(f"starting to analyze {paths}")
	results = analyze_corpus(paths)

	print("printing summary...")
	print_corpus_summary(results)


if __name__ == "__main__":
	main()