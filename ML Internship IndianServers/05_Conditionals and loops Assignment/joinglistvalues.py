
def getval(n):
    l=[]
    for x in range(n):
        w=x+1
        l.append(w)
    print(''.join(map(str, l)))



if __name__ == '__main__':
    n = int(input())
    getval(n)