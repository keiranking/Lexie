import re
import requests as req
from bs4 import BeautifulSoup as BS
import operator
import math

MINIMUM_WORD_LENGTH = 4
MAXIMUM_WORD_LENGTH = 4
MINIMUM_WORD_FREQUENCY = 2 # How often a word has to appear in the raw corpus to qualify for the wordlist

def read(filename, delimiter="\t"):
    raw = open(filename,"r").read().split('\n')
    wl_arr = []
    if delimiter:
        for i in range(0, len(raw)):
            wl_arr.append(raw[i].split(delimiter))
    else:
        wl_arr = raw
    return wl_arr

def count(wl_arr_of_arrs, column, has_header=True):
    column -= 1
    wl_dict = {}
    start = 1
    if not has_header:
        start = 0
    for i in range(start, len(wl_arr_of_arrs)):
        key = wl_arr_of_arrs[i][column].upper()
        wl_dict[key] = wl_dict.get(key, 0) + 1 # increment its frequency
    return wl_dict

def clean(wl, flags):
    for key, value in list(wl.items()):
        isInvalid = False
        if "r" in flags: # remove rare entries
            if value < MINIMUM_WORD_FREQUENCY:
                isInvalid = True
        if "l" in flags: # remove entries too short or long to be in a puzzle
            if len(key) < MINIMUM_WORD_LENGTH or len(key) > MAXIMUM_WORD_LENGTH:
                isInvalid = True
        if "i" in flags: # remove entries that aren't all letters
            if not key.isalpha():
                isInvalid = True
        if isInvalid:
            del wl[key]
    return wl

def segregate(wl_dict):
    wl_arr = []
    for key, value in list(wl_dict.items()):
        if len(key) >= len(wl_arr):
            while len(key) >= len(wl_arr):
                wl_arr.append({})
        wl_arr[len(key)][key] = value
    # for i in range(len(wl_arr)):
    #     wl_arr[i].sort()
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
