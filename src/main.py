import random

from pathlib import Path

from catalog import MelodyCatalog, remove_duplicate_melodies

from markov import MarkovChain

#getting the database location
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
db_path = project_root / "data" / "melody_catalog.db"

#asks the user for an integer and optionally enforces a min value
def ask_integer(prompt, minimum=None):
	while True:
		value = input(prompt).strip()

		try:
			number = int(value)
		except ValueError:
			print("Please enter an integer")
			continue

		if minimum is not None and number < minimum:
			print(f"Please anter a value of at least {minimum}.")
			continue

		return number

#Asks for optional text
def ask_optional_text(prompt):
	value = input(prompt).strip()

	if not value:
		return None

	return value

#Returns all distinct MIDI ptiches in the training data
def get_available_pitches(training_sequences):
	return sorted(
	{pitch for sequence in training_sequences for pitch in sequence})

#Prints all distinct MIDI pitches in the training data
def print_available_pitches(training_sequences):
	pitches = get_available_pitches(training_sequences)
	print(
		f"\nAVAILABLE MIDI PITCHES\n"
		f"----------------------\n")
	print(" ".join(str(pitch) for pitch in pitches))

#Converts a str MIDI sequence into a tuple
def parse_pitch_sequence(text):
	parts = text.replace(",", " ").split()
	if not parts:
		raise ValueError("No pitches were entered")

	try:
		pitches = tuple(int(value) for value in parts)
	except ValueError:
		raise ValueError("All pitches must be integers")

	invalid = [pitch for pitch in pitches if pitch < 0 or pitch > 127]

	if invalid:
		raise ValueError("MIDI pitches must be between 0 and 127")

	return pitches

#Asks the user for a MIDI pitch sequence
def ask_pitch_sequence(prompt, exact_length=None):
	while True:
		text = input(prompt).strip()

		try:
			pitches = parse_pitch_sequence(text)
		except ValueError as error:
			print(f"Error: {error}")
			continue

		if exact_length is not None:
			if len(pitches) != exact_length:
				print(f"Enter exactly {exact_length} pitches.")
				continue

		return pitches

#Ask the user for training data
def ask_custom_training_data():
	print(
		f"\n"
		f"CUSTOM TRAINING DATA\n"
		f"--------------------\n"
		f"Enter the training melody as MIDI pitches separated by spaces\n"
		)

	sequence = ask_pitch_sequence("Training melody: ")

	return [sequence]

def choose_training_data(catalog):
	print(
		f"\n"
		f"TRAINING DATA\n"
		f"-------------\n")

	while True:
		print(
			f"Type 'c' for corpus/database melodies.\n"
			f"Type 'u' to give own training melody.\n"
			)
		choice = input("Training data: ").strip().lower()
		if choice == "u":
			return ask_custom_training_data()
		if choice == "c":
			melodies = search_melodies(catalog)

			if not melodies:
				print("No melodies found.")
				continue

			print_search_results(melodies)
			selected = choose_training_melodies(melodies)
			print_training_set(selected)
			return [melody.pitches for melody in selected]

#Ask the user for a starting context
def ask_custom_start(chain, training_sequences):
	print(
		f"\n"
		f"CUSTOM STARTING SEQUENCE\n"
		f"------------------------\n"
		)

	print_available_pitches(training_sequences)

	print()

	while True:
		start = ask_pitch_sequence(
			f"Enter exactly {chain.order} pitches: ", exact_length=chain.order)

		available_pitches = set(get_available_pitches(training_sequences))

		for pitch in start:
			if pitch not in available_pitches:
				raise ValueError(
					f"{pitch} does not occur in the selected training data."
					)

		counts = chain.trie.next_counts(start)

		if not counts:
			print(
				f"This starting sequence has no known continuation, "
				f"give another sequence"
				)
			continue

		return start

#Asks for the preferred starting context
def choose_start_mode():
	print(
		f"\n"
		f"STARTING SEQUENCE\n"
		f"-----------------\n"
		f"Type 'r' for a random position in training data\n"
		f"Type 'u' for your own starting sequence\n"
		)

	while True:
		choice = input("Starting sequence: ").strip().lower()
		if choice in ("r", "u"):
			return choice
		print("Choose 'r' or 'u'.")

#Asks user for title/key parameters and returns matching melodies
def search_melodies(catalog):
	print(
		f"\n"
		f"MELODY SEARCH\n"
		f"-------------\n"
		f"Leave a field empty to ignore it.\n"
		f"Give key as 'A major', 'a minor', 'c# minor' ect.\n"
		)
	title = ask_optional_text("Title: ")
	key = ask_optional_text("Key: ")

	melodies = catalog.search(
		title = title,
		key = key,
		limit = 500,
		)

	return melodies

