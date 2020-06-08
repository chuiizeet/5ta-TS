import contextlib, sys
import huffmancoding


# Command line main application function.
def main(args):
	# Handle command line arguments
	if len(args) != 2:
		sys.exit("Usage: python adaptive-huffman-compress.py InputFile OutputFile")
	inputfile, outputfile = args
	
	# Perform file compression
	with open(inputfile, "rb") as inp, \
			contextlib.closing(huffmancoding.BitOutputStream(open(outputfile, "wb"))) as bitout:
		compress(inp, bitout)


def compress(inp, bitout):
	initfreqs = [1] * 257
	freqs = huffmancoding.FrequencyTable(initfreqs)
	enc = huffmancoding.HuffmanEncoder(bitout)
	enc.codetree = freqs.build_code_tree()  # Don't need to make canonical code because we don't transmit the code tree
	count = 0  # Number of bytes read from the input file
	while True:
		# Read and encode one byte
		symbol = inp.read(1)
		if len(symbol) == 0:
			break
		enc.write(symbol[0])
		count += 1
		
		# Update the frequency table and possibly the code tree
		freqs.increment(symbol[0])
		if (count < 262144 and is_power_of_2(count)) or count % 262144 == 0:  # Update code tree
			enc.codetree = freqs.build_code_tree()
		if count % 262144 == 0:  # Reset frequency table
			freqs = huffmancoding.FrequencyTable(initfreqs)
	enc.write(256)  # EOF


def is_power_of_2(x):
	return x > 0 and x & (x - 1) == 0


# Main launcher
if __name__ == "__main__":
	main(sys.argv[1 : ])