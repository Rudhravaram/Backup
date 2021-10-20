import regex as re
import requests
import time
import pandas as pd
import re
import string
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process
from datetime import datetime
import pandas as pd

def filteritem(string,required_length):
    t = string.split()
    for i in t:
        if len(i)>=required_length:
            return i
        
def magic_reliance(text_json):
    rto_data = pd.read_excel(r'packages/RTO.xlsx')
    rto = pd.DataFrame(rto_data, columns=["RegNo","Place","State","STATE"])
    count=0
    for i in range(len(text_json)):
        print(text_json[i].get('text'))
        print(text_json[i].get('boundingBox'))
        print("######################")
    visited = {}
    result = {}
    z = ""
    new = 0
    for i in range(50):
        if ("RENWEABLE" and "INTIMATION" and "LETTER") in text_json[i].get("text"):
            new = 1
    for i in range(len(text_json)):
        z = text_json[i].get("text")
        bb = text_json[i].get("boundingBox")

        if fuzz.WRatio("Insured Name" , z)>70 and "Insured Name" not in visited:
            try:
                for j in range(i+1, i+5):
                    bx = text_json[j].get("boundingBox")
                    if abs(bx[0]-bb[0]) < 10 and abs(bx[1]-bb[7])<30 and new==0:
                        result["insured_name"] = text_json[j].get("text")
                        visited["Insured Name"] = True
                        break
                if new==1:
                    result["insured_name"] = text_json[i].get("text")[text_json[i].get("text").index(":")+1:]
                    visited["Insured Name"] = True
            except:
                result["insured_name"] = ""
        if fuzz.WRatio("Period of Insurance" , z)>70 and "Period of Insurance" not in visited and new==0:
            try:
                for j in range(i+1, i+5):
                    bx = text_json[j].get("boundingBox")
                    if abs(bx[1]-bb[7]) < 30 and abs(bx[0] - bb[0])<20 and "Period of Insurance" not in visited:
                        t = text_json[j].get("text")
                        print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
                        print(t)
                        t = t[9:]
                        result["period_of_insurance_start_date"] = t[t.index("on")+2:t.index("to")]
                        result["period_of_insurance_end_date"] = t[t.index("of")+2:]
                        visited["Period of Insurance"] = True
                        break
            except:
                pass
        if fuzz.WRatio("Policy Number" , z)>70 and "Policy Number" not in visited:
            try:
                if len(z.replace(":","").strip()) > 16:
                    t = z.strip(":").strip(",").strip("-")
                    t = t.split()
                    if t[-1].isnumeric():
                        result["previous_policy_number"] = t[-1]
                        visited["Policy Number"] = True
                else:
                    for j in range(i+1, i+5):
                        bx = text_json[j].get("boundingBox")
                        if abs(bx[1]-bb[3]) < 35 and abs(bx[7]-bb[5])<35:
                            if "".join(text_json[j].get("text").split()).isnumeric():
                                result["previous_policy_number"] = text_json[j].get("text")
                                visited["Policy Number"] = True
                                break
                if "Policy Number" not in visited:
                    for j in range(i+1, i-6,-1):
                        bx = text_json[j].get("boundingBox")
                        if abs(bx[1]-bb[3]) < 25 and abs(bx[7]-bb[5])<25 and text_json[j].get("text").isnumeric() and bx[0]>bb[2]:
                            result["previous_policy_number"] = text_json[j].get("text")
                            visited["Policy Number"] = True
                            break 
            except:
                result["previous_policy_number"] = ""
        if fuzz.WRatio("Policy Schedule" , z)>70 and "Product Type" not in visited and new==0:
            try:
                if "Two" in z:
                    result["product_type"] = "Two Wheeler"
                if "Two" not in z:
                    result["product_type"] = "Four Wheeler"
                visited["Product Type"] = True
            except:
                result["Product Type"] = ""

        if fuzz.WRatio("Registration", z)>60 and "Registration" not in visited and new==0:
            try:
                for j in range(i+1, len(text_json)):
                    bx = text_json[j].get("boundingBox")
                    if abs(bx[1]-bb[3]) < 20 and abs(bx[7] - bb[5])<20 and bx[0]>bb[2]:
                        result["registration_no"] = text_json[j].get("text")
                        visited["Registration"] = True
                        break
            except:
                result["registration_no"] =  ""
        if fuzz.WRatio("Make / Model" , z)>70 and "Make / Model" not in visited:
            try:
                s=""
                for j in range(i+1, i+6):
                    bx = text_json[j].get("boundingBox")
                    if abs(bx[1]-bb[3]) < 20 and abs(bx[7] - bb[5])<20 and bx[0]>bb[2]:
                        if "CC" in text_json[j].get("text"):
                            if text_json[j].get("text").replace("CC","").replace("HP",'').strip()[:-1]!="":
                                s+=text_json[j].get("text").replace("CC","").replace("HP",'').strip() + " "
                        if "CC" not in text_json[j].get("text"):
                            s+=text_json[j].get("text")+" "
                            # visited["Make / Model"] = True
                            # break
                if s!="":
                    result["Make / Model"] = s
                    visited["Make / Model"] = True
                if "Make / Model" not in visited:
                    for j in range(i-1, i-5,-1):
                        bx = text_json[j].get("boundingBox")
                        if abs(bx[1]-bb[3]) < 20 and abs(bx[7] - bb[5])<20 and bx[0]>bb[2] and "CC" not in text_json[j].get("text"):
                            result["Make / Model"] = text_json[j].get("text")

                            visited["Make / Model"] = True
                            break
            except:
                result["Make / Model"] = ""
                    
        if fuzz.WRatio("Engine No./Chassis No." , z)>80 and "Engine No./Chassis No." not in visited:
            try:
                if z.count("/")==2 and "Date" not in z:
                    t = " ".join(z.split("/")).split()
                    result["engine_no"] = t[-2].strip("/")
                    result['chassis_no'] = t[-1].strip("/")
                    visited["Engine No./Chassis No."] = True
                if "Engine No./Chassis No." not in visited:
                    for j in range(i+1, len(text_json)):
                        bx = text_json[j].get("boundingBox")
                        if abs(bx[1]-bb[3]) < 15 and abs(bx[7]-bb[5])<15 and "Engine No./Chassis No." not in visited:
                            #t = z.split(":")
                            e = text_json[j].get("text").index("/")
                            result["engine_no"] = text_json[j].get("text")[:e]
                            result['chassis_no'] = text_json[j].get("text")[e+1:]
                            visited["Engine No./Chassis No."] = True
                            break
                
            except:
                count+=1
        if fuzz.WRatio("Nominee Name" , z)>90 and len('Nominee Name') < len(z) and "Nominee Name" not in visited:
            try:
                t = z.split(":")
                result["nominee_for_owner_driver_nominee_name"] = t[-1]
                visited["Nominee Name"] = True
            except:
                result["nominee_for_owner_driver_nominee_name"] = ""
        if fuzz.WRatio("Email-ID" , z)>60 and "Email-ID" not in visited:
            try:
                if "@" in z and "Email-ID" not in visited:
                    result["email_id"] = z.split()[-1]
                    visited["Email-ID"] = True
                elif "NA" in z and "Email-ID" not in visited:
                    result["email_id"] = "NA"
                    visited["Email-ID"] = True
                elif "Email-ID" not in visited and z.replace(z[:z.index(":")],"").strip()!="":
                    result["email_id"] = z[z.index(":")+1:]
                    visited["Email-ID"] = True
                elif "Email-ID" not in visited:
                    for j in range(i+1, i+5):
                        bx = text_json[j].get("boundingBox")
                        if abs(bx[1]-bb[3])< 20 and abs(bx[7]-bb[5])<20 and "Email-ID" not in visited:
                            if ".com" in text_json[j].get("text"):
                                result["email_id"] = text_json[j].get("text")
                                visited["Email-ID"] = True
                                break
            except:
                result["email_id"] = ""
            
                
        if fuzz.WRatio("Mobile No" , z)>70 and "Mobile No" not in visited and "Address" in visited:
            try:
                #t = z.strip()
                #t = t.split()
                # for w in t:
                #     w = w.strip().replace(" ","")
                #     if len(w)==10  and w.isnumeric() == True:
                #         result["Mobile No"] = t[-1].replace(":","")
                #         visited["Mobile No"] = True
                if "/" not in z and "&" not in z:
                    result["mobile"] = z[z.index(":"):].replace(":","").replace(",","").replace(".","")
                    visited["Mobile No"] = True
            except:
                for j in range(i+1, i+5):
                    bx = text_json[j].get("boundingBox")
                    if abs(bx[1]-bb[3]) < 20 and abs(bx[7]-bb[5])<20 and bx[0]>bb[2] :
                        if text_json[j].get("text").replace(",",".").isnumeric()==True and "Mobile No" not in visited:
                            result["mobile"] = text_json[j].get("text").replace(",",".")
                            visited["Mobile No"] = True
                            break
        if fuzz.WRatio("Mobile No. of Insured" , z)>70 and "Mobile No. of Insured" not in visited and "Mobile" in z and new ==1:
            try:
                result["mobile"] = z[z.index(":")+1:]
                visited["Mobile No. of Insured"] = True
            except:
                result["mobile"] =""
        if fuzz.WRatio("Email ID of Insured" , z)>70 and "Email ID of Insured" not in visited and new ==1:
            try:
                result["email_id"] = z[z.index(":")+1:]
                visited["Email ID of Insured"] = True
            except:
                result["mobile"] =""
        if fuzz.WRatio("Region Name" , z)>70 and "Region Name" not in visited and new ==1 and "Region" in z:
            try:
                result["region_name"] = z[z.index(":")+1:]
                visited["Region Name"] = True
            except:
                result["region_name"] =""
        if fuzz.WRatio("Branch Code/Name" , z)>70 and "Branch Code/Name" not in visited and new ==1 and "Branch" in z and "Name" in z:
            try:
                result["branch_code/name"] = z[z.index(":")+1:]
                visited["Branch Code/Name"] = True
            except:
                result["branch_code/name"] =""
        if fuzz.WRatio("Communication Address" , z)>70 and "Address" not in visited:
            try:
                string = ""
                temp_count=0
                try:
                    if new==1:
                        string =string +  text_json[i].get("text")[text_json[i].get("text").index(":")+1:] + " "
                except:
                    pass
                for j in range(i+1, len(text_json)):
                    bx = text_json[j].get("boundingBox")
                    if "Mobile" in text_json[j].get("text"):
                        break
                    if abs(bx[0]-bb[0]) < 105 and temp_count<4:
                        string+=text_json[j].get("text") + " "
                        temp_count+=1
                result["address"] = string.replace(",,",",")
                visited["Address"] = True
            except:
                result["address"] = ""

        if fuzz.WRatio("Tax Invoice" , z)>70 and "Date" not in visited:
            try:
                if z.count("/")==2:
                    s = z.split()
                    date = datetime.strptime(str(s[-1].replace(".","").replace(",","")), '%d/%m/%Y').strftime( '%d-%b-%Y')
                    result["date"] = date
                    visited["Date"] = True
            except:
                result["date"] = ""

        if fuzz.WRatio("CC/HP/Watt" , z)>70 and "CC/HP/Watt" not in visited:
            try:
                for j in range(i+1, i+5):
                    bx = text_json[j].get("boundingBox")
                    if abs(bx[1]-bb[3]) < 20 and abs(bx[7]-bb[5])<20 and bb[2]<bx[0] and text_json[j].get("text").isnumeric()==True:
                        result["cubic_capacity"] = text_json[j].get("text")
                        visited["CC/HP/Watt"]  = True
                        break
                if "CC/HP/Watt" not in visited:
                    for j in range(i+1, i-5,-1):
                        bx = text_json[j].get("boundingBox")
                        if abs(bx[1]-bb[3])< 25 and abs(bx[7]-bb[5])<25 and bb[2]<bx[0] and text_json[j].get("text").isnumeric()==True:
                            result["cubic_capacity"] = text_json[j].get("text")
                            visited["CC/HP/Watt"]  = True
                            break

            except:
                result["cubic_capacity"] = ""
        if fuzz.WRatio("Hypothecation/Lease" , z)>70 and "Hypothecation" not in visited:
            try:
                for j in range(i+1, len(text_json)):
                    bx = text_json[j].get("boundingBox")
                    if abs(bx[1]-bb[3] )< 20 and abs(bx[7]-bb[5])<20:
                        result["hypothecation"] = text_json[j].get("text")
                        visited["Hypothecation"] = True
                        break
            except:
                result["hypothecation"] =""
        if fuzz.WRatio( "Mfg Month & Year" , z)>70 and "Mfg Year" not in visited:
            try:
                for j in range(i+1, i+5):
                    bx = text_json[j].get("boundingBox")
                    if abs(bx[1]-bb[3]) < 40 and abs(bx[7]-bb[5])<40 and bx[0]>bb[2] and "-" in text_json[j].get("text"):
                        t = text_json[j].get("text")
                        s = t[t.index("-")+1:]
                        if s.isnumeric()==True and int(s)>1900:
                            result["mfg_yr"] = s
                            visited["Mfg Year"] = True
                            break
                    if "Mfg Year" not in visited:
                        for j in range(i+1, i-5,-1):
                            bx = text_json[j].get("boundingBox")
                            if abs(bx[1]-bb[3]) < 40 and abs(bx[7]-bb[5])<40 and bx[0]>bb[2] and "-" in text_json[j].get("text"):
                                t = text_json[j].get("text")
                                s = t[t.index("-")+1:]
                                if s.isnumeric()==True and int(s)>1900:
                                    result["mfg_yr"] = s
                                    visited["Mfg Year"] = True
                                    break
            except:
                result["mfg_yr"] = ""

        if fuzz.WRatio("RTO Location" , z)>70 and "RTO Location" not in visited:
            try:
                for j in range(i+1, i+5):
                    bx = text_json[j].get("boundingBox")
                    if abs(bx[1]-bb[3] )< 15 and abs(bx[7]-bb[5])<15:
                        result["rto"] = text_json[j].get("text")
                        visited["RTO Location"] = True
                        break
                    else:
                        if "rto" not in result or "Total" in result["rto"]:
                            for j in range(i-1, i-5,-1):
                                bx = text_json[j].get("boundingBox")
                                if abs(bx[1]-bb[3] )< 15 and abs(bx[7]-bb[5])<15:
                                    if text_json[j].get("text").split()[0] in " ".join(rto["State"].unique()).upper():
                                        result["rto"] = text_json[j].get("text")
                                        visited["RTO Location"] = True
                                        break
            except:
                result["rto"] = ""
        if fuzz.WRatio("Registration Date", z)>87 and "Registration Date" not in visited and new==1:
            try:
                for j in range(i+1, i+5):
                    bx = text_json[j].get("boundingBox")
                    if abs(bx[1]-bb[3]) < 20 and abs(bx[7] - bb[5])<20 and bx[0]>bb[2]:
                        result["registration_date"] = text_json[j].get("text")
                        visited["Registration Date"] = True
                        break
            except:
                result["registration_date"] =  ""
        if fuzz.WRatio("Place of Registration", z)>87 and "Place of Registration" not in visited and new==1:
            try:
                for j in range(i+1, i+5):
                    bx = text_json[j].get("boundingBox")
                    if abs(bx[1]-bb[3]) < 20 and abs(bx[7] - bb[5])<20 and bx[0]>bb[2]:
                        result["place_of_registration"] = text_json[j].get("text")
                        visited["Place of Registration"] = True
                        break
            except:
                result["place_of_registration"] =  ""
        if fuzz.WRatio("Chassis Number", z)>87 and "Chassis Number" not in visited and new==1:
            try:
                for j in range(i+1, i+5):
                    bx = text_json[j].get("boundingBox")
                    if abs(bx[1]-bb[3]) < 20 and abs(bx[7] - bb[5])<20 and bx[0]>bb[2]:
                        result["chassis_no"] = text_json[j].get("text")
                        visited["Chassis Number"] = True
                        break
            except:
                result["chassis_no"] =  ""
        if fuzz.WRatio("Engine Number", z)>87 and "Engine Number" not in visited and new==1:
            try:
                for j in range(i+1, i+5):
                    bx = text_json[j].get("boundingBox")
                    if abs(bx[1]-bb[3]) < 20 and abs(bx[7] - bb[5])<20 and bx[0]>bb[2]:
                        result["engine_no"] = text_json[j].get("text")
                        visited["Engine Number"] = True
                        break
            except:
                result["engine_no"] =  ""
        if fuzz.WRatio("Engine Number", z)>87 and "Engine Number" not in visited and new==1:
            try:
                for j in range(i+1, i+5):
                    bx = text_json[j].get("boundingBox")
                    if abs(bx[1]-bb[3]) < 20 and abs(bx[7] - bb[5])<20 and bx[0]>bb[2]:
                        result["engine_no"] = text_json[j].get("text")
                        visited["Engine Number"] = True
                        break
            except:
                result["engine_no"] =  ""
        if fuzz.WRatio("Manufacturing Year", z)>87 and "Manufacturing Year" not in visited and new==1:
            try:
                for j in range(i+1, i+5):
                    bx = text_json[j].get("boundingBox")
                    if abs(bx[1]-bb[3]) < 20 and abs(bx[7] - bb[5])<20 and bx[0]>bb[2]:
                        result["mfg_yr"] = text_json[j].get("text")
                        visited["Manufacturing Year"] = True
                        break
            except:
                result["mfg_yr"] =  ""
        if fuzz.WRatio("Registration Number", z)>87 and "Registration Number" not in visited and new==1:
            try:
                for j in range(i+1, i+5):
                    bx = text_json[j].get("boundingBox")
                    if abs(bx[1]-bb[3]) < 20 and abs(bx[7] - bb[5])<20 and bx[0]>bb[2]:
                        result["registration_no"] = text_json[j].get("text")
                        visited["Registration Number"] = True
                        break
            except:
                result["registration_no"] =  ""
        if fuzz.WRatio("Vehicle Details", z)>87 and "Vehicle Details" not in visited and new==1:
            try:
                for j in range(i+1, i+5):
                    bx = text_json[j].get("boundingBox")
                    if abs(bx[1]-bb[3]) < 20 and abs(bx[7] - bb[5])<20 and bx[0]>bb[2]:
                        result["make"] = text_json[j].get("text").split()[0]
                        result["model"] = " ".join(text_json[j].get("text").split()[1:])
                        visited["Vehicle Details"] = True
                        break
            except:
                result["make"] =  ""
                result["model"] =  ""
    try:
        salutation = result["insured_name"].split()[0].replace(".","").replace(",","")
        if salutation=="MR" or salutation=="MRS" or salutation=="MISS" or salutation=="Mr" or salutation=="Mrs" or salutation=="M/S" or (salutation.upper().startswith("MR") and len(salutation)<4):
            result["salutation"] = salutation
    except:
        result["salutation"] = ""
    try:
        if len(result["salutation"])>3:
            result["salutation"] = salutation.split()[0]
    except:
        pass
    try:
        if "AUTO" in result["Make / Model"]:
            result["product_type"] = "3 Wheeler"
    except:
        result["product_type"] = ""
    count = 0
    try:
        if visited["RTO Location"] != True:
            result["rto"] = rto[rto["RegNo"] == result["registration"][:4]]["State"].values[0] + " - " + rto[rto["RegNo"] ==result["registration"][:4]]["Place"].values[0]
    except:
        pass
    try:
        vlist = ["Hero","Honda", "Bajaj","Yamaha","Royal Enfield","TVS","Hundai","Tata","Mahindra","Ford","Mercedes","Totota"]
        if "Make / Model" in visited:
            for j in vlist:
                if result["Make / Model"].upper().__contains__(j.upper()):
                    result["make"] = j
    except:
        pass
    try:
        result["date_of_registration"] = result["date"]
        result.pop("date")
    except:
        pass
    try:
        if "Make / Model" in visited:
            index = result["Make / Model"].index("/")
            result["make"] = result["Make / Model"][:index]
            result["model"] = result["Make / Model"][index+1:]
            result.pop("Make / Model")
    except:
        if "make" not in result:
            result["make"] = ""
        result["model"] = result["Make / Model"]
        result.pop("Make / Model")
    result["hypothecation"] = "NA"
    try:
        address_string = result["address"].replace("."," ").replace(","," ").replace("-"," ").split()
        # print(rto["STATE"].unique())
        for i in range(len(address_string)):
            if address_string[i] in rto["STATE"].unique():
                result["customer_state"] = address_string[i]
    except:
        pass
    try:
        address_string = result["address"].replace("."," ").replace(","," ").replace("-"," ").split()
        if "customer_state" not in result:
            result["customer_state"]=result["rto"][:result["rto"].index("-")].upper()
    except:
        pass
    try:
        address_string = result["address"].replace("."," ").replace(","," ").replace("-"," ").split()
        for i in address_string:
            if i.strip().isnumeric()==True and len(i.strip())==6:
                result["pincode"] = i
    except:
        pass
    result["source_system"] = "OCR"
    result["previous_insurer_name"] = "Reliance General Insurance Company Limited"
    try:
        key_list = ["address","chassis_no","cubic_capacity","customer_state","date_of_registration","email_id","engine_no","financier_branch","financier_name","hypothecation","insured_name",
        "make","mfg_yr","mobile","model","ncb","nominee_for_owner_driver_nominee_name","nominee_for_owner_driver_nominee_relation","period_of_insurance_end_date",
        "period_of_insurance_start_date","pincode","policy_issuance_date","previous_insurer_name","previous_policy_number","previous_policy_type","product_type",
        "registration_no","rto","salutation","source_system"]
        for i in key_list:
            if i not in result:
                result[i] = ""
    except:
        pass
    if "Nominee" in result["nominee_for_owner_driver_nominee_name"]:
        result["nominee_for_owner_driver_nominee_name"] = ""
    x = 1
    for key in result.keys():
        try:
            print(str(x) + " " + key + " -> " + str(result[key]))
        except:
            print(str(x) + " " + key)
            print(result[key])
        x = x + 1

    return result


