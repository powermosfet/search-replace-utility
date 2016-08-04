import sys, re, argparse

argParser = argparse.ArgumentParser(description = "Perform mass replacements in a text file")
argParser.add_argument("-p", "--pattern", help = "prompt if replacement for <pattern> is missing")
argParser.add_argument("replacementsfile", help = "filename for replacement dictionary")
argParser.add_argument("filename", help = "file to do replacements on")

args = argParser.parse_args()

filename = args.filename
replacementFilename = args.replacementsfile
pattern = args.pattern
replacements = {}
ignorewords = []
replaceCount = 0
newReplacements = 0

def sub(this, that, contents):
    global replaceCount
    subContents = contents
    for a, b in [(this, that), (this.upper(), that.upper())]:
        subContents, n = re.subn(r"\b{}\b".format(a), b, subContents)    
        replaceCount += n
    return subContents

with open(replacementFilename, 'r') as r:
    for line in r:
        words = line.split() 
        if len(words) == 2:
            replacements[words[0]] = words[1]
        else:
            raise Exception("Syntax error in replacement file")

print("Loaded {} replacements from {}".format(len(replacements), replacementFilename))
                
with open(filename) as infile, open("OUT_" + filename, 'w') as outfile:
    contents = infile.read()
    for key in replacements:
        contents = sub(key, replacements[key], contents)
        print("{:<10}".format(replaceCount), end="\r")
    if pattern:
        for match in [ m for m in sorted(set(map(lambda c: c.lower(), re.findall(pattern, contents)))) \
                                                    if m not in ignorewords]:
            rep = input("Enter a replacement for '{}' (blank to ignore): ".format(match)).lower()
            if not rep:
                ignorewords.append(match)
                continue
            replacements[match] = rep
            newReplacements += 1
            contents = sub(match, rep, contents)
    outfile.write(contents)
    print("Performed {} replacements in {}.".format(replaceCount, filename))

if newReplacements:
    print("Got {} new replacements. rewriting {}.".format(newReplacements, replacementFilename))
    with open(replacementFilename, 'w') as r:
        r.writelines(["{} {}\n".format(k, replacements[k]) for k in replacements])
