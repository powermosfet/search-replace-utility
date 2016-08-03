import sys, re

replacements = {}
filename = sys.argv[1]

with open('rename.txt', 'r') as r:
	for line in r:
		words = line.split() 
		if len(words) == 2:
			replacements[words[0]] = words[1]
			replacements[words[0].upper()] = words[1].upper()

print("Loaded {} replacements from rename.txt".format(len(replacements)))
				
with open(filename) as infile, open("OUT_" + filename, 'w') as outfile:
	replaceCount = 0
	for line in infile:
		for key in replacements:
			line, n = re.subn(r"\b{}\b".format(key), replacements[key], line)	
			replaceCount += n
		outfile.write(line)
	print("Performed {} replacements in {}.".format(replaceCount, filename))
