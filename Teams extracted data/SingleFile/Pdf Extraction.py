import pandas as pd
import os, re

list1 = []
list2 = []


def incCaps(m):
    replaced = '|' + m.group(0) + '|'
    return replaced


# f = "56768 3456slfkd"

data = pd.read_excel(r'C:\Teams extracted data\SingleFile\JCG (3).xlsx')
df = pd.DataFrame(data)

for i in range(396):
    list1.append(df.iat[i, 10])
    list2 = list1
    list2[i] = re.sub('[ ]{2,}', ' | ', str(list2[i]))
    list2[i] = re.sub('([0-9]\S+)', r'|\1|', str(list2[i]))
    list2[i] = list2[i].replace('=', ' | ').replace('| | |', ' | ')
    df.iat[i, 10] = list2[i]

df.to_excel(r'C:\Teams extracted data\SingleFile\JCG (3).xlsx')