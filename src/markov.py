import random

from typing import Generic, Hashable, TypeVar

from trie import Trie

T = TypeVar("T", bound=Hashable)

#Creates an n-order markov chain
class MarkovChain(Generic[T]):
	def __init__(self, order: int):
		if order < 1:
			raise ValueError("order must be at least 1")

		self.order = order
		self.trie = Trie[T]()
		self.initial_contexts: list[tuple[T, ...]] = []

	#trains the chain on multpiple sequences
	def fit(self, sequences):
		self.trie = Trie[T]()
		self.initial_contexts = []

		for sequence in sequences:
			sequence = tuple(sequence)

			if len(sequence) < self.order:
				continue

			initial_context = sequence[:self.order]

			self.initial_contexts.append(initial_context)

			for i in range(len(sequence) - self.order):
				window = sequence[i:i + self.order + 1]
				self.trie.insert(window)

	#Randomly chooses the next state
	def choose_next(self, context: tuple[T, ...], rng: random.Random):
		counts = self.trie.next_counts(context)

		if not counts:
			return None

		states = list(counts.keys())
		weights = list(counts.values())

		return rng.choices(states, weights=weights, k=1)[0]

	#Generates a sequence of states
	def generate(self, note_count: int, start=None, rng=None):

		if note_count <= 0:
			raise ValueError("note_count must be greater than zero")

		if not self.initial_contexts:
			raise RuntimeError("the Markov chain has not been trained")

		if rng is None:
			rng = random.Random()

		if start is None:
			context = rng.choice(self.initial_contexts)
		else:
			context = tuple(start)

			if len(context) != self.order:
				raise ValueError(f"start must contain exactly {self.order} states")

		generated = list(context)
		while len(generated) < note_count:
			next_state = self.choose_next(tuple(generated[-self.order:]),rng)

			if next_state is None:
				break

			generated.append(next_state)

		return generated
