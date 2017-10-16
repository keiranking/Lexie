from matplotlib import pyplot as plt
import json
import math

ct = json.loads(open("ct-intersect.json.txt","r").read())
sp = json.loads(open("sp.json.txt","r").read())
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
        # blacklist_y.append(ct[l][entry])
        blacklist_y.append(math.log10(int(sp[l][entry])))

for entry in whitelist:
    if entry:
        l = len(entry)
        whitelist_x.append(math.log10(gs[l][entry]))
        # whitelist_y.append(ct[l][entry])
        whitelist_y.append(math.log10(int(sp[l][entry])))

# for list in [whitelist_x, whitelist_y, blacklist_x, blacklist_y]:
#     for point in list:
#         print(point)
#     print("\n")

plt.scatter(whitelist_x, whitelist_y, None, c="lightskyblue", alpha=0.9, marker=r'o',
            label="good")
plt.scatter(blacklist_x, blacklist_y, None, c="black", alpha=0.9, marker=r'o',
            label="bad")
plt.xlabel("Google hits in the past year, in millions (log scale)")
plt.ylabel("(SP) Crossword appearances (log scale)")
plt.legend(loc=2)
plt.show()
