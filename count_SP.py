lines = open("../WL-SP (since 1970).tsv").read().split("\n")[1:]
# sp = []
counts = [0 for i in range(17)]
print("Counting...")
for line in lines:
    entry = line.split("\t")[2]
    print(entry)
    if entry:
        l = len(entry)
        if l > 16:
            l = 16
        counts[l] += 1
        print(entry, "makes", str(counts[l]), str(l) + "-letter words")
print("Saul Pwanson word tallies since 1970")
for i in range(len(counts)):
    print(str(counts[i]), str(i) + "-letter words")
