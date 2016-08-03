import sys, re, argparse

argParser = argparse.ArgumentParser(description = "Perform mass replacements in a text file")
argParser.add_argument("-p", "--pattern", help = "prompt if replacement for <pattern> is missing")
argParser.add_argument("replacementsfile", help = "filename for replacement dictionary")
argParser.add_argument("filename", help = "file to do replacements on")

args = argParser.parse_args()

replacements = {}
newReplacements = {}
filename = args.filename
replacementFilename = args.replacementsfile
pattern = args.pattern
ignorewords = []

with open(replacementFilename, 'r') as r:
    for line in r:
        words = line.split() 
        if len(words) == 2:
            replacements[words[0]] = words[1]
            replacements[words[0].upper()] = words[1].upper()
        else:
            raise Exception("Syntax error in replacement file")

print("Loaded {} replacements from {}".format(len(replacements) // 2, replacementFilename))
                
with open(filename) as infile, open("OUT_" + filename, 'w') as outfile:
    replaceCount = 0
    for line in infile:
        for key in replacements:
            line, n = re.subn(r"\b{}\b".format(key), replacements[key], line)    
            replaceCount += n
        if pattern:
            for match in sorted(set(re.findall(pattern, line))):
                match = match.lower()
                if match in ignorewords:
                    continue
                rep = input("Enter a replacement for '{}': ".format(match)).lower()
                if not rep:
                    ignorewords.append(match)
                    continue
                newReplacements[match] = rep
                newReplacements[match.upper()] = rep.upper()
                replacements[match]    = rep
                replacements[match.upper()]    = rep.upper()
            for key in newReplacements:
                line, n = re.subn(r"\b{}\b".format(key), newReplacements[key], line)    
                replaceCount += n
        outfile.write(line)
    print("Performed {} replacements in {}.".format(replaceCount, filename))

if len(newReplacements):
    print("Got {} new replacements. rewriting {}.".format(len(newReplacements) // 2, replacementFilename))
    with open(replacementFilename, 'w') as r:
        r.writelines(["{} {}\n".format(k, replacements[k]) for k in replacements if k.islower()])
