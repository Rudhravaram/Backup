if __name__ == '__main__':
    l1 = []
    f1 = []
    for _ in range(int(input())):
        name = input()
        score = float(input())
        l = []
        l.append(name)
        l.append(score)
        l1.append(l)
    # print(l1)
    for I in range(len(l1)):
        fi = l1[I][1]
        f1.append(fi)
    f1.sort()
    myl = list(dict.fromkeys(f1))
    print()
    # print(f1)
    ll = []
    for I in range(len(l1)):
        if myl[1] == l1[I][1]:
            ll.append(l1[I][0])

    ll.sort()
    for n in range(len(ll)):
        print(ll[n])