#Prints the search results
def print_search_results(melodies):
	print(f"\nFound {len(melodies)} melodies.\n")

	if not melodies:
		return

	for i, melody in enumerate(melodies, start = 1):
		print(
			f"{i:3} | "
			f"{melody.title} | "
			f"{melody.key} | "
			f"{melody.note_count} notes | "
			f"pitch range: "
			f"{melody.lowest_pitch}-"
			f"{melody.highest_pitch}"
			)

#Asks the user which training results will be used as training data. 
def choose_training_melodies(melodies):
	if not melodies:
		raise ValueError("There are no melodies")

	print(
		f"\n"
		f"How should the training melodies be selected?\n"
		f"Type 'a' for    - use all search results\n"
		f"Type 'r' for    - randomly choose N results\n"
		f"Type 'n' for    - enter result numbers, e.g. 1, 4, 7\n"
		)

	while True:
		choice = input("Selection: ").strip()
		if choice.lower() == "a":
			selected = list(melodies)
			break

		elif choice.lower() == "r":
			amount = ask_integer("How many random results: ", minimum=1)
			try:
				amount = int(amount)
			except ValueError:
				print("The number must be an integer")
				continue

			if amount > len(melodies):
				print(f"Only {len(melodies)} melodies are available.")
				continue

			selected = random.sample(melodies, amount)
			break

		elif choice.lower() == "n":
			numbers = input("enter result numbers, e.g. 1, 4, 7: ")
			try:
				indices = [int(value.strip()) for value in numbers.split(",")]
			except ValueError:
				print("Enter numbers such as 1, 4, 7")
				continue
			if not indices:
				print("Select at least one melody")
				continue

			if any(index < 1 or index > len(melodies) for index in indices):
				print("One or more numbers are outside the result range.")
				continue

			selected = [melodies[index - 1] for index in indices]

			break

		else:
			print("Choose one of the following, 'a', 'r' or 'n'")
			continue

	selected = remove_duplicate_melodies(selected)

	return selected

#Prints th melodies that will be used for training
def print_training_set(melodies):
	print(
		f"\n"
		f"TRAINING SET ({len(melodies)} melodies)\n"
		f"-------------------------------------\n"
		)

	for melody in melodies:
		print(
			f"{melody.title} | "
			f"{melody.key} | "
			f"{melody.note_count} notes"
			)

#Ask the user for Markov order and output lenght
def ask_generation_settings():
	print(
		f"\n"
		f"GENERATION SETTINGS\n"
		f"-------------------\n"
		)

	order = ask_integer("Markov order: ", minimum=1)
	note_count = ask_integer("Number of generated notes: ", minimum=1)

	if note_count < order:
		raise ValueError("Generated note count must be at least the Markov order")

	return order, note_count

#Trains a Markov chain using the selected melodies
def create_chain(training_sequences, order):
	usable_sequences = [
	sequence for sequence in training_sequences if len(sequence) > order
	]

	if not usable_sequences:
		raise ValueError("The training data is not long enough for this Markov order")

	chain = MarkovChain(order=order)
	chain.fit(usable_sequences)

	return chain

#Print generated pitches as MIDI numbers
def print_generated_melody(pitches):
	print(
		f"\n"
		f"GENERATED MELODY\n"
		f"----------------\n"
		)
	print(" ".join(str(pitch) for pitch in pitches))

#Generates melodies repeatedly until the user quits
def generate_repeatedly(chain, note_count, start_mode, custom_start = None):
	rng = random.Random()

	while True:
		if start_mode == "r":
			start = None
		else:
			start = custom_start

		generated = chain.generate(note_count=note_count, start=start, rng=rng)
		print_generated_melody(generated)
		print()

		if len(generated) < note_count:
			print(
				f"Warning: generated only {len(generated)} out of "
				f"{note_count} requested notes.\n"
				f"The current Markov context has no known continuation."
				)

		command = input(
			"\nPress Enter to generate again or type 'q' to quit:"
			).strip().lower()

		if command =="q":
			break

def main():
	catalog = MelodyCatalog(db_path)

	print(
		f"=================================\n"
		f"     MARKOV MELODY GENERATOR\n"
		f"=================================\n"
		)


	try:
		training_sequences = choose_training_data(catalog)
		order, note_count = (ask_generation_settings())
		chain = create_chain(training_sequences, order)
		start_mode = choose_start_mode()
		custom_start = None

		if start_mode == "u":
			custom_start = ask_custom_start(chain, training_sequences)

	except ValueError as error:
		print(f"\nError: {error}")
		return


	print(
		f"\n"
		f"Training Markov chain of order {order}...\n"
		f"Using {len(training_sequences)} melodies.")

	generate_repeatedly(chain, note_count, start_mode, custom_start)

if __name__ == "__main__":
	main()

