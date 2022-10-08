import cs50
while True:
    n = cs50.get_int("Height: ")
    if 1 <= n <= 8:
        for i in range(1, n+1):
            for l in range(n, i, -1):
                print(" ", end="")
            for j in range(0, i):
                print("#", end="")
            for k in range(2):
                print(" ", end="")
            for h in range(0, i):
                print("#", end="")
            print()
        break