import regex as re
from packages.icici.image.interpretation_icici import check_icici
import requests
import time
import pandas as pd
import re
import xlrd
import string
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def common_member(a, b):
    a_set = set(a)
    b_set = set(b)
    return a_set & b_set

def clean(s):
    return s.strip(" : . ( ) ;  _  ")

def correct_alpha(a):
    x1 = {'1': 'I', '0': 'O', '8': 'B', ')': 'I', '(': 'I', '5': 'S', '~': 'N', ']': 'I', '[': 'I', '_': ''}

    for key in x1.keys():
        if key == a:
            a = x1[key]

    return a

def correct_num(a):
    x1 = {'s': '5', 'Z': '2', 'T': '1', 'S': '5', 'R': '2', 'Q': '0', 'O': '0', 'A': '4', 'G': '6', 'H': '4',
          'a': '2', 'o': '0', 'y': '4', 'z': '2', 'f': '5', 't': '1',
          'b': '6', 'F': '5', 'B': '8', 'L': '1', 'C': '0', 'D': '1', 'l': '1', 'I': '1', 'i': '1', 'j': '1',
          'J': '7', 'P': '9', ')': '1', '(': '1', 'd': '0', '.':'0','N':'0','E':'0','q':'9'}

    for key in x1.keys():
        if key == a:
            a = x1[key]

    return a

def correct_time(a1):

    # a1 = a1.strip("a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z")
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
        result = ""
        if "," in a[-1]:
            date = a[-1].strip().split(",")[0]
            year = a[-1].strip(', .').split(",")[-1]
            year = year.strip().split()[0]
            result = date + "-" + month + "-" + year
        elif "." in a[-1]:
            # print("yesss")
            date = a[-1].strip().split(".")[0]
            year = a[-1].strip(', .').split(".")[-1]
            year = year.strip().split()[0]
            result = date + "-" + month + "-" + year
        else:
            date = a[-1].strip().split()[0]
            year = a[-1].strip(', .').split()[-1]
            year = year.strip().split()[0]
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

