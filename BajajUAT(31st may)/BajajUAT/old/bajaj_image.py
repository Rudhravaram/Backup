import pandas as pd
from fuzzywuzzy import fuzz

def filteritem(string,required_length):
    t = string.split()
    for i in t:
        if len(i)>=required_length:
            return i

def bajaj(text_json):
    df1 = pd.read_excel(r"packages/bajaj/Bajaj.xlsx")
    df = pd.DataFrame(df1, columns=["Right","Value","Key","Exclude","Rest","Down", "Key1"])
    result={}
    visited={}
    j=0
    x = 0
    i=0
    while i<len(text_json):
        try:
            if fuzz.WRatio("Policy Number" , text_json[i].get('text'))>85  and "policy_no" not in visited:
                bb=text_json[i].get("boundingBox")
                for j in range(i+1,i+5):
                    bx = text_json[j].get("boundingBox")
                    if abs(bx[1]-bb[3]) < 25 and abs(bx[7] - bb[5])<25 and bx[0]>bb[2] and text_json[j].get('text').count("-")==4:
                        result["policy_no"] = text_json[j].get('text')
                        visited["policy_no"] = True
                        break
            if "policy_no" not in visited:
                for j in range(i-1,i-5,-1):
                    bx = text_json[j].get("boundingBox")
                    if abs(bx[1]-bb[3]) < 20 and abs(bx[7] - bb[5])<20 and bx[0]>bb[2] and text_json[j].get('text').count("-")==4:
                        result["policy_no"] = text_json[j].get('text')
                        visited["policy_no"] = True
                        break
        except:
            pass
            # if "insured_name" in result:
            #     bb=text_json[i-1].get("boundingBox")
            #     s=""
            #     count=0
            #     for j in range(i,i+25):
            #         bx = text_json[j].get("boundingBox")
            #         print(text_json[i].get('text'))
            #         if abs(bx[1]-bb[7]) < 260 and abs(bx[3] - bb[5])<260 and abs(bb[0]-bx[0])<20 and count<7 and text_json[j].get('text') not in df["Exclude"].unique():
            #             s+=" " +text_json[j].get('text')
            #             count+=1
            #         if "Geographical" in text_json[j].get('text'):
            #             break
            #     result["address"] = s
            #     visited["address"] = True
        if fuzz.WRatio("Insured Name", text_json[i].get('text'))>80 and "insured_name" not in visited:
                bb=text_json[i].get("boundingBox")
                try:
                    for j in range(i+1, len(text_json)):
                        bx = text_json[j].get("boundingBox")
                    if abs(bx[1]-bb[3]) < 20 and abs(bx[7] - bb[5])<20 and bx[0]>bb[2] and "-" not in text_json[j].get("text"):
                        result["insured_name"] = text_json[j].get("text").replace("Zone","")
                        visited["insured_name"] = True
                        break
                except:
                    result["insured_name"] =  ""
        if fuzz.WRatio("Policy Issued on", text_json[i].get('text'))>87 and "Policy Issued on" not in visited:
            bb=text_json[i].get("boundingBox")
            try:
                for j in range(i+1, len(text_json)):
                    bx = text_json[j].get("boundingBox")
                    if abs(bx[1]-bb[3]) < 20 and abs(bx[7] - bb[5])<20 and bx[0]>bb[2]:
                        result["policy_issuance_date"] = text_json[j].get("text")
                        visited["Policy Issued on"] = True
                        break
            except:
                result["policy_issuance_date"] =  ""
        if fuzz.WRatio("Vehicle Type", text_json[i].get('text'))>60 and "Vehicle Type" not in visited:
            bb=text_json[i].get("boundingBox")
            try:
                for j in range(i+1, len(text_json)):
                    bx = text_json[j].get("boundingBox")
                    if abs(bx[1]-bb[3]) < 20 and abs(bx[7] - bb[5])<20 and bx[0]>bb[2]:
                        result["Vehicle Type"] = text_json[j].get("text")
                        visited["Vehicle Type"] = True
                        break
            except:
                result["Vehicle Type"] =  ""
        if fuzz.WRatio("Period of Insurance", text_json[i].get('text'))>87 and "Period of Insurance" not in visited:
            bb=text_json[i].get("boundingBox")
            try:
                s=""
                if "From" in text_json[i].get('text'):
                    s+=text_json[i].get('text')
                for j in range(i, i+7):
                        bx = text_json[j].get("boundingBox")
                        if abs(bx[1]-bb[3]) < 20 and abs(bx[7] - bb[5])<20 and bx[0]>bb[2]:
                            if "From"  in text_json[j].get('text') or "To" in text_json[j].get('text')  or "Midnight" in text_json[j].get('text'):
                                s+=text_json[j].get('text')+ " "
                        result["Period of Insurance"] = s
                        visited["Period of Insurance"] = True
            except:
                result["Period of Insurance"] =  ""
        # if  fuzz.WRatio("Policy Period", text_json[i].get('text'))>88 and "Period of Insurance" not in visited:
        #     bb=text_json[i].get("boundingBox")
        #     try:
        #         s=""
        #         for j in range(i+1,i+7):
        #             if "From" in text_json[j].get('text') or "To" in text_json[j].get('text'):
        #                 s=s+text_json[j].get('text')+" "
        #         result["Period of Insurance"] = s
        #         visited["Policy Period"] = True
        #     except:
        #         result["Period of Insurance"] =  ""
        if  fuzz.WRatio("Place of Supply/State", text_json[i].get('text'))>87 and "customer_state" not in visited:
            bb=text_json[i].get("boundingBox")
            try:
                if "-" in text_json[i].get('text') and "No." not in text_json[i].get('text') and "Code" not in text_json[i].get('text'):
                    result["customer_state"] = text_json[i].get('text').split()[-1]
                visited["customer_state"] =True
                if "-" not in text_json[i].get('text') and "No." not in text_json[i+1].get('text') and "Code" not in text_json[i].get('text'):
                    result["customer_state"] = text_json[i+1].get('text').split("-")[-1]
                    visited["customer_state"] =True
            except:
                result["customer_state"] =  ""
        # if fuzz.WRatio("STATE CODE / NAME", text_json[i].get('text'))>85  and "customer_state" not in visited:
        #     bb=text_json[i].get("boundingBox")
        #     try:
        #         if "-" in text_json[i].get('text') and "No." not in text_json[i].get('text') and "Code" not in text_json[i].get('text'):
        #             result["customer_state"] = text_json[i].get('text').split()[-1]
        #             visited["customer_state"] =True
        #         if "-" not in text_json[i].get('text') and "No." not in text_json[i+1].get('text') and "Code" not in text_json[i].get('text'):
        #             result["customer_state"] = text_json[i+1].get('text').split()[-1]
        #             visited["customer_state"] =True
        #     except:
        #         result["customer_state"] =  ""
        if fuzz.WRatio("Insured Address", text_json[i].get('text'))>86 and "address" not in result:
            bb=text_json[i].get("boundingBox")
            try:
            #if result["address"][-1].isnumeric()!=True:
                s=""
                count=0
                for j in range(i+1, i+7):
                    bx = text_json[j].get("boundingBox")
                    if bx[0]>bb[2] and count<6 and text_json[j].get("text") not in df["Exclude"].unique() and "Policy" not in text_json[j].get("text") and bx[0]<400:
                        s+= text_json[j].get("text")+" "
                        count+=1
                    if s.strip()[-1].isnumeric()==True:
                        break
                result["address"] =s
                visited["address"] = True
            except:
                result["address"] =  ""
        try:
            for a in range(len(df["Down"])):
                if fuzz.WRatio(text_json[i].get('text') , df["Down"][a])>86 and df["Key1"][a] not in visited:
                    for j in range(i+1,i+15):
                        if abs(text_json[j].get('boundingBox')[1]-text_json[i].get('boundingBox')[7])<100 and abs(text_json[j].get('boundingBox')[3]-text_json[i].get('boundingBox')[5])<100 and abs(text_json[j].get('boundingBox')[0]-text_json[i].get('boundingBox')[0])<30 and text_json[j].get('text') not in df["Exclude"].unique() and df["Key1"][a] not in visited:
                            result[df["Key1"][a]] = text_json[j].get('text')
                            if df["Key1"][a]=="mfg_yr" and text_json[j].get('text').isnumeric()==True and 'mfg_yr' not in result:
                                if int(text_json[j].get('text'))<1980:
                                    result["mfg_yr"] =text_json[j+1].get('text')
                            if "make" in result:
                                if result["make"].isdigit():
                                    break
                            for q in range(j+1,j+7):
                                if abs(text_json[q].get('boundingBox')[1]-text_json[j].get('boundingBox')[7])<20 and abs(text_json[j].get('boundingBox')[0]-text_json[q].get('boundingBox')[0])<40 and text_json[q].get('text') not in df["Exclude"].unique():
                                    result[df["Key1"][a]]+= " "+text_json[q].get('text')
                                    break

                            visited[df["Key1"][a]] = True
        except:
            pass
        try:
            if "Place of Supply" in text_json[i].get('text') and "No." not in text_json[i].get('text') and "customer_state" not in result and "Code" not in text_json[i].get('text'):
                result["customer_state"] = text_json[i].get('text').split()[-1]
        except:
            pass
        if fuzz.WRatio("SCHEDULE OF PREMIUM",text_json[i].get('text'))>90:
            break
        i+=1
    if "address" in result:
        try:
            t= result["address"].replace(","," ").replace("."," ").replace("-"," ").split()
            for d in range(len(t)):
                if t[d].isdigit() and len(t[d].strip())==6:
                    result["pincode"] = t[d]
        except:
            pass
    if "policy_issuance_date" in result:
        try:
            t = result["policy_issuance_date"].index("-")
            result["policy_issuance_date"] = result["policy_issuance_date"][t-2:t+8].strip()
        except:
            pass  
    if "Period of Insurance" in result:
        try:
            t= result["Period of Insurance"].replace("From"," ").replace("To"," ").replace(":","").replace("Midnight","").strip().split()
            for w in range(len(t)):
                if t[w].count("-")>=1 and len(t[w])>2:
                    result["period_of_insurance_start_date"] = t[w]
            for w in t[::-1]:
                if w.count("-")>=1 and len(w)>2:
                    result["period_of_insurance_end_date"] = w
            if result["period_of_insurance_end_date"]==result["period_of_insurance_start_date"]:
                t = result["period_of_insurance_end_date"].strip().split("-")
                result["period_of_insurance_start_date"] = str(int(t[0])+1)+"-"+str(t[1])+"-"+str(int(t[-1])-1)
        except:
            pass       
    if "Vehicle Type" in result:
        try:
            if "GOODS" in result["Vehicle Type"].upper() or "CAR" in result["Vehicle Type"].upper() or "4" in result["Vehicle Type"]:
                result["product_type"] = "Four Wheeler"
            if "TWO" in result["Vehicle Type"].upper() or "2" in result["Vehicle Type"].upper():
                result["product_type"] = "Two Wheeler"  
            result.pop("Vehicle Type")             
        except:
            pass
    if "sub_type" in result:
        if "BUS" in result["sub_type"] or "PICK UP" in result["sub_type"]:
            result["product_type"] = "Four Wheeler"
        result.pop("sub_type")
    try:
        if "Registration" in result:
            result["registration_no"] = result["Registration"]
            result.pop("Registration")
    except:
        pass
    try:
        if "2" in result["seating_capacity"]:
            result["product_type"]="Two Wheeler"
        result.pop("seating_capacity")
    except:
        pass
    result["hypothecation"] = ""
    try:
        result.pop("Period of Insurance")
    except:
        pass
    for i in range(len(df["Rest"])):
        if df["Rest"][i] not in result:
            result[df["Rest"][i]] = ""
    result["source_system"] = "OCR"

    print(result)
    return result

# def magic_RC(file_list, res):
#     text_json = icr_run(file_list)
#     for i in range(len(text_json)):
#         print(text_json[i].get('text'))
#         print(text_json[i].get('boundingBox'))
#         print("######################")
#     res = bajaj(text_json,res)
#     return res
# file_list=[r'E:\IAIL\reliance\Bajaj\bajaj1\WhatsApp Image 2021-04-22 at 14.14.33.jpeg']
# def run(file_list):
#     res={}
#     for i in file_list:
#         res=magic_RC(i,res)
#     print(res.keys())
#     import json
#     with open("BAJAJ.json", "w") as twitter_data_file:
#         json.dump(res, twitter_data_file, indent=4, sort_keys=True)
# run(file_list)