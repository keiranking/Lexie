MINIMUM_WORD_LENGTH = 3
MAXIMUM_WORD_LENGTH = 15
WORD_FREQUENCY_THRESHOLD = 2 # How often a word has to appear in the raw corpus to qualify for the wordlist

def read(filename, delimiter="\t"):
    raw = open(filename,"r").read().split('\n')
    wl_arr = []
    for i in range(0, len(raw)):
        wl_arr.append(raw[i].split(delimiter))
    return wl_arr

def count(wl_arr_of_arrs, column, hasHeader=True):
    column -= 1
    wl_dict = {}
    start = 1
    if not hasHeader:
        start = 0
    for i in range(start, len(wl_arr_of_arrs)):
        key = wl_arr_of_arrs[i][column].upper()
        wl_dict[key] = wl_dict.get(key, 0) + 1 # increment its frequency
    return wl_dict

def clean(wl, flags):
    for key, value in list(wl.items()):
        isInvalid = False
        if "r" in flags: # remove rare entries
            if value < WORD_FREQUENCY_THRESHOLD:
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

def write(wl_arr, filepath, scored=False):
    doc = open(filepath, "w")
    for i in range(3, len(wl_arr)):
        doc.write(str(i) + "\n") # Print a heading for each word length
        for key in sorted(wl_arr[i].keys()):
            doc.write(key)
            if scored:
                doc.write("\t" + str(wl_arr[i][key]))
            doc.write("\n")
        doc.write("\n")
    doc.close()

# Main
# print(open_data_file("../GN-300,000.tsv")[0:20])

# ngrams = {}
# for i in range(1, len(raw)):
#     row = raw[i].split(delimiter)
#     ngrams[row[0]] = row[1]
# crosswords = segregate_by_length(remove_illegal(remove_rare(open_data_file("../WL-SPGood.tsv", 3)))), "wl.txt")

# Take a wordlist, clean it, order by length and write to file, unscored or scored by frequency
write(segregate(clean(count(read("../WL-SP.tsv"), 3), "-ilr")), "wl.txt")

