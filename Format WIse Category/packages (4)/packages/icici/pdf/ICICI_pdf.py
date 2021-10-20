import subprocess
import os
import re
import pandas as pd
from shutil import copyfile
from openpyxl import load_workbook
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process


def icici_pdf(s, z):
    df1 = pd.read_excel(r"packages/icici/pdf/ICICI.xlsx")
    df = pd.DataFrame(df1, columns=["Key", "Item", "Value", "Down", "Breaking", "State", "Rest"])
    print(df)
    print(s)
    def clean(t):
        return t.strip(" . , : ; - _ ! \n ' ' + | / =  , , , , , , ,").replace("`", "")
    result = {}
    visited={}
    i = 0
    j=0
    page=1
    first = []
    for a in df["Key"].unique():
        first.append(a.split()[0])
    for a in range(len(s)):
        if ("CERTIFICATE" and "OF" and "INSURANCE") in s[a]:
            page=2
            for b in range(a+1,a+5):
                if "ICICI" not in s[a] and "Two" in s[b]:
                    result["product_type"] = "Two Wheeler"
                if "ICICI" not in s[a] and "Car" in s[b]:
                    result["product_type"] = "Four Wheeler"
                if "ICICI" not in s[a] and "Goods" in s[b]:
                    result["product_type"] = "Four Wheeler"                
            break
    while i < len(s):
        for t in range(len(df["Key"])):
            if df["Key"][t] in s[i] and df["Key"][t] not in visited:
                print("i came here")
                # result[df["Key"][t]] = s[i].replace(df["Key"][t],"").strip()
                # visited[df["Key"][t]] = True
                ind = s[i][s[i].index(df["Key"][t]):].replace(df["Key"][t],"").strip().split()
                text=""
                for a in range(len(ind)):
                    if ind[a] in list(first) or ind[a] in df["Breaking"].unique():
                        break
                    text+= ind[a].strip()+" "
                result[df["Item"][t]] = text[1:].strip() if text[0]==":" else text
                text=""
                visited[df["Key"][t]] = True
        if ("CERTIFICATE" and "OF" and "INSURANCE") in s[i]:
            break
        if "Date" in s[i] and "address" not in visited and "Ref." in s[i-1]:# and "insured_name" in visited:
            i+=2
            address=""
            count=0
            for j in range(i,len(s[i])):
                count+=1
                if "Mobile" in s[j] or count>6 or len(address)>100:
                    result["address"] = address
                    visited["address"] = True
                    break
                address+=s[j].strip()+" "
            result["address"] = address
            visited["address"] = True
        i+=1

    if page==2:
        i=0
        while i<len(s):
            key = {}
            temp_dict = {}
            for t in range(len(df["Key"])):
                # if "Age" in s[i] and "age" not in visited:
                #     result["age"] = s[i].replace(":","").replace("Age","").strip().split()[0]
                #     visited["age"] = True
                try:
                    if df["Key"][t] in s[i] and df["Key"][t] not in visited and df["Key"][t] not in df["Down"].unique():
                        ind = s[i][s[i].index(df["Key"][t]):].replace(df["Key"][t],"").strip().split()
                        text=""
                        for a in range(len(ind)):
                            if ind[a] in list(first) or ind[a] in df["Breaking"].unique() :
                                break
                            text+= ind[a].strip()+" "
                        result[df["Item"][t]] = text[1:].strip() if text[0]==":" else text
                        text=""
                        visited[df["Key"][t]] = True
                    if "Registration No." in s[i] and "Engine" in s[i]:
                        item = ["Registration","CC/KW","Make","Model","Type of","Chassis No","Engine No","Mfg Yr"]
                        for w in range(len(item)):
                            if item[w] in s[i]:
                                key[item[w]] = s[i].index(item[w])
                        for d in range(i+2,i+5):
                            if "Premium Details" in s[d] or "Vehicle IDV" in s[d] or ind[a] in df["Breaking"].unique():
                                break
                            w = s[d].split("  ")
                            for l in range(len(w)):
                                if w[l] != "":
                                    temp_dict[w[l]] = s[d].index(w[l])
                except:
                    pass
            for d in range(len(key)):
                s=""
                if item[d] not in visited:
                    try:
                        for e in range(len(temp_dict)):
                            if abs(list(key.values())[d]-list(temp_dict.values())[e])<6:
                                s+= list(temp_dict.keys())[e]
                            result["_".join(list(key)[d].split()).lower()]  = s.replace("\n","")
                            if "_".join(list(key)[d].split()).lower()=="mfg_yr":
                                t = s.replace("\n","").strip().split()
                                try:
                                    if len(t[0])==4:
                                        result["mfg_yr"] = t[0]
                                        visited["mfg_yr"] = True
                                        break
                                    if len(t[-1])==4:
                                        result["mfg_yr"] = t[-1]
                                        visited["mfg_yr"] = True
                                        break
                                except:
                                    pass
                    except:
                        pass

            i+=1
    if "type_of" in result:
        #result["type_of_body"] = result["type_of"]
        result.pop("type_of")
    if "trailer_Chassis" in result:
        result["trailer_chassis_no"] = result["trailer_chassis"]
        result.pop("trailer_chassis")   
    if "Product Code" in result:
        try:
            result["product_code"] = result["Product Code"].split()[0]
        except:
            pass
    if "vehicle_make/model" in result:
        result["make"] = result["vehicle_make/model"].split("/")[0]
        result["model"] = result["vehicle_make/model"].split("/")[-1]
        result.pop("vehicle_make/model")
    if "period_of_insurance" in result:
        try:
            t = result["period_of_insurance"].replace("-","").replace("Damage","").replace("Own","").split("to")[0].strip().replace(",","").split()
            result["period_of_insurance_start_date"] = t[1]+"-" +t[0]+"-" + t[-1]
            t = result["period_of_insurance"].split("to")[-1].strip().replace(",","").split()
            result["period_of_insurance_end_date"] = t[1]+"-" +t[0]+"-" + t[-1]
            result.pop("period_of_insurance")
        except:
            pass
    if "policy_issued_on" in result:
        t = result["policy_issued_on"].replace(",","").replace("-"," ").strip().split()
        result["policy_issued_on"] = t[1]+"-" +t[0]+"-" + t[-1]
    if "policy_issuance_date" in result:
        t = result["policy_issuance_date"].replace(",","").replace("-"," ").strip().split()
        result["policy_issuance_date"] = t[1]+"-" +t[0]+"-" + t[-1]
    if "date_of_registration" in result:
        t = result["date_of_registration"].replace(",","").replace("-"," ").strip().split()
        result["date_of_registration"] = t[1]+"-" +t[0]+"-" + t[-1]     
    if "cc/kw" in result:
        result["cubic_capacity"] = result["cc/kw"]
        result.pop("cc/kw")
    if "address" in result:
        try:
            for a in range(len(df["State"])):
                if df["State"][a].upper() in result["address"].upper():
                    result["customer_state"] = df["State"][a].upper()
                    break
            t = result["address"].split()
            for i in range(len(t)):
                if len(t[i])==6 and t[i].isnumeric()==True:
                    result["pincode"] = t[i]
                    break
        except:
            pass
    try:
        if "which" in result["policy_no"]:
            result["policy_no"] = result["policy_no"][:result["policy_no"].index("which")]
    except:
        pass
    result["ncb"] = ""
    result["previous_insurer_name"] = "ICICI Lombard General Insurance Company Limited (ICICI Lombard)"
    if "seating_capacity" not in result:
        try:
            if int(result["seating_capacity"])==2:
                result["product_type"] = "Two Wheeler"
            if int(result["seating_capacity"])>2:
                result["product_type"] = "Four Wheeler"
        except:
            pass
    if "registration" in result.keys():
        result["registration_no"] = result["registration"]
        result.pop("registration")
    try:
        result.pop("seating_capacity")
    except:
        pass
    try:
        salutation = result["insured_name"].split()[0].replace(".","").replace(",","")
        if salutation=="MR" or salutation=="MRS" or salutation=="MISS" or salutation=="Mr" or salutation=="Mrs" or salutation=="M/S" or (salutation.upper().startswith("MR") and len(salutation)<4):
            result["salutation"] = salutation
    except:
        result["salutation"] = ""
    if "satutation" not in result:
        result["salutation"] = ""
    result["source_system"] = "OCR"
    result["previous_policy_type"] = ""
    for a in range(len(df["Rest"])):
        if df["Rest"][a] not in result:
            result[df["Rest"][a]] = ""
    return result
