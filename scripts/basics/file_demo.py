with open("data.txt","w") as f:
    f.write("12\n")
    f.write("7.5\n")
    f.write("9\n")

with open("data.txt") as f:
    for line in f:
        print(repr(line))
