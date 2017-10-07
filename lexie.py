import re
import requests as req
from bs4 import BeautifulSoup as BS
import operator
import math

MINIMUM_WORD_LENGTH = 3
MAXIMUM_WORD_LENGTH = 3
MINIMUM_WORD_FREQUENCY = 2  # Minimum crossword appearances to qualify for wordlist
MINIMUM_WORD_SCORE = 60

class Wordlist(object):
    def __init__(self, file): # takes file containing one entry per line and nothing else
        self.words = []
        self._temp_words = []
        try:
            with open(file, "r") as raw:
                print("Importing " + file + "...")
                raw_list = raw.read().split("\n")
                for new_word in raw_list:
                    if new_word:
                        new_word = new_word.strip().upper()
                        while len(new_word) >= len(self._temp_words):
                            self._temp_words.append([])
                            self.words.append({})
                        if MAXIMUM_WORD_LENGTH >= len(new_word) >= MINIMUM_WORD_LENGTH\
                                and new_word not in self._temp_words[len(new_word)]:
                            self._temp_words[len(new_word)].append(new_word)

                for i in range(3, len(self._temp_words)):
                    self.words[i] = self.score(self._temp_words[i])
                print("Wordlist imported.")

        except FileNotFoundError:
            print("Could not open '" + file + "'.")
            return

    def score(self, words):
        scored_wl = {}
        for word in words:
            # print(word)
            if word:
                xw_page = BS(req.get("http://crosswordtracker.com/search/?answer=" + word.lower()).content,
                             "html.parser")
                cu_page = BS(req.get("https://www.google.com/search?q=" + word.lower() + "&tbs=qdr:y").content,
                             "html.parser")

                # Crossword score is all-time appearances in major crosswords (from Crossword Tracker, max=20)
                try:
                    xw_score = int(re.search(r'\d+', str(xw_page.find_all(string=re.compile("we have spotted"))))[0])
                except TypeError:
                    xw_score = 0
                # Culture score is Google results dated within the past year, in millions
                cu_score = int(
                    re.search(r'\d+(,?\d*)*', str(cu_page.find(id="resultStats").string))[0].replace(",", "")) / 1000000
                if not xw_score or xw_score < MINIMUM_WORD_FREQUENCY:  # Disqualify non-crossword words
                    scored_wl[word] = 0
                else:
                    scored_wl[word] = round(cu_score * xw_score)
                print(word, scored_wl[word])
        return scored_wl

    def write(self, filepath, scored=False, sorted_by="keys"):
        try:
            doc = open(filepath, "w")
            for i in range(3, len(self.words)):
                doc.write(str(i) + "\n")  # Print a heading for each word length
                if sorted_by == "keys":
                    sorted_wl = sorted(self.words[i].items())
                else:
                    sorted_wl = sorted(self.words[i].items(), key=operator.itemgetter(1))
                for key, value in sorted_wl:
                    doc.write(key)
                    if scored:
                        doc.write("\t" + str(value))
                    doc.write("\n")
                doc.write("\n")
                print("Wrote " + str(i) + "-letter words to file")
            doc.close()
            print("Finished writing to file")
        except FileNotFoundError:
            print("Could not open '" + file + "'.")
            return

# def read(filename, delimiter="\t"):
#     raw = open(filename,"r").read().split('\n')
#     wl_arr = []
#     if delimiter:
#         for i in range(0, len(raw)):
#             wl_arr.append(raw[i].split(delimiter))
#     else:
#         wl_arr = raw
#     return wl_arr

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

# wl = score(read("wl-test2.txt", False))
# for key, value in sorted(wl.items(), key=operator.itemgetter(1)):
#     print(key + "\t" + str(value))

# print(score(["THE"]))

wl = Wordlist("wl-test.txt")
wl.write("wl-test-results12.txt", True, "scores")