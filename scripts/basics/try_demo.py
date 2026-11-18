values=["12","7.5","abc","9"]
for v in values:
    try:
        n=float(v)
        print(v,"→",n)
    except ValueError:
        print(v,"→不是数字，跳过")
