# import pyrebase
import requests
import time
import urllib.parse, urllib.error
import pandas as pd
import re
import string
import csv
from openpyxl import load_workbook


def common_member(a, b):
    a_set = set(a)
    b_set = set(b)
    return a_set & b_set

def clean(s):
    return s


def diff(x, y, z, df):
    xx = ["x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7"]
    # print(df.loc[z, "x0"])
    for xc in xx:
        # print(df.loc[z, xc])
        if not df.loc[z, xc] == "None":
            if abs(x[int(xc[-1])] - y[int(xc[-1])]) > df.loc[z, xc]:
                return False
    return True


def check(text_json, sheet1):

    # for i in range(len(text_json)):
    #     print(text_json[i].get('text'))
    #     print(text_json[i].get('boundingBox'))
    #     print("######################")

    data = pd.read_excel(r'packages/hdfc/image/Directives_Images.xlsx', sheet_name=sheet1)
    df = pd.DataFrame(data,
                      columns=['Key', 'Available', 'Value Navigation', 'Breaking Condition', 'Name', 'x0', 'x1', 'x2', 'x3', 'x4',
                               'x5', 'x6', 'x7', 'Cols', 'Ignore'])

    result = {}
    stopwords = {"Licence Carrying", "License C"}
    for j in range(df.shape[0]):
        if (df.loc[j, "Available"] == 'Y'):
            result[df.loc[j, "Name"]] = ""

    counters = {}
    visited = {}

    for i in range(df.shape[0]):
        visited[df.loc[i, "Name"]] = False
    flag = 0
    for i in range(len(text_json)):
        for j in range(df.shape[0]):
            try:
                if (df.loc[j, "Available"] == 'Y') and (df.loc[j, "Key"] in text_json[i].get("text")) and ((visited[df.loc[j, "Name"]] == False) or (result[df.loc[j, "Name"]].strip(" ") == "")):
                    if df.loc[j, "Value Navigation"] == 'R':
                        # print(df.loc[j, "Key"])
                        if df.loc[j, "Name"] == "RTO" and df.loc[j, "Key"] == "RT" and not (text_json[i].get("text").strip() == "RT" or text_json[i].get("text").strip() == "RTO" or text_json[i].get("text").strip() == "RTC"):
                            continue
                        x = text_json[i].get("boundingBox")
                        xcx = x
                        for z in range(i+1, len(text_json)):
                            if df.loc[j, "Breaking Condition"] in text_json[z].get("text"):
                                break
                            if df.loc[j, "Name"] == "RTO":
                                # print(text_json[z].get("text"))
                                if text_json[z].get("text") == "Correspondence" or text_json[z].get("text").upper().__contains__("CORR") or text_json[z].get("text") == "Corr.Address":
                                    continue
                            if diff(x, text_json[z].get("boundingBox"), j, df):
                                # print(df.loc[j,"x0"])
                                # print(text_json[z].get("text"))
                                if df.loc[j, "Name"] == "RTO":
                                    if text_json[z].get("text")[-2:].isdigit() or text_json[z].get("text").__contains__("Chassis"):
                                        continue
                                if df.loc[j, "Name"] == "Registration No.":
                                    if text_json[z].get("text").__contains__("From"):
                                        continue
                                if df.loc[j, "Name"] == "Make":
                                    p = text_json[z].get("text")
                                    if p[-2:].isdigit() or p.__contains__("Make") or p.__contains__("Mudial") or p.__contains__("Model - Variant") or p.__contains__("Registration") or p.__contains__("Policy") or p.__contains__("Engine") or len(p) > 22 or p.replace(" ", "").isnumeric():
                                        continue
                                if df.loc[j, "Name"] == "Model":
                                    if text_json[z].get("text").__contains__("TATA MOTORS LTD") or text_json[z].get("text").__contains__("From") or text_json[z].get("text").__contains__("Policy") or (text_json[z].get("text").replace(" ", "")).isnumeric():
                                        continue
                                if df.loc[j, "Name"] == "Chassis No":
                                    p = text_json[z].get("text")
                                    p = p.replace(":", "1")
                                    # print(p)
                                    q = "None"
                                    if "Engine No." in result.keys():
                                        q = result["Engine No."]
                                    if (not p[-3:-1].isdigit()) or p == q:
                                        # print("yesss")
                                        continue
                                if df.loc[j, "Name"] == "Engine No.":
                                    if text_json[z].get("text").__contains__(result["Registration No."]) or text_json[z].get("text").__contains__("Body") or (not text_json[z].get("text")[-2:].isdigit()) or len(text_json[z].get("text")) > 18:
                                        continue
                                if df.loc[j, "Name"] == "Cubic Capacity":
                                    p = text_json[z].get("text")
                                    p = p.split("Seat")[0]
                                    p = p.strip()
                                    # print(p)
                                    if len(p.replace("CC", "").replace("(", "").replace(")", "").strip()) > 5 or len(p.replace("CC", "").replace("(", "").replace(")", "").strip()) < 2 or (not p.replace("CC", "").replace("(", "").replace(")", "").strip()[-2:].isdigit()):
                                        # print("yesss")
                                        continue
                                if df.loc[j, "Name"] == "Mfg. Year":
                                    p = text_json[z].get("text")
                                    # print(p)
                                    p = p.replace("0 3H", "")
                                    p = p.split("Body")[0]
                                    p = p.strip()
                                    if not p[-2:].isdigit():
                                        continue
                                if df.loc[j, "Name"] == "NCB":
                                    if not text_json[z].get("text").isnumeric():  # Previous Policy Number
                                        continue
                                if df.loc[j, "Name"] == "Policy Number":
                                    if not (text_json[z].get("text").replace(" ", "")).isnumeric():
                                        continue

                                result[df.loc[j, "Name"]] = str(clean(text_json[z].get("text"))).replace(df.loc[j,"Ignore"], "").replace(df.loc[j, "Breaking Condition"], "").strip()
                                visited[df.loc[j, "Name"]] = True

                                if "Cubic Capacity" in result.keys():
                                    p = result["Cubic Capacity"]
                                    p = p.split("Seat")[0]
                                    # print(p)
                                    result["Cubic Capacity"] = p.strip()

                                if "Insured Name" in result.keys():
                                    # print(result["Insured Name"])
                                    if (df.loc[j, "Name"] == "Insured Name" and result["Insured Name"][0] != 'M') or result["Insured Name"].__contains__("PAN N") or len(result["Insured Name"]) > 35:
                                        # print("yesss")
                                        visited[df.loc[j, "Name"]] = False
                                        result["Insured Name"] = ""
                                        continue
                                if "Engine No." in result.keys():
                                    # print("yesss")
                                    z = result["Engine No."]
                                    # print(z)
                                    if (z[0] == 'M' and z[-6] != " " and z[-6] != "F" and z[1] != "8") or "Date" in z or "Chassis" in z or "invoice" in z:  # and (not z[1] == "B")
                                        visited[df.loc[j, "Name"]] = False
                                        result["Engine No."] = ""
                                        continue
                                # if "Chassis No" in result.keys():
                                #     # print("yesss")
                                #     z = result["Chassis No"]
                                #     print(z + "&&&&&")
                                #     if z.strip().isalpha():
                                #         visited[df.loc[j, "Name"]] = False
                                #         result["Chassis No"] = ""
                                #         continue

                                # if "Make" in result.keys():
                                #     # print("yesss")
                                #     z = result["Make"]
                                #     if "Details" in z or "Make" in z or "Model" in z or "Policy" in z or z[-3:].isdigit():
                                #         visited[df.loc[j, "Name"]] = False
                                #         result["Make"] = ""
                                #         continue

                                if len(result[df.loc[j, "Name"]]) == 0:
                                    # print(text_json[z].get("text"))
                                    continue
                                else:
                                    visited[df.loc[j, "Name"]] = True
                                    break
                                # break
                        if df.loc[j, "Key"] == "Cubic Capacity":
                            # print(result["Cubic Capacity"])
                            result["Cubic Capacity"] = result["Cubic Capacity"].replace("Watts", "").replace("Wats", "").replace("Seats", "")
                        if df.loc[j, "Name"] == "Engine No." and visited["Engine No."] == False:
                            # print("yesss")
                            cvb = i - 20
                            for z in range(i - 1, cvb, -1):
                                # print(text_json[z].get("text"))
                                if len(text_json[z].get("text")) < 5 or (not text_json[z].get("text")[-3:].isdigit()) \
                                        or text_json[z].get("text").upper().__contains__("REGISTRATION")\
                                        or "KA-15-H4-3634" in text_json[z].get("text") or len(text_json[z].get("text")) > 18:
                                    # print("noooo")
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
                                if len(text_json[z].get("text")) > 18 or len(text_json[z].get("text")) < 5:
                                    continue
                                if len(text_json[z].get("text").split()) > 4 or not text_json[z].get("text")[-4:-2].isdigit():
                                    continue
                                if diff(x, text_json[z].get("boundingBox"), j, df):
                                    result[df.loc[j, "Name"]] = clean(text_json[z].get("text")).replace(df.loc[j, "Ignore"], "")
                                    visited[df.loc[j, "Name"]] = True
                                    break
                        if df.loc[j, "Name"] == "Make" and visited["Make"] == False:
                            # print("yesss")
                            cvb = i - 20
                            for z in range(i - 1, cvb, -1):
                                # print(text_json[z].get("text"))
                                if len(text_json[z].get("text")) > 30:
                                    continue
                                if diff(x, text_json[z].get("boundingBox"), j, df):
                                    result[df.loc[j, "Name"]] = clean(text_json[z].get("text")).replace(
                                        df.loc[j, "Ignore"], "")
                                    visited[df.loc[j, "Name"]] = True
                                    break
                        if df.loc[j, "Name"] == "Policy Number" and visited["Policy Number"] == False:
                            # print("yesss")
                            cvb = i - 20
                            for z in range(i - 1, cvb, -1):
                                # print(text_json[z].get("text"))
                                if not (text_json[z].get("text").replace(" ", "")).isnumeric():
                                    continue
                                if diff(x, text_json[z].get("boundingBox"), j, df):
                                    result[df.loc[j, "Name"]] = clean(text_json[z].get("text")).replace(
                                        df.loc[j, "Ignore"], "")
                                    visited[df.loc[j, "Name"]] = True
                                    break
                        # if df.loc[j, "Name"] == "NCB":
                        #     # print(result["NCB"])
                        #     if not result[df.loc[j, "Name"]].isnumeric():
                        #         result["NCB"] = ""
                        if len(result[df.loc[j, "Name"]].strip('. / | ,')) == 0 and not df.loc[j, "Name"] == "RTO":
                            visited[df.loc[j, "Name"]] = False
                            continue
                        i = i - 1
                        if (result["RTO"] == "" or result["RTO"] == "No." or result["RTO"] == "No" or len(result["RTO"].split())>2) and df.loc[j, "Name"] == "RTO":
                            i = i + 1
                            x = xcx
                            kj = i
                            # print("kaise " + text_json[i].get("text"))
                            for z in range(i - 10, len(text_json)):
                                # print("dekho "+text_json[z].get("text"))
                                # print(df.loc[j, "Key"])
                                # print("options " + text_json[z].get("text"))
                                if kj == z:
                                    # print("hgf " + text_json[z].get("text"))
                                    continue
                                # print("tyu " + text_json[z].get("text"))
                                if text_json[z].get("text").__contains__("Insure") or text_json[z].get("text").__contains__(result["Insured Name"]):
                                    continue
                                # print("xzc " + text_json[z].get("text"))
                                if text_json[z].get("text") == "Correspondence" or text_json[z].get("text").__contains__("Corr"):
                                    continue
                                # print(text_json[z].get("text"))
                                # print(x)
                                # print(text_json[z].get("boundingBox"))
                                if diff(x, text_json[z].get("boundingBox"), j, df):
                                    # print("problem")
                                    result[df.loc[j, "Name"]] = str(clean(text_json[z].get("text"))).replace(
                                        df.loc[j, "Ignore"], "").replace(df.loc[j, "Breaking Condition"], "").strip()
                                    visited[df.loc[j, "Name"]] = True
                                    break
                                if df.loc[j, "Breaking Condition"] in text_json[z].get("text"):
                                    break
                        break
                    elif df.loc[j, "Value Navigation"] == 'INIT':
                        x = text_json[i].get("text")
                        x = x.split(df.loc[j, "Key"])[1].strip()
                        # print(df.loc[j, "Key"])
                        # print(x)
                        result[df.loc[j, "Name"]] = x.replace(df.loc[j, "Ignore"], "").strip().split(df.loc[j, "Breaking Condition"])[0]
                        visited[df.loc[j, "Name"]] = True
                        # print(result["Cubic Capacity"].replace("CC)", ""))
                        if df.loc[j, "Key"] == "Cubic Capacity":
                            result["Cubic Capacity"] = result["Cubic Capacity"].replace("Watts", "").replace("Wats", "").replace("CC", "").strip(" / . , ) ")
                        if df.loc[j, "Name"] == "Policy Issuance Date":
                            if result["Policy Issuance Date"].replace(" ", "").isalpha():
                                result["Policy Issuance Date"] = ""
                        if df.loc[j, "Name"] == "RTO":
                            if result["RTO"].strip() == "O" or result["RTO"] == "No.":
                                result["RTO"] = ""
                        if len(result[df.loc[j, "Name"]].strip('. , / |')) == 0:
                            visited[df.loc[j, "Name"]] = False
                            continue
                        if "Issuance Date" in text_json[i].get("text"):
                            continue
                        i = i - 1
                        break
                    elif df.loc[j, "Value Navigation"] == 'BML':
                        try:
                            result[df.loc[j, "Name"]] = ""
                            x = text_json[i].get("boundingBox")
                            xc = i + 1
                            # if df.loc[j, "Name"] == "Chassis No":
                            #     print(text_json[xc].get("text"))
                            # print(df.loc[j, "Key"])
                            while df.loc[j, "Breaking Condition"] not in text_json[xc].get("text"):
                                # print("yes" + text_json[xc].get("text"))
                                # print(x)
                                # print(text_json[xc].get("boundingBox"))
                                # if df.loc[j, "Name"] == "Chassis No":
                                #     print(text_json[xc].get("text"))
                                if diff(x, text_json[xc].get("boundingBox"), j, df):
                                    # print("no" + text_json[xc].get("text"))
                                    if df.loc[j, "Name"] == "Chassis No":
                                        if result["Engine No"] == text_json[xc].get("text"):
                                            xc = xc + 1
                                            continue
                                    if df.loc[j, "Name"] == "Model":
                                        p = text_json[xc].get("text")
                                        if p.__contains__("Mig") or p.__contains__("Engine") or p.__contains__("Chassis") or p.__contains__("License") or p.__contains__("Carrying"):
                                            xc = xc + 1
                                            continue
                                        # print("all    " + text_json[xc].get("text"))
                                    result[df.loc[j, "Name"]] = result[df.loc[j, "Name"]] + "," + text_json[xc].get("text").replace(df.loc[j,"Ignore"], "").replace(df.loc[j, "Breaking Condition"], "")
                                    x = text_json[xc].get("boundingBox")
                                    visited[df.loc[j, "Name"]] = True
                                xc = xc + 1
                        except:
                            print("Error2 " + df.loc[j, "Name"] + " " + df.loc[j, "Key"])
                            # print("Error2")# + df.loc[j, "Name"]+ " " + result[df.loc[j, "Name"]])
                        i = i - 1
                        break
                    elif df.loc[j, "Value Navigation"] == 'TBML':
                        result[df.loc[j, "Name"]] = ""
                        x = text_json[i].get("boundingBox")
                        xc = i
                        while df.loc[j, "Breaking Condition"] not in text_json[xc].get("text"):
                            if diff(x, text_json[xc].get("boundingBox"), j, df):
                                result[df.loc[j, "Name"]] = result[df.loc[j, "Name"]] + " " + text_json[xc].get("text").replace(df.loc[j,"Ignore"], "").replace(df.loc[j, "Breaking Condition"], "")
                                x = text_json[xc].get("boundingBox")
                                visited[df.loc[j, "Name"]] = True
                            xc = xc + 1
                        i = i - 1
                        break
                    elif df.loc[j, "Value Navigation"] == "TABLE":
                        col = df.loc[j, "Cols"].split(',')
                        xc = i + 1
                        x = text_json[xc].get("boundingBox")
                        xz = 0
                        while df.loc[j, "Breaking Condition"] not in text_json[xc].get("text"):
                            # print(text_json[xc].get("text"))
                            if diff(x, text_json[xc].get("boundingBox"), j, df):
                                result[col[xz]] = clean(text_json[xc].get("text")).replace(df.loc[j,"Ignore"], "")
                                x = text_json[xc].get("boundingBox")
                                xz = xz + 1
                                visited[df.loc[j, "Name"]] = True
                            xc = xc + 1
                        i = i - 1
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
                                    result[col[xz]] = clean(text_json[xc].get("text")).replace(df.loc[j,"Ignore"], "")
                                    xz = xz + 1
                                else:
                                    a = a.replace("|", "").replace("  ", " ").split(' ')
                                    for iv in range(len(a)):
                                        result[col[xz]] = a[iv].replace(df.loc[j,"Ignore"], "")
                                        xz = xz + 1
                                x = text_json[xc].get("boundingBox")
                                visited[df.loc[j, "Name"]] = True
                            xc = xc + 1
                        i = i - 1
                        break
                    elif df.loc[j, "Value Navigation"] == 'RBML':
                        x = text_json[i].get("boundingBox")
                        # print((text_json[i].get('text')))
                        xc = i + 1
                        coor = text_json[xc].get("boundingBox")
                        # print((text_json[xc].get('text')))
                        # print(df.loc[j,"Key"])
                        try:
                            while abs(x[1]-coor[1]) > df.loc[j, "x1"] or ((not text_json[xc].get("text").strip()[0] == 'F') and df.loc[j,"Name"] == "Period of Insurance"):
                                if df.loc[j,"Name"] == "Only Address":
                                    if text_json[xc].get("text") == "RTO" or text_json[xc].get("text") == "RT":
                                        # print("yesssss")
                                        xc = xc + 1
                                        continue
                                xc = xc + 1
                                if df.loc[j,"Name"] == "Only Address":
                                    if text_json[xc].get("text") == "RTO" or text_json[xc].get("text") == "RT":
                                        xc = xc + 1
                                        continue
                                coor = text_json[xc].get("boundingBox")
                            result[df.loc[j, "Name"]] = text_json[xc].get("text").replace(df.loc[j,"Ignore"], "")
                            x = coor
                            xc = xc + 1
                            coor = text_json[xc].get("boundingBox")
                            # print(text_json[xc].get("text"))
                            while df.loc[j, "Breaking Condition"] not in text_json[xc].get("text"):
                                if df.loc[j,"Name"] == "Only Address":
                                    if text_json[xc].get("text").__contains__("RTO"):
                                        xc = xc + 1
                                        continue
                                if abs(x[0]-coor[0]) <= int(df.loc[j, "x0"]):
                                    result[df.loc[j, "Name"]] = result[df.loc[j, "Name"]] + " " + text_json[xc].get("text").replace(df.loc[j,"Ignore"], "")
                                    x = coor
                                xc = xc + 1
                                coor = text_json[xc].get("boundingBox")
                        except:
                            print("Error")
                            xc = i - 10
                            coor = text_json[xc].get("boundingBox")
                            # print((text_json[xc].get('text')))
                            # print(df.loc[j,"Key"])
                            try:
                                while abs(x[1] - coor[1]) > df.loc[j, "x1"] or (
                                        (not text_json[xc].get("text").strip()[0] == 'F') and df.loc[j, "Name"] == "Period of Insurance"):
                                    xc = xc + 1
                                    # print(text_json[xc].get("text"))
                                    coor = text_json[xc].get("boundingBox")
                                result[df.loc[j, "Name"]] = text_json[xc].get("text").replace(df.loc[j, "Ignore"], "")
                                x = coor
                                xc = xc + 1
                                coor = text_json[xc].get("boundingBox")
                                while df.loc[j, "Breaking Condition"] not in text_json[xc].get("text"):
                                    if abs(x[0] - coor[0]) <= int(df.loc[j, "x0"]):
                                        result[df.loc[j, "Name"]] = result[df.loc[j, "Name"]] + " " + text_json[xc].get(
                                            "text").replace(df.loc[j, "Ignore"], "")
                                        x = coor
                                    xc = xc + 1
                                    coor = text_json[xc].get("boundingBox")
                            except:
                                print("Error 101")
                        i = i - 1
                    elif df.loc[j, "Value Navigation"] == "B":
                        x = text_json[i].get("boundingBox")
                        for z in range(i + 1, len(text_json)):
                            if df.loc[j, "Name"] == "Chassis No" and text_json[z].get("text") == result["Engine No"]:
                                continue
                            if df.loc[j, "Name"] == "Engine No" and text_json[z].get("text") == "Chassis No":
                                continue
                            if df.loc[j, "Name"] == "Mfg. Year" and not text_json[z].get("text").isnumeric():
                                continue
                            elif df.loc[j, "Name"] == "Mfg. Year":
                                xq = int(text_json[z].get("text"))
                                if xq < 1980 or xq > 2100:
                                    continue
                            if diff(x, text_json[z].get("boundingBox"), j, df):
                                # print(df.loc[j,"x0"])
                                result[df.loc[j, "Name"]] = clean(text_json[z].get("text")).replace(df.loc[j,"Ignore"], "").replace(df.loc[j, "Breaking Condition"], "")
                                visited[df.loc[j, "Name"]] = True
                                i = i - 1
                                break
                            if df.loc[j, "Breaking Condition"] in text_json[z].get("text"):
                                break
                        # elif df.loc[j, "Value Navigation"] == "ADDRESS":
            except:
                print("Interpretation")

    return result
