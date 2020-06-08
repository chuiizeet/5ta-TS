import heapq


# ---- Huffman coding core classes ----

# Encodes symbols and writes to a Huffman-coded bit stream.
class HuffmanEncoder:
	
	def __init__(self, bitout):
		self.output = bitout
		self.codetree = None
	
	
	def write(self, symbol):
		if not isinstance(self.codetree, CodeTree):
			raise ValueError("Invalid current code tree")
		bits = self.codetree.get_code(symbol)
		for b in bits:
			self.output.write(b)

class HuffmanDecoder:
	
	def __init__(self, bitin):
		self.input = bitin
		self.codetree = None
	
	def read(self):
		if not isinstance(self.codetree, CodeTree):
			raise ValueError("Invalid current code tree")
		currentnode = self.codetree.root
		while True:
			temp = self.input.read_no_eof()
			if   temp == 0: nextnode = currentnode.leftchild
			elif temp == 1: nextnode = currentnode.rightchild
			else: raise AssertionError("Invalid value from read_no_eof()")
			
			if isinstance(nextnode, Leaf):
				return nextnode.symbol
			elif isinstance(nextnode, InternalNode):
				currentnode = nextnode
			else:
				raise AssertionError("Illegal node type")

class FrequencyTable:
	
	def __init__(self, freqs):
		self.frequencies = list(freqs)  # Make a copy
		if len(self.frequencies) < 2:
			raise ValueError("At least 2 symbols needed")
		if any(x < 0 for x in self.frequencies):
			raise ValueError("Negative frequency")
	
	def get_symbol_limit(self):
		return len(self.frequencies)
	
	def get(self, symbol):
		self._check_symbol(symbol)
		return self.frequencies[symbol]
	
	def set(self, symbol, freq):
		self._check_symbol(symbol)
		if freq < 0:
			raise ValueError("Negative frequency")
		self.frequencies[symbol] = freq
	
	def increment(self, symbol):
		self._check_symbol(symbol)
		self.frequencies[symbol] += 1
	
	def _check_symbol(self, symbol):
		if 0 <= symbol < len(self.frequencies):
			return
		else:
			raise ValueError("Symbol out of range")

	def __str__(self):
		result = ""
		for (i, freq) in enumerate(self.frequencies):
			result += "{}\t{}\n".format(i, freq)
		return result
	
	def build_code_tree(self):
		# Note that if two nodes have the same frequency, then the tie is broken
		# by which tree contains the lowest symbol. Thus the algorithm has a
		# deterministic output and does not rely on the queue to break ties.
		# Each item in the priority queue is a tuple of type (int frequency,
		# int lowestSymbol, Node node). As per Python rules, tuples are ordered asceding
		# by the lowest differing index, e.g. (0, 0) < (0, 1) < (0, 2) < (1, 0) < (1, 1).
		pqueue = []
		
		for (i, freq) in enumerate(self.frequencies):
			if freq > 0:
				heapq.heappush(pqueue, (freq, i, Leaf(i)))
		
		for (i, freq) in enumerate(self.frequencies):
			if len(pqueue) >= 2:
				break
			if freq == 0:
				heapq.heappush(pqueue, (freq, i, Leaf(i)))
		assert len(pqueue) >= 2
		
		while len(pqueue) > 1:
			x = heapq.heappop(pqueue)
			y = heapq.heappop(pqueue)
			z = (x[0] + y[0], min(x[1], y[1]), InternalNode(x[2], y[2]))
			heapq.heappush(pqueue, z)
		
		return CodeTree(pqueue[0][2], len(self.frequencies))

