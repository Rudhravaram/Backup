import regex as re
import os
from packages.hdfc.pdf.Interpretation import magic
import pandas as pd
from fuzzywuzzy import fuzz

# def pdftotext(path, output_file):
#     #Generate a text rendering of a PDF file in the form of a list of lines.
#     args = ['pdftotext', '-layout', path, output_file]
#     cp = subprocess.run(
#       args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
#       check=True, text=True
#     )
#     return cp.stdout


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

def final_run(z, s):

    def clean(t):
        return t.strip(" . , : ; - _ ! \n ' ' + | / =  , , , , , , ,").replace("`", "")

    # result = magic(z, "T2")
    k = 0
    gvw = 0
    lcc = 0
    wheel = 0
    for i in range(25):
        if z[i].upper().__contains__("TWO WHEELER"):#change
            wheel = 1
        if z[i].__contains__("Make") and z[i].__contains__("Model") and z[i].__contains__("Engine"):
            k = 1
        if z[i].__contains__("GVW"):
            gvw = 1
        if z[i].__contains__("LCC"):
            lcc = 1

    # # try:
    # if k == 1:
    #     if "GVW" in s and not "LCC" in s:
    #         print("T2-1")
    #         result = magic(z, "T2-1")
    #     elif "GVW" in s and "LCC" in s:
    #         print("T1-1")
    #         result = magic(z, "T1-1")
    #     else:
    #         result = magic(z, "T2")
    #         print("T2")
    # else:
    #     result = magic(z, "T1")
    #     print("T1")
    # # except:
    # #     print("Interpretation")

    if k == 1:
        if gvw == 1 and not lcc == 1:
            print("T2-1")
            result = magic(z, "T2-1")
        elif gvw == 1 and lcc == 1:
            print("T1-1")
            result = magic(z, "T1-1")
        else:
            result = magic(z, "T2")
            print("T2")
    else:
        result = magic(z, "T1")
        print("T1")

    try:
        keys = result.keys()
    except:
        result = {}
        print("no result")

    try:
        if "NCB" in keys and not result["NCB"].isalpha():
            result["NCB"] = result["NCB"].split("%")[1].strip('( )').split()[0]
        else:
            result["NCB"] = ""
        if result["NCB"].isalpha():
            result["NCB"] = ""
    except:
        result["NCB"] = ""
        print("NCB")

    try:
        if "Period of Insurance" in keys:
            result["Period of Insurance start date"] = result["Period of Insurance"].split("To")[0].strip(' ,').replace("From", "")
            result["Period of Insurance End date"] = result["Period of Insurance"].split("To")[1].strip(' ,')
            if result["Period of Insurance End date"].split(",")[-1].strip().isnumeric():
                x = result["Period of Insurance End date"].split(",")[-1]
                result["Period of Insurance End date"] = result["Period of Insurance End date"].replace(x, "").strip(' ,')
            del result["Period of Insurance"]
            if result["Period of Insurance start date"].__contains__("Insurance"):
                result["Period of Insurance start date"] = result["Period of Insurance start date"].split("Insurance")[0]
    except:
        print("Period of Insurance")
        del result["Period of Insurance"]

    try:
        if "Insured Name" in keys:
            result["Salutation"] = result["Insured Name"].split(" ")[0]
            if len(result["Salutation"]) > 3:
                result["Salutation"] = ""
    except:
        print("Insured Name")

    state = ["Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chhattisgarh", "Delhi", "Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Orissa","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu","Lakshadweep","National Capital Territory of Delhi","Puducherry"]
    state = [elem.upper() for elem in state]

    try:
        if "Address" in keys:
            # print(result["Address"])
            result["Address"] = result["Address"].lstrip(', 0 1 2 3 4 5 6 7 8 9 ')
            Pattern = re.compile("[0-9]{6}|[0-9]{3}\s[0-9]{3}")  # ^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$")
            x = Pattern.search(result["Address"])
            try:
                result["Pincode"] = x.group()
            except:
                print("Pincode")
            Pattern = re.compile("(0/91)?[6-9][0-9]{9}")
            x = Pattern.search(result["Address"])
            try:
                result["Mobile"] = x.group()
            except:
                print("Mobile")
            result["Insured Name"] = result["Address"].split(',')[0]
            result["Salutation"] = result["Insured Name"].split(" ")[0]
            if len(result["Salutation"]) > 3:
                result["Salutation"] = ""
            result["Address"] = result["Address"].replace(result["Insured Name"], "").lstrip(', ')
            # print(state)
            for i in state:
                if i.replace(" ","") in result["Address"].replace(",", "").replace(" ",""):
                    result["CUSTOMER_STATE"] = i
                    # print(result["CUSTOMER_STATE"])
                    break
            try:
                result["Address"] = result["Address"].split(result["CUSTOMER_STATE"])[0] + result["CUSTOMER_STATE"]
            except:
                print("state")
            result["Address"] = result["Address"].replace("Cubic Capacity/Watts", "")
    except:
        print("Address")

    try:
        if "Engine No." in keys:
            result["Engine No."] = result["Engine No."].split("     ")[0]
    except:
        print("Engine No.")

    try:
        if "Model" in keys and "Variant" in result["Model"]:
            x = result["Model"].split("           ")
            zx = []
            for z in x:
                if z is not "":
                    zx.append(z)
            result["Model"] = zx[1]
    except:
        print("Model")

    try:
        if "Registration No" in keys:
            result["Registration No"] = result["Registration No"].split("           ")[0]
    except:
        print("Registration No")

    try:
        if "RTO" in keys:
            result["RTO"] = result["RTO"].split('       ')[0]
    except:
        print("RTO")

    try:
        if "Nominee for Owner driver" in keys:
            result["Nominee for Owner driver (Nominee Relation)"] = result["Nominee for Owner driver"].split()[-1]
            result["Nominee for Owner driver (Nominee Name)"] = result["Nominee for Owner driver"].replace(result["Nominee for Owner driver (Nominee Relation)"], "")
            del result["Nominee for Owner driver"]
    except:
        print("Nominee")
        del result["Nominee for Owner driver"]

    try:
        if "TABLE" in keys:
            # print(result["TABLE"])
            # try:
            # print(result["TABLE"])
            # print("hahahaha")
            for x in result["TABLE"][0].keys():
                if x in ["License Carrying Capacity", "Body Type", "GVW", "Private/Public Carrier"]:
                    continue
                result[x] = result["TABLE"][0][x]
            # except:
            #     print(result["TABLE"])
            #     print("Table")
            del result["TABLE"]
    except:
        print("TABLE")

    try:
        if "Place of Supply" in keys:
            # print(result["Place of Supply"])
            result["Place of Supply"] = result["Place of Supply"].replace("Place of Supply", "")
            Pattern = re.compile("[0-9]{6}|[0-9]{3}\s[0-9]{3}")  # ^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$")
            x = Pattern.search(result["Place of Supply"])
            try:
                result["Pincode"] = x.group()
            except:
                print("Pincode")
            # print(result["Place of Supply"].replace(",", "").replace(" ", ""))
            for i in state:
                if i.replace(" ","") in result["Place of Supply"].replace(",", "").replace(" ",""):
                    result["CUSTOMER_STATE"] = i
                    # print(result["CUSTOMER_STATE"])
                    break
    except:
        print("Place of Supply")

    try:
        if "Policy No." in keys:
            result["Policy No."] = result["Policy No."].strip('A B C D E F G H I J K L M N O P Q R S T U V W X Y Z . a b c d e f g h i j k l m n o p q r s t u v w x y z')
    except:
        print("Policy No.")

    for key in result.keys():
        result[key] = str(result[key]).strip('. , ; / : |')

    if "Email id" in keys:
        result["Email ID"] = result["Email id"]
        del result["Email id"]

    if "Registration No." in keys:
        result["Registration No"] = result["Registration No."]
        del result["Registration No."]

    if "Engine No" in keys:
        result["Engine No."] = result["Engine No"]
        del result["Engine No"]

    if "Place of Supply" in keys:
        result["Address"] = result["Place of Supply"]
        del result["Place of Supply"]

    if wheel == 0:   #shan
        result["Product type"] = "Four Wheeler"
    else:
        result["Product type"] = "Two Wheeler"

    ask = ["Make", "Model", "Policy No.", "Registration No", "RTO", "Policy Issuance Date", "Chassis No", "Cubic Capacity",
           "Mfg Yr", "Engine No.", "Email ID", "NCB", "Address", "Period of Insurance start date", "Period of Insurance End date",
           "Pincode", "Mobile", "Insured Name", "Salutation", "CUSTOMER_STATE", "Nominee for Owner driver (Nominee Relation)",
           "Nominee for Owner driver (Nominee Name)", "HYPOTHECATION", "FINANCIER_NAME", "FINANCIER_BRANCH", "Date of Registration",
           "Source System", "Product type", "Previous Policy Type"]

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

    return result
