from matplotlib import pyplot as plt
import json
import math

ct = json.loads(open("ct-intersect.json.txt","r").read())
gs = json.loads(open("gs-intersect.json.txt","r").read())

blacklist = open("blacklist.txt", "r").read().split("\n")
whitelist = open("whitelist.txt", "r").read().split("\n")

blacklist_x = []
blacklist_y = []
whitelist_x = []
whitelist_y = []

for entry in blacklist:
    if entry:
        l = len(entry)
        blacklist_x.append(math.log10(gs[l][entry]))
        blacklist_y.append(ct[l][entry])

for entry in whitelist:
    if entry:
        l = len(entry)
        whitelist_x.append(math.log10(gs[l][entry]))
        whitelist_y.append(ct[l][entry])

plt.scatter(whitelist_x, whitelist_y, None, c="blue", alpha=0.4, marker=r'o',
            label="good")
plt.scatter(blacklist_x, blacklist_y, None, c="red", alpha=0.8, marker=r'o',
            label="bad")
plt.xlabel("Cultural relevance")
plt.ylabel("Crossword appearances")
# plt.legend(loc=2)
plt.show()
