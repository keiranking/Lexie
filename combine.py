import json

def read(filename):
    print("Opening", filename + "...")
    return json.loads(open(filename,"r").read())

def intersect(ct, gs):
    MAX = len(ct)
    ct_intersect = [dict() for i in range(MAX)]
    gs_intersect = [dict() for i in range(MAX)]
    for i in range(MAX):
        print("Finding " + str(i) + "-letter entries with both crossword and culture scores...")
        for key, value in sorted(ct[i].items()):
            count = 0
            if gs[i].get(key):
                ct_intersect[i][key] = value
                gs_intersect[i][key] = gs[i][key]
                count += 1
                print(key)
            print(count, "of", len(ct[i]), "entries")
    return (ct_intersect, gs_intersect)

def write(wl, filename):
    print("Writing to", filename + "...")
    doc = open(filename, "w")
    doc.write(json.dumps(wl, indent=4))

(ct, gs) = intersect(read("../WL-CT (clean, 105k).json.txt"), read("../WL-GS (clean, 144k).json.txt"))

write(ct, "ct-intersect.json.txt")
write(gs, "gs-intersect.json.txt")
# for i in range(len(ct)):
#     print(str(len(ct[i])), str(i) + "-letter words")

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
