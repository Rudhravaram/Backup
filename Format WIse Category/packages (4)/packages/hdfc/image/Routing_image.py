import subprocess
import pandas as pd
import regex as re
from packages.hdfc.image.Image_Interpretation import check
import requests
import time
#import cv2
import numpy as np
import urllib.parse, urllib.error
import pandas as pd
import re
import string
import csv
from openpyxl import load_workbook
import pandas as pd
from fuzzywuzzy import fuzz

def common_member(a, b):
    a_set = set(a)
    b_set = set(b)
    return a_set & b_set

def correct_time(a1):

    a1 = a1.strip("a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z")
    a = a1
    b = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}

    try:
        keys = b.keys()
        month = ""
        for key in keys:
            if key in a:
                # print(key)
                month = key
                break
        a = a.split(month)
        # month = b[month]
        date = a[0].strip()
        year = a[1].strip(', .').split()[0]
        result = date + "-" + month + "-" + year
        # print(a)
        # print(result)
        return result
    except:
        try:
            a = a.split('/')
            date = a[0]
            month = a[1]
            year = a[2].split()[0]
            b1 = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
                 "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}
            # keys = b1.keys()
            # for key in keys:
            #     if key in month:
            #         print(key)
            #         month = key
            #         break
            # print(date)
            # print(month)
            # print(year)
            month = b1[month]
            result = date + "-" + month + "-" + year
            # print(result)
            return result
        except:
            # print(a1)
            return a1

