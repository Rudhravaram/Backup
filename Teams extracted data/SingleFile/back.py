import pandas as pd
import os, re

list1 = []
list2 = []


def incCaps(m):
    replaced = '|' + m.group(0) + '|'
    return replaced


# f = "56768 3456slfkd"

data = pd.read_excel(r'C:\Users\DEBJYOTI BANERJEE\Downloads\PROCLAIM\PROCLAIM from 200 - 400 & 600 +.xlsx')
df = pd.DataFrame(data)

for i in range(680):
    list1.append(df.iat[i, 10])
    list2 = list1
    list2[i] = re.sub('[ ]{2,}', ' | ', str(list2[i]))
    list2[i] = re.sub('([0-9]\S+)', r'|\1|', str(list2[i]))
    list2[i] = list2[i].replace('=', ' | ').replace('| | |', ' | ')
    df.iat[i, 10] = list2[i]

df.to_excel(r'C:\Users\DEBJYOTI BANERJEE\Downloads\PROCLAIM\PROCLAIM from 200 - 400 & 600 +.xlsx')


import pandas as pd
import os, re

list1 = []
list2 = []

data = pd.read_excel(r'C:\Users\DEBJYOTI BANERJEE\Downloads\TEAM Final\TEAM\TEAM from 1- 219 & 431-499.xlsx')
df = pd.DataFrame(data)

for i in range(220):
    list1.append(df.iat[i, 10])
    list2 = list1
    list2[i] = re.sub('[ ]{2,}', ' | ', str(list2[i]))
    df.iat[i, 10] = list2[i]

df.to_excel(r'C:\Users\DEBJYOTI BANERJEE\Downloads\TEAM Final\TEAM\TEAM from 1- 219 & 431-499.xlsx')