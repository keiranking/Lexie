import json
import operator

def read(filename):
    print("Opening", filename + "...")
    return json.loads(open(filename,"r").read())

def intersect(a, b): # takes two arrays of dictionaries and finds the intersect
    MAX = len(a)
    a_intersect = [dict() for i in range(MAX)]
    b_intersect = [dict() for i in range(MAX)]
    a_not_in_b = [dict() for i in range(MAX)]

    for i in range(MAX):
        print("Finding " + str(i) + "-letter entries with both crossword and culture scores...")
        for key, value in sorted(a[i].items()):
            count = 0
            if b[i].get(key):
                a_intersect[i][key] = value
                b_intersect[i][key] = b[i][key]
                count += 1
                print(key)
            else:
                a_not_in_b[i][key] = value
            print(count, "of", len(a[i]), "entries")
    return (a_intersect, b_intersect, a_not_in_b)

def write(wl, filename):
    print("Writing to", filename + "...")
    doc = open(filename, "w")
    doc.write(json.dumps(wl, indent=4))

def write_sorted(wl_arr, filepath, print_score=False, sorted_by="keys"):
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


# (ct, gs) = intersect(read("../WL-CT (clean, 105k).json.txt"), read("../WL-GS (clean, 144k).json.txt"))

# (wk, ct, wk_not_ct) = intersect(read("bigrams.json.txt"), read("../WL-CT (clean, 105k).json.txt"))
# write(wk, "wk-intersect.json.txt")
# write(wk_not_ct, "wk-outersect.json.txt")

# for i in range(len(ct)):
#     print(str(len(ct[i])), str(i) + "-letter words")

write_sorted(read("wk-intersect.json.txt"), "wk-intersect-sorted.txt", True, "values")
write_sorted(read("wk-outersect.json.txt"), "wk-outersect-sorted.txt", True, "values")

class Entry(object):
    def __init__(self, entry="", cross_freq=0, culture_freq=0):
        self.entry = entry.upper()
        self.xw = cross_freq
        self.cu = culture_freq

    def __str__(self):
        return self.entry + ": " + str(self.xw) + " puzzles, " + str(self.cu) + "m hits"

    def __len__(self):
        return len(self.entry)

    def score(self):
        # some function of xw and cu
        return self.xw * self.cu

# box = Entry("box", 4, 28.435)
# print(len(box))