def main_image_run(text_json):
    # file = r"Testing/Set3/4.jpg"
    # file = r"Samples/10.jpeg"

    # text_json = icr_run(file)
    
    state = ["Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Orissa","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu","Lakshadweep","National Capital Territory of Delhi","Puducherry","Delhi"]

    type1 = ["Two Wheeler comprehensive policy through CSC", "Motor Insurance - Two Wheeler Comprehensive Policy", "Motor Insurance - Two Wheeler Policy - Bundled"]
    type2 = ["Goods carrying Comprehensive policy through CSC"]
    


    # z_list = []
    # for i in range(30):
    #     z_list.append(text_json[i].get("text"))
    # result = {}
    # if common_member(z_list, type1):
    #     print("Two Wheeler Compre CSC")
    #     result = check(text_json, "Two Wheeler Compre CSC")
    # elif common_member(z_list, type2):
    #     print("Goods Compre CSC")
    #     result = check(text_json, "Goods Compre CSC")
    # else:
    #     print("Others")
    #     result = check(text_json, "Others")
    wheel = 0
    result = {}
    z_list = []
    sheet = ""
    for i in range(len(text_json)):
        # print(text_json[i].get("text"))
        # z_list.append(text_json[i].get("text"))
        if text_json[i].get("text").upper().__contains__("TWO WHEELER"):  ####impo
            wheel = 1
        if text_json[i].get("text").__contains__("Insured Name"):
            k = 0
            for z in range(i, len(text_json)):
                if text_json[z].get("text").__contains__("RTO"):
                    ka = 0
                    for j in range(z, len(text_json)):
                        if text_json[j].get("text").__contains__("Trailer"):
                            sheet = "T3"
                            print("T3")
                            result = check(text_json, "T3")
                            ka = 1
                            break
                    if ka == 1:
                        k = 1
                        break
                    else:
                        sheet = "T4"
                        print("T4")
                        result = check(text_json, "T4")
                        k = 1
                        break

            if k == 1:
                break
        if text_json[i].get("text").__contains__("Make"):
            if text_json[i+1].get("text").__contains__("HERO MOTOCORP") or text_json[i+1].get("text").__contains__("TVS"):
                wheel = 1
            if text_json[i+1].get("text").__contains__("Model"):
                sheet = "T2"
                print("T2")
                result = check(text_json, "T2")
            else:
                print("T1")
                sheet = "T1"
                result = check(text_json, "T1")
            break
        elif text_json[i].get("text").__contains__("Model"):
            if text_json[i+1].get("text").__contains__("Engine"):
                sheet = "T2"
                print("T2")
                result = check(text_json, "T2")
            else:
                print("T1")
                sheet = "T1"
                result = check(text_json, "T1")
            break
        elif text_json[i].get("text").__contains__("Engine"):
            if text_json[i+1].get("text").__contains__("Chassis"):
                sheet = "T2"
                print("T2")
                result = check(text_json, "T2")
            else:
                print("T1")
                sheet = "T1"
                result = check(text_json, "T1")
            break

    keys = result.keys()

    try:
        if "Insured Name" in keys:
            result["Salutation"] = result["Insured Name"].split(" ")[0]
            result["Insured Name"] = result["Insured Name"].replace("RTO", "")
            if len(result["Salutation"]) > 3:
                result["Salutation"] = ""
            if result["Insured Name"].split()[1] == "ROAD":
                result["Address"] = result["Insured Name"] + result["Address"]
                result["Insured Name"] = ""
    except:
        print("Insured Name")
    try:
        if "Address" in keys:
            result["Address"] = result["Address"].replace("Cubic Capacity/Watts", "").replace("Cubic Capacity", "")
            result["Address"] = result["Address"].lstrip(', 0 1 2 3 4 5 6 7 8 9 ')
            result["Address"] = result["Address"].split("Online")[-1]
            result["Address"] = result["Address"].split("DO505360600000")[-1]
            result["Address"] = result["Address"].split("C601")[-1]
            result["Address"] = result["Address"].split("Vellicle")[0]
            result["Address"] = result["Address"].replace("!", "", 1)
            # print(result["Address"])
            x = result["Address"].split(',')[0]
            if x.__contains__("Insurance"):
                result["Address"] = result["Address"].replace(x, "")
                result["Address"] = result["Address"].lstrip(', 0 1 2 3 4 5 6 7 8 9 ')

            Pattern = re.compile("[0-9]{6}|[0-9]{3}\s[0-9]{3}")  # ^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$")
            x = Pattern.search(result["Address"])
            try:
                result["Pincode"] = x.group()
            except:
                print("Pincode")
            Pattern = re.compile("(0/91)?[5-9][0-9]{9}")
            x = Pattern.search(result["Address"].replace(" ", ""))
            try:
                result["Mobile"] = x.group()
            except:
                print("Mobile")

            result["Address"] = result["Address"].lstrip(" ,")
            # print(result["Address"])
            # print(result["Address"].split(',')[0])
            result["Insured Name"] = ""
            if len(result["Address"].split()) > 1 and result["Address"].split()[1] == "ROAD":
                result["Insured Name"] = ""
            else:
                result["Insured Name"] = result["Address"].split(',')[0]
                result["Insured Name"] = result["Insured Name"].replace("My", "Mr") #.replace("MI", "Mr")

                result["Salutation"] = result["Insured Name"].split(" ")[0]
                result["Salutation"] = result["Salutation"].replace("MIS", "M/S").replace("MI", "Mr").replace("M.", "Mr")

                if len(result["Salutation"]) > 3:
                    result["Salutation"] = ""
            result["Address"] = result["Address"].replace(result["Insured Name"], "").lstrip(', ')
            state = [elem.upper() for elem in state]
            # print(result["Insured Name"])
            for i in state:
                if i in result["Address"]:
                    result["CUSTOMER_STATE"] = i
                    # print(result["CUSTOMER_STATE"])
                    break
            try:
                result["Address"] = result["Address"].split(result["CUSTOMER_STATE"])[0] + result["CUSTOMER_STATE"]
            except:
                print("state")
    except:
        print("Address")

    try:
        if result["Address"] == "" and sheet == "T1":
            result["Address"] = ""
            for i in range(len(text_json)):
                if "Trailer" in text_json[i].get("text"):
                    break
                x = text_json[i].get("boundingBox")
                if int(x[0]) < 150:
                    result["Address"] = result["Address"] + "," + text_json[i].get("text")
            result["Address"] = result["Address"].replace("Certificate of Insurance cum Policy Schedule", "")
            result["Address"] = result["Address"].lstrip(', 0 1 2 3 4 5 6 7 8 9 ')
            x = result["Address"].split(',')[0]
            if x.__contains__("Insurance"):
                result["Address"] = result["Address"].replace(x, "")
                result["Address"] = result["Address"].lstrip(', 0 1 2 3 4 5 6 7 8 9 ')

            Pattern = re.compile("[0-9]{6}|[0-9]{3}\s[0-9]{3}")  # ^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$")
            x = Pattern.search(result["Address"])
            try:
                result["Pincode"] = x.group()
            except:
                print("Pincode 2")
            Pattern = re.compile("(0/91)?[5-9][0-9]{9}")
            x = Pattern.search(result["Address"].replace(" ", ""))
            try:
                result["Mobile"] = x.group()
            except:
                print("Mobile 2")

            result["Address"] = result["Address"].lstrip(" ,")
            result["Address"] = result["Address"].replace("Cubic", "").replace("Capacity/Watts", "")
            result["Address"] = result["Address"].split("Vehicle")[0]
            # print(result["Address"])
            # print(result["Address"].split(',')[0])
            result["Insured Name"] = ""
            if len(result["Address"].split()) > 1 and result["Address"].split()[1] == "ROAD":
                result["Insured Name"] = ""
            else:
                result["Insured Name"] = result["Address"].split(',')[0]
                result["Insured Name"] = result["Insured Name"].replace("My", "Mr")  # .replace("MI", "Mr")

                result["Salutation"] = result["Insured Name"].split(" ")[0]
                result["Salutation"] = result["Salutation"].replace("MIS", "M/S").replace("MI", "Mr")

                if len(result["Salutation"]) > 3:
                    result["Salutation"] = ""

            # print(result["Insured Name"])
            result["Address"] = result["Address"].replace(result["Insured Name"], "").lstrip(', ')
            state = [elem.upper() for elem in state]
            # print(state)
            for i in state:
                if i in result["Address"]:
                    result["CUSTOMER_STATE"] = i
                    # print(result["CUSTOMER_STATE"])
                    break
            try:
                result["Address"] = result["Address"].split(result["CUSTOMER_STATE"])[0] + result["CUSTOMER_STATE"]
            except:
                print("state 2")
    except:
        print("Address 2")

    try:
        if "Only Address" in keys:
            result["Address"] = result["Only Address"]
            del result["Only Address"]
            z = result["Address"]
            # print(z)
            z = z.lstrip(', 0 1 2 3 4 5 6 7 8 9 ')
            z = z.replace("Corr.Address/", "").replace("Place of Supply", "").replace("Correspondence", "").replace("Address", "")
            result["Address"] = z
            # print(z)
            Pattern = re.compile("[0-9]{6}|[0-9]{3}\s[0-9]{3}")  #  |[0-9]{5} [0-9]{6}|[0-9]{3}\s[0-9]{3}  ^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$
            x = Pattern.search(result["Address"])
            # print(x)
            try:
                result["Pincode"] = x.group()
            except:
                print("Pincode")
            state = [elem.upper() for elem in state]
            for i in state:
                if i in result["Address"]:
                    result["CUSTOMER_STATE"] = i
                    # print(result["CUSTOMER_STATE"])
                    break
            try:
                result["Address"] = result["Address"].split(result["CUSTOMER_STATE"])[0] + result["CUSTOMER_STATE"]
            except:
                print("state")
    except:
        print("Only Address")

    try:
        if "Period of Insurance" in keys:
            # print(result["Period of Insurance"])
            result["Period of Insurance start date"] = result["Period of Insurance"].split("To")[0].lstrip("From ")
            result["Period of Insurance End date"] = result["Period of Insurance"].split("To")[1].lstrip(" ")

            result["Period of Insurance End date"] = result["Period of Insurance End date"].replace(":", "").replace("Of", "06")
            del result["Period of Insurance"]

            result["Period of Insurance start date"] = result["Period of Insurance start date"].replace("-9050", "")
    except:
        print("Period of Insurance")
        del result["Period of Insurance"]

    try:
        if "Issuance Date" in keys:
            result["Policy Issuance Date"] = result["Issuance Date"].strip('a b c d e f g h i j k l m n o p q r s t u v w x y z D')
            del result["Issuance Date"]
    except:
        print("Issuance Date")
    try:
        if "Mfg. Year" in keys:
            result["Mfg. Year"] = result["Mfg. Year"].strip('a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z')
    except:
        print("Mfg. Year")

    try:
        if "Cubic Capacity" in keys:
            result["Cubic Capacity"] = result["Cubic Capacity"].replace("Watts","").replace("Wats","").replace("07 CC)", "97")
        if not result["Cubic Capacity"].strip().isnumeric():
            result["Cubic Capacity"] = ""
    except:
        print("Cubic Capacity")
    try:
        if "Model" in keys:
            z = result["Model"]
            z = z.lstrip(",")
            # print(z)
            if z[0] == "(":
                z = z.replace("(", "i", 1)
            if z[0] == "1":
                z = z.replace("1", "I", 1)
            if z.__contains__("(") and (not z.__contains__(")")):
                if z.__contains__("CC"):
                    z = z + ")"
                else:
                    z = z + " CC)"
            # print(z)
            z = z.replace("Make", "").replace(result["Make"], "").replace(result["Chassis No"], "").replace("BEW53", "").replace("Registration No", "").replace("egistration No", "").replace("Insurance", "").replace("Policy No", "")
            z = z.split("The Vehicle")[0]
            z = z.lstrip(",")
            q = z.split(",")
            if len(q) > 1:
                for j in range(2, len(q)):
                    # print(q[j])
                    if "CC" in q[j]:
                        q[0] = q[0].replace("Period of", "")
                        q[0] = q[0] + " " + q[j]
                        break
            z = " ".join(q)
            # print(z)
            p = z.split(",")[0]
            p = p.split("Period of")[0]
            if len(z.split(",")) > 1:
                z = p + " " + z.split(",")[1]
            else:
                z = p
            # print(z)
            z = z.split("HAT")[0]
            z = z.split("Period")[0]
            z = z.split("Perod of")[0]
            z = z.split("Parod of")[0]
            z = z.split("Penod of")[0]
            z = z.split("Proud of")[0]
            z = z.split("iod of")[0]
            z = z.split("id of")[0]
            z = z.split("From")[0]
            z = z.split("MUV")[0]

            z = z.replace("Engine No", "").replace("Chassis No", "").replace("Mfg Yr", "").replace("Seats", "").replace("Body Type", "").replace("Trailer", "").replace("|", "").replace(".", "-").replace("]", ")")  #.replace("CC", "")
            z = z.replace("Insured's Declared", "")
            result["Model"] = z

            if result["Cubic Capacity"] == "" or int(result["Cubic Capacity"]) < 50:
                if z.__contains__("CC") or z.__contains__("("):
                    cc = z.split("(")[-1]
                    cc = cc.split("CC")[0]
                    result["Cubic Capacity"] = cc.rstrip(")")
    except:
        print("Model")
    try:
        if "Nominee for Owner driver" in keys:
            result["Nominee for Owner driver (Nominee Relation)"] = result["Nominee for Owner driver"].split(" ")[-1]
            result["Nominee for Owner driver (Nominee Name)"] = result["Nominee for Owner driver"].replace(result["Nominee for Owner driver (Nominee Relation)"],"").strip()
            del result["Nominee for Owner driver"]
    except:
        print("Nominee for Owner drive")
        del result["Nominee for Owner driver"]

    try:
        if result["Policy Number"] == "":
            for i in range(len(text_json)):
                abc = text_json[i].get("text").replace(" ", "")
                if abc.isnumeric() and len(abc)==19:
                    result["Policy Number"] = text_json[i].get("text")
    except:
        print("Policy Number")

    try:
        if "RTO" in keys:
            z = result["RTO"]
            if z == "TAP":
                result["RTO"] = "TAPI"
    except:
        print("RTO")

    # try:
    #     if "NCB" in keys:
    #         z = result["NCB"]
    #         z = z.replace("(", "").replace(")", "")
    #         if len(z) == 4:
    #             result["NCB"] = z[:2] + z[3]
    #         else:
    #             result["NCB"] = z
    # except:
    #     print("RTO")

    if "Chassis No" in keys:
        result["Chassis No"] = result["Chassis No"].replace("Capacity", "").replace(":", "1").replace("#", "B")
        result["Chassis No"] = result["Chassis No"].split("Cover")[0]

    if "Engine No." in keys:
        result["Engine No."] = result["Engine No."].replace("/", "7")

    if "Registration No." in keys:
        result["Registration No."] = result["Registration No."].replace(".", "-")
        if "To " in result["Registration No."] or "HSN" in result["Registration No."]:
            result["Registration No."] = ""

    if "Salutation" in keys:
        z = result["Salutation"]
        if z == "M" or z == "W":
            result["Salutation"] = "Mr"

    try:
        if sheet!="T1":

            if len(result["Chassis No"].split())>1:
                if result["Chassis No"].split()[0].__contains__("Insure") or result["Chassis No"].split()[0].__contains__("("):
                    result["Chassis No"] = ""
            if result["Chassis No"] == "" and result["Mfg. Year"] == "" and len(result["Engine No"].split())==3:
                result["Chassis No"] = result["Engine No"].split()[1]
                result["Mfg. Year"] = result["Engine No"].split()[2]
            elif result["Chassis No"] == "" and len(result["Engine No"].split())==2:
                result["Chassis No"] = result["Engine No"].split()[1]

            if result["Mfg. Year"] == "" and len(result["Chassis No"].split())==2:
                result["Mfg. Year"] = result["Chassis No"].split()[1]

            result["Model"] = result["Model"].replace(result["Engine No"],"").replace(result["Chassis No"],"").replace(result["Mfg. Year"],"")
            result["Engine No"] = result["Engine No"].replace(result["Chassis No"],"") .replace("-","")    # .replace(result["Mfg. Year"],"")
            result["Chassis No"] = result["Chassis No"].replace(result["Mfg. Year"],"").replace(",","")
            # print(result["Chassis No"])

            if result["Mfg. Year"] == "" and len(result["Chassis No"].split())==2:
                result["Mfg. Year"] = result["Chassis No"].split()[1]
                result["Chassis No"] = result["Chassis No"].replace(result["Mfg. Year"], "").replace(",", "")

            if result["Email id"].strip('. / , |') == "No" or ((not result["Email id"].upper().__contains__("COM")) and (not result["Email id"].upper().__contains__("IN")) and (not result["Email id"].upper().__contains__("@"))):
                # print("yes")
                result["Email id"] = ""

            if result["RTO"] == "No.":
                result["RTO"] = ""
    except:
        print("not T1")

    for key in result.keys():
        result[key] = result[key].strip('. , ; / : |')

    if "Policy Number" in keys:
        result["Policy No."] = result["Policy Number"]
        del result["Policy Number"]

    if "Email id" in keys:
        result["Email ID"] = result["Email id"]
        del result["Email id"]

    if "Registration No." in keys:
        result["Registration No"] = result["Registration No."]
        del result["Registration No."]

    if "Registration Number" in keys:
        result["Registration No"] = result["Registration Number"]
        del result["Registration Number"]

    if "Mfg. Year" in keys:
        result["Mfg Yr"] = result["Mfg. Year"]
        del result["Mfg. Year"]

    if "Engine No" in keys:
        result["Engine No."] = result["Engine No"]
        del result["Engine No"]

    if "Hypothecated" in keys:
        result["HYPOTHECATION"] = result["Hypothecated"]
        del result["Hypothecated"]

    ask = ["Make", "Model", "Policy No.", "Registration No", "RTO", "Policy Issuance Date", "Chassis No",
           "Cubic Capacity",
           "Mfg Yr", "Engine No.", "Email ID", "NCB", "Address", "Period of Insurance start date",
           "Period of Insurance End date",
           "Pincode", "Mobile", "Insured Name", "Salutation", "CUSTOMER_STATE",
           "Nominee for Owner driver (Nominee Relation)",
           "Nominee for Owner driver (Nominee Name)", "HYPOTHECATION", "FINANCIER_NAME", "FINANCIER_BRANCH",
           "Date of Registration",
           "Source System", "Product type", "Previous Policy Type"]

    if wheel == 0:   # shan
        result["Product type"] = "Four Wheeler"
    else:
        result["Product type"] = "Two Wheeler"

    for h in ask:
        if h not in keys:
            result[h] = ""

    final_model = result["Model"]
    try:
        a = final_model.split("-")[0].strip()
        if a == "":
            try:
                a = final_model.split("-")[1].strip()
                result["Model"] = a
            except:
                pass
            result["Model"] = a
    except:
        result["Model"] = final_model 

    if len(result["Chassis No"].split()) > 3:
        result["Chassis No"] = ""
    if result["Chassis No"] == "":
        result["Chassis No"] = result["Engine No."]
    result["Address"] = result["Address"].replace(result["Insured Name"],"")

    result["HYPOTHECATION"] = "NONE"
    result["Previous Policy Number"] = result["Policy No."]
    del result["Policy No."]
    result["Source System"] = "OCR"
    result["Previous Insurer Name"] = "HDFC ERGO General Insurance Company Limited"
    result["Period of Insurance start date"] = correct_time(result["Period of Insurance start date"].replace("00:01",""))
    result["Period of Insurance End date"] = correct_time(result["Period of Insurance End date"].replace("00:01",""))
    result["Policy Issuance Date"] = correct_time(result["Policy Issuance Date"].replace("00:01",""))

    result["Chassis No"] = result["Chassis No"].replace(" ", "")
    result["Engine No."] = result["Engine No."].replace(" ", "")
    result["Email ID"] = result["Email ID"].replace(" ", "")
    result["Mobile"] = result["Mobile"].replace(" ", "")

    x = 1
    for key in result.keys():
        result[key] = result[key].strip('. , / : |')
        print(str(x) + ". " + key + " -> " + result[key])
        x = x + 1

    return result
