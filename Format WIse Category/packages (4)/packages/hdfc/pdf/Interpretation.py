import pandas as pd


def clean(t):
    return t.strip(" . ,:;-_! \n ' ' + | / =  , , , , , , ,( ) ").replace("`", "")


def magic(s, x):

    data = pd.read_excel(r'packages/hdfc/pdf/Directives.xlsx', sheet_name=x)
    df = pd.DataFrame(data, columns=['SL No','Key', 'Available', 'Value Navigation',
                                     'Breaking Condition', 'REGEX', 'Ignore', 'Cols', 'Counters', 'Name', 'Remo'])

    result = {}

    counters = {}
    x = df["Counters"]
    visited = {}

    for i in range(df.shape[0]):
        visited[df.loc[i, "Name"]] = False

    for i in range(df.shape[0]):
        result[df.loc[i, "Name"]] = ""

    flag = 0
    for i in x:
        if not i == "None":
            counters[i] = 0
    for i in range(len(s)):
        for j in counters.keys():
            if j in s:
                counters[j] = counters[j] + 1
        for j in range(df.shape[0]):
            if (df.loc[j, "Available"] == 'Y') and (df.loc[j, "Key"] in s[i]) and (visited[df.loc[j, "Name"]] == False or result[df.loc[j, "Name"]] == ""):
                # try:
                if df.loc[j, "Value Navigation"] == 'R':
                    x = s[i]
                    x = x.split(df.loc[j, "Key"])[1]
                    if not df.loc[j, "Breaking Condition"] == "None":
                        x = x.split(df.loc[j, "Breaking Condition"])
                        x = x[0]
                    # result[df.loc[j, "Name"]] = clean(x).replace(df.loc[j, "Ignore"], "").split("              ")[0]
                    result[df.loc[j, "Name"]] = clean(x).replace(df.loc[j, "Ignore"], "")
                    visited[df.loc[j, "Name"]] = True
                    # if df.loc[j, "Key"] == "Period of":
                    #     result[df.loc[j, "Name"]] = result[df.loc[j, "Name"]] + " " + s[i + 1].split("Insurance")[
                    #         1].strip()
                    if df.loc[j, "Name"] == "Cubic Capacity" and result[df.loc[j, "Name"]].__contains__("GSTIN"):
                        x = clean(s[i + 1])
                        x = x.split("Seats")[0]
                        result[df.loc[j, "Name"]] = x
                elif df.loc[j, "Value Navigation"] == 'BML':
                    x = df.loc[j, "Breaking Condition"]
                    i = i + 1
                    z = ""
                    while x not in s[i]:
                        z = z + ', ' + clean(s[i]).replace(df.loc[j, "Ignore"], "")
                        i = i + 1
                    result[df.loc[j, "Name"]] = clean(z)
                    visited[df.loc[j, "Name"]] = True
                elif df.loc[j, "Value Navigation"] == 'RBML':
                    # print(df.loc[j, "SL No"])
                    x = df.loc[j, "Breaking Condition"]
                    z = s[i].split(df.loc[j, "Key"])[1].split(df.loc[j, "Remo"])[0]
                    # print("add " + z)
                    # print(z)
                    # z = z.split("       ")[0]
                    z = clean(z).split("   ")[0]
                    # print(z)
                    # replace(df.loc[j, "Ignore"], "")
                    k = i + 1
                    # print(df.loc[j, "SL No"])
                    zf = 1
                    while x not in s[k]:
                        # print(s[k])
                        z = z + ', ' + clean(s[k].strip().split("               ")[0].replace(df.loc[j, "Ignore"], "")).replace(df.loc[j, "Remo"],"").replace("Address","")
                        # print("add1 " + z)
                        # print(str(zf) + " " + z)
                        zf = zf + 1
                        k = k + 1
                    result[df.loc[j, "Name"]] = clean(z).replace("   ", " ")
                    # print(result[df.loc[j, "Name"]])
                    visited[df.loc[j, "Name"]] = True
                    # Original
                    # x = df.loc[j, "Breaking Condition"]
                    # z = s[i].split(df.loc[j, "Key"])[1]
                    # z = clean(z).replace(df.loc[j, "Ignore"], "")
                    # i = i + 1
                    # while x not in s[i]:
                    #     z = z + ', ' + clean(s[i]).replace(df.loc[j, "Ignore"], "")
                    #     i = i + 1
                    # result[df.loc[j, "Name"]] = clean(z).replace("   ", " ")
                    # visited[df.loc[j, "Key"]] = True
                elif df.loc[j, "Value Navigation"] == 'RBML1':
                    x = df.loc[j, "Breaking Condition"]
                    z = s[i].split(df.loc[j, "Key"])[1]
                    # print(z)
                    # z = z.split("       ")[0]
                    z = clean(z).split("   ")[0]
                    # print(z)
                    # replace(df.loc[j, "Ignore"], "")
                    k = i + 1
                    while x not in s[k]:
                        z = z + ', ' + clean(s[k].strip().replace(df.loc[j, "Ignore"], ""))
                        k = k + 1
                    result[df.loc[j, "Name"]] = clean(z).replace("   ", " ")
                    visited[df.loc[j, "Name"]] = True
                elif df.loc[j, "Value Navigation"] == 'TABLE':
                    x = df.loc[j, "Breaking Condition"]
                    i = i + 1
                    cols = df.loc[j, "Cols"].replace(df.loc[j, "Ignore"], "").split(',')
                    count = len(cols)
                    z_list = []
                    prev_z = []
                    prev_zlen = 0
                    while True:
                        # print(s[i])
                        z = s[i].replace(df.loc[j, "Ignore"], "").split("   ")
                        z = [k.strip('\n ') for k in z if k]
                        # print(z)
                        # print(str(count) + " " + str(len(z)))
                        # print(z)
                        # print(len(z))
                        if x in s[i]:
                            break
                        elif len(z) == count:
                            # print(z)
                            z_list.append(z)
                        # elif len(z) < count:
                        elif prev_zlen + len(z) == count:
                            xv = []
                            res = []
                            a = s[i-1]
                            b = s[i]
                            c = s[i+1]
                            ih = False
                            it = False
                            co = 0
                            for xc in range(len(b)):
                                if xc < len(a) and a[xc] != " ":
                                    if ih == True:
                                        for vb in range(5):
                                            xv.append("  ")
                                    elif it == False:
                                        xv.append(" ")
                                    ih = False
                                    it = True
                                    xv.append(a[xc])
                                    if xc < len(c) and c[xc] != " ":
                                        res.append(c[xc])
                                        if xc + 1 < len(c) and c[xc + 1] == " ":
                                            res.append(" ")
                                    if xc+1<len(a) and a[xc+1] == " ":
                                        xv.append(" ")
                                elif b[xc]!=" ":
                                    xv.extend(res)
                                    it = False
                                    if co>3:
                                        for vb in range(5):
                                            xv.append(" ")
                                        co=0
                                    ih = True
                                    if res != []:
                                        for vb in range(5):
                                            xv.append(" ")
                                    res = []
                                    xv.append(b[xc])
                                else:
                                    # if it == True:
                                    #     xv.append(" ")
                                    co = co + 1
                                    if xc < len(c) and c[xc] != " ":
                                        res.append(c[xc])
                                        if xc + 1 < len(c) and c[xc + 1] == " ":
                                            res.append(" ")
                            # print(xv)

                            cv = ""
                            for xc in range(len(xv)):
                                if xv[xc]!='\n':
                                    cv = cv + xv[xc]

                            # print(cv)
                            z = cv.replace(df.loc[j, "Ignore"], "").split("     ")
                            z = [k.strip('\n ') for k in z if k]
                            z_list.append(z)
                            # print(z)
                            # print("z")
                            # print(z_list)
                            # print("z_list")
                        i = i + 1
                        prev_z = z
                        prev_zlen = len(z)
                    fin_table = []
                    for ad in range(len(z_list)):
                        # print(z_list[ad])
                        if len(z_list[ad]) == count:
                            res = {cols[i].strip(): z_list[ad][i].strip() for i in range(len(cols))}
                            # print(res)
                        # result.update(res)
                        #     print(res)
                            fin_table.append(res)
                    # result["Gross Loss"] = str(round(tot_gross_loss,2))
                    result["TABLE"] = fin_table
                    if result["TABLE"]!=[]:
                        visited["TABLE"] = True
                    # print(fin_table)
                elif df.loc[j, "Value Navigation"] == 'ADDRESS':
                    # print("hahahaha")
                    i = i + 1
                    r = i
                    ans = ""
                    while not df.loc[j, "Breaking Condition"] in s[r]:  # and ("For the Vehicle" in s[j])):
                        che = len(s[r]) - len(s[r].lstrip())
                        #             print(s[j])
                        #             print(che)
                        if che < 5:
                            # print(che)
                            z = s[r].split("   ")[0].split(df.loc[j, "Ignore"])[0]
                            #                 print(z)
                            if not ((z == " " or z == "") or z.strip().isnumeric()):
                                ans = ans + z.replace("\n", "") + ','
                        r = r + 1
                    result["Address"] = ans.rstrip(",")
                elif df.loc[j, "Value Navigation"] == 'RIGHT':
                    x = df.loc[j, "Breaking Condition"]
                    k = i
                    y = ""
                    z = ""
                    while x not in s[k]:
                        y = s[k].split("   ")[-1]
                        y = y.replace("   ", " ")
                        z = z + ', ' + clean(y).replace(df.loc[j, "Ignore"], "")
                        k = k + 1

                    result[df.loc[j, "Name"]] = clean(z)
                    visited[df.loc[j, "Name"]] = True
                else:  # B3L
                    x = df.loc[j, "Value Navigation"]
                    x = int(x[1])
                    z = ""
                    i = i + 1
                    xc = df.loc[j, "Breaking Condition"]
                    while x != 0:
                        if xc in s[i]:
                            z = z + clean(s[i]).split(xc)[0]
                            break
                        z = z + clean(s[i])
                        i = i + 1
                        x = x - 1
                    result[df.loc[j, "Name"]] = clean(z).split(df.loc[j, "Ignore"])[0]
                    visited[df.loc[j, "Name"]] = True
                # except:
                #     print(result[df.loc[j, "SL No"]])
                #     print("Interpretation Code")
                #     result[df.loc[j, "Name"]] = ""

    return result