def magic_icici(text_json):

    wheel = 0
    pre_insurer = 0
    for i in range(len(text_json)):
        # print(i)
        print(text_json[i].get('text'))
        print(text_json[i].get('boundingBox'))
        print("######################")
        if text_json[i].get("text").upper().__contains__("WO WHEELER") or text_json[i].get("text").upper().__contains__("TUP WHEELER") or \
                text_json[i].get("text").upper().__contains__("O WHEEL") or text_json[i].get("text").upper().__contains__("MOTORCYCLE"):
            # print("yesss")
            wheel = 1
        if text_json[i].get("text").upper().__contains__("ICICI") and text_json[i].get("text").upper().__contains__("LOMBARD"):
            pre_insurer = 1


    state = ["Andhra Pradesh", "Arunachal Pradesh ", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana",
             "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh",
             "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Orissa", "Odisha", "Punjab", "Rajasthan",
             "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
             "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli", "Daman and Diu", "Lakshadweep",
             "National Capital Territory of Delhi", "Puducherry", "Delhi"]

    # print(text_json)
    text_json1 = []

    result = {}

    sheet = ""
    bck = 0

    for i in range(5):  # len(text_json)
        if text_json[i].get("text").upper().__contains__("CERTIFICATE OF INSURANCE") or \
                text_json[i].get("text").upper().__contains__("CUM POLICY SCHEDULE"):
            sheet = "T1"
            print("T1")
            result = check_icici(text_json, "T1", bck)
            break

    if sheet != "T1":
        for i in range(len(text_json)):
            if text_json[i].get("text").upper().__contains__("NIBHAYE VAADE") or \
                    text_json[i].get("text").upper().__contains__("NIBHAVE VAADE") or \
                    text_json[i].get("text").upper().__contains__("NIBHAVE VAADS"):
                sheet = "T1"
                print("T1")
                result = check_icici(text_json, "T1", bck)
                break
    if sheet != "T1":
        for i in range(len(text_json)):
            if text_json[i].get("text").__contains__("CERTIFICATE CUM INSURANCE"):
                sheet = "T2"
                print("T2")
                result = check_icici(text_json, "T2", bck)
                break
    if sheet != "T1" and sheet != "T2":
        for i in range(len(text_json)):
            if text_json[i].get("text").__contains__("CERTIFICATE OF INSURANCE"):
                sheet = "T3"
                print("T3")
                result = check_icici(text_json, "T3", bck)
                break

    if wheel == 0:   # shan
        result["Product type"] = "Four Wheeler"
    else:
        result["Product type"] = "Two Wheeler"

    # print(pre_insurer)
    if pre_insurer == 1:
        result["PREVIOUS_INSURER"] = "ICICI Lombard"

    keys = result.keys()
    # print(keys)

    #####
    if "insured name" not in keys:
        result["insured name"] = ""
    if "policy no" not in keys:
        result["policy no"] = ""
    if "email" not in keys:
        result["email"] = ""
    if "nominee name" not in keys:
        result["nominee name"] = ""
    if "nominee relation" not in keys:
        result["nominee relation"] = ""
    if "policy issuance date" not in keys:
        result["policy issuance date"] = ""

    if "chassis no" not in keys:
        result["chassis no"] = ""
    if "engine no" not in keys:
        result["engine no"] = ""
    if "cc" not in keys:
        result["cc"] = ""
    if "registration no" not in keys:
        result["registration no"] = ""
    if "mfg yr" not in keys:
        result["mfg yr"] = ""
    if "Address" not in keys:
        result["Address"] = ""
    if "Product type" not in keys:
        result["Product type"] = ""
    if "Period of Insurance Start date" not in keys:
        result["Period of Insurance Start date"] = ""
    if "Period of Insurance End date" not in keys:
        result["Period of Insurance End date"] = ""
    if "Pincode" not in keys:
        result["Pincode"] = ""

    if "CUSTOMER_STATE" not in keys:
        result["CUSTOMER_STATE"] = ""
    if "PREVIOUS_INSURER" not in keys:
        result["PREVIOUS_INSURER"] = ""
    # if "ncb" not in keys:
    #     result["ncb"] = ""
    if "gstin" not in keys:
        result["gstin"] = ""



    result["Period of Insurance Start date"] = ""
    result["Period of Insurance End date"] = ""
    try:
        if "Period of Insurance" in keys:
            # print(result["Period of Insurance"])
            result["Period of Insurance"] = result["Period of Insurance"].replace("Jut", "Jul").replace("te", "to").replace("Map", "May").replace("mm", "to")
            if result["Period of Insurance"].__contains__("to"):
                result["Period of Insurance Start date"] = result["Period of Insurance"].split("to")[0].lstrip("From ")
                result["Period of Insurance End date"] = result["Period of Insurance"].split("to")[1].lstrip(" ")
                if result["policy no"] in result["Period of Insurance Start date"]:
                    result["Period of Insurance Start date"] = result["Period of Insurance Start date"].replace(result["policy no"], "").lstrip(";")
                # print(result["Period of Insurance Start date"])
                result["Period of Insurance Start date"] = result["Period of Insurance Start date"].replace("Sup", "Sep")
                result["Period of Insurance Start date"] = result["Period of Insurance Start date"].split("on")[-1]
                result["Period of Insurance Start date"] = correct_time(result["Period of Insurance Start date"])

                result["Period of Insurance End date"] = result["Period of Insurance End date"].replace(":", "").replace("Of", "06")
                result["Period of Insurance End date"] = result["Period of Insurance End date"].split("Mobile")[0]
                result["Period of Insurance End date"] = clean(result["Period of Insurance End date"]).split(";")[0]
                # print(result["Period of Insurance End date"])
                result["Period of Insurance End date"] = result["Period of Insurance End date"].replace("Aor", "Apr")
                result["Period of Insurance End date"] = result["Period of Insurance End date"].split("on")[-1]
                result["Period of Insurance End date"] = result["Period of Insurance End date"].split("or")[-1]
                result["Period of Insurance End date"] = correct_time(result["Period of Insurance End date"])
                del result["Period of Insurance"]

                result["Period of Insurance Start date"] = result["Period of Insurance Start date"].replace("-9050", "")

            elif result["Period of Insurance"].__contains__("To"):
                result["Period of Insurance Start date"] = result["Period of Insurance"].split("To")[0].lstrip("From ")
                result["Period of Insurance End date"] = result["Period of Insurance"].split("To")[1].lstrip(" ")
                if result["policy no"] in result["Period of Insurance Start date"]:
                    result["Period of Insurance Start date"] = result["Period of Insurance Start date"].replace(result["policy no"], "").lstrip(";")
                # print(result["Period of Insurance Start date"])
                result["Period of Insurance Start date"] = result["Period of Insurance Start date"].replace("Sup", "Sep").replace("OD:", "")
                result["Period of Insurance Start date"] = correct_time(result["Period of Insurance Start date"])

                result["Period of Insurance End date"] = result["Period of Insurance End date"].replace(":","").replace("Of", "06")
                result["Period of Insurance End date"] = result["Period of Insurance End date"].split("Mobile")[0]
                result["Period of Insurance End date"] = clean(result["Period of Insurance End date"]).split(";")[0]
                # print(result["Period of Insurance End date"])
                result["Period of Insurance End date"] = result["Period of Insurance End date"].replace("Aor", "Apr")
                result["Period of Insurance End date"] = correct_time(result["Period of Insurance End date"])
                del result["Period of Insurance"]

                result["Period of Insurance Start date"] = result["Period of Insurance Start date"].replace("-9050", "")

    except:
        print("Period of Insurance")
        del result["Period of Insurance"]

    # try:
    if "registration no" in keys:
        result["registration no"] = result["registration no"].replace(" ", "").replace("-", "")
        if len(result["registration no"]) == 10:
            a = correct_alpha(result["registration no"][0])
            b = correct_alpha(result["registration no"][1])

            c = correct_num(result["registration no"][2])
            d = correct_num(result["registration no"][3])

            e = correct_alpha(result["registration no"][4])
            f = correct_alpha(result["registration no"][5])

            g = correct_num(result["registration no"][6])
            h = correct_num(result["registration no"][7])
            i = correct_num(result["registration no"][8])
            j = correct_num(result["registration no"][9])

            result["registration no"] = a + b + c + d + e + f + g + h + i + j

        if len(result["registration no"]) == 9:
            a = correct_alpha(result["registration no"][0])
            b = correct_alpha(result["registration no"][1])

            c = correct_num(result["registration no"][2])
            d = correct_num(result["registration no"][3])

            e = correct_alpha(result["registration no"][4])

            f = correct_num(result["registration no"][5])
            g = correct_num(result["registration no"][6])
            h = correct_num(result["registration no"][7])
            i = correct_num(result["registration no"][8])

            result["registration no"] = a + b + c + d + e + f + g + h + i

    # except:
    #     print("registration no")

    try:
        if "nominee name" in keys:
            result["nominee name"] = result["nominee name"].split("Named")[0]
    except:
        print("nominee name")

    try:
        if "policy issuance date" in keys:
            # print(result["policy issuance date"])
            result["policy issuance date"] = result["policy issuance date"].replace("[UIN : --]", "")
            result["policy issuance date"] = correct_time(result["policy issuance date"])
    except:
        print("policy issuance date")

    try:
        if "make" in keys:
            result["make"] = result["make"].replace(";", " ")
            result["make"] = result["make"].split("Side")[0]
            result["make"] = result["make"].split("ide")[0]
            result["make"] = result["make"].split("Mig")[0]
            result["make"] = result["make"].replace("TOFOTA", "TOYOTA")
    except:
        print("make")

    try:
        if "model" in keys:
            result["model"] = result["model"].replace(";", " ")
    except:
        print("model")

    try:
        if "chassis no" in keys:
            result["chassis no"] = result["chassis no"].replace("$", "1").replace("/", "1")  # .replace(" ", "")
            if result["engine no"] == "" and len(result["chassis no"]) > 25 and result["chassis no"].__contains__(" "):
                result["engine no"] = result["chassis no"].split()[1]
                result["chassis no"] = result["chassis no"].replace(result["engine no"], "")
            if result["chassis no"][:3] == "MEI":  # 29th Apr, 2021
                result["chassis no"] = "ME1" + result["chassis no"][3:]
    except:
        print("chassis no")

    try:
        if "engine no" in keys:
            if result["engine no"][:4] == "HATD":
                result["engine no"] = "HA10" + result["engine no"][4:]
    except:
        print("engine no")

    try:
        if "policy no" in keys:
            result["policy no"] = result["policy no"].replace("/", "").replace(" ", "").replace(";", "")
            if result["policy no"][-2:] == "OO":
                result["policy no"] = result["policy no"][:-2] + "00"
    except:
        print("policy no")

    try:
        if result["cc"] == result["mfg yr"]:
            result["cc"] = ""
    except:
        print("cc")

    try:
        if "ncb" in keys and result["ncb"] == "":
            result["ncb"] = "0"
    except:
        print("ncb")

    try:
        if (result["cc"] == "" and result["model"] != ""):
            p = ""
            q = result["model"].replace("CC", "")
            p = [int(i) for i in q.split() if i.isdigit()]
            result["cc"] = str(p).replace("[", "").replace("]", "")
    except:
        cc = 0

    try:
        if "Address" in keys:
            result["Address"] = result["Address"].replace("Cubic Capacity/Watts", "").replace("Cubic Capacity", "").replace("elephone No", "")

            result["Address"] = result["Address"].split("Online")[-1]
            result["Address"] = result["Address"].split("DO505360600000")[-1]
            result["Address"] = result["Address"].split("C601")[-1]
            result["Address"] = result["Address"].split("Vellicle")[0]
            result["Address"] = result["Address"].split("Registration")[0]
            result["Address"] = result["Address"].split("on Ne")[0]
            result["Address"] = result["Address"].split("on No")[0]
            result["Address"] = result["Address"].replace("!", "", 1).replace("Kamataka", "Karnataka").replace(
                "icles Liability Policy", "").replace("ingistrati", "").replace("Customer GSTIN", "").replace(
                "GUMLAT", "GUJARAT").replace("GUIARAT", "GUJARAT").replace("Customer CSTIN", "")
            # print(result["Address"])
            x = result["Address"].split(',')[0]
            if x.__contains__("Insurance"):
                result["Address"] = result["Address"].replace(x, "")
                result["Address"] = result["Address"].lstrip(', 0 1 2 3 4 5 6 7 8 9 ')

            result["Address"] = result["Address"].lstrip(" ,").lstrip(";")
            if result["gstin"] != "":
                if result["gstin"] in result["Address"]:
                    result["Address"] = result["Address"].replace(result["gstin"], "")

            result["Address"] = result["Address"].lstrip(', 0 1 2 3 4 5 6 7 8 9 ')

            Pattern = re.compile("[0-9]{6}|[0-9]{3}\s[0-9]{3}")  # ^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$")
            x = Pattern.search(result["Address"].replace(" ", ""))
            try:
                result["Pincode"] = x.group()
            except:
                print("Pincode")
            # Pattern = re.compile("(0/91)?[5-9][0-9]{9}")
            # x = Pattern.search(result["Address"].replace(" ", ""))
            # try:
            #     result["Mobile"] = x.group()
            # except:
            #     print("Mobile")


            state = [elem.upper() for elem in state]
            # print(result["Insured Name"])
            for i in state:
                if i in result["Address"].upper():
                    result["CUSTOMER_STATE"] = i
                    # print(result["CUSTOMER_STATE"])
                    break
            try:
                result["Address"] = result["Address"].split(result["CUSTOMER_STATE"])[0] + result["CUSTOMER_STATE"]
                result["Address"] = result["Address"].replace(result["insured name"], "")
                result["Address"] = result["Address"].lstrip(";")
            except:
                print("state")
    except:
        print("Address")

    try:
        ask = ["insured name", "policy no", "email", "nominee name", "nominee relation", "policy issuance date",
               "chassis no", "engine no", "cc", "registration no", "mfg yr", "Address", "Product type", "Period of Insurance Start date", "Period of Insurance End date", "Pincode",
               "CUSTOMER_STATE", "PREVIOUS_INSURER"]  # "mobile", "rto", "make", "model", "hypothecation"

        ask1 = ["insured_name", "previous_policy_number", "email_id", "nominee_for_owner_driver_nominee_name", "nominee_for_owner_driver_nominee_relation", "policy_issuance_date",
                "chassis_no", "engine_no", "cubic_capacity", "registration_no", "mfg_yr", "address", "product_type", "period_of_insurance_start_date", "period_of_insurance_end_date", "pincode",
                "customer_state", "previous_insurer_name"]

        for i in range(len(ask)):
            a = ask[i]
            b = ask1[i]
            result[b] = result[a]
            del result[a]
    except:
        print("keys")

    try:
        ask2 = ["make", "model", "previous_policy_number", "registration_no", "rto", "policy_issuance_date", "chassis_no",
               "cubic_capacity", "mfg_yr", "engine_no", "email_id", "ncb", "address", "period_of_insurance_start_date",
               "period_of_insurance_end_date", "pincode", "mobile", "insured_name", "salutation", "customer_state",
               "nominee_for_owner_driver_nominee_relation", "nominee_for_owner_driver_nominee_name", "hypothecation",
                "financier_name", "financier_branch", "date_of_registration", "source_system", "product_type",
                "previous_policy_type", "previous_insurer_name", "ncb", "gstin"]

        for h in ask2:
            if h not in keys:
                result[h] = ""

    except:
        print("key")

    if result["source_system"] == "":
        result["source_system"] = "OCR"

    del result["gstin"]

    print("Last Line of Routing_Sheet")

    return result