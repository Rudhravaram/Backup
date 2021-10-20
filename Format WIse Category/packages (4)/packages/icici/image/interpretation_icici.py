import requests
import time
import urllib.parse
import urllib.error
import pandas as pd
import re
import string
import csv
from openpyxl import load_workbook
# from pdf2image import convert_from_path
import copy


def clean(s):
    return s.strip(' " : .  - * # ')


def diff(x, y, z, df):
    xx = ["x0", "x1",  "x6", "x7", "x2", "x3", "x4", "x5"]
    for xc in xx:
        if not df.loc[z, xc] == "None":
            if abs(x[int(xc[-1])] - y[int(xc[-1])]) > df.loc[z, xc]:
                return False
    return True


def check_icici(text_json, sheet1, bck):  # , state, bck

    # st = state
    # print(st)

    data = pd.read_excel(r'packages/icici/image/directives_icici.xlsx', sheet_name=sheet1)
    df = pd.DataFrame(data, columns=['Key', 'Available', 'Value Navigation', 'Front Breaking', 'Reverse Breaking', 'Name',
                                     'x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'Cols', 'Ignore', "REGEX", "Not IN", "INIT2", "Counters", "Name2"])

    result = {}
    for j in range(df.shape[0]):
        if df.loc[j, "Available"] == 'Y':
            result[df.loc[j, "Name"]] = ""

    counters = {}
    visited = {}

    # try:
    #     result["Vehicle Class"] = ""
    #     for i in range(len(text_json)):
    #         s = text_json[i].get("text")
    #         if "LMV" in s:
    #             result["Vehicle Class"] = result["Vehicle Class"] + ", " + "LMV"
    #         if "MCWG" in s:
    #             result["Vehicle Class"] = result["Vehicle Class"] + ", " + "MCWG"
    #         if "TRANS" in s:
    #             result["Vehicle Class"] = result["Vehicle Class"] + ", " + "TRANS"
    # except:
    #     print("Prime Vehicle Class")

    for i in range(df.shape[0]):
        visited[df.loc[i, "Name"]] = False

    flag = 0
    # print(len(text_json))

    for i in range(len(text_json)):
        for j in range(df.shape[0]):
            if (df.loc[j, "Available"] == 'Y') and ((df.loc[j, "Key"] in text_json[i].get("text")) and (df.loc[j, "Not IN"] not in text_json[i].get("text"))) \
                    and ((visited[df.loc[j, "Name"]] == False) or (result[df.loc[j, "Name"]].strip(" ") == "")):
                # print(df.loc[j, "Key"])
                # print(text_json[i].get("text"))
                try:
                    if df.loc[j, "Value Navigation"] == 'R':
                        # print(df.loc[j, "Key"])
                        x = text_json[i].get("boundingBox")
                        for z in range(i+1, len(text_json)):
                            if df.loc[j, "Front Breaking"] in text_json[z].get("text"):
                                break
                            if text_json[z].get("text").strip(". : ,") == "":
                                continue
                            if diff(x, text_json[z].get("boundingBox"), j, df):
                                # print(df.loc[j, "x0"])
                                # print((text_json[z].get("text")))
                                # if df.loc[j, "Name"] == "LICENCE NO":
                                #     print("xyz")
                                #     print((text_json[z].get("text")))
                                result[df.loc[j, "Name"]] = str(clean(text_json[z].get("text"))).replace(df.loc[j, "Ignore"], "").strip()

                                ############
                                # if df.loc[j, "Name"] == "DL Number":
                                #     z = result["DL Number"]
                                #
                                #     if z.__contains__("an-2-0") or (not z[-2:].isdigit()) or z.__contains__("WEST BENGAL"):
                                #         visited[df.loc[j, "Name"]] = False
                                #         result["DL Number"] = ""
                                #         continue
                                # if df.loc[j, "Name"] == "Exp Date(T)":
                                #     z = result["Exp Date(T)"]
                                #     if z.upper().__contains__("ISSUING"):
                                #         visited[df.loc[j, "Name"]] = False
                                #         result["Exp Date(T)"] = ""
                                #         continue
                                # if df.loc[j, "Name"] == "DOI":
                                #     z = result["DOI"]
                                #     if not z[:2].isdigit():
                                #         visited[df.loc[j, "Name"]] = False
                                #         result["DOI"] = ""
                                #         continue
                                # if df.loc[j, "Name"] == "NAME":
                                #     z = result["NAME"]
                                #     # print(z)
                                #     # try:
                                #     # pattern2 = re.compile("(\d{2})[/.-](\d{2})[/.-](\d{4})$")
                                #     # x = pattern2.search(z)
                                #     # # print(x.group())
                                #     # if x.group() != "":
                                #     #     # print("yessss")
                                #     #     visited[df.loc[j, "Name"]] = False
                                #     #     result["NAME"] = ""
                                #     #     continue
                                #     # except:
                                #     if z.__contains__("DOI") or z.__contains__("NAME"):
                                #         visited[df.loc[j, "Name"]] = False
                                #         result["NAME"] = ""
                                #         continue
                                # if df.loc[j, "Name"] == "DOB":
                                #     z = result["DOB"]
                                #     z = clean(z)
                                #     if not z[:2].isdigit():
                                #         visited[df.loc[j, "Name"]] = False
                                #         result["DOB"] = ""
                                #         continue
                                #################################

                                if df.loc[j, "Name"] == "policy issuance date":
                                    z = result["policy issuance date"]
                                    z = z.replace("[UIN : --]", "")
                                    z = clean(z)
                                    if len(z) > 15:
                                        visited[df.loc[j, "Name"]] = False
                                        result["policy issuance date"] = ""
                                        continue
                                    if not z[-2:].isdigit():
                                        visited[df.loc[j, "Name"]] = False
                                        result["policy issuance date"] = ""
                                        continue
                                if df.loc[j, "Name"] == "model":
                                    z = result["model"]
                                    z = clean(z)
                                    if len(z) < 3:
                                        visited[df.loc[j, "Name"]] = False
                                        result["model"] = ""
                                        continue
                                    if z.__contains__("Body") or z.__contains__("Yr"):
                                        visited[df.loc[j, "Name"]] = False
                                        result["model"] = ""
                                        continue
                                if df.loc[j, "Name"] == "rto":
                                    z = result["rto"]
                                    z = clean(z)
                                    if z[-2:].isdigit() or z.__contains__("Hypothecated") or z.__contains__("FINANCE"):
                                        visited[df.loc[j, "Name"]] = False
                                        result["rto"] = ""
                                        continue
                                if df.loc[j, "Name"] == "policy no":
                                    z = result["policy no"]
                                    z = clean(z)
                                    if not z[-2:].isdigit():
                                        visited[df.loc[j, "Name"]] = False
                                        result["policy no"] = ""
                                        continue
                                if df.loc[j, "Name"] == "cc":
                                    z = result["cc"]
                                    z = clean(z)
                                    if len(z) < 2:
                                        visited[df.loc[j, "Name"]] = False
                                        result["cc"] = ""
                                        continue
                                    if not z[:2].isdigit() or z == result["mfg yr"]:
                                        visited[df.loc[j, "Name"]] = False
                                        result["cc"] = ""
                                        continue
                                if df.loc[j, "Name"] == "mfg yr":
                                    z = result["mfg yr"]
                                    z = clean(z)
                                    if len(z) < 4:
                                        visited[df.loc[j, "Name"]] = False
                                        result["mfg yr"] = ""
                                        continue
                                    if (not z[:2].isdigit()) or int(z) > 2050:
                                        visited[df.loc[j, "Name"]] = False
                                        result["mfg yr"] = ""
                                        continue
                                if df.loc[j, "Name"] == "chassis no":
                                    z = result["chassis no"]
                                    z = clean(z)
                                    if len(z) < 3:
                                        visited[df.loc[j, "Name"]] = False
                                        result["chassis no"] = ""
                                        continue
                                    if z.__contains__("Capacity"):
                                        visited[df.loc[j, "Name"]] = False
                                        result["chassis no"] = ""
                                        continue
                                if df.loc[j, "Name"] == "engine no":
                                    z = result["engine no"]
                                    z = clean(z)
                                    if len(z) < 3:
                                        visited[df.loc[j, "Name"]] = False
                                        result["engine no"] = ""
                                        continue
                                    if (not z[-2:].isdigit()): # and (not z[-2:] == "XX")
                                        visited[df.loc[j, "Name"]] = False
                                        result["engine no"] = ""
                                        continue
                                if df.loc[j, "Name"] == "nominee name":
                                    z = result["nominee name"]
                                    z = clean(z)
                                    if z.__contains__("Relationship") or z.__contains__("@") or z.__contains__("Spouse"):
                                        visited[df.loc[j, "Name"]] = False
                                        result["nominee name"] = ""
                                        continue
                                if df.loc[j, "Name"] == "nominee relation":
                                    z = result["nominee relation"]
                                    z = clean(z)
                                    if z.__contains__("Age") or z.__contains__("Ace") or z.__contains__("Ape") or z == result["nominee name"]:
                                        visited[df.loc[j, "Name"]] = False
                                        result["nominee relation"] = ""
                                        continue
                                if df.loc[j, "Name"] == "email":
                                    z = result["email"]
                                    z = clean(z)
                                    if z.__contains__("GMAIL"):
                                        visited[df.loc[j, "Name"]] = True
                                        result["email"] = z
                                        break
                                    if z.isnumeric() or z.__contains__("Nominee") or (not z.__contains__("@")):
                                        visited[df.loc[j, "Name"]] = False
                                        result["email"] = ""
                                        continue
                                if df.loc[j, "Name"] == "mobile":
                                    z = result["mobile"]
                                    z = clean(z)
                                    if not z[-2:].isdigit():
                                        visited[df.loc[j, "Name"]] = False
                                        result["mobile"] = ""
                                        continue
                                if df.loc[j, "Name"] == "ncb":
                                    z = result["ncb"]
                                    z = clean(z)
                                    if not z.isnumeric():
                                        visited[df.loc[j, "Name"]] = False
                                        result["ncb"] = ""
                                        continue
                                if df.loc[j, "Name"] == "hypothecation":
                                    z = result["hypothecation"]
                                    z = clean(z)
                                    if z == result["rto"] or z.isnumeric() or z.__contains__("Category") or z.__contains__("Number") or z.__contains__("Invoice"):
                                        visited[df.loc[j, "Name"]] = False
                                        result["hypothecation"] = ""
                                        continue
                                if df.loc[j, "Name"] == "insured name":
                                    z = result["insured name"]
                                    z = clean(z)
                                    if len(z) > 33:
                                        visited[df.loc[j, "Name"]] = False
                                        result["insured name"] = ""
                                        continue
                                    if z.__contains__("ddress") or z.__contains__("nsured") or z.__contains__("INDIVIDUAL") or z.__contains__("aye Vaade"):
                                        visited[df.loc[j, "Name"]] = False
                                        result["insured name"] = ""
                                        continue

                            if len(result[df.loc[j, "Name"]]) == 0:
                                # print(df.loc[j, "Key"])
                                # print(text_json[z].get("text"))
                                continue
                            else:
                                visited[df.loc[j, "Name"]] = True
                                break

                        if df.loc[j, "Name"] == "nominee name" and visited["nominee name"] == False:
                            # print("yesss")
                            cvb = i - 5
                            for z in range(i - 1, cvb, -1):
                                if clean(text_json[z].get("text"))[:2].isdigit() or clean(text_json[z].get("text")).__contains__("@") or clean(text_json[z].get("text")).__contains__("mail Address"):
                                    continue
                                if diff(x, text_json[z].get("boundingBox"), j, df):
                                    # print(text_json[z].get("text"))
                                    result[df.loc[j, "Name"]] = clean(text_json[z].get("text")).replace(df.loc[j, "Ignore"], "")
                                    visited[df.loc[j, "Name"]] = True
                                    break
                        if df.loc[j, "Name"] == "nominee relation" and visited["nominee relation"] == False:
                            # print("yesss")
                            cvb = i - 5
                            for z in range(i - 1, cvb, -1):
                                if clean(text_json[z].get("text")).__contains__("Nominee") or clean(text_json[z].get("text")) == result["nominee name"]:
                                    continue
                                if diff(x, text_json[z].get("boundingBox"), j, df):
                                    # print(text_json[z].get("text"))
                                    result[df.loc[j, "Name"]] = clean(text_json[z].get("text")).replace(df.loc[j, "Ignore"], "")
                                    visited[df.loc[j, "Name"]] = True
                                    break
                        if df.loc[j, "Name"] == "insured name" and visited["insured name"] == False:
                            # print("yesss")
                            cvb = i - 5
                            for z in range(i - 1, cvb, -1):
                                # if clean(text_json[z].get("text"))[:2].isdigit() or z.__contains__("@"):
                                #     continue
                                if diff(x, text_json[z].get("boundingBox"), j, df):
                                    # print(text_json[z].get("text"))
                                    result[df.loc[j, "Name"]] = clean(text_json[z].get("text")).replace(df.loc[j, "Ignore"], "")
                                    visited[df.loc[j, "Name"]] = True
                                    break
                        if df.loc[j, "Name"] == "rto" and visited["rto"] == False:
                            # print("yesss")
                            cvb = i - 5
                            for z in range(i - 1, cvb, -1):
                                # if clean(text_json[z].get("text"))[:2].isdigit() or z.__contains__("@"):
                                #     continue
                                if diff(x, text_json[z].get("boundingBox"), j, df):
                                    # print(text_json[z].get("text"))
                                    result[df.loc[j, "Name"]] = clean(text_json[z].get("text")).replace(df.loc[j, "Ignore"], "")
                                    visited[df.loc[j, "Name"]] = True
                                    break
                        if df.loc[j, "Name"] == "mobile" and visited["mobile"] == False:
                            # print("yesss")
                            cvb = i - 7
                            for z in range(i - 1, cvb, -1):
                                # print(text_json[z].get("text"))
                                if clean(text_json[z].get("text")).__contains__("E-Policy"):
                                    continue
                                if diff(x, text_json[z].get("boundingBox"), j, df):
                                    # print(text_json[z].get("text"))
                                    result[df.loc[j, "Name"]] = clean(text_json[z].get("text")).replace(df.loc[j, "Ignore"], "")
                                    visited[df.loc[j, "Name"]] = True
                                    break
                        if df.loc[j, "Name"] == "policy issuance date" and visited["policy issuance date"] == False:
                            # print("yesss")
                            cvb = i - 5
                            for z in range(i - 1, cvb, -1):
                                if not clean(text_json[z].get("text"))[-2:].isdigit():
                                    continue
                                if diff(x, text_json[z].get("boundingBox"), j, df):
                                    # print(text_json[z].get("text"))
                                    result[df.loc[j, "Name"]] = clean(text_json[z].get("text")).replace(df.loc[j, "Ignore"], "")
                                    visited[df.loc[j, "Name"]] = True
                                    break
                        if df.loc[j, "Name"] == "email" and visited["email"] == False:
                            # print("yesss")
                            cvb = i - 5
                            for z in range(i - 1, cvb, -1):
                                # if not clean(text_json[z].get("text"))[-2:].isdigit():
                                #     continue
                                if diff(x, text_json[z].get("boundingBox"), j, df):
                                    # print(text_json[z].get("text"))
                                    result[df.loc[j, "Name"]] = clean(text_json[z].get("text")).replace(df.loc[j, "Ignore"], "")
                                    visited[df.loc[j, "Name"]] = True
                                    break

                    elif df.loc[j, "Value Navigation"] == 'INIT':
                        # print(df.loc[j, "Key"])
                        x = text_json[i].get("text")
                        x = x.split(df.loc[j, "Key"])[1].strip()
                        data = x.replace(df.loc[j, "Ignore"], "").strip(" - ? ; . , ").split(df.loc[j, "Front Breaking"])[0]

                        z = x.replace(data, "")
                        init2 = z.split(df.loc[j, "INIT2"]) #[1].strip()
                        # print(init2)
                        if len(init2) > 1:
                            data2 = init2[1].strip()
                            result[df.loc[j, "Name2"]] = clean(data2)

                        result[df.loc[j, "Name"]] = clean(data)

                        if df.loc[j, "Name"] == "mobile":
                            z = result["mobile"]
                            z = clean(z)
                            if len(z) < 4:
                                visited[df.loc[j, "Name"]] = False
                                result["mobile"] = ""
                                continue

                        # print(result["Engine No"])

                        if len(result[df.loc[j, "Name"]]) == 0:
                            # print(df.loc[j, "Key"])
                            continue
                        else:
                            visited[df.loc[j, "Name"]] = True
                            break

                    elif df.loc[j, "Value Navigation"] == 'BML':
                        try:
                            result[df.loc[j, "Name"]] = ""
                            x = text_json[i].get("boundingBox")
                            xc = i + 1
                            count = 0
                            counter = 0
                            # print(df.loc[j, "Key"])
                            while df.loc[j, "Front Breaking"] not in text_json[xc].get("text"):
                                if diff(x, text_json[xc].get("boundingBox"), j, df):
                                    count = count + 1
                                    # if df.loc[j, "Key"] == "Addr":
                                    #     print(text_json[xc].get("text"))
                                    if df.loc[j, "Name"] == "Address":
                                        if text_json[xc].get("text").__contains__("Period of") or text_json[xc].get("text").__contains__("Telephone") or text_json[xc].get("text").__contains__("E-Policy"):
                                            counter = counter + 1
                                            xc = xc + 1
                                            continue
                                        if text_json[xc].get("text").isnumeric() and len(text_json[xc].get("text")) != 6:
                                            counter = counter + 1
                                            xc = xc + 1
                                            continue
                                    if df.loc[j, "Name"] == "Period of Insurance":
                                        if text_json[xc].get("text").__contains__("Policy"):
                                            xc = xc + 1
                                            continue
                                    if df.loc[j, "Name"] == "model":
                                        if text_json[xc].get("text").__contains__("Type"):
                                            xc = xc + 1
                                            continue
                                    data = text_json[xc].get("text")
                                    result[df.loc[j, "Name"]] = result[df.loc[j, "Name"]] + ";" + clean(data.replace(df.loc[j, "Ignore"], ""))
                                    x = text_json[xc].get("boundingBox")
                                xc = xc + 1
                            if not result["Period of Insurance"].__contains__("to") and result["Period of Insurance"] != "":
                                cvb = i - 5
                                p = ""
                                for z in range(i - 1, cvb, -1):
                                    # if not clean(text_json[z].get("text"))[-2:].isdigit():
                                    #     continue
                                    if diff(x, text_json[z].get("boundingBox"), j, df):
                                        if text_json[z].get("text").__contains__("to"):
                                            # print(text_json[z].get("text"))
                                            result["Period of Insurance"] = clean(text_json[z].get("text")).replace(
                                                df.loc[j, "Ignore"], "") + result["Period of Insurance"]
                                            # visited[df.loc[j, "Name"]] = True
                                            break

                            if df.loc[j, "Name"] == "Address":
                                # print(count - counter)
                                # print(result["Address"])
                                count = count - counter
                                if count == 1:  # or count == 2
                                    cvb = i - 5
                                    p = ""
                                    for z in range(i - 1, cvb, -1):
                                        if clean(text_json[z].get("text")).__contains__("Insurance"):
                                            continue
                                        if diff(x, text_json[z].get("boundingBox"), j, df):
                                            # print(text_json[z].get("text"))
                                            result["Address"] = clean(text_json[z].get("text")) + result["Address"]
                                            # visited[df.loc[j, "Name"]] = True
                                            break

                            visited[df.loc[j, "Name"]] = True
                        except:
                            # + df.loc[j, "Name"]+ " " + result[df.loc[j, "Name"]])
                            print("Error BML")
                        # print(result["Address"])
                        break

                    elif df.loc[j, "Value Navigation"] == 'TBML':
                        # print(df.loc[j, "Key"] + "$$$$$")
                        try:
                            result[df.loc[j, "Name"]] = ""
                            x = text_json[i].get("boundingBox")
                            xc = i

                            while df.loc[j, "Front Breaking"] not in text_json[xc].get("text"):

                                if diff(x, text_json[xc].get("boundingBox"), j, df):
                                    # print(text_json[xc].get("text"))

                                    result[df.loc[j, "Name"]] = result[df.loc[j, "Name"]] + " " + clean(text_json[xc].get("text").replace(df.loc[j, "Ignore"], "").split(df.loc[j, "Key"])[-1])

                                    x = text_json[xc].get("boundingBox")

                                    # visited[df.loc[j, "Name"]] = True
                                xc = xc + 1

                            if len(result[df.loc[j, "Name"]]) == 0:
                                # print(df.loc[j, "Key"])
                                continue
                            else:
                                visited[df.loc[j, "Name"]] = True
                                break
                        except:
                            print("Error TBML")
                        break


                except:
                    print("interpretation issue")

    result1 = copy.deepcopy(result)
    if bck == 1:
        for key in result1.keys():
            if result1[key] == "":
                del result[key]

    return result