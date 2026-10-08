import random
import unittest

from trie import Trie
from markov import MarkovChain

class Tests(unittest.TestCase):

	#The trie should caintain exatly the inserted sequences
	def test_experiment_1_sequences(self):
		trie = Trie()

		sequences = [
			(1, 2, 3), (2, 3, 4), (3, 4, 5),
			(4, 5, 6), (5, 6, 5), (6, 5, 7)]

		for sequence in sequences:
			trie.insert(sequence)

		stored = trie.get_sequences()

		self.assertCountEqual(stored, sequences)

		#testing the __str__ method
		string_sequences = str(trie).splitlines()

		expected_strings = [
			"1 2 3", "2 3 4", "3 4 5",
			"4 5 6", "5 6 5", "6 5 7"]

		self.assertCountEqual(string_sequences, expected_strings)

	#Trie should be able to preserve repeated insertions
	def test_experiment_1_duplicate_count(self):
		trie = Trie()

		for _ in range(2):
			trie.insert((1, 2, 3))
		trie.insert((1, 2, 4))

		expected = [(1, 2, 3), (1, 2, 3), (1, 2, 4)]

		self.assertCountEqual(trie.get_sequences(), expected)

		self.assertCountEqual(trie.next_counts((1, 2)), {3: 2, 4: 1})

	#All the following tests (2-5) test the Markov chain

	#Is it handled if 
	#A
	#Starting context includes a state that is not in training data
	def test_experiment_2_unknown_state(self):
		chain = MarkovChain(order = 2)
		chain.fit([[1, 2, 3, 2, 1]])
		with self.assertRaises(ValueError):
			chain.generate(note_count=10, start=(9, 2))
	#B
	#Individual states do occur in training data but the given starting
	#combination does not
	def test_experiment_2_unknown_combination(self):
		chain = MarkovChain(order = 2)
		chain.fit([[1, 2, 3, 2, 1]])
		with self.assertRaises(ValueError):
			chain.generate(note_count=10, start=(1, 3))

	#Testing if the generated sequence obeys the training data
	def test_experiment_3_valid_transitions(self):
		training = [1, 2, 3, 4, 5, 6, 5, 7]
		chain = MarkovChain(order = 1)
		chain.fit([training])

		generated = chain.generate(note_count=50, start=(1,), 
				rng=random.Random(42))

		self.assertEqual(generated[:5], [1, 2, 3, 4, 5])

		valid_transitions = {1: {2}, 2: {3}, 3: {4},
							4: {5}, 5:{6, 7}, 6: {5}}

		for current, next_state in zip(generated, generated[1:]):
			self.assertIn(next_state, valid_transitions[current])

	#Cheking that long-run probablities stay
	def test_experiment_4_long_run_distribution(self):
		chain = MarkovChain(order = 1)
		chain.fit([[2, 3, 4, 3, 4, 5, 2, 3]])

		generated = chain.generate(note_count=100000, start=(2,))

		total = len(generated)

		counts = {}
		for number in generated:
			try:
				counts[number] += 1
			except:
				counts[number] = 1

		frequencies = {state: counts[state] / total for state in counts}

		self.assertAlmostEqual(frequencies[2], 1/6, delta=0.02)
		self.assertAlmostEqual(frequencies[3], 1/3, delta=0.02)
		self.assertAlmostEqual(frequencies[4], 1/3, delta=0.02)
		self.assertAlmostEqual(frequencies[5], 1/6, delta=0.02)

		four_transitions = {3: 0, 5: 0}
		for current, next_state in zip(generated, generated[1:]):
			if current == 4:
				four_transitions[next_state] += 1

		total_four_transitions = sum(four_transitions.values())

		self.assertAlmostEqual(four_transitions[3] / 
			total_four_transitions, 0.5, delta=0.03)
		self.assertAlmostEqual(four_transitions[5] / 
			total_four_transitions, 0.5, delta=0.03)

	#The Trie and Markov chains should work with any hashable objects
	#The test is the same as test 4 but with hashables
	def test_experiment_5_generic_hashable_values(self):
			chain = MarkovChain(order = 1)
			chain.fit([["hello", range(4), b"0101", range(4), 
				b"0101", True, "hello", range(4)]])

			generated = chain.generate(note_count=100000, start=("hello",))

			total = len(generated)

			counts = {}
			for hashable in generated:
				try:
					counts[hashable] += 1
				except:
					counts[hashable] = 1

			frequencies = {state: counts[state] / total for state in counts}

			self.assertAlmostEqual(frequencies["hello"], 1/6, delta=0.02)
			self.assertAlmostEqual(frequencies[range(4)], 1/3, delta=0.02)
			self.assertAlmostEqual(frequencies[b"0101"], 1/3, delta=0.02)
			self.assertAlmostEqual(frequencies[True], 1/6, delta=0.02)

			four_transitions = {range(4): 0, True: 0}
			for current, next_state in zip(generated, generated[1:]):
				if current == b"0101":
					four_transitions[next_state] += 1

			total_four_transitions = sum(four_transitions.values())

			self.assertAlmostEqual(four_transitions[range(4)] / 
				total_four_transitions, 0.5, delta=0.03)
			self.assertAlmostEqual(four_transitions[True] / 
				total_four_transitions, 0.5, delta=0.03)

if __name__ == "__main__":
	unittest.main(verbosity=2)