'''
## 馮文龍 2018/11/06
## License GPL v2

一對夫婦計劃生孩子生到有女兒才停，或生了三個就停止。
他們會擁有女兒的機率是多少？
    * 第l 步：機率模型
        每一個孩子是女孩的機率是0.49 ，是男孩的機率是0.51。
        各個孩子的性別是互相獨立的。
    * 第2 步：分配隨機數字。
        用兩個數字模擬一個孩子的性別: 00, 01, 02, …, 48 ＝ 女孩; 49, 50, 51, …, 99 ＝ 男孩
    * 第3 步：模擬生孩子策略
        從表A當中讀取一對一對的數字，直到這對夫婦有了女兒，或已有三個孩子。
        10次重複中，有9次生女孩。會得到女孩的機率的估計是9/10=0.9。
        如果機率模型正確的話，用數學計算會有女孩的真正機率是0.867。(我們的模
        擬答案相當接近了。除非這對夫婦運氣很不好，他們應該可以成功擁有一個女
        兒。)
R :
girl.born <- function(n, show.id = F){
    girl.count <- 0
    for (i in 1:n) {
        if (show.id) cat(i,": ")
        child.count <- 0
        repeat {
            rn <- sample(0:99, 1) # random number
            if (show.id) cat(paste0("(", rn, ")"))
            is.girl <- ifelse(rn <= 48, TRUE, FALSE)
            child.count <- child.count + 1
            if (is.girl){
                girl.count <- girl.count + 1
                if (show.id) cat("女+")
                break
            } else if (child.count == 3) {
                if (show.id) cat("男")
                break
            } else{
                if (show.id) cat("男")
            }
        }
    if (show.id) cat("\n")
    }
    p <- girl.count / n
    p
}
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


print("Opportunities with detail, if 10 families try: ", get_opportunities(10, True))
print("Opportunities, if 10,000 families try: ", get_opportunities(10000))
