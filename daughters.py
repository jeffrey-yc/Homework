'''
## 馮文龍 2018/11/06
## License MIT
'''

import numpy as np
import sys


def get_opportunities(families, show_detail=False):
    daughters = 0
    for family in range(0, families):
        children = 0
        is_son = True
        if show_detail:
            sys.stdout.write(str(family)+":")
        while is_son and children < 3:
            rn = np.random.randint(0,99)
            if show_detail:
                sys.stdout.write("("+str(rn)+")")

            children += 1

            if rn <= 48:
                daughters += 1
                is_son = False

            if not is_son:
                if show_detail:
                    sys.stdout.write('女+')
            elif children == 3:
                if show_detail:
                    sys.stdout.write("男")
            else:
                if show_detail:
                    sys.stdout.write("男")
        if show_detail:
            print(" ")

    return daughters/families


print("Opportunity if 10 families try: ", get_opportunities(10, True))
print("Opportunity if 10,000 families try: ", get_opportunities(10000))