# A binary tree that represents a mapping between symbols
# and binary strings. There are two main uses of a code tree:
# - Read the root field and walk through the tree to extract the desired information.
# - Call getCode() to get the binary code for a particular encodable symbol.
# The path to a leaf node determines the leaf's symbol's code. Starting from the root, going
# to the left child represents a 0, and going to the right child represents a 1. Constraints:
# - The root must be an internal node, and the tree is finite.
# - No symbol value is found in more than one leaf.
# - Not every possible symbol value needs to be in the tree.
# Illustrated example:
#   Huffman codes:
#     0: Symbol A
#     10: Symbol B
#     110: Symbol C
#     111: Symbol D
#   Code tree:
#       .
#      / \
#     A   .
#        / \
#       B   .
#          / \
#         C   D
class CodeTree:
	
	def __init__(self, root, symbollimit):
		def build_code_list(node, prefix):
			if isinstance(node, InternalNode):
				build_code_list(node.leftchild , prefix + (0,))
				build_code_list(node.rightchild, prefix + (1,))
			elif isinstance(node, Leaf):
				if node.symbol >= symbollimit:
					raise ValueError("Symbol exceeds symbol limit")
				if self.codes[node.symbol] is not None:
					raise ValueError("Symbol has more than one code")
				self.codes[node.symbol] = prefix
			else:
				raise AssertionError("Illegal node type")
		
		if symbollimit < 2:
			raise ValueError("At least 2 symbols needed")
		self.root = root

		self.codes = [None] * symbollimit
		build_code_list(root, ())  # Fill 'codes' with appropriate data
	
	
	def get_code(self, symbol):
		if symbol < 0:
			raise ValueError("Illegal symbol")
		elif self.codes[symbol] is None:
			raise ValueError("No code for given symbol")
		else:
			return self.codes[symbol]
	
	def __str__(self):
		def to_str(prefix, node):
			if isinstance(node, InternalNode):
				return to_str(prefix + "0", node.leftchild) + to_str(prefix + "0", node.rightchild)
			elif isinstance(node, Leaf):
				return "Code {}: Symbol {}\n".format(prefix, node.symbol)
			else:
				raise AssertionError("Illegal node type")
		
		return to_str("", self.root)

class Node:
	pass

class InternalNode(Node):
	def __init__(self, left, right):
		if not isinstance(left, Node) or not isinstance(right, Node):
			raise TypeError()
		self.leftchild = left
		self.rightchild = right

class Leaf(Node):
	def __init__(self, sym):
		if sym < 0:
			raise ValueError("Symbol value must be non-negative")
		self.symbol = sym



