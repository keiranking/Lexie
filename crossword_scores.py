import re
import requests as req
from bs4 import BeautifulSoup as BS
import operator
import math
import os
import json

MINIMUM_WORD_LENGTH = 3
MAXIMUM_WORD_LENGTH = 15
MINIMUM_WORD_FREQUENCY = 2 # How often a word has to appear in the raw corpus to qualify for the wordlist

def collect_CT_frequency(rootpath):
    xw_scores = [ {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {} ]
    for dirpath, dirnames, filenames in os.walk(rootpath):
        for dirname in dirnames:
            file = os.path.join(dirpath, dirname, "index.html")
            with open(file, "r") as raw:
                xw_scrape = BS(raw.read(), "html.parser")
                xw_score = int(re.search(r'\d+', str(xw_scrape.find_all(string=re.compile("we have spotted"))))[0])
                # print(dirname + "\t" + str(xw_score))

                if xw_score >= MINIMUM_WORD_FREQUENCY and MAXIMUM_WORD_LENGTH >= len(dirname) >= MINIMUM_WORD_LENGTH and dirname.isalpha():
                    xw_scores[len(dirname)][dirname.upper()] = xw_score
                    print(dirname.upper(), xw_score)
    # print(xw_scores)
    try:
        doc = open("test3-r2.txt", "w")
        doc.write(json.dumps(xw_scores, indent=4))
    except:
        print("Error opening file to write")

def read(filename, delimiter="\t"):
    print("Opening", filename)
    raw = open(filename,"r").read().split('\n')
    wl_arr = []
    if delimiter:
        for i in range(0, len(raw)):
            wl_arr.append(raw[i].split(delimiter))
    else:
        wl_arr = raw
    print("Read", str(len(wl_arr)), "lines")
    return wl_arr

def remove_before_year(wl_arr_of_arrs, year, has_header=True):
    print("Removing entries before", str(year), "...")
    count = 0
    for entry in wl_arr_of_arrs:
        if not entry[1].isalpha():
            if int(entry[1]) < year:
                wl_arr_of_arrs.remove(entry)
                count += 1
                print(str(count), "entries before", str(year), "removed")
    print("Entries removed.")
    return wl_arr_of_arrs

def count(wl_arr_of_arrs, column, has_header=True):
    print("Counting entries...")
    column -= 1
    wl_dict = {}
    start = 1
    if not has_header:
        start = 0
    for i in range(start, len(wl_arr_of_arrs)):
        # key = wl_arr_of_arrs[i][column].upper()
        # wl_dict[key] = wl_dict.get(key, 0) + 1 # increment its frequency
        key = wl_arr_of_arrs[i][column].replace(" ","").upper() # bigrams.tsv
        wl_dict[key] = float(wl_arr_of_arrs[i][0])
        print(key, str(wl_dict[key]))
    print("Entries counted.")
    return wl_dict

def clean(wl, flags):
    print("Cleaning entries...")
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
            print("Removed", key, str(wl[key]))
            del wl[key]
    print("Entries cleaned.")
    return wl

def segregate(wl_dict):
    print("Segregating entries by length...")
    wl_arr = []
    for key, value in list(wl_dict.items()):
        if len(key) >= len(wl_arr):
            while len(key) >= len(wl_arr):
                wl_arr.append({})
        wl_arr[len(key)][key] = value
    # for i in range(len(wl_arr)):
    #     wl_arr[i].sort()
    print("Entries segregated")
    for i in range(3, len(wl_arr)):
        print(str(len(wl_arr[i])), str(i) + "-letter entries")
    return wl_arr

def write(wl_arr, filepath, print_score=False, sorted_by="keys"):
    doc = open(filepath, "w")
    for i in range(3, len(wl_arr)):
        doc.write(str(i) + "\n") # Print a heading for each word length
        if sorted_by == "keys":
            sorted_wl = sorted(wl_arr[i].items())
        else:
            sorted_wl = sorted(wl_arr[i].items(), key=operator.itemgetter(1))
        for key, value in sorted_wl:
            doc.write(key)
            if print_score:
                doc.write("\t" + str(value))
            doc.write("\n")
        doc.write("\n")
    doc.close()

def writeJSON(wl_arr, filepath, sorted_by="keys"):
    print("Writing to", filepath)
    # sorted_wl = []
    # for i in range(len(wl_arr)):
    #     if sorted_by == "keys":
    #         sorted_wl.append(sorted(wl_arr[i].items()))
    #     else:
    #         sorted_wl.append(sorted(wl_arr[i].items(), key=operator.itemgetter(1)))
    doc = open(filepath, "w")
    doc.write(json.dumps(wl_arr, indent=4))
    doc.close()


# Main
# ====
# Take a wordlist, clean it, reorder and write to file, scored or unscored
# writeJSON(segregate(clean(count(remove_before_year(read("../WL-SP -1970.tsv"), 1970), 3), "-ilr")), "test.txt")
# write(segregate(clean(count(read("../WL-SP.tsv"), 3), "-il")), "wl-test.txt", False, "values")
writeJSON(segregate(count(read("../WL-WK (scored).tsv"), 2)), "bigrams.json.txt")



# writeJSON([{}, {}, {}, {"ant": 8, "boy": 6, "cat": 4}, {"boxy": 7, "cozy": 5, "dogs": 9}, {"cover": 15, "duvet": 13}], "test.txt", "values")

# for word in score(read("wl-test.txt", False)):
#     if word:
#         (crossword_score, culture_score) = score(word)
#         print(word + "\t" + str(crossword_score) + "\t" + str(culture_score))

# collect_CT_frequency("../answer")

# arr = read("wl-sp.txt")
# wl = []
# for item in arr:
#     if len(item) > 1:
#         while len(item[0]) >= len(wl):
#             wl.append({})
#         if int(item[1]) >= MINIMUM_WORD_FREQUENCY:
#             wl[len(item[0])][item[0]] = item[1]
# try:
#     doc = open("wl-sp.json.txt", "w")
#     doc.write(json.dumps(wl, indent=4))
# except:
#     print("Error opening file to write")

# print(remove_before_year([["nyt", "1945"], ["nyt", "2005"], ["lat", "1969"], ["usa", "1970"]], 1970))
