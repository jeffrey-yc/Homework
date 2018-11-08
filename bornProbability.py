import random

def bornProbability(n, showDetails = False):
    girlCount = 0

    for i in range(1, n+1):
        if (showDetails): print(str(i) + ": ")
        childCount = 0

        while (True):
            rn = random.randint(0, 99)
            if (showDetails): print("(" + str(rn) +")", end='')

            isGirl = True if rn <= 48 else False
            childCount += 1

            if (isGirl):
                girlCount += 1
                if (showDetails): print("女+")
                break
            elif childCount == 3:
                if (showDetails): print("男")
                break
            else:
                if (showDetails): print("男")

        if (showDetails): print("\n")

    p = girlCount / n
    print('The probability of a girl being born is: ' + str(p))

    return

bornProbability(10, showDetails = True)
bornProbability(10)
