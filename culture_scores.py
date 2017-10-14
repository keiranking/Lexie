import re
import json

def read(filename):
    print("Opening", filename + "...")
    return open(filename,"r").read().split('\n')

def parse(line):
    entry = line[:line.find(":")]
    freq = 0
    if re.search("About", line) != None:
        freq = re.search(r'\d+(,?\d*)*', line)[0]
        freq = int(freq.replace(",", "")) / 1000000
    return (entry, freq)

def segregate(arr):
    print("Segregating wordlist by length...")
    wl = []
    for line in arr:
        key, value = parse(line)
        while len(key) >= len(wl): # extend the array if needed
            wl.append({})
        wl[len(key)][key] = value
        print(key, "into", str(len(key)) + "-letter words")
    print("Wordlist segregated")
    return wl

def alphabetize(wl):
    for i in range(len(wl)):
        print("Alphabetizing", len(wl[i]), str(i) + "-letter words...")
        unsorted = wl[i]
        wl[i] = {}
        for key, value in sorted(unsorted.items()):
            wl[i][key] = value
    return wl

def write(wl, filename):
    print("Writing to", filename + "...")
    doc = open(filename, "w")
    doc.write(json.dumps(wl, indent=4))

write(alphabetize(segregate(read("../WL-GS (original).txt"))), "WL-GS.json.txt")
