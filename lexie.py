# Lexie scores wordlists for crosswords.
# She takes any text file with one word or phrase per line.
# She rejects entries new to crosswords (conservative).
# She boosts what is current, and demotes what is obsolete (myopic).
# =============================================================================
import re
import requests as req
from bs4 import BeautifulSoup as BS
import operator

MINIMUM_WORD_LENGTH = 3
MAXIMUM_WORD_LENGTH = 15
MINIMUM_XW_APPEARANCES = 1  # Minimum crossword appearances to qualify for wordlist
MINIMUM_WORD_SCORE = 60

class Wordlist(object):
    def __init__(self, file=False): # takes file containing one entry per line and nothing else
        self.words = []
        if not file:
            return

        try:
            with open(file, "r") as raw:
                print("Importing " + file + "...")
                self.add(raw.read().split("\n"))
        except FileNotFoundError:
            print("Could not open '" + file + "'.")
            return

    def __iter__(self):
        return self.words

    def __getitem__(self, i):
        return self.words[i]

    def add(self, list):
        new_words = []
        count = 0
        for new_word in list:
            if new_word:
                new_word = new_word.strip().upper()
                l = len(new_word.replace(" ", ""))
                while l >= len(new_words):
                    new_words.append([])
                while l >= len(self.words):
                    self.words.append({})
                if MAXIMUM_WORD_LENGTH >= l >= MINIMUM_WORD_LENGTH \
                        and new_word not in new_words[l]:
                    new_words[l].append(new_word)
                    count += 1

        for i in range(3, len(new_words)):
            print("Adding " + str(i) + "-letter words...")
            merged_words = {**self.words[i], **self.score(new_words[i])}
            self.words.pop(i)
            self.words.insert(i, merged_words)
        print(str(count) + " words added.")

    def score(self, list):
        scored_wl = {}
        if not list:
            return scored_wl
        for word in list:
            # print(word)
            if word:
                # Crossword score is all-time appearances in major crosswords
                candidate = word.upper().replace(" ", "")
                xw_query = word.lower().replace(" ", "")
                xw_scrape = BS(req.get("http://crosswordtracker.com/search/?answer=" + xw_query).content,
                             "html.parser")
                try:
                    xw_score = int(re.search(r'\d+', str(xw_scrape.find_all(string=re.compile("we have spotted"))))[0])
                except TypeError:
                    xw_score = 0
                if xw_score < MINIMUM_XW_APPEARANCES:  # Disqualify non-crossword words
                    scored_wl[candidate] = 0
                else:
                    # Culture score is Google search results from the past year, in millions
                    cu_query = word.lower().replace(" ", "+")
                    cu_scrape = BS(req.get("https://www.google.com/search?q=" + cu_query + "&tbs=qdr:y").content,
                                 "html.parser")
                    cu_score = int(
                        re.search(r'\d+(,?\d*)*', str(cu_scrape.find(id="resultStats").string))[0].replace(",", "")) / 1000000

                    scored_wl[candidate] = round(cu_score * xw_score)
                print(candidate, xw_score, cu_score, scored_wl[candidate])
        return scored_wl

    def write(self, filepath, scored=False, sorted_by="keys"):
        try:
            doc = open(filepath, "w")
            for i in range(3, len(self.words)):
                doc.write(str(i) + "\n")  # Print a heading for each word length
                if sorted_by == "keys":
                    sorted_wl = sorted(self.words[i].items())
                else:
                    sorted_wl = sorted(self.words[i].items(), key=operator.itemgetter(1), reverse=True)
                for key, value in sorted_wl:
                    doc.write(key)
                    if scored:
                        doc.write("\t" + str(value))
                    doc.write("\n")
                doc.write("\n")
                print("Wrote " + str(i) + "-letter words to " + str(filepath))
            doc.close()
            print("Finished writing to " + str(filepath))
        except FileNotFoundError:
            print("Could not open '" + file + "'.")
            return

# Main
# ====
wl = Wordlist("wl-scratch.txt")
# wl.write("wl-test-results4.txt", True, "scores")

# wl = Wordlist()
# wl.add(["doi", "sonofa", "grr", "yadig", "taylorswift", "sanfran", "ohwow", "tryon"])
# wl.add(["keepsake"])
# print(wl, wl[4])
# wl.write("wl-test3-results1.txt", True, "scores")
