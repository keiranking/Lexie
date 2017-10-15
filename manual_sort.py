import json
import re
import random

def read(filename):
    print("Opening", filename + "...")
    return json.loads(open(filename,"r").read())

ct = read("ct-intersect.json.txt")
blacklist = open("blacklist.txt","r").read().split("\n")
whitelist = open("whitelist.txt", "r").read().split("\n")

# print(bad, good)
l = int(input("What length (3-15) entries do you want to vet? "))
if 3 <= l <= 15:
    print("Type any key to reject an entry, nothing to accept it, or 'q' to quit.")
    count = 0
    response = ""
    while response is not "q":
        word, value = random.choice(list(ct[l].items()))
        while word in blacklist or word in whitelist:
            word = random.choice(ct[l].keys())
        response = input(word + "(" + str(value) + "): ")
        if response:
            if response is "q":
                break
            else:
                b = open("blacklist.txt", "a")
                b.write(word + "\n")
                blacklist.append(word)
        else:
            w = open("whitelist.txt", "a")
            w.write(word + "\n")
            whitelist.append(word)
        count += 1
    print(str(count) + " entries vetted.")
