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
    return s.strip(' " : .  - * # ')


def diff(x, y, z, df):
    xx = ["x0", "x1",  "x6", "x7", "x2", "x3", "x4", "x5"]
    #yy = []
    # print(df.loc[z, "x0"])
    for xc in xx:
        if not df.loc[z, xc] == "None":
            if abs(x[int(xc[-1])] - y[int(xc[-1])]) > df.loc[z, xc]:
                return False
    # for yc in yy:
    #     if not df.loc[z, yc] == "None":
    #         if abs(x[int(yc[-1])]) - abs(y[int(yc[-1])]) < df.loc[z, yc]:
    #             return False
    return True


def check_rc(text_json, sheet1, state, bck):


    st = state
    print(st)

    data = pd.read_excel(r'packages/rc/Directives_RC.xlsx', sheet_name=sheet1)
    df = pd.DataFrame(data,
                      columns=['Key', 'Available', 'Value Navigation', 'Breaking Condition', 'Name', 'x0', 'x1', 'x2', 'x3', 'x4',
                               'x5', 'x6', 'x7', 'Cols', 'Ignore', "REGEX"])

    result = {}
    for j in range(df.shape[0]):
        if df.loc[j, "Available"] == 'Y':
            result[df.loc[j, "Name"]] = ""

    counters = {}
    visited = {}

    for i in range(df.shape[0]):
        visited[df.loc[i, "Name"]] = False
    flag = 0
    # print(len(text_json))
    for i in range(len(text_json)):
        for j in range(df.shape[0]):

            if (df.loc[j, "Available"] == 'Y') and (df.loc[j, "Key"] in text_json[i].get("text")) and (
                    (visited[df.loc[j, "Name"]] == False) or (result[df.loc[j, "Name"]].strip(" ") == "")):
                try:
                    if df.loc[j, "Value Navigation"] == 'R':
                        # print(df.loc[j, "Key"])
                        x = text_json[i].get("boundingBox")
                        for z in range(i + 1, len(text_json)):
                            if df.loc[j, "Breaking Condition"] in text_json[z].get("text"):
                                break
                            if text_json[z].get("text").strip(". : ,") == "":
                                continue
                            if df.loc[j, "Key"] == "CC":  # only for cc
                                if text_json[z].get("text").__contains__("/") or text_json[z].get("text").rstrip(
                                        ":00") == "":
                                    continue
                            if df.loc[j, "Key"] == "Name":  # only for Name
                                if text_json[z].get("text").__contains__("-") or text_json[z].get("text").__contains__(
                                        "S/D/W of") or text_json[z].get("text").__contains__("S/DAW of"):
                                    continue
                            if df.loc[j, "Key"] == "Manufacturing Dt":
                                if text_json[z].get("text").__contains__("Cubic Capacity"):
                                    continue
                            if df.loc[j, "Key"] == "Manufacturer":
                                if text_json[z].get("text").__contains__("SALOON"):
                                    continue
                            if df.loc[j, "Key"] == "Manufacture by":
                                if text_json[z].get("text").__contains__("Cubic Capacity") or text_json[z].get(
                                        "text").__contains__("Wheel Base") or text_json[z].get("text").__contains__("Fuel"):
                                    continue
                            if df.loc[j, "Key"] == "Registration No":
                                if text_json[z].get("text").__contains__("Registration Date"):
                                    continue
                            if df.loc[j, "Key"] == "Registration Date":
                                if text_json[z].get("text").__contains__("Weight") or text_json[z].get(
                                        "text").__contains__(
                                        "Manufacture by"):
                                    continue
                            if df.loc[j, "Key"] == "Engine No":
                                if text_json[z].get("text").__contains__("Standing Capacity") or text_json[z].get(
                                        "text").__contains__("Model NO"):
                                    continue

                            if df.loc[j, "Key"] == "CERTIFICATE OF REGISTRATION":  # only for Name
                                if text_json[z].get("text").__contains__("104%"):
                                    continue

                            if diff(x, text_json[z].get("boundingBox"), j, df):
                                # print(df.loc[j, "x0"])
                                # print((text_json[z].get("text")))
                                # if df.loc[j, "Name"] == "Registration Number":
                                #     print("xyz")
                                #     print((text_json[z].get("text")))
                                result[df.loc[j, "Name"]] = str(clean(text_json[z].get("text"))).replace(
                                    df.loc[j, "Ignore"], "").strip()

                                if df.loc[j, "Name"] == "Registration Number":
                                    z = result["Registration Number"]
                                    z = z.split("GOVERNMENT")[0]
                                    z = z.split("Unladen")[0]
                                    z = z.split("E. NO")[0]
                                    z = z.split("E NO")[0]
                                    z = z.replace("(", "").replace(")", "").replace("/", "").replace("-", "")
                                    z = z.replace(" ", "")
                                    z = clean(z)
                                    # print(z)
                                    # print(z[-5:-2])
                                    if len(z) < 5 or len(z) > 14:
                                        visited[df.loc[j, "Name"]] = False
                                        result["Registration Number"] = ""
                                        continue
                                    if z[-1] == "R":
                                        visited[df.loc[j, "Name"]] = False
                                        result["Registration Number"] = ""
                                        continue
                                    if z[-1] == "A":
                                        result["Registration Number"] = z[:-1]
                                    if (not z[0].isalpha()) or (not z[-3:-2].isdigit()) or z.upper().__contains__(
                                            "CERTIFICATE OF REGISTRATION") or z.upper().__contains__("MOTOR") or \
                                            z.upper().__contains__("DATE") or z.upper().__contains__("GOVERNMENT") or \
                                            z.upper().__contains__("THANSMMINT") or z.upper().__contains__(
                                        "TRANSPORT") or z.upper().__contains__("FORM"):
                                        visited[df.loc[j, "Name"]] = False
                                        result["Registration Number"] = ""
                                        continue

                                if df.loc[j, "Name"] == "Mfg Yr":
                                    if not 12 > len(result["Mfg Yr"]) > 3:
                                        visited[df.loc[j, "Name"]] = False
                                        result["Mfg Yr"] = ""
                                        continue
                                    if not result["Mfg Yr"][-2:].isdigit():
                                        visited[df.loc[j, "Name"]] = False
                                        result["Mfg Yr"] = ""
                                        continue

                                if df.loc[j, "Name"] == "Date of Registration":
                                    z = result["Date of Registration"]
                                    z = z.split("Class")[0]
                                    z = z.split("CLASS")[0]
                                    z = z.replace("D", "0").replace("y", "9").replace("C", "0")
                                    z = z.replace("(", "").replace(")", "")
                                    z = z.replace(" ", "")
                                    z = clean(z)
                                    # print(z)
                                    if len(z) < 8:
                                        visited[df.loc[j, "Name"]] = False
                                        result["Date of Registration"] = ""
                                        continue
                                    if (not z[-2:].replace("-", "").isdigit()) or (not z[0].isdigit()):
                                        visited[df.loc[j, "Name"]] = False
                                        result["Date of Registration"] = ""
                                        continue

                                if df.loc[j, "Name"] == "Engine No":
                                    z = result["Engine No"]
                                    # z = z.replace(" ", "")
                                    z = z.replace("(", "").replace(")", "").replace(".", "")
                                    z = clean(z)
                                    if len(z) < 5:
                                        visited[df.loc[j, "Name"]] = False
                                        result["Engine No"] = ""
                                        continue
                                    if (not z[-4].replace("S", "5").replace("Y", "1").isdigit()) or z == result[
                                        "Chassis No"] or z.isalpha():  # or z[0] == "M"
                                        visited[df.loc[j, "Name"]] = False
                                        result["Engine No"] = ""
                                        continue

                                if df.loc[j, "Name"] == "Chassis No":
                                    z = result["Chassis No"]
                                    z = z.replace(" ", "")
                                    z = z.replace("(", "").replace(")", "")
                                    z = z.replace(" ", "").replace("~", "") # .replace("-", "")
                                    z = z.split("REGD.DT")[0]
                                    z = clean(z)
                                    # print(z)
                                    if len(z) < 8:
                                        visited[df.loc[j, "Name"]] = False
                                        result["Chassis No"] = ""
                                        continue
                                    if z[1] == "T" or z[8] == "-":
                                        visited[df.loc[j, "Name"]] = False
                                        result["Chassis No"] = ""
                                        continue
                                    if (not z[-4].isdigit()) or z.upper().__contains__("NO") or z.upper().__contains__(
                                            "CERTIFICATE") or \
                                            z.upper().__contains__("ENGINE") or z.__contains__("Ju") or z.__contains__("to"):  # or not z[0].isalpha()
                                        # print("YYY")
                                        visited[df.loc[j, "Name"]] = False
                                        result["Chassis No"] = ""
                                        continue

                                if df.loc[j, "Name"] == "Seating Capacity":
                                    z = result["Seating Capacity"]
                                    # print(z)
                                    z = z.replace("!", "2")
                                    z = z.replace("(", "").replace(")", "").replace("'", "")
                                    z = z.split("including")[0]
                                    z = z.split("Including")[0]
                                    z = z.split("/")[0]
                                    z = z.split("No Of Cyc")[0]
                                    z = z.split("No. Of Cyc")[0]
                                    z = z.split("Owner")[0]
                                    z = z.replace("a", "").replace("s", "").replace("S", "5")
                                    z = clean(z)
                                    # print(z)
                                    # print(len(z))
                                    if len(z) > 3 or len(z) == 0:
                                        visited[df.loc[j, "Name"]] = False
                                        result["Seating Capacity"] = ""
                                        continue
                                    if (not z[-1].isdigit()) or z.__contains__("NO Of") or z.upper().__contains__(
                                            "OWNER"): # or z == result["No of Cylinders"]
                                        visited[df.loc[j, "Name"]] = False
                                        result["Seating Capacity"] = ""
                                        continue
                                    if "No of Cylinders" in result.keys():
                                        if result["No of Cylinders"] == z:
                                            visited[df.loc[j, "Name"]] = False
                                            result["Seating Capacity"] = ""
                                            continue

                                if df.loc[j, "Name"] == "Cubic Capacity":
                                    z = result["Cubic Capacity"]
                                    # print(z)
                                    z = z.replace("CC", "").replace(".", "").replace("GC", "")
                                    z = z.replace("(", "").replace(")", "").replace("/", "7").replace("G", "6").replace(
                                        "D", "0").replace("O", "0")
                                    z = clean(z)
                                    z = z.lstrip("0")
                                    if z.__contains__(".") or z.__contains__(","):
                                        z = z.rstrip("0")
                                        if z[-1] == "," or z[-1] == ".":
                                            z = z.rstrip(",")
                                            z = z.rstrip(".")
                                    z = z.replace(" ", "")
                                    if len(z) > 7 or (len(z) < 2 and int(z) < 20):
                                        visited[df.loc[j, "Name"]] = False
                                        result["Cubic Capacity"] = ""
                                        continue
                                    if (not z[-3:].isdigit()):
                                        visited[df.loc[j, "Name"]] = False
                                        result["Cubic Capacity"] = ""
                                        continue

                                if df.loc[j, "Name"] == "Gross Vehicle Weight":
                                    # print(result["Gross Vehicle Weight"])
                                    z = result["Gross Vehicle Weight"]
                                    z = z.replace("kgs", "").replace("kg", "").replace("Kgs", "").replace("Kgs",
                                                                                                          "").replace(
                                        "xg", "").replace("Mos", "").replace("J", "0").replace("U", "0")
                                    z = z.replace("(", "").replace(")", "").replace("D", "0").replace("O", "0").replace(
                                        "$", "1")
                                    p = z.split("/")
                                    z = p[-1]
                                    q = z.split(".")
                                    if len(q) == 2:
                                        if len(q[1]) == 4:
                                            z = q[1]
                                    z = clean(z)
                                    z = z.replace(" ", "").replace("r", "")
                                    # z = z.lstrip("0")
                                    # print(z)
                                    if len(z) > 6 or len(z) < 3 or len(p) > 2:
                                        # print("ffff")# len(z) > 5
                                        visited[df.loc[j, "Name"]] = False
                                        result["Gross Vehicle Weight"] = ""
                                        continue
                                    if (not z[:2].isdigit()):
                                        # print(z)
                                        visited[df.loc[j, "Name"]] = False
                                        result["Gross Vehicle Weight"] = ""
                                        continue

                                if df.loc[j, "Name"] == "Make":
                                    # print(result["Make"])
                                    z = result["Make"]
                                    z = z.replace("(", "").replace(")", "")
                                    z = clean(z)
                                    # print(z)
                                    if z[:2].isdigit() or z[-3:-1].isdigit() or z.__contains__(
                                            "COLOUR") or z.__contains__("OWNERNAME") or \
                                            z.__contains__("ROAD") or z.upper().__contains__(
                                        "ENGINE") or z.upper().__contains__("SILKY") or \
                                            z.upper().__contains__("HSRP") or z.upper().__contains__("MAXI CAB") or \
                                            z.upper().__contains__("TYPE OF BODY") or z.upper().__contains__(
                                        "1.M. V ICARY") or z.upper().__contains__("HIGHLINE") or \
                                            z.upper().__contains__("REGN") or z.__contains__("Rogn") or z.__contains__(
                                        "Regd") or z.__contains__("S/o") or z.__contains__("tyres") or z.__contains__("Bite of") \
                                            or z.__contains__("NASHIK") or z.__contains__("TAX") or z.__contains__("BANK"):
                                        visited[df.loc[j, "Name"]] = False
                                        result["Make"] = ""
                                        continue

                                if df.loc[j, "Name"] == "Model - Variant":
                                    z = result["Model - Variant"]
                                    z = z.replace("(", "").replace(")", "").replace("Wheel base", "").replace(
                                        "Month & Yr.of Mig", "").replace("Month & Yr. of Mig", "")
                                    z = clean(z)
                                    # print(z)
                                    # print(z[-5:-2].isdigit())
                                    if len(z) == 1:  # 5 and len(z.replace(" ", "")) != 4 and len(z.replace(" ", "")) != 3 and len(z.replace(" ", "")) != 2
                                        visited[df.loc[j, "Name"]] = False
                                        result["Model - Variant"] = ""
                                        continue
                                    if len(z) == 2 and z.isdigit():
                                        if int(z) < 20:
                                            visited[df.loc[j, "Name"]] = False
                                            result["Model - Variant"] = ""
                                            continue
                                    if len(z) == 4 and z[:2].isdigit():
                                        visited[df.loc[j, "Name"]] = False
                                        result["Model - Variant"] = ""
                                        continue
                                    if len(z) == 3 and z.isalpha():
                                        visited[df.loc[j, "Name"]] = False
                                        result["Model - Variant"] = ""
                                        continue

                                    #### problem with z[2] condition
                                    if z[2].isdigit():
                                        z = z.replace("1", "i", 1).replace("I", "i", 1)
                                        # print(z)
                                        if z[0] != "i" and z[0] != "X":
                                            visited[df.loc[j, "Name"]] = False
                                            result["Model - Variant"] = ""
                                            continue

                                    if z[-5:-2].isdigit() or z.upper().__contains__(
                                            "FORM") or z.__contains__("Manufacture") or \
                                            z.__contains__("Wheel-Base") or z.__contains__(
                                        "Wheel Base") or (z.__contains__("Owner Name") and not z.__contains__("MAHINDRA SCORPIO")) or z.__contains__("owner") or \
                                            z.__contains__("Hypothecated") or z.__contains__(
                                        "Month & Yr") or z.__contains__("Variant") \
                                            or z.__contains__("Tandem") or z.__contains__("STATE") or z.__contains__("REGD. DATE") or z.__contains__(
                                        "Articulated") or z.__contains__("Dealer") or z.__contains__("MOTORS [PI LTD") or z.__contains__("MULTISPECIALTY HOSPI") or z == result[
                                        "Make"]:              # (1616 XL) z[:2].isdigit() or z.__contains__("HR"), z[-2:], z[4], z[3]
                                        visited[df.loc[j, "Name"]] = False
                                        result["Model - Variant"] = ""
                                        continue

                                if df.loc[j, "Name"] == "FINANCIER_NAME":
                                    z = result["FINANCIER_NAME"]
                                    z = z.replace("Seating(in all)/Standing/Sleeping Capacity", "")
                                    if z[-2:].isdigit() or z == "NA" or z.__contains__("Capacity"):
                                        visited[df.loc[j, "Name"]] = False
                                        result["FINANCIER_NAME"] = ""
                                        continue

                                if df.loc[j, "Name"] == "Insured Name":
                                    z = result["Insured Name"]
                                    z = z.split("Son/wife")[0]
                                    z = z.replace("(", "").replace(")", "")
                                    z = clean(z)
                                    # print(z)
                                    if len(z) > 45 or len(z) == 0:
                                        visited[df.loc[j, "Name"]] = False
                                        result["Insured Name"] = ""
                                        continue
                                    if z[-2:].isdigit() or z[-1].isdigit() or z.__contains__(
                                            "S/D/W") or z.__contains__("S/DAWN of") or z.__contains__(
                                            "SID/B/H") or (z.__contains__("CLASS") and not z.__contains__("CLASSIC")) or \
                                            z.__contains__("S/OWW of") or z.__contains__("Name") or z.__contains__(
                                        "S/WID OF") or z.__contains__("SIDW of") or z.__contains__("SIDIW of") or \
                                            z.__contains__("Permanent") or z.__contains__("S W/D/o") or z.__contains__(
                                        "S/D/B/H") or z.__contains__("EV/DIO") or \
                                            z.__contains__("BOLERO") or z.__contains__("OWNER") or z.__contains__("Luxury Cab") or z.__contains__(
                                        "SD/B/H") or z.__contains__("Weight") or z.__contains__("REGD") or z.__contains__("Luxury Cab3") or z.__contains__("AMAZE 1.2") or z.__contains__(
                                        "W/o") or z.strip() == "NA" or z.strip() == "Fuel" or z == result["Make"] or z == result["Model - Variant"]:
                                        visited[df.loc[j, "Name"]] = False
                                        result["Insured Name"] = ""
                                        continue
                                if df.loc[j, "Name"] == "S/D/W":
                                    z = result["S/D/W"]
                                    # print(z)
                                    z = z.replace("(", "").replace(")", "")
                                    if z == result["Insured Name"] or z.upper().__contains__("ADDRESS"):
                                        visited[df.loc[j, "Name"]] = False
                                        result["S/D/W"] = ""
                                        continue

                                if len(result[df.loc[j, "Name"]]) == 0:
                                    # print(text_json[z].get("text"))
                                    continue
                                else:
                                    visited[df.loc[j, "Name"]] = True
                                    break

                        if len(result[df.loc[j, "Name"]]) == 0 and not df.loc[j, "Name"] == "FINANCIER_NAME":
                            # print(df.loc[j, "Key"])
                            visited[df.loc[j, "Name"]] = False
                            # print(visited[df.loc[j, "Key"]])
                            for z in range(i - 1, i - 7, -1):
                                if df.loc[j, "Breaking Condition"] in text_json[z].get("text"):
                                    break
                                if text_json[z].get("text").strip(". : ,") == "":
                                    continue
                                if diff(x, text_json[z].get("boundingBox"), j, df):
                                    # print(df.loc[j, "x0"])
                                    # print(text_json[z].get("text"))
                                    result[df.loc[j, "Name"]] = str(clean(text_json[z].get("text"))).replace(
                                        df.loc[j, "Ignore"], "").strip()

                                    if df.loc[j, "Name"] == "Insured Name":
                                        z = result["Insured Name"]
                                        z = z.replace("Son/wife/daughter", "")
                                        z = z.replace("(", "").replace(")", "")
                                        z = clean(z)
                                        z = z.rstrip(",")
                                        if len(z) > 35:
                                            visited[df.loc[j, "Name"]] = False
                                            result["Insured Name"] = ""
                                            continue
                                        if z.__contains__("Regn. Number") or z.__contains__("Number of Axle") or z[
                                            -1].isdigit() or z == "OF":
                                            visited[df.loc[j, "Name"]] = False
                                            result["Insured Name"] = ""
                                            continue

                                    if df.loc[j, "Name"] == "S/W/D":
                                        z = result["S/W/D"]
                                        z = z.replace("(", "").replace(")", "")
                                        if z == result["Insured Name"]:
                                            visited[df.loc[j, "Name"]] = False
                                            result["S/W/D"] = ""
                                            continue

                                    if df.loc[j, "Name"] == "FINANCIER_NAME":
                                        if result["FINANCIER_NAME"].__contains__("FORM"):
                                            visited[df.loc[j, "Name"]] = False
                                            result["FINANCIER_NAME"] = ""
                                            continue

                                    if df.loc[j, "Name"] == "Date of Registration":
                                        z = result["Date of Registration"]
                                        z = z.replace("(", "").replace(")", "")
                                        z = clean(z)
                                        if len(z) < 8:
                                            visited[df.loc[j, "Name"]] = False
                                            result["Date of Registration"] = ""
                                            continue
                                        if not z[-2:].isdigit() or not z[:2].isdigit():
                                            visited[df.loc[j, "Name"]] = False
                                            result["Date of Registration"] = ""
                                            continue

                                    if df.loc[j, "Name"] == "Make":
                                        z = result["Make"]
                                        z = z.replace("(", "").replace(")", "")
                                        z = clean(z)
                                        if z[:2].isdigit() or z[-2:].isdigit():
                                            visited[df.loc[j, "Name"]] = False
                                            result["Make"] = ""
                                            continue
                                        if z.__contains__("Date") or z.__contains__("tyres"):
                                            visited[df.loc[j, "Name"]] = False
                                            result["Make"] = ""
                                            continue

                                    if df.loc[j, "Name"] == "Model - Variant":
                                        z = result["Model - Variant"]
                                        z = z.replace("(", "").replace(")", "")
                                        z = clean(z)
                                        # print(z)
                                        if z.__contains__("insured") or z.__contains__("E. NO") or z == "KE":
                                            visited[df.loc[j, "Name"]] = False
                                            result["Model - Variant"] = ""
                                            continue

                                    if df.loc[j, "Name"] == "Engine No":
                                        z = result["Engine No"]
                                        z = z.replace(" ", "")
                                        z = z.replace("(", "").replace(")", "")
                                        z = clean(z)
                                        if len(z) < 5:
                                            visited[df.loc[j, "Name"]] = False
                                            result["Engine No"] = ""
                                            continue
                                        if (not z[-4].isdigit()) or z == result["Chassis No"]:  # or z[0] == "M"
                                            visited[df.loc[j, "Name"]] = False
                                            result["Engine No"] = ""
                                            continue

                                    if df.loc[j, "Name"] == "Chassis No":
                                        z = result["Chassis No"]
                                        z = z.replace(" ", "")
                                        z = z.replace("(", "").replace(")", "")
                                        z = clean(z)
                                        if len(z) < 7:
                                            visited[df.loc[j, "Name"]] = False
                                            result["Chassis No"] = ""
                                            continue
                                        if (not z[-4:-2].isdigit()) or z.__contains__("to"):
                                            visited[df.loc[j, "Name"]] = False
                                            result["Chassis No"] = ""
                                            continue

                                    if df.loc[j, "Name"] == "Seating Capacity":
                                        z = result["Seating Capacity"]
                                        z = z.replace("(", "").replace(")", "")
                                        z = z.split("including")[0]
                                        z = z.split("Including")[0]
                                        z = z.split("Inchiding")[0]
                                        z = z.replace("a", "").replace("s", "")
                                        z = clean(z)
                                        # print(z)
                                        if len(z) > 6:
                                            visited[df.loc[j, "Name"]] = False
                                            result["Seating Capacity"] = ""
                                            continue
                                        if (not z[0].isdigit()) or int(z) > 11 or z == result["No of Cylinders"]:
                                            visited[df.loc[j, "Name"]] = False
                                            result["Seating Capacity"] = ""
                                            continue

                                    if df.loc[j, "Name"] == "Mfg Yr":
                                        z = result["Mfg Yr"]
                                        z = z.replace("(", "").replace(")", "")
                                        z = clean(z)
                                        if not 12 > len(z) > 4:
                                            visited[df.loc[j, "Name"]] = False
                                            result["Mfg Yr"] = ""
                                            continue
                                        if not z[-2:].isdigit():
                                            visited[df.loc[j, "Name"]] = False
                                            result["Mfg Yr"] = ""
                                            continue

                                    if df.loc[j, "Name"] == "Cubic Capacity":
                                        z = result["Cubic Capacity"]
                                        z = z.replace("CC", "").replace(".", "").replace("GC", "")
                                        z = z.replace("(", "").replace(")", "").replace("/", "7")
                                        z = clean(z)
                                        # print(result["Cubic Capacity"])
                                        if len(z) > 6:
                                            visited[df.loc[j, "Name"]] = False
                                            result["Cubic Capacity"] = ""
                                            continue
                                        if not z.replace("CC", "")[-2:].isdigit():
                                            visited[df.loc[j, "Name"]] = False
                                            result["Cubic Capacity"] = ""
                                            continue

                                    if df.loc[j, "Name"] == "Gross Vehicle Weight":
                                        z = result["Gross Vehicle Weight"]
                                        z = z.replace("kgs", "").replace("kg", "").replace("Kgs", "").replace("Kgs",
                                                                                                              "").replace(
                                            "Mos", "")
                                        z = z.replace("(", "").replace(")", "")
                                        z = clean(z)
                                        if len(z) > 5 or len(z) < 3:
                                            visited[df.loc[j, "Name"]] = False
                                            result["Gross Vehicle Weight"] = ""
                                            continue
                                        if not z[-2:].isdigit():
                                            visited[df.loc[j, "Name"]] = False
                                            result["Gross Vehicle Weight"] = ""
                                            continue

                                    if df.loc[j, "Name"] == "Registration Number":
                                        z = result["Registration Number"].replace(" ", "")
                                        z = z.replace("(", "").replace(")", "")
                                        z = clean(z)
                                        if len(z) < 5 or len(z) > 14:
                                            visited[df.loc[j, "Name"]] = False
                                            result["Registration Number"] = ""
                                            continue
                                        if not z[-4:-2].isdigit() or not z[:2].isalpha() or z.upper().__contains__(
                                                "DATE"):
                                            visited[df.loc[j, "Name"]] = False
                                            result["Registration Number"] = ""
                                            continue

                                    if len(result[df.loc[j, "Name"]]) == 0:
                                        # print(text_json[z].get("text"))
                                        continue
                                    else:
                                        visited[df.loc[j, "Name"]] = True
                                        break
                        i = i - 1

                    elif df.loc[j, "Value Navigation"] == 'INIT':
                        # print(df.loc[j, "Key"])
                        x = text_json[i].get("text")
                        x = x.split(df.loc[j, "Key"])[1].strip()
                        result[df.loc[j, "Name"]] = clean(x.replace(df.loc[j, "Ignore"], "").strip(" - ? ; . , ").split(
                            df.loc[j, "Breaking Condition"])[0])
                        # print(result["Engine No"])

                        if df.loc[j, "Name"] == "Insured Name":
                            z = result["Insured Name"]
                            if z.__contains__("MAHINDRA SCORPIO"):
                                visited[df.loc[j, "Name"]] = False
                                result["Insured Name"] = ""
                                continue

                        if df.loc[j, "Name"] == "Chassis No":
                            z = result["Chassis No"]
                            if z[0] == "R":
                                visited[df.loc[j, "Name"]] = False
                                result["Chassis No"] = ""
                                continue

                        if df.loc[j, "Name"] == "Engine No":
                            z = result["Engine No"]
                            z = z.replace(" ", "")
                            z = z.replace("(", "").replace(")", "")
                            z = clean(z)
                            if len(z) < 5 or z.__contains__("Number"):
                                visited[df.loc[j, "Name"]] = False
                                result["Engine No"] = ""
                                continue
                            # if len(z) < 5:
                            #     visited[df.loc[j, "Name"]] = False
                            #     result["Engine No"] = ""
                            #     continue
                            if (not z[-4].replace("S", "5").replace("Y", "1").isdigit()) or z == result["Chassis No"] or z.isalpha():  # or z[0] == "M"
                                visited[df.loc[j, "Name"]] = False
                                result["Engine No"] = ""
                                continue

                        if df.loc[j, "Name"] == "Chassis No":
                            z = result["Chassis No"]
                            z = z.replace(" ", "")
                            z = z.replace("(", "").replace(")", "")
                            z = clean(z)
                            if z.__contains__("CYL"):
                                visited[df.loc[j, "Name"]] = False
                                result["Chassis No"] = ""
                                continue

                        if df.loc[j, "Name"] == "Date of Registration":
                            z = result["Date of Registration"]
                            z = z.replace(" ", "")
                            z = clean(z)
                            if z.__contains__("ofRegn"):
                                visited[df.loc[j, "Name"]] = False
                                result["Date of Registration"] = ""
                                continue

                        if len(result[df.loc[j, "Name"]]) == 0:
                            # print(df.loc[j, "Key"])
                            continue
                        else:
                            visited[df.loc[j, "Name"]] = True
                            i = i - 1
                            break

                    elif df.loc[j, "Value Navigation"] == 'RBML':
                        print("I did come here")
                        x = text_json[i].get("boundingBox")
                        xc = i + 1
                        coor = text_json[xc].get("boundingBox")
                        # print((text_json[xc].get('text')))
                        # print(df.loc[j,"x1"])
                        # print(abs(x[1] - coor[1]))
                        try:
                            while abs(x[1] - coor[1]) > df.loc[j, "x1"] or clean(text_json[xc].get('text')).isdigit():
                                xc = xc + 1
                                # print(text_json[xc].get("text"))
                                coor = text_json[xc].get("boundingBox")
                            result[df.loc[j, "Name"]] = text_json[xc].get("text").replace(df.loc[j, "Ignore"], "")
                            x = coor
                            # print(x[0])
                            # print(coor[0])
                            xc = xc + 1
                            coor = text_json[xc].get("boundingBox")
                            while df.loc[j, "Breaking Condition"] not in text_json[xc].get("text"):
                                if abs(x[0] - coor[0]) <= int(df.loc[j, "x0"]):
                                    result[df.loc[j, "Name"]] = result[df.loc[j, "Name"]] + " " + \
                                                                text_json[xc].get("text").replace(
                                                                    df.loc[j, "Ignore"], "")
                                    x = coor
                                xc = xc + 1
                                coor = text_json[xc].get("boundingBox")
                        except:
                            print("Error1 - RBML")

                    elif df.loc[j, "Value Navigation"] == 'BML':
                        try:
                            result[df.loc[j, "Name"]] = ""
                            x = text_json[i].get("boundingBox")
                            xc = i + 1
                            # print(df.loc[j, "Key"])
                            while df.loc[j, "Breaking Condition"] not in text_json[xc].get("text"):
                                if diff(x, text_json[xc].get("boundingBox"), j, df):
                                    # if df.loc[j, "Key"] == "Addr":
                                    #     print(text_json[xc].get("text"))
                                    data = text_json[xc].get("text")
                                    if st == "WEST BENGAL":
                                        if not data.upper().__contains__("CC"):
                                            result[df.loc[j, "Name"]] = result[df.loc[j, "Name"]] + ";" + \
                                                                        clean(data.replace(df.loc[j, "Ignore"], ""))
                                    else:
                                        result[df.loc[j, "Name"]] = result[df.loc[j, "Name"]] + ";" + \
                                                                    clean(data.replace(df.loc[j, "Ignore"], ""))

                                    x = text_json[xc].get("boundingBox")
                                xc = xc + 1

                            visited[df.loc[j, "Name"]] = True
                        except:
                        # + df.loc[j, "Name"]+ " " + result[df.loc[j, "Name"]])
                            print("Error2")
                        # print(result["Address"])
                        break

                    elif df.loc[j, "Value Navigation"] == 'TBML':
                        # print(df.loc[j, "Key"])
                        try:
                            result[df.loc[j, "Name"]] = ""
                            x = text_json[i].get("boundingBox")
                            xc = i
                            yc = 4

                            while df.loc[j, "Breaking Condition"] not in text_json[xc].get("text") and yc > 0:

                                if diff(x, text_json[xc].get("boundingBox"), j, df):
                                    # print(text_json[xc].get("text"))
                                    data = \
                                    text_json[xc].get("text").replace(df.loc[j, "Ignore"], "").split(df.loc[j, "Key"])[
                                        -1]

                                ### for Odisha

                                    data = data.split("Registered Laden Weight")[0]
                                    data = data.split("No. of Cylinders")[0]
                                    data = data.split("Unladen Weight")[0]
                                    data = data.split("unladen Weight")[0]
                                    data = data.split("Standing Capacity")[0]
                                    data = data.split("Standing Dapacitya")[0]

                                    ### for Haryana
                                    data = data.split("Date of Issue")[0]
                                    # data = data.split("EMISSION")[0]
                                    # data = data.split("BHARAT")[0]

                                    ### for MP
                                    data = data.split("SEATING")[0]
                                    data = data.split("STANDING")[0]
                                    data = data.split("FUEL USED")[0]
                                    # print(data)

                                    # if len(data) == 0:
                                    #     # print("yessss")
                                    #     xc = xc + 1
                                    #     x = text_json[xc].get("boundingBox")
                                    #     zc = 4
                                    #     while df.loc[j, "Breaking Condition"] not in text_json[xc].get("text") and zc > 0:
                                    #         if diff(x, text_json[xc].get("boundingBox"), j, df):
                                    #             data = text_json[xc].get("text").replace(df.loc[j, "Ignore"], "").split(df.loc[j, "Key"])[-1]
                                    #             # print(data)

                                    result[df.loc[j, "Name"]] = result[df.loc[j, "Name"]] + " " + clean(data)

                                    x = text_json[xc].get("boundingBox")
                                    yc = yc - 1
                                    # visited[df.loc[j, "Name"]] = True
                                xc = xc + 1

                            if len(result[df.loc[j, "Name"]]) == 0:
                                # print(df.loc[j, "Key"])
                                continue
                            else:
                                visited[df.loc[j, "Name"]] = True
                                break

                        except:
                            print("Error3")
                        break

                    elif df.loc[j, "Value Navigation"] == 'TTBML':
                        # print(df.loc[j, "Key"])
                        try:
                            result[df.loc[j, "Name"]] = ""
                            x = text_json[i].get("boundingBox")
                            xc = i
                            # yc = 4

                            while df.loc[j, "Breaking Condition"] not in text_json[xc].get("text"):

                                if diff(x, text_json[xc].get("boundingBox"), j, df):
                                    # print(text_json[xc].get("text"))
                                    data = text_json[xc].get("text").replace(df.loc[j, "Ignore"], "").split(df.loc[j, "Key"])[-1]

                                    ### for Odisha
                                    data = data.split("Registered Laden Weight")[0]
                                    data = data.split("No. of Cylinders")[0]
                                    data = data.split("Unladen Weight")[0]
                                    data = data.split("unladen Weight")[0]
                                    data = data.split("Standing Capacity")[0]
                                    data = data.split("Standing Dapacitya")[0]

                                    ### for Haryana
                                    data = data.split("Date of Issue")[0]
                                    # data = data.split("EMISSION")[0]
                                    # data = data.split("BHARAT")[0]

                                    ### for MP
                                    data = data.split("SEATING")[0]
                                    data = data.split("STANDING")[0]
                                    data = data.split("FUEL USED")[0]

                                    result[df.loc[j, "Name"]] = result[df.loc[j, "Name"]] + " " + clean(data)

                                    x = text_json[xc].get("boundingBox")
                                    # yc = yc - 1
                                    # visited[df.loc[j, "Name"]] = True
                                xc = xc + 1

                            if len(result[df.loc[j, "Name"]]) == 0:
                                # print(df.loc[j, "Key"])
                                continue
                            else:
                                visited[df.loc[j, "Name"]] = True
                                break

                        except:
                            print("Error4")
                        break

                except:
                    print("Interpretation Issue")
    result1 = copy.deepcopy(result)
    if bck == 1:
        for key in result1.keys():
            if result1[key] == "":
                del result[key]

    return result