# A canonical Huffman code, which only describes the code length
# of each symbol. Code length 0 means no code for the symbol.
# The binary codes for each symbol can be reconstructed from the length information.
# In this implementation, lexicographically lower binary codes are assigned to symbols
# with lower code lengths, breaking ties by lower symbol values. For example:
#   Code lengths (canonical code):
#     Symbol A: 1
#     Symbol B: 3
#     Symbol C: 0 (no code)
#     Symbol D: 2
#     Symbol E: 3
#   Sorted lengths and symbols:
#     Symbol A: 1
#     Symbol D: 2
#     Symbol B: 3
#     Symbol E: 3
#     Symbol C: 0 (no code)
#   Generated Huffman codes:
#     Symbol A: 0
#     Symbol D: 10
#     Symbol B: 110
#     Symbol E: 111
#     Symbol C: None
#   Huffman codes sorted by symbol:
#     Symbol A: 0
#     Symbol B: 110
#     Symbol C: None
#     Symbol D: 10
#     Symbol E: 111
class CanonicalCode:
	
	# Constructs a canonical code in one of two ways:
	# - CanonicalCode(codelengths):
	#   Builds a canonical Huffman code from the given array of symbol code lengths.
	#   Each code length must be non-negative. Code length 0 means no code for the symbol.
	#   The collection of code lengths must represent a proper full Huffman code tree.
	#   Examples of code lengths that result in under-full Huffman code trees:
	#   * [1]
	#   * [3, 0, 3]
	#   * [1, 2, 3]
	#   Examples of code lengths that result in correct full Huffman code trees:
	#   * [1, 1]
	#   * [2, 2, 1, 0, 0, 0]
	#   * [3, 3, 3, 3, 3, 3, 3, 3]
	#   Examples of code lengths that result in over-full Huffman code trees:
	#   * [1, 1, 1]
	#   * [1, 1, 2, 2, 3, 3, 3, 3]
	# - CanonicalCode(tree, symbollimit):
	#   Builds a canonical code from the given code tree.
	def __init__(self, codelengths=None, tree=None, symbollimit=None):
		if codelengths is not None and tree is None and symbollimit is None:
			# Check basic validity
			if len(codelengths) < 2:
				raise ValueError("At least 2 symbols needed")
			if any(cl < 0 for cl in codelengths):
				raise ValueError("Illegal code length")
			
			codelens = sorted(codelengths, reverse=True)
			currentlevel = codelens[0]
			numnodesatlevel = 0
			for cl in codelens:
				if cl == 0:
					break
				while cl < currentlevel:
					if numnodesatlevel % 2 != 0:
						raise ValueError("Under-full Huffman code tree")
					numnodesatlevel //= 2
					currentlevel -= 1
				numnodesatlevel += 1
			while currentlevel > 0:
				if numnodesatlevel % 2 != 0:
					raise ValueError("Under-full Huffman code tree")
				numnodesatlevel //= 2
				currentlevel -= 1
			if numnodesatlevel < 1:
				raise ValueError("Under-full Huffman code tree")
			if numnodesatlevel > 1:
				raise ValueError("Over-full Huffman code tree")
			
			self.codelengths = list(codelengths)
		
		elif tree is not None and symbollimit is not None and codelengths is None:
			def build_code_lengths(node, depth):
				if isinstance(node, InternalNode):
					build_code_lengths(node.leftchild , depth + 1)
					build_code_lengths(node.rightchild, depth + 1)
				elif isinstance(node, Leaf):
					if node.symbol >= len(self.codelengths):
						raise ValueError("Symbol exceeds symbol limit")
					if self.codelengths[node.symbol] != 0:
						raise AssertionError("Symbol has more than one code")
					self.codelengths[node.symbol] = depth
				else:
					raise AssertionError("Illegal node type")
			
			if symbollimit < 2:
				raise ValueError("At least 2 symbols needed")
			self.codelengths = [0] * symbollimit
			build_code_lengths(tree.root, 0)
		
		else:
			raise ValueError("Invalid arguments")
	
	def get_symbol_limit(self):
		return len(self.codelengths)

	def get_code_length(self, symbol):
		if 0 <= symbol < len(self.codelengths):
			return self.codelengths[symbol]
		else:
			raise ValueError("Symbol out of range")
	
	def to_code_tree(self):
		nodes = []
		for i in range(max(self.codelengths), -1, -1):  
			assert len(nodes) % 2 == 0
			newnodes = []
			
			if i > 0:
				for (j, codelen) in enumerate(self.codelengths):
					if codelen == i:
						newnodes.append(Leaf(j))
			
			for j in range(0, len(nodes), 2):
				newnodes.append(InternalNode(nodes[j], nodes[j + 1]))
			nodes = newnodes
		
		assert len(nodes) == 1
		return CodeTree(nodes[0], len(self.codelengths))


class BitInputStream:
	
	def __init__(self, inp):
		self.input = inp
		self.currentbyte = 0
		self.numbitsremaining = 0

	def read(self):
		if self.currentbyte == -1:
			return -1
		if self.numbitsremaining == 0:
			temp = self.input.read(1)
			if len(temp) == 0:
				self.currentbyte = -1
				return -1
			self.currentbyte = temp[0]
			self.numbitsremaining = 8
		assert self.numbitsremaining > 0
		self.numbitsremaining -= 1
		return (self.currentbyte >> self.numbitsremaining) & 1
	
	def read_no_eof(self):
		result = self.read()
		if result != -1:
			return result
		else:
			raise EOFError()
	
	
	def close(self):
		self.input.close()
		self.currentbyte = -1
		self.numbitsremaining = 0


class BitOutputStream:
	
	def __init__(self, out):
		self.output = out  
		self.currentbyte = 0 
		self.numbitsfilled = 0  
	
	
	def write(self, b):
		if b not in (0, 1):
			raise ValueError("Argument must be 0 or 1")
		self.currentbyte = (self.currentbyte << 1) | b
		self.numbitsfilled += 1
		if self.numbitsfilled == 8:
			towrite = bytes((self.currentbyte,))
			self.output.write(towrite)
			self.currentbyte = 0
			self.numbitsfilled = 0
	
	def close(self):
		while self.numbitsfilled != 0:
			self.write(0)
		self.output.close()