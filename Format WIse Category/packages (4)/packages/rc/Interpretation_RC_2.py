import requests
import time
import urllib.parse
import urllib.error
import pandas as pd
import re
import string
import csv
from openpyxl import load_workbook
import copy


def clean(s):
    return s.strip(" : . ( ) ")

def check_rc_2(text_json):
    # data = pd.read_excel(r'Directives_RC.xlsx', sheet_name=sheet1)
    # df = pd.DataFrame(data,
    #                   columns=['Key', 'Available', 'Value Navigation', 'Breaking Condition', 'Name', 'x0', 'x1', 'x2',
    #                            'x3', 'x4', 'x5', 'x6', 'x7', 'Cols', 'Ignore', "REGEX"])
    #
    # result = {}
    # for j in range(df.shape[0]):
    #     if df.loc[j, "Available"] == 'Y':
    #         result[df.loc[j, "Name"]] = ""
    #
    # counters = {}
    # visited = {}
    #
    # for i in range(df.shape[0]):
    #     visited[df.loc[i, "Name"]] = False
    # flag = 0
    result = {}
    add = ""
    x0 = ""
    x2 = ""
    box = []
    add = ""

    def diff(x, x0, x1):
        if x[0] > int(x0) and x[2] < int(x1):
            return True
        return False

    try:
        for i in range(40):
            reg = text_json[i].get("text").replace(" ", "")
            if reg.__contains__("TN") or reg.__contains__("MH") or reg.__contains__("MI") and reg[-4:].isdigit():
                box = text_json[i].get("boundingBox")
                # print(reg)
                x0 = int(box[0]) - 50
                x2 = int(box[2]) + 177
                break
        # print(box)
        # print(x0)
        # print(x2)
        for j in range(len(text_json)):
            x = text_json[j].get("boundingBox")
            if diff(x, x0, x2):
                # print(clean(text_json[j].get("text")))
                add = add + ";" + clean(text_json[j].get("text"))

        # temp1 = add.split(";")
        # while "" in temp1:
        #     temp1.remove("")
        #
        # surname = temp1[2]
        # surname = surname.split(" ")[-1]
        # # print(surname)
        #
        # temp2 = temp1[3:]
        #
        # add2 = ",".join(temp2)
        # add2 = add2.split(surname)[-1]
        # print(add2)
        result["Address"] = add
    except:
        print("Add")

    try:
        # print(result["Address"])
        result["Address"] = result["Address"].replace("Full Address", "").replace("Temporary",
                                                                                  "")  # .replace("Son/wife/daughter of", "")
        result["Address"] = result["Address"].lstrip(', 0 1 2 3 4 5 6 7 8 9 : ( )')
        # print(result["Address"])
        # try:
        #     Pattern = re.compile("(0/91)?[6-9][0-9]{9}")
        #     x = Pattern.search(result["Correspondence Address"])
        #     mobile = x.group()
        #     pin = result["Address"].replace(",", "").replace(" ", "").replace(mobile, "")
        # except:
        #     print("No Mobile")
        #     pin = result["Address"].replace(",", "").replace(" ", "")
        try:
            pattern = re.compile("[0-9]{6}|[0-9]{3}\s[0-9]{3}")  # ^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$")
            pin = result["Address"].replace(",", "").replace(" ", "")
            x = pattern.search(pin)
            result["Pincode"] = x.group()
            result["Address"] = result["Address"].split(result["Pincode"])[0]  # + " " + result["Pincode"]
        except:
            print("Pincode")
    except:
        print("Address")

    return result
