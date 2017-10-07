import re
import requests as req
from bs4 import BeautifulSoup as BS
import operator
import math

MINIMUM_WORD_LENGTH = 3
MAXIMUM_WORD_LENGTH = 3
MINIMUM_WORD_FREQUENCY = 2  # How often a word has to appear in the raw corpus to qualify for the wordlist

def read(filename, delimiter="\t"):
    raw = open(filename,"r").read().split('\n')
    wl_arr = []
    if delimiter:
        for i in range(0, len(raw)):
            wl_arr.append(raw[i].split(delimiter))
    else:
        wl_arr = raw
    return wl_arr

def write(wl_arr, filepath, scored=False, sorted_by="keys"):
    doc = open(filepath, "w")
    for i in range(3, len(wl_arr)):
        doc.write(str(i) + "\n") # Print a heading for each word length
        if sorted_by == "keys":
            sorted_wl = sorted(wl_arr[i].items())
        else:
            sorted_wl = sorted(wl_arr[i].items(), key=operator.itemgetter(1))
        for key, value in sorted_wl:
            doc.write(key)
            if scored:
                doc.write("\t" + str(value))
            doc.write("\n")
        doc.write("\n")
    doc.close()

def score(words):
    scored_wl = {}
    for word in words:
        # print(word)
        if word:
            xw_page = BS(req.get("http://crosswordtracker.com/search/?answer=" + word.lower()).content, "html.parser")
            cu_page = BS(req.get("https://www.google.com/search?q=" + word.lower() + "&tbs=qdr:y").content, "html.parser")

            # Crossword score is number of appearances in major crosswords (from Crossword Tracker, max=20)
            try:
                xw_score = int(re.search(r'\d+', str(xw_page.find_all(string=re.compile("we have spotted"))))[0])
            except TypeError:
                xw_score = 0
            # Culture score is number of Google results in the past year, in millions
            cu_score = int(re.search(r'\d+(,?\d*)*', str(cu_page.find(id="resultStats").string))[0].replace(",","")) / 1000000
            if not xw_score or xw_score < MINIMUM_WORD_FREQUENCY: # Disqualify non-crossword words
                scored_wl[word] = 0
            else:
                scored_wl[word] = round(cu_score * xw_score)
            print(word, scored_wl[word])
    return scored_wl

# Main
# ====
# print(read("../GN-300,000.tsv")[0:20])

# Take a wordlist, clean it, reorder and write to file, scored or unscored
# write(segregate(clean(count(read("../WL-SP.tsv"), 3), "-ilr")), "wl.txt")
# write(segregate(clean(count(read("../WL-SP.tsv"), 3), "-il")), "wl-test.txt", False, "values")

# for word in score(read("wl-test.txt", False)):
#     if word:
#         (crossword_score, culture_score) = score(word)
#         print(word + "\t" + str(crossword_score) + "\t" + str(culture_score))

wl = score(read("wl-test2.txt", False))
for key, value in sorted(wl.items(), key=operator.itemgetter(1)):
    print(key + "\t" + str(value))

# print(score(["THE"]))