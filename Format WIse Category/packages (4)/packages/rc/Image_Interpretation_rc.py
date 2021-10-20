# import pyrebase
import requests
import time
import urllib.parse, urllib.error
import pandas as pd
import re
import string
import csv
from openpyxl import load_workbook
import copy

def clean(s):
    return s.strip(" : - ")


def diff(x, y, z, df):
    xx = ["x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7"]
    # print(df.loc[z, "x0"])
    for xc in xx:
        # print(df.loc[z, xc])
        if not df.loc[z, xc] == "None":
            if abs(x[int(xc[-1])] - y[int(xc[-1])]) > df.loc[z, xc]:
                return False
    return True


def check(text_json, sheet1, state, bck):

    # for i in range(len(text_json)):
    #     print(text_json[i].get('text'))
    #     print(text_json[i].get('boundingBox'))
    #     print("######################")

    data = pd.read_excel(r'packages/rc/Directives_Images_rc.xlsx', sheet_name=sheet1)
    df = pd.DataFrame(data,
                      columns=['Key', 'Available', 'Value Navigation', 'Breaking Condition', 'Name', 'x0', 'x1', 'x2', 'x3', 'x4',
                               'x5', 'x6', 'x7', 'Cols', 'Ignore'])


    # result = {"Engine No": "", "Insured Name": "", "Registration Number": "", "Make": "", "Date of Registration": "",
    #           "Model - Variant": "", "Mfg Yr": "", "Address": "", "Chassis No": "", "Gross Vehicle Weight": "",
    #           "Seating Capacity": "",
    #           "Cubic Capacity": "", "CUSTOMER_STATE": "", "Pincode": "", "RTO": "", "HYPOTHECATION": "None",
    #           "FINANCIER_NAME": "",
    #           "FINANCIER_BRANCH": "", "Carrying Capacity": ""}

    result = {}
    counters = {}
    visited = {}
    stopwords = ["Manufacturer with Make", "Date of Manufacture", "S/0-", "Description of Vehicle",
                 "Full Address: (Permanent)", "OTHER, NA..", "INDIVIDUAL", "Vehicle Class", "S/WID of", "S/W/D of"]
    for i in range(df.shape[0]):
        visited[df.loc[i, "Name"]] = False
        result[df.loc[i, "Name"]] = ""
    flag = 0
    for i in range(len(text_json)):
        for j in range(df.shape[0]):

            if (df.loc[j, "Available"] == 'Y') and (df.loc[j, "Key"] in text_json[i].get("text")) and visited[df.loc[j, "Name"]] == False:
                try:
                    if df.loc[j, "Value Navigation"] == 'R':
                        # print(df.loc[j, "Key"])
                        x = text_json[i].get("boundingBox")
                        for z in range(i + 1, len(text_json)):
                            if df.loc[j, "Breaking Condition"] in text_json[z].get("text"):
                                break
                            if diff(x, text_json[z].get("boundingBox"), j, df) and text_json[z].get(
                                    "text") not in stopwords:
                                # print(text_json[z].get("text"))
                                # if df.loc[j, "Name"] == "Gross Vehicle Weight":
                                #     print("xyz")
                                #     print((text_json[z].get("text")))
                                if df.loc[j, "Name"] == "Mfg Yr":
                                    if not text_json[z].get("text").replace("/", "").replace(":", "").replace("(",
                                                                                                              "").replace(
                                            " ", "").isnumeric() or len(
                                            text_json[z].get("text").replace("/", "").replace(": ", "")) < 6:
                                        continue
                                result[df.loc[j, "Name"]] = clean(text_json[z].get("text")).replace(df.loc[j, "Ignore"],
                                                                                                    "")

                                if df.loc[j, "Name"] == "Insured Name":
                                    # print(result["Engine No"])
                                    z = result["Insured Name"]
                                    if z[-2:].isdigit() or z.__contains__("AUTOMOBILES") or z.__contains__("REGIONAL") \
                                            or z.__contains__("EXHIBITION") or z.__contains__("FORM 23A") or \
                                            z.__contains__("Date of Registration") or z.__contains__("Owner") \
                                            or z == result["Registration Number"]:
                                        visited[df.loc[j, "Name"]] = False
                                        result["Insured Name"] = ""
                                        continue

                                if df.loc[j, "Name"] == "S/W/D":
                                    # print(result["Engine No"])
                                    if len(result["S/W/D"]) > 25:
                                        visited[df.loc[j, "Name"]] = False
                                        result["S/W/D"] = ""
                                        continue

                                if df.loc[j, "Name"] == "Registration Number":
                                    # print(result["Registration Number"])
                                    z = result["Registration Number"]
                                    z = z.rstrip("L")
                                    z = clean(z)
                                    if len(z) < 5:
                                        visited[df.loc[j, "Name"]] = False
                                        result["Registration Number"] = ""
                                        continue
                                    if z[:2].isdigit() or (not z[-2:].isdigit()) or z.__contains__(
                                            "Registration Date") or z.__contains__("Financer") or z.__contains__(
                                            "TRANSPORT") or \
                                            z.__contains__("Number") or z.__contains__("Address") or z.__contains__(
                                        "Owner"):
                                        visited[df.loc[j, "Name"]] = False
                                        result["Registration Number"] = ""
                                        continue

                                if df.loc[j, "Name"] == "Date of Registration":
                                    # print(result["Date of Registration"])
                                    z = result["Date of Registration"]
                                    z = z.replace("Owner's Serial", "")
                                    z = clean(z)
                                    if len(z) < 8 or len(z) > 18:
                                        visited[df.loc[j, "Name"]] = False
                                        result["Date of Registration"] = ""
                                        continue
                                    if not z[:2].isdigit():
                                        visited[df.loc[j, "Name"]] = False
                                        result["Date of Registration"] = ""
                                        continue
                                if df.loc[j, "Name"] == "Engine No":
                                    # print(result["Engine No"])
                                    if not result["Engine No"][-4:-2].isdigit() or result["Engine No"].__contains__(
                                            "Registration") or result["Engine No"] == result["Chassis No"]:
                                        visited[df.loc[j, "Name"]] = False
                                        result["Engine No"] = ""
                                        continue
                                if df.loc[j, "Name"] == "Chassis No":
                                    z = result["Chassis No"]
                                    z = z.replace(" ", "")
                                    z = clean(z)
                                    # print(len(z))
                                    if len(z) < 9:
                                        visited[df.loc[j, "Name"]] = False
                                        result["Chassis No"] = ""
                                        continue
                                    if not z[-4:-2].isdigit() or z.__contains__("CC") or z[2] == "H": #or z[2] == "K"
                                        visited[df.loc[j, "Name"]] = False
                                        result["Chassis No"] = ""
                                        continue
                                if df.loc[j, "Name"] == "Cubic Capacity":
                                    z = result["Cubic Capacity"]
                                    z = z.replace("his site its the", "")
                                    # print(z)
                                    if len(z) > 7:
                                        visited[df.loc[j, "Name"]] = False
                                        result["Cubic Capacity"] = ""
                                        continue
                                if df.loc[j, "Name"] == "Seating Capacity":
                                    z = result["Seating Capacity"]
                                    # print(z)
                                    z = z.split("including")[0]
                                    z = z.split("Including")[0]
                                    z = z.replace("(", "")
                                    z = z.strip()
                                    # print(z)
                                    if not z[-1].isdigit() or int(z[-2:]) > 20:
                                        visited[df.loc[j, "Name"]] = False
                                        result["Seating Capacity"] = ""
                                        continue
                                if df.loc[j, "Name"] == "Make":
                                    z = result["Make"]
                                    z = z.replace(" ", "").replace(".", "")
                                    z = z.strip()
                                    if z[-2:].isdigit() or z.__contains__("SALOON") or z.__contains__(
                                            "INNOVA") or z.__contains__("DZIRE") or z.__contains__(
                                            "motteted") or z.__contains__("Agreement"):
                                        visited[df.loc[j, "Name"]] = False
                                        result["Make"] = ""
                                        continue
                                if df.loc[j, "Name"] == "Model - Variant":
                                    z = result["Model - Variant"]
                                    z = z.replace(" ", "").replace(".", "")
                                    z = z.strip()
                                    if z[-2:].isdigit() or z.__contains__("SALOON"):
                                        visited[df.loc[j, "Name"]] = False
                                        result["Model - Variant"] = ""
                                        continue
                                if df.loc[j, "Name"] == "Gross Vehicle Weight":
                                    z = result["Gross Vehicle Weight"]
                                    z = z.replace("kgs", "")
                                    z = z.strip()
                                    if len(z) < 3:
                                        visited[df.loc[j, "Name"]] = False
                                        result["Gross Vehicle Weight"] = ""
                                        continue
                                    if z == result["Mfg Yr"] or (not z[-2:].isdigit()):
                                        visited[df.loc[j, "Name"]] = False
                                        result["Gross Vehicle Weight"] = ""
                                        continue

                                if len(result[df.loc[j, "Name"]]) == 0:
                                    # print(text_json[z].get("text"))
                                    # print(df.loc[j, "Name"])
                                    continue
                                else:
                                    # print(df.loc[j, "Name"])
                                    visited[df.loc[j, "Name"]] = True
                                    break
                        if df.loc[j, "Name"] == "Cubic Capacity" and visited["Cubic Capacity"] == False:
                            # print("yesss")
                            cvb = i - 5
                            for z in range(i - 1, cvb, -1):

                                if not clean(text_json[z].get("text"))[:2].isdigit():
                                    continue
                                if diff(x, text_json[z].get("boundingBox"), j, df):
                                    # print(text_json[z].get("text"))
                                    result[df.loc[j, "Name"]] = clean(text_json[z].get("text")).replace(
                                        df.loc[j, "Ignore"], "")
                                    visited[df.loc[j, "Name"]] = True
                                    break
                        if df.loc[j, "Name"] == "Mfg Yr" and visited["Mfg Yr"] == False:
                            cvb = i - 5
                            for z in range(i - 1, cvb, -1):
                                if diff(x, text_json[z].get("boundingBox"), j, df) and text_json[z].get("text").replace(
                                        "/",
                                        "").isnumeric():
                                    result[df.loc[j, "Name"]] = clean(text_json[z].get("text")).replace(
                                        df.loc[j, "Ignore"],
                                        "")
                                    visited[df.loc[j, "Name"]] = True
                                    break
                        if df.loc[j, "Name"] == "Insured Name" and visited["Insured Name"] == False:
                            cvb = i - 26
                            for z in range(i - 1, cvb, -1):
                                # print(text_json[z].get("text"))
                                if len(text_json[z].get("text").split()) > 4 or text_json[z].get("text")[-3:].isdigit() \
                                        or text_json[z].get("text").__contains__("Registration No") or text_json[z].get("text").__contains__("FORM 23"):
                                    continue
                                if diff(x, text_json[z].get("boundingBox"), j, df):
                                    result[df.loc[j, "Name"]] = clean(text_json[z].get("text")).replace(
                                        df.loc[j, "Ignore"],"")
                                    visited[df.loc[j, "Name"]] = True
                                    break
                        if df.loc[j, "Name"] == "Date of Registration" and visited["Date of Registration"] == False:
                            # print("yesss")
                            cvb = i - 5
                            for z in range(i - 1, cvb, -1):
                                if not clean(text_json[z].get("text"))[:2].isdigit():
                                    continue
                                if diff(x, text_json[z].get("boundingBox"), j, df):
                                    result[df.loc[j, "Name"]] = clean(text_json[z].get("text")).replace(
                                        df.loc[j, "Ignore"],
                                        "")
                                    visited[df.loc[j, "Name"]] = True
                                    break
                        if df.loc[j, "Name"] == "Engine No" and visited["Engine No"] == False:
                            # print("yesss")
                            cvb = i - 20
                            for z in range(i - 1, cvb, -1):
                                # print(text_json[z].get("text"))
                                if len(text_json[z].get("text").split()) > 4 or not text_json[z].get("text")[
                                                                                    -3:].isdigit() or text_json[z].get(
                                        "text").upper().__contains__("REGISTRATION"):
                                    continue
                                if diff(x, text_json[z].get("boundingBox"), j, df):
                                    result[df.loc[j, "Name"]] = clean(text_json[z].get("text")).replace(
                                        df.loc[j, "Ignore"], "")
                                    visited[df.loc[j, "Name"]] = True
                                    break
                        if df.loc[j, "Name"] == "Chassis No" and visited["Chassis No"] == False:
                            # print("yesss")
                            cvb = i - 20
                            for z in range(i - 1, cvb, -1):
                                # print(text_json[z].get("text"))
                                if len(text_json[z].get("text")) > 30 or len(text_json[z].get("text")) < 9:
                                    continue
                                if len(text_json[z].get("text").split()) > 4 or not text_json[z].get("text")[
                                                                                    -4:-2].isdigit():
                                    continue
                                if diff(x, text_json[z].get("boundingBox"), j, df):
                                    result[df.loc[j, "Name"]] = clean(text_json[z].get("text")).replace(
                                        df.loc[j, "Ignore"], "")
                                    visited[df.loc[j, "Name"]] = True
                                    break
                    elif df.loc[j, "Value Navigation"] == 'INIT':
                        x = text_json[i].get("text")
                        x = x.split(df.loc[j, "Key"])[1]
                        result[df.loc[j, "Name"]] = x
                        visited[df.loc[j, "Name"]] = True

                        if df.loc[j, "Name"] == "Insured Name":
                            # print(z)
                            # print(result["Registration Number"])
                            z = result["Insured Name"]
                            if z.upper().__contains__("ADDRESS"):
                                visited[df.loc[j, "Name"]] = False
                                result["Insured Name"] = ""
                                continue

                        if len(result[df.loc[j, "Name"]].strip(". , / |")) == 0:
                            visited[df.loc[j, "Name"]] = False
                            continue
                        break
                    elif df.loc[j, "Value Navigation"] == 'BML':
                        result[df.loc[j, "Name"]] = ""
                        x = text_json[i].get("boundingBox")
                        xc = i + 1
                        # print(df.loc[j, "Key"])
                        while df.loc[j, "Breaking Condition"] not in text_json[xc].get("text"):
                            if diff(x, text_json[xc].get("boundingBox"), j, df):
                                result[df.loc[j, "Name"]] = result[df.loc[j, "Name"]] + ", " + text_json[xc].get("text")
                                x = text_json[xc].get("boundingBox")
                                visited[df.loc[j, "Name"]] = True
                            xc = xc + 1
                        # print(result["Address"])
                        if result["Address"]:
                            z = result["Address"]
                            z = z.split("Date of Registration")[0]
                            z = z.split("Sonwireldaughter of")[0]
                            if len(z) < 15:
                                visited[df.loc[j, "Name"]] = False
                                result["Address"] = ""
                                continue
                        break
                    elif df.loc[j, "Value Navigation"] == 'TBML':
                        result[df.loc[j, "Name"]] = ""
                        x = text_json[i].get("boundingBox")
                        xc = i
                        while df.loc[j, "Breaking Condition"] not in text_json[xc].get("text"):
                            if diff(x, text_json[xc].get("boundingBox"), j, df):
                                result[df.loc[j, "Name"]] = result[df.loc[j, "Name"]] + " " + text_json[xc].get("text")
                                x = text_json[xc].get("boundingBox")
                                visited[df.loc[j, "Name"]] = True
                            xc = xc + 1
                        break
                    elif df.loc[j, "Value Navigation"] == "TABLE":
                        col = df.loc[j, "Cols"].split(',')
                        xc = i + 1
                        x = text_json[xc].get("boundingBox")
                        xz = 0
                        while df.loc[j, "Breaking Condition"] not in text_json[xc].get("text"):
                            # print(text_json[xc].get("text"))
                            if diff(x, text_json[xc].get("boundingBox"), j, df):
                                result[col[xz]] = clean(text_json[xc].get("text"))
                                x = text_json[xc].get("boundingBox")
                                xz = xz + 1
                                visited[df.loc[j, "Name"]] = True
                            xc = xc + 1
                        break
                    elif df.loc[j, "Value Navigation"] == "TTABLE":
                        col = df.loc[j, "Cols"].split(',')
                        xc = i + 1
                        x = text_json[xc].get("boundingBox")
                        xz = 0
                        while df.loc[j, "Breaking Condition"] not in text_json[xc].get("text"):
                            # print(text_json[xc].get("text"))
                            if diff(x, text_json[xc].get("boundingBox"), j, df):
                                a = text_json[xc].get("text")
                                if a.isalpha():
                                    result[col[xz]] = clean(text_json[xc].get("text"))
                                    xz = xz + 1
                                else:
                                    a = a.replace("|", "").replace("  ", " ").split(' ')
                                    for iv in range(len(a)):
                                        result[col[xz]] = a[iv]
                                        xz = xz + 1
                                x = text_json[xc].get("boundingBox")
                                visited[df.loc[j, "Name"]] = True
                            xc = xc + 1
                        break
                    elif df.loc[j, "Value Navigation"] == 'RBML':
                        x = text_json[i].get("boundingBox")
                        xc = i + 1
                        coor = text_json[xc].get("boundingBox")
                        if df.loc[j, "Name"] == "Address" and state == "BIHAR":
                            while abs(x[1] - coor[1]) > df.loc[j, "x1"]:
                                xc = xc + 1
                                coor = text_json[xc].get("boundingBox")
                        elif df.loc[j, "Name"] == "Address" and state == "UTTAR PRADESH":
                            while abs(x[1] - coor[1]) > df.loc[j, "x1"] or not len(
                                    text_json[xc].get("text").strip(": ").split()) >= 4:
                                # print(text_json[xc].get("text"))
                                xc = xc + 1
                                coor = text_json[xc].get("boundingBox")
                        elif df.loc[j, "Name"] == "Address":
                            while abs(x[1] - coor[1]) > df.loc[j, "x1"] or not len(
                                    text_json[xc].get("text").strip(": ").split()) >= 3:
                                # print(text_json[xc].get("text"))
                                xc = xc + 1
                                coor = text_json[xc].get("boundingBox")
                        else:
                            while abs(x[1] - coor[1]) > df.loc[j, "x1"]:
                                xc = xc + 1
                                if xc >= len(text_json):
                                    break
                                coor = text_json[xc].get("boundingBox")
                        result[df.loc[j, "Name"]] = text_json[xc].get("text")
                        x = coor
                        xc = xc + 1
                        coor = text_json[xc].get("boundingBox")
                        while df.loc[j, "Breaking Condition"] not in text_json[xc].get("text"):
                            # print(text_json[xc].get("text"))
                            if abs(x[0] - coor[0]) <= int(df.loc[j, "x0"]):
                                result[df.loc[j, "Name"]] = result[df.loc[j, "Name"]] + " " + text_json[xc].get("text")
                                x = coor
                            xc = xc + 1
                            # print(text_json[xc].get("text"))
                            coor = text_json[xc].get("boundingBox")
                            if state == "BIHAR" and "Venicle" in text_json[xc].get("text"):
                                break
                    elif df.loc[j, "Value Navigation"] == "B":
                        x = text_json[i].get("boundingBox")
                        for z in range(i + 1, len(text_json)):
                            if diff(x, text_json[z].get("boundingBox"), j, df):
                                # print(df.loc[j,"x0"])
                                result[df.loc[j, "Name"]] = clean(text_json[z].get("text"))
                                visited[df.loc[j, "Name"]] = True
                                break
                except:
                    print("Interpretation Issue")
    result1 = copy.deepcopy(result)
    if bck == 1:
        for key in result1.keys():
            if result1[key] == "":
                del result[key]

    return result

