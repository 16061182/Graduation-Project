Well = [1,2,5,10]
Price = [[0,1,2,3],[1,0,-1,2],[2,-1,0,5],[3,2,5,0]]

tmp = []
cost = 0

def func(price):
    tmp = []
    for i in range(0, len(price) - 1):
        for j in range(1, len(price)):
            if(price[i][j] > 0):
                tmp.append([price[i][j], i, j])

    for i in range(len(price) - 1, 0, -1):
        for j in range(0, i):
            if tmp[j][0] > tmp[j+1][0]:
                ans = []
                ans.append(tmp[j][0], )
