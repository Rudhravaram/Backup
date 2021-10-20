import re
from collections import Iterable
def hmc_invoice():
    file = open(r'D:\HMC Invoice data extraction latest code\Information Extraction\part.txt', 'r')
    list1 = []
    dict1 = {}
    for line in file:
        # print(line)
        list1.append(line)
    file.close()
    # print(list1)
    print("################################################################")
    print('\n')
    for i in range(len(list1)):
        if str(list1[i]).__contains__("Invoice No"):
            var1 = str(list1[i]).split('\n')
    dict1['Invoice No'] = re.split('[ ]{2,}', var1[0])[1]
    print(dict1['Invoice No'])
    print("##################################################################")