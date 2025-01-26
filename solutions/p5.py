n=20
while True:
    r = True
    for i in range(1,21):
        if n%i !=0:
            r = False
            break
    if r:
        print(n)
        break
    n=n+1
