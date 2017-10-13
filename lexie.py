import json

def read(filename):
    print("Opening", filename + "...")
    return json.loads(open(filename,"r").read())

# ct = read("../WL-CT (clean, 105k).json.txt")
# for i in range(len(ct)):
#     print(str(len(ct[i])), str(i) + "-letter words")

class Entry(object):
    def __init__(self, entry="", cross_freq=0, culture_freq=0):
        self.entry = entry.upper()
        self.xw = cross_freq
        self.cu = culture_freq

    def printify(self):
        print(self.entry + ":", self.xw, "puzzles,", str(self.cu) + "m Google results")


box = Entry("box", 4, 28.435)
box.printify()
