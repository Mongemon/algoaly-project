from typing import Generic, Hashable, TypeVar

T = TypeVar("T", bound=Hashable,)

class TrieNode(Generic[T]):
	def __init__(self):
		self.children: dict[T, TrieNode[T]] = {}

		#number of inserted sequences going through this node
		self.count = 0

class Trie(Generic[T]):
	def __init__(self):
		self.root = TrieNode()

	#inserts a sequence into the trie
	def insert(self, sequence, count = 1):
		if count <= 0:
			raise ValueError("count must be greater than zero")

		sequence = tuple(sequence)

		if not sequence:
			raise ValueError("cannot insert and empty sequence")

		current = self.root

		for state in sequence:
			if state not in current.children:
				current.children[state] = TrieNode()

			current = current.children[state]
			current.count += count

	#retuns the last node belonging to a prefix
	def find_node(self, prefix):
		current = self.root

		for state in prefix:
			if state not in current.children:
				return None

			current = current.children[state]

		return current

	#returns the frequencies of possible next states
	def next_counts(self, prefix):
		node = self.find_node(prefix)

		if node is None:
			return {}

		return {state: child.count for state, child in node.children.items()}





