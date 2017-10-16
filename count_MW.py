mw = open("../Unused Wordlists/WL-MW.txt").read().split("\n")
counts = [0 for i in range(17)]
for word in mw:
    l = len(word)
    if l > 16:
        l = 16
    counts[l] += 1
    print(str(counts[l]), str(l) + "-letter words")
print("Mirriam-Webster word tallies")
for i in range(len(counts)):
    print(str(counts[i]), str(i) + "-letter words")
