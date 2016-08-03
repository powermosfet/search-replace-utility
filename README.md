# search-replace-utility
command line utility to do mass-replacements in textfiles

##Usage:

    $ python rename.py [-h] [-p PATTERN] replacementsfile filename

The script use a dictionary file containing key-value pairs separated by space.
The results will be written to a file named `OUT_<filename>`

##Example:
Replace using rename.txt as a dictionary. Prompt for words that starts with a z.

    $ python rename.py -p "\b[zZ]\w*\b" rename.txt something.nugg
