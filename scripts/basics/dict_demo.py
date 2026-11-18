text="hello world"
counts={}
for ch in text:
    if ch in counts:
        counts[ch]=counts[ch]+1
    else:
        counts[ch]=1
print(counts)
