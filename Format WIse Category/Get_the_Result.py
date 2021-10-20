import re
import numpy as np
import os
import subprocess
from tabula import read_pdf
from openpyxl import load_workbook
import pandas as pd
from pdf2image import convert_from_path


tabless={
'city/Kilowatt',
'of Regn'
}
states = {
    "Andaman and Nicobar Islands",
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chandigarh",
    "Chhattisgarh",
    "Dadra and Nagar Haveli",
    "Daman and Diu",
    "Delhi",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jammu and Kashmir",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Ladakh",
    "Lakshadweep",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Puducherry",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal",
    "GOA"
}
def clean_list(list_: list):
    temp_list = []
    for ele in list_:
        if bool(str(ele).strip()):
            temp_list.append(str(ele).strip())
    return temp_list
def pdf_to_img(pdfName, folderName):
    if os.path.exists(str(pdfName)):
        path_s = str(pdfName)
        print(46)
    pages = convert_from_path(path_s, 400)
    no_of_pages = len(pages)
    i = 1
    pdfNamesss = pdfName.replace('.pdf', '').replace('PDF', '').replace('.', '')
    for img in range(no_of_pages):
        filename = pdfNamesss + str(i)
        a = '"' + path_s + '"'
        a1='"' + filename + '"'
        subprocess.run("pdftotext -layout " + a + " -f "+ str(i) +" -l "+str(i)+"  "+a1+".txt")
        i += 1
def Transcript_of_Proposal(fw,file_name,path_s,page_no):
    lines = fw
    var1 = ''
    dict1 = {}
    pathology = False
    print('*************************************Proposer Name*********************************************')
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Proposer Name"):
            pathology = True
        if "Proposer Address" in lines[i]:
            break
        if not pathology:
            continue
        data_list = lines[i].replace('\n', '').split("  ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        if len(data_list)>=2:
            dict1['insured_name']=data_list[1].replace(':','')
        else:
            dict1['insured_name']=''
    print(dict1['insured_name'])
    print('*************************************Proposer Address*********************************************')
    Proposer_Address=False
    Proposer_Address_list=[]
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Proposer Address"):
            Proposer_Address = True
        if "Proposer Mobile Number" in lines[i]:
            break
        if not Proposer_Address:
            continue
        data_list = lines[i].replace('\n', '').replace('Proposer Address','').replace('2.','').split("   ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        for data in range(len(data_list)):
            Proposer_Address_list.append(data_list[data])
    Proposer_list=''
    # print(Proposer_Address_list)
    if Proposer_Address_list:
        for i in range(len(Proposer_Address_list)):
            Proposer_list += Proposer_Address_list[i].replace(':','')
    if Proposer_list:
        dict1['address']=Proposer_list
        try:
            addr = dict1["address"]
            z = 0
            dict1["customer_state"] = ""
            for state in states:
                if state.upper() in Proposer_list.upper():
                    dict1["customer_state"] = state
                    z = 1
                    break
            pattern4 = re.compile(r"\d\d\d\d\d\d")
            x = pattern4.search(addr)
            pincode = x.group()
            dict1["pincode"] = pincode
            print('sdb' + pincode)
        except:
            try:
                addr = addr.upper()
                df = pd.read_csv("pincode_final.csv", engine='python')
                if dict1["customer_state"] != "":
                    df = df[df["statename"] == state]
                region = df['regionname'].unique().tolist()
                region = [x for x in region if str(x) != 'nan']
                reg = False
                dis = False
                tal = False
                k = 0
                for i in region:
                    if i in addr:
                        print("region")
                        k = 1
                        reg = True
                        break
                if k == 1:
                    df = df[df["regionname"] == i]
                district = df["Districtname"].unique().tolist()
                district = [x for x in district if str(x) != 'nan']
                k = 0
                for i in district:
                    if i in addr:
                        print("district")
                        k = 1
                        dis = True
                        break
                if k == 1:
                    df = df[df["Districtname"] == i]
                taluk = df["Taluk"].unique().tolist()
                taluk = [x for x in taluk if str(x) != 'nan']
                k = 0
                if taluk != []:
                    for i in taluk:
                        if i in addr:
                            print("taluk")
                            print(i)
                            k = 1
                            tal = True
                            break
                if k == 1:
                    df = df[df["Taluk"] == i]
                try:
                    if reg is True or dis is True or tal is True:
                        dict1["pincode"] = str(df.iloc[0]["pincode"])
                    else:
                        print("No Match")
                        dict1["pincode"] = ""
                except:
                    print("Not there")
            except:
                print("Pincode Excel")
                dict1["pincode"] = ''
    else:
        dict1['address']=''
    print(dict1['address'])
    print('*****************************************Proposer Mobile Number*****************************************')
    Proposer_Mobile_Number = False
    temp_Proposer_Mobile_Number=''
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Proposer Mobile Number"):
            Proposer_Mobile_Number = True
        if "Proposer Residential Number" in lines[i]:
            break
        if not Proposer_Mobile_Number:
            continue
        data_list = lines[i].replace('\n', '').replace(':','').replace('3.', '').split("   ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        for i in range(len(data_list)):
            if data_list[i].__contains__('Proposer Mobile Number'):
                temp_Proposer_Mobile_Number=data_list[i+1].replace('-','')
    if temp_Proposer_Mobile_Number:
        dict1['mobile']=temp_Proposer_Mobile_Number
    else:
        dict1['mobile']=''
    print(dict1['mobile'])
    print('*****************************************Proposer Residential Number*****************************************')
    Proposer_Residential_Number = False
    temp_Proposer_Residential_Number = ''
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Proposer Residential Number"):
            Proposer_Residential_Number = True
        if "Proposer e-mail id" in lines[i]:
            break
        if not Proposer_Residential_Number:
            continue
        data_list = lines[i].replace('\n', '').replace(':', '').replace('4.', '').split("   ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        for i in range(len(data_list)):
            if data_list[i].__contains__('Proposer Residential Number'):
                temp_Proposer_Residential_Number = data_list[i + 1]
    if temp_Proposer_Residential_Number:
        dict1['Proposer Residential Number'] = temp_Proposer_Residential_Number
    else:
        dict1['Proposer Residential Number'] = ''
    print(dict1['Proposer Residential Number'])
    print('*****************************************Proposer e-mail id*****************************************')
    Proposer_e_mail_id = False
    temp_Proposer_e_mail_id = ''
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Proposer e-mail id"):
            Proposer_e_mail_id = True
        if "Proposer Profession" in lines[i]:
            break
        if not Proposer_e_mail_id:
            continue
        data_list = lines[i].replace('\n', '').replace(':', '').replace('5.', '').split("   ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        for i in range(len(data_list)):
            if data_list[i].__contains__('Proposer e-mail id'):
                temp_Proposer_e_mail_id = data_list[i + 1]
    if temp_Proposer_e_mail_id:
        dict1['email_id'] = temp_Proposer_e_mail_id
    else:
        dict1['email_id'] = ''
    print(dict1['email_id'])
    print('*****************************************Proposer Profession*****************************************')
    Proposer_Profession = False
    temp_Proposer_Profession = ''
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Proposer Profession"):
            Proposer_Profession = True
        if "Vehicle Details" in lines[i]:
            break
        if not Proposer_Profession:
            continue
        data_list = lines[i].replace('\n', '').replace(':', '').replace('6.', '').split("   ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        for i in range(len(data_list)):
            if data_list[i].__contains__('Proposer Profession'):
                temp_Proposer_Profession = data_list[i + 1]
    if temp_Proposer_Profession:
        dict1['Profession'] = temp_Proposer_Profession
    else:
        dict1['Profession'] = ''
    print(dict1['Profession'])
    print('*****************************************Reference*****************************************')
    print('*****************************************Vehicle Details*****************************************')
    Vehicle_Details = []
    Vehicle_Details_1 = []
    Vehicle_Details_2 = []
    Vehicle_Details_3 = []
    final_res = []
    final_res1=[]
    final_res111=[]
    final_res1112 = []
    final_res11 = []
    final_res12 = []
    final_res2=[]
    json_da = read_pdf(path_s, pages=int(page_no), output_format='json',silent=True,lattice=True)
    print(json_da)
    Vehicle_jsondata = json_da[0].get('data')
    Vehicle_jsondata2 = json_da[1].get('data')
    for i in range(len(Vehicle_jsondata)):
        for j in range(len(Vehicle_jsondata[i])):
            Vehicle_Details.append(Vehicle_jsondata[i][j].get('text'))
    print(len(Vehicle_Details))
    print(Vehicle_Details)
    Vehicle_Details=clean_list(Vehicle_Details)
    if len(Vehicle_Details)==18:
        two_split = np.array_split(Vehicle_Details, 2)
        for array in two_split:
            Vehicle_Details_2.append(list(array))
        print(Vehicle_Details_2)
        if len(Vehicle_Details_2) == 2:
            for i1 in range(len(Vehicle_Details_2[1])):
                final_res.append(Vehicle_Details_2[1][i1].replace('\r','&'))
    print(final_res)
    print('*****************************************Vehicle Details Part 2*****************************************')
    for i in range(len(Vehicle_jsondata2)):
        for j in range(len(Vehicle_jsondata2[i])):
            Vehicle_Details_1.append(Vehicle_jsondata2[i][j].get('text'))
    print(len(Vehicle_Details_1))
    print(Vehicle_Details_1)
    tem_vi=''
    temp_Chassis=[]
    Vehicle_Details_1=clean_list(Vehicle_Details_1)
    if len(Vehicle_Details_1)==14:
        two_split = np.array_split(Vehicle_Details_1, 2)
        for array in two_split:
            Vehicle_Details_3.append(list(array))
        if len(Vehicle_Details_3) == 2:
            for i in range(len(Vehicle_Details_3[1])):
                temp_Chassis.append(Vehicle_Details_3[1][i])
                final_res2.append(Vehicle_Details_3[1][i].replace('\r',''))
    print('================================================Registration Number=============================================================')
    if final_res:
        dict1['registration_no']=str(final_res[0]).replace('&',' ')
    else:
        dict1['registration_no']=''
    print(dict1['registration_no'])
    print('================================================Month / Year of Regn=============================================================')
    if final_res:
        dict1['date_of_registration']=final_res[1].replace('&',' ')
    else:
        dict1['date_of_registration']=''
    print(dict1['date_of_registration'])
    print('================================================Vehicle Make=============================================================')
    if final_res:
        dict1['make']=final_res[2].replace('\r','').replace('-','').replace('&','')
    else:
        dict1['make']=''
    print(dict1['make'])
    print('================================================Vehicle Model=============================================================')
    if final_res:
        dict1['model']=final_res[3].replace('- ','').replace('\r',' ').replace('&',' ')
    else:
        dict1['model']=''
    print(dict1['model'])
    print('================================================Cubic Capacity/ Kilowatt=============================================================')
    if final_res:
        dict1['cubic_capacity']=final_res[6].replace('&',' ')
    else:
        dict1['cubic_capacity']=''
    print(dict1['cubic_capacity'])
    print('================================================Year of Manufacture=============================================================')
    if final_res:
        dict1['mfg_yr']=final_res[7].replace('&',' ')
    else:
        dict1['mfg_yr']=''
    print(dict1['mfg_yr'])
    print('================================================Engine Number=============================================================')
    fin_Eng= ''
    var_temp_Eng = ''
    if final_res2:
        temp_var = str(temp_Chassis[0]).split('\r')
        print(temp_var)
        if len(temp_var) >= 1:
            var_temp_Eng = temp_var[0]
            for i in range(len(lines)):
                if str(lines[i]).__contains__(temp_var[0]):
                    data_list2 = lines[i].split(" ")
                    data_list2 = clean_list(data_list2)
                    print(data_list2)
                    break
            if data_list2:
                for i in range(len(data_list2)):
                    if str(data_list2[i]).__contains__(temp_var[0]):
                        fin_Eng = data_list2[i]
    if fin_Eng and var_temp_Eng:
        dict1['engine_no'] = str(final_res2[0]).replace(var_temp_Eng, fin_Eng)
        print(dict1['engine_no'])
    else:
        dict1['engine_no'] = ''
    print(dict1['engine_no'])
    print('================================================Chassis Number=============================================================')
    fin_chas=''
    fin_chas1=''
    var_temp_chassd=''
    var_temp_chassd1=''
    data_list1=[]
    data_list11=[]
    if final_res2:
        temp_var=str(temp_Chassis[1]).split('\r')
        print(temp_var)
        if len(temp_var)>=1:
            var_temp_chassd=temp_var[0]
            if len(temp_var)!=1:
                var_temp_chassd1=temp_var[1]
            for i in range(len(lines)):
                if str(lines[i]).__contains__(temp_var[0]):
                    data_list1 = lines[i].split(" ")
                    data_list1 = clean_list(data_list1)
                if len(temp_var)!=1:
                    if str(lines[i]).__contains__(temp_var[1]):
                        data_list11 = lines[i].split(" ")
                        data_list11 = clean_list(data_list11)
            print(data_list11)
            print(data_list1)
            if data_list1:
                for i in range(len(data_list1)):
                    if str(data_list1[i]).__contains__(temp_var[0]):
                        fin_chas=data_list1[i]
            if data_list11:
                for i in range(len(data_list11)):
                    if str(data_list11[i]).__contains__(temp_var[1]):
                        fin_chas1 = data_list11[i]
        if fin_chas and var_temp_chassd:
            dict1['chassis_no'] = str(final_res2[1]).replace(var_temp_chassd,fin_chas).replace(var_temp_chassd1,fin_chas1).replace('-','')
            print(dict1['chassis_no'])
        else:
            dict1['chassis_no'] = ''
        print(dict1['chassis_no'])
    print('================================================Type Of file=============================================================')
    name='Transcript of Proposal'
    print(dict1)
    return dict1,name
def Transcript_of_Proposal_for_Commercial(fw,file_name,path_s,page_no):
    lines = fw
    var1 = ''
    dict1 = {}
    pathology = False
    print('*************************************Proposer Name*********************************************')
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Proposer Name"):
            pathology = True
        if "Proposer Address" in lines[i]:
            break
        if not pathology:
            continue
        data_list = lines[i].replace('\n', '').split("  ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        if len(data_list)>=2:
            dict1['insured_name']=data_list[1].replace(':','')
        else:
            dict1['insured_name']=''
    print(dict1['insured_name'])
    print('*************************************Proposer Address*********************************************')
    Proposer_Address=False
    Proposer_Address_list=[]
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Proposer Address"):
            Proposer_Address = True
        if "Proposer Mobile Number" in lines[i]:
            break
        if not Proposer_Address:
            continue
        data_list = lines[i].replace('\n', '').replace('Proposer Address','').replace('2.','').split("   ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        for data in range(len(data_list)):
            Proposer_Address_list.append(data_list[data])
    Proposer_list=''
    # print(Proposer_Address_list)
    if Proposer_Address_list:
        for i in range(len(Proposer_Address_list)):
            Proposer_list += Proposer_Address_list[i].replace(':','')
    if Proposer_list:
        dict1['address']=Proposer_list
        try:
            addr = dict1["address"]
            z = 0
            dict1["customer_state"] = ""
            for state in states:
                if state.upper() in Proposer_list.upper():
                    dict1["customer_state"] = state
                    z = 1
                    break
            pattern4 = re.compile(r"\d\d\d\d\d\d")
            x = pattern4.search(addr)
            pincode = x.group()
            dict1["pincode"] = pincode
            print('sdb' + pincode)
        except:
            try:
                addr = addr.upper()
                df = pd.read_csv("pincode_final.csv", engine='python')
                if dict1["customer_state"] != "":
                    df = df[df["statename"] == state]
                region = df['regionname'].unique().tolist()
                region = [x for x in region if str(x) != 'nan']
                reg = False
                dis = False
                tal = False
                k = 0
                for i in region:
                    if i in addr:
                        print("region")
                        k = 1
                        reg = True
                        break
                if k == 1:
                    df = df[df["regionname"] == i]
                district = df["Districtname"].unique().tolist()
                district = [x for x in district if str(x) != 'nan']
                k = 0
                for i in district:
                    if i in addr:
                        print("district")
                        k = 1
                        dis = True
                        break
                if k == 1:
                    df = df[df["Districtname"] == i]
                taluk = df["Taluk"].unique().tolist()
                taluk = [x for x in taluk if str(x) != 'nan']
                k = 0
                if taluk != []:
                    for i in taluk:
                        if i in addr:
                            print("taluk")
                            print(i)
                            k = 1
                            tal = True
                            break
                if k == 1:
                    df = df[df["Taluk"] == i]
                try:
                    if reg is True or dis is True or tal is True:
                        dict1["pincode"] = str(df.iloc[0]["pincode"])
                    else:
                        print("No Match")
                        dict1["pincode"] = ""
                except:
                    print("Not there")
            except:
                print("Pincode Excel")
                dict1["pincode"] = ''
    else:
        dict1['address']=''
    print(dict1['address'])
    print('*****************************************Proposer Mobile Number*****************************************')
    Proposer_Mobile_Number = False
    temp_Proposer_Mobile_Number=''
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Proposer Mobile Number"):
            Proposer_Mobile_Number = True
        if "Proposer Residential Number" in lines[i]:
            break
        if not Proposer_Mobile_Number:
            continue
        data_list = lines[i].replace('\n', '').replace(':','').replace('3.', '').split("   ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        for i in range(len(data_list)):
            if data_list[i].__contains__('Proposer Mobile Number'):
                temp_Proposer_Mobile_Number=data_list[i+1].replace('-','')
    if temp_Proposer_Mobile_Number:
        dict1['mobile']=temp_Proposer_Mobile_Number
    else:
        dict1['mobile']=''
    print(dict1['mobile'])
    print('*****************************************Proposer Residential Number*****************************************')
    Proposer_Residential_Number = False
    temp_Proposer_Residential_Number = ''
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Proposer Residential Number"):
            Proposer_Residential_Number = True
        if "Proposer e-mail id" in lines[i]:
            break
        if not Proposer_Residential_Number:
            continue
        data_list = lines[i].replace('\n', '').replace(':', '').replace('4.', '').split("   ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        for i in range(len(data_list)):
            if data_list[i].__contains__('Proposer Residential Number'):
                temp_Proposer_Residential_Number = data_list[i + 1]
    if temp_Proposer_Residential_Number:
        dict1['Proposer Residential Number'] = temp_Proposer_Residential_Number
    else:
        dict1['Proposer Residential Number'] = ''
    print(dict1['Proposer Residential Number'])
    print('*****************************************Proposer e-mail id*****************************************')
    Proposer_e_mail_id = False
    temp_Proposer_e_mail_id = ''
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Proposer e-mail id"):
            Proposer_e_mail_id = True
        if "Proposer Profession" in lines[i]:
            break
        if not Proposer_e_mail_id:
            continue
        data_list = lines[i].replace('\n', '').replace(':', '').replace('5.', '').split("   ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        for i in range(len(data_list)):
            if data_list[i].__contains__('Proposer e-mail id'):
                temp_Proposer_e_mail_id = data_list[i + 1]
    if temp_Proposer_e_mail_id:
        dict1['email_id'] = temp_Proposer_e_mail_id
    else:
        dict1['email_id'] = ''
    print(dict1['email_id'])
    print('*****************************************Proposer Profession*****************************************')
    Proposer_Profession = False
    temp_Proposer_Profession = ''
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Proposer Profession"):
            Proposer_Profession = True
        if "Vehicle Details" in lines[i]:
            break
        if not Proposer_Profession:
            continue
        data_list = lines[i].replace('\n', '').replace(':', '').replace('6.', '').split("   ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        for i in range(len(data_list)):
            if data_list[i].__contains__('Proposer Profession'):
                temp_Proposer_Profession = data_list[i + 1]
    if temp_Proposer_Profession:
        dict1['Profession'] = temp_Proposer_Profession
    else:
        dict1['Profession'] = ''
    print(dict1['Profession'])
    print('*****************************************Vehicle Details*****************************************')
    Vehicle_Details = []
    Vehicle_Details_2 = []
    final_res = []
    json_da = read_pdf(path_s, pages=int(page_no), output_format='json',silent=True,lattice=True)
    print(json_da)
    Vehicle_jsondata = json_da[0].get('data')
    for i in range(len(Vehicle_jsondata)):
        for j in range(len(Vehicle_jsondata[i])):
            Vehicle_Details.append(Vehicle_jsondata[i][j].get('text'))
    print(len(Vehicle_Details))
    print(Vehicle_Details)
    if len(Vehicle_Details)==18:
        two_split = np.array_split(Vehicle_Details, 2)
        for array in two_split:
            Vehicle_Details_2.append(list(array))
        print(Vehicle_Details_2)
        if len(Vehicle_Details_2) == 2:
            for i1 in range(len(Vehicle_Details_2[1])):
                final_res.append(Vehicle_Details_2[1][i1].replace('\r',''))
    print(final_res)
    print('================================================Registration Number=============================================================')
    if final_res:
        dict1['registration_no']=final_res[0]
    else:
        dict1['registration_no']=''
    print(dict1['registration_no'])
    print('================================================Vehicle Make=============================================================')
    if final_res:
        dict1['make']=final_res[1].replace('\r','')
    else:
        dict1['make']=''
    print(dict1['make'])
    print('================================================Vehicle Model=============================================================')
    if final_res:
        dict1['model']=final_res[3].replace('- ','').replace('\r','')
    else:
        dict1['model']=''
    print(dict1['model'])
    print('================================================Cubic Capacity/ Kilowatt=============================================================')
    if final_res:
        dict1['cubic_capacity']=final_res[4]
    else:
        dict1['cubic_capacity']=''
    print(dict1['cubic_capacity'])
    print('================================================Year of Manufacture=============================================================')
    if final_res:
        dict1['mfg_yr']=final_res[5]
    else:
        dict1['mfg_yr']=''
    print(dict1['mfg_yr'])
    print('================================================Engine Number=============================================================')
    if final_res:
        dict1['engine_no']=final_res[8]
    else:
        dict1['engine_no']=''
    print(dict1['engine_no'])
    print('================================================Chassis Number=============================================================')
    if final_res:
        dict1['chassis_no']=final_res[7]
    else:
        dict1['chassis_no']=''
    print(dict1['chassis_no'])
    print('================================================Type Of file=============================================================')
    name='Transcript_of_Proposal_for_Commercial'
    print(dict1)
    return dict1,name
def Coverage_opted(fw,file_name,path_s,page_no):
    lines = fw
    var1 = ''
    dict1 = {}
    pathology = False
    print('*************************************Period of Insurance*********************************************')
    PeriodofInsurance=[]
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Period of Insurance"):
            pathology = True
        if "2." in lines[i]:
            break
        if not pathology:
            continue
        data_list = lines[i].replace('\n', '').replace('1. Period of Insurance','').replace('From','').replace('To','').replace(':','').split("  ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        for i in range(len(data_list)):
            PeriodofInsurance.append(data_list[i])
    if PeriodofInsurance:
        if len(PeriodofInsurance)==2:
            temp_var=PeriodofInsurance[0].split(' ')
            temp_var = PeriodofInsurance[0].split(' ')
            if len(temp_var) == 2:
                dict1['period_of_insurance_start_date'] = temp_var[0]
            else:
                dict1['period_of_insurance_start_date'] = PeriodofInsurance[0].replace('0001(Hrs)', '')
            dict1['period_of_insurance_end_date'] =PeriodofInsurance[1].replace('Midnight','')
    else:
        dict1['period_of_insurance_start_date'] = ''
        dict1['period_of_insurance_end_date'] = ''
    print(dict1['period_of_insurance_start_date'])
    print(dict1['period_of_insurance_end_date'])
    name='Coverage opted'
    print(dict1)
    return dict1,name
def CERTIFICATE_CUM_POLICY(fw,file_name,path_s,page_no):
    lines = fw
    var1 = ''
    dict1 = {}
    pathology11 = False
    print('*************************************Policy Number*********************************************')
    Policy_Number = []
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Policy Number"):
            pathology11 = True
        if "Period Of Insurance" in lines[i]:
            break
        if not pathology11:
            continue
        data_list = lines[i].replace('\n', '').replace(':', '').split("  ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        for i in range(len(data_list)):
            if data_list[i].__contains__('Policy Number'):
                Policy_Number=(data_list[i+1])
    if Policy_Number:
        dict1['policy_number']=Policy_Number
    else:
        dict1['policy_number'] =''
    print(dict1['policy_number'])
    print('*************************************Policy Period Of Insurance*********************************************')
    Policy_Period_Of_Insurance = []
    Policy_Period_Of_Insurance_Temp=False
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Period Of Insurance"):
            Policy_Period_Of_Insurance_Temp = True
        if "Scrutiny No" in lines[i]:
            break
        if not Policy_Period_Of_Insurance_Temp:
            continue
        data_list = lines[i].replace('\n', '').replace('From', '').replace('To','').split("  ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        Policy_Period_Of_Insurance.append(data_list)
    if Policy_Period_Of_Insurance:
        if len(Policy_Period_Of_Insurance) == 2:
            print(Policy_Period_Of_Insurance)
            for ii in range(len(Policy_Period_Of_Insurance)):
                for jj in range(len(Policy_Period_Of_Insurance[ii])):
                    if Policy_Period_Of_Insurance[ii][jj].__contains__('Period Of Insurance'):
                        dict1['period_of_insurance_start_date'] = Policy_Period_Of_Insurance[ii][jj+1].replace(': ','').replace('00:01','').replace('23:45','')
                    elif Policy_Period_Of_Insurance[ii][jj].__contains__('Midnight'):
                        dict1['period_of_insurance_end_date'] = Policy_Period_Of_Insurance[ii][jj].replace(':','').replace('Midnight','')
                    elif Policy_Period_Of_Insurance[ii][jj].__contains__('Policy issued on'):
                        dict1['policy_issuance_date'] = Policy_Period_Of_Insurance[ii][jj+1].replace(' -', '')
        else:
            dict1['policy_issuance_date'] = ''
            dict1['period_of_insurance_end_date'] = ''
            dict1['period_of_insurance_start_date']=''
    else:
        dict1['policy_issuance_date'] = ''
        dict1['period_of_insurance_end_date'] = ''
        dict1['period_of_insurance_start_date']=''
    print(dict1['period_of_insurance_start_date'])
    print(dict1['period_of_insurance_end_date'])
    print(dict1['policy_issuance_date'])
    print('*************************************Insured Name*********************************************')
    Insured_Name = []
    Insured_Name_temp=False
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Insured Name"):
            Insured_Name_temp = True
        if "Insured Address" in lines[i]:
            break
        if not Insured_Name_temp:
            continue
        data_list = lines[i].replace('\n', '').replace(':', '').split("  ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        print(data_list)
        for i in range(len(data_list)):
            if data_list[i].__contains__('Insured Name'):
                Insured_Name = data_list[i + 1]
    if Insured_Name:
        dict1['insured_name'] = Insured_Name
    else:
        dict1['insured_name'] = ''
    print(dict1['insured_name'])
    print('*************************************Insured Address*********************************************')
    Insured_Address = ''
    Insured_Address_temp = False
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Insured Address"):
            Insured_Address_temp = True
        if "Customer ID" in lines[i]:
            break
        if not Insured_Address_temp:
            continue
        data_list = lines[i].replace('\n', '').replace(':', '').replace('Insured Address','').split("  ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
    #     print(data_list)
        for i in range(len(data_list)):
            Insured_Address+=data_list[i]
    if Insured_Address:
        dict1['address'] = Insured_Address
        try:
            addr = dict1["address"]
            z = 0
            dict1["customer_state"] = ""
            for state in states:
                if state.upper() in Insured_Address.upper():
                    dict1["customer_state"] = state
                    z = 1
                    break
            pattern4 = re.compile(r"\d\d\d\d\d\d")
            x = pattern4.search(addr)
            pincode = x.group()
            dict1["pincode"] = pincode
            print('sdb' + pincode)
        except:
            try:
                addr = addr.upper()
                df = pd.read_csv("pincode_final.csv", engine='python')
                if dict1["customer_state"] != "":
                    df = df[df["statename"] == state]
                region = df['regionname'].unique().tolist()
                region = [x for x in region if str(x) != 'nan']
                reg = False
                dis = False
                tal = False
                k = 0
                for i in region:
                    if i in addr:
                        print("region")
                        k = 1
                        reg = True
                        break
                if k == 1:
                    df = df[df["regionname"] == i]
                district = df["Districtname"].unique().tolist()
                district = [x for x in district if str(x) != 'nan']
                k = 0
                for i in district:
                    if i in addr:
                        print("district")
                        k = 1
                        dis = True
                        break
                if k == 1:
                    df = df[df["Districtname"] == i]
                taluk = df["Taluk"].unique().tolist()
                taluk = [x for x in taluk if str(x) != 'nan']
                k = 0
                if taluk != []:
                    for i in taluk:
                        if i in addr:
                            print("taluk")
                            print(i)
                            k = 1
                            tal = True
                            break
                if k == 1:
                    df = df[df["Taluk"] == i]
                try:
                    if reg is True or dis is True or tal is True:
                        dict1["pincode"] = str(df.iloc[0]["pincode"])
                    else:
                        print("No Match")
                        dict1["pincode"] = ""
                except:
                    print("Not there")
            except:
                print("Pincode Excel")
                dict1["pincode"] = ''
    else:
        dict1['address'] = ''
    print(dict1['address'])
    print('*************************************Vehicle Details*********************************************')
    Vehicle_Details = []
    Vehicle_Details_2 = []
    final_res = []
    json_da = read_pdf(path_s, pages=int(page_no), output_format='json',silent=True,lattice=True)
    Vehicle_jsondata = json_da[0].get('data')
    for i in range(len(Vehicle_jsondata)):
        for j in range(len(Vehicle_jsondata[i])):
            Vehicle_Details.append(Vehicle_jsondata[i][j].get('text'))
    print(Vehicle_Details)
    print(len(Vehicle_Details))
    if len(Vehicle_Details) == 18:
        two_split = np.array_split(Vehicle_Details, 2)
        for array in two_split:
            Vehicle_Details_2.append(list(array))
        temp_Chassis = []
        if len(Vehicle_Details_2) == 2:
            for i1 in range(len(Vehicle_Details_2[1])):
                final_res.append(Vehicle_Details_2[1][i1].replace('\r','$'))
                temp_Chassis.append(Vehicle_Details_2[1][i1])
    print(final_res)
    print('================================================Registration Number=============================================================')
    if final_res:
        dict1['registration_no'] = final_res[0].replace('$',' ')
    else:
        dict1['registration_no'] = ''
    print(dict1['registration_no'])
    print('================================================Vehicle Make=============================================================')
    if final_res:
        dict1['make'] = final_res[1].replace('\r','').replace('-','').replace('$','')
    else:
        dict1['make'] = ''
    print(dict1['make'])
    print('================================================Vehicle Model=============================================================')
    if final_res:
        dict1['model'] = final_res[3].replace('- ','').replace('\r',' ').replace('$','')
    else:
        dict1['model'] = ''
    print(dict1['model'])
    print('================================================Cubic Capacity/ Kilowatt=============================================================')
    if final_res:
        dict1['cubic_capacity'] = final_res[4].replace('$','')
    else:
        dict1['cubic_capacity'] = ''
    print(dict1['cubic_capacity'])
    print('================================================Year of Manufacture=============================================================')
    if final_res:
        dict1['mfg_yr'] = final_res[5].replace('$','')
    else:
        dict1['mfg_yr'] = ''
    print(dict1['mfg_yr'])
    print('================================================Chassis Number=============================================================')
    # if final_res:
    #     dict1['chassis_no'] = final_res[7].replace(' ','')
    # else:
    #     dict1['chassis_no'] = ''
    # print(dict1['chassis_no'])
    fin_chas = ''
    var_temp_chassd = ''
    var_temp_chassd1 = ''
    data_list11=[]
    data_list1=[]
    fin_chas1=''
    if final_res:
        temp_var = str(temp_Chassis[7]).split('\r')
        if len(temp_var) >= 1:
            var_temp_chassd = temp_var[0]
            if len(temp_var)!=1:
                var_temp_chassd1 = temp_var[1]
            for i in range(len(lines)):
                if str(lines[i]).__contains__(temp_var[0]):
                    data_list1 = lines[i].split(" ")
                    data_list1 = clean_list(data_list1)
                if len(temp_var)!=1:
                    if str(lines[i]).__contains__(temp_var[1]):
                        data_list11 = lines[i].split(" ")
                        data_list11 = clean_list(data_list11)
            if data_list1:
                for i in range(len(data_list1)):
                    if str(data_list1[i]).__contains__(temp_var[0]):
                        fin_chas = data_list1[i]
            if data_list11:
                for i in range(len(data_list11)):
                    if str(data_list11[i]).__contains__(temp_var[1]):
                        fin_chas1 = data_list11[i]
        if fin_chas and var_temp_chassd:
            dict1['chassis_no'] = str(final_res[7]).replace('$','').replace(var_temp_chassd, fin_chas).replace(var_temp_chassd1,fin_chas1).replace(' ','').replace('-','')
            print(dict1['chassis_no'])
        else:
            dict1['chassis_no'] = ''
        print(dict1['chassis_no'])
    print(
        '================================================Engine Number=============================================================')
    fin_eng = ''
    var_temp_eng = ''
    data_list1=[]
    if final_res:
        temp_var = str(temp_Chassis[8]).split('\r')
        if len(temp_var) >= 1:
            var_temp_eng = temp_var[0]
            for i in range(len(lines)):
                if str(lines[i]).__contains__(temp_var[0]):
                    data_list1 = lines[i].split(" ")
                    data_list1 = clean_list(data_list1)
                    break
            if data_list1:
                for i in range(len(data_list1)):
                    if str(data_list1[i]).__contains__(temp_var[0]):
                        fin_eng = data_list1[i]
        if fin_eng and var_temp_eng:
            dict1['engine_no'] = str(final_res[8]).replace('$', '').replace(var_temp_eng, fin_eng).replace(' ', '')
            print(dict1['engine_no'])
        else:
            dict1['engine_no'] = ''
        print(dict1['engine_no'])
    name='CERTIFICATE CUM POLICY'
    print('================================================No Claim Bonus=============================================================')
    No_Claim_Bonus = []
    No_Claim_Bonus_temp=False
    for i in range(len(lines)):
        if str(lines[i]).__contains__("No Claim Bonus"):
            No_Claim_Bonus_temp = True
        if "Nominee Details" in lines[i]:
            break
        if not No_Claim_Bonus_temp:
            continue
        data_list = lines[i].replace('\n', '').replace(':', '').split("  ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        for i in range(len(data_list)):
            if data_list[i].__contains__('No Claim Bonus'):
                No_Claim_Bonus = (data_list[i + 1])
    if No_Claim_Bonus:
        dict1['No_Claim_Bonus'] = No_Claim_Bonus
    else:
        dict1['No_Claim_Bonus'] = ''
    print(dict1['No_Claim_Bonus'])
    print('================================================Nominee Details=============================================================')
    Nominee_Details = []
    Nominee_Details_temp = False
    nominee_for_owner_driver_nominee_name = ''
    nominee_for_owner_driver_nominee_relation = ''
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Nominee Details"):
            Nominee_Details_temp = True
        if "LIMITS OF LIABILITY" in lines[i]:
            break
        if not Nominee_Details_temp:
            continue
        data_list = lines[i].replace('\n', '').replace(':', '').split("  ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        print(data_list)
        for i in range(len(data_list)):
            if data_list[i].__contains__('Name') and data_list[i + 1].__contains__('Relationship'):
                nominee_for_owner_driver_nominee_name = ''
            else:
                if data_list[i].__contains__('Name'):
                    nominee_for_owner_driver_nominee_name = data_list[i + 1]
            if data_list[i].__contains__('Relationship') and data_list[-1].__contains__('Relationship'):
                nominee_for_owner_driver_nominee_relation = ''
            else:
                if data_list[i].__contains__('Relationship') and not data_list[-1].__contains__('Relationship'):
                    nominee_for_owner_driver_nominee_relation = data_list[i + 1]
    if nominee_for_owner_driver_nominee_name:
        dict1['nominee_for_owner_driver_nominee_name'] = nominee_for_owner_driver_nominee_name
    else:
        dict1['nominee_for_owner_driver_nominee_name'] = ''
    if nominee_for_owner_driver_nominee_relation:
        dict1['nominee_for_owner_driver_nominee_relation'] = nominee_for_owner_driver_nominee_relation
    else:
        dict1['nominee_for_owner_driver_nominee_relation'] = ''
    print(dict1['nominee_for_owner_driver_nominee_name'])
    print(dict1['nominee_for_owner_driver_nominee_relation'])
    print(dict1)
    print(dict1['No_Claim_Bonus'])
    return dict1,name
def CERTIFICATE_CUM_POLICY_FOR_COMMERCIAL(fw,file_name,path_s,page_no):
    lines = fw
    var1 = ''
    dict1 = {}
    pathology11 = False
    print('*************************************Policy Number*********************************************')
    Policy_Number = []
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Policy Number"):
            pathology11 = True
        if "Period Of Insurance" in lines[i]:
            break
        if not pathology11:
            continue
        data_list = lines[i].replace('\n', '').replace(':', '').split("  ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        for i in range(len(data_list)):
            if data_list[i].__contains__('Policy Number'):
                Policy_Number=(data_list[i+1])
    if Policy_Number:
        dict1['policy_number']=Policy_Number
    else:
        dict1['policy_number'] =''
    print(dict1['policy_number'])
    print('*************************************Policy Period Of Insurance*********************************************')
    Policy_Period_Of_Insurance = []
    Policy_Period_Of_Insurance_Temp=False
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Period Of Insurance"):
            Policy_Period_Of_Insurance_Temp = True
        if "Scrutiny No" in lines[i]:
            break
        if not Policy_Period_Of_Insurance_Temp:
            continue
        data_list = lines[i].replace('\n', '').replace('From', '').replace('To','').split("  ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        Policy_Period_Of_Insurance.append(data_list)
    if Policy_Period_Of_Insurance:
        if len(Policy_Period_Of_Insurance) == 2:
            print(Policy_Period_Of_Insurance)
            for ii in range(len(Policy_Period_Of_Insurance)):
                for jj in range(len(Policy_Period_Of_Insurance[ii])):
                    if Policy_Period_Of_Insurance[ii][jj].__contains__('Period Of Insurance'):
                        dict1['period_of_insurance_start_date'] = Policy_Period_Of_Insurance[ii][jj+1].replace(': ','').replace('00:01','')
                    elif Policy_Period_Of_Insurance[ii][jj].__contains__('Midnight'):
                        dict1['period_of_insurance_end_date'] = Policy_Period_Of_Insurance[ii][jj].replace(':','').replace('Midnight','')
                    elif Policy_Period_Of_Insurance[ii][jj].__contains__('Policy issued on'):
                        dict1['policy_issuance_date'] = Policy_Period_Of_Insurance[ii][jj+1].replace(' -', '')
        else:
            dict1['policy_issuance_date'] = ''
            dict1['period_of_insurance_end_date'] = ''
            dict1['period_of_insurance_start_date']=''
    else:
        dict1['policy_issuance_date'] = ''
        dict1['period_of_insurance_end_date'] = ''
        dict1['period_of_insurance_start_date']=''
    print(dict1['period_of_insurance_start_date'])
    print(dict1['period_of_insurance_end_date'])
    print(dict1['policy_issuance_date'])
    print('*************************************Insured Name*********************************************')
    Insured_Name = []
    Insured_Name_temp=False
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Insured Name"):
            Insured_Name_temp = True
        if "Insured Address" in lines[i]:
            break
        if not Insured_Name_temp:
            continue
        data_list = lines[i].replace('\n', '').replace(':', '').split("  ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        print(data_list)
        for i in range(len(data_list)):
            if data_list[i].__contains__('Insured Name'):
                Insured_Name = data_list[i + 1]
    if Insured_Name:
        dict1['insured_name'] = Insured_Name
    else:
        dict1['insured_name'] = ''
    print(dict1['insured_name'])
    print('*************************************Insured Address*********************************************')
    Insured_Address = ''
    Insured_Address_temp = False
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Insured Address"):
            Insured_Address_temp = True
        if "Customer ID" in lines[i]:
            break
        if not Insured_Address_temp:
            continue
        data_list = lines[i].replace('\n', '').replace(':', '').replace('Insured Address','').split("  ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
    #     print(data_list)
        for i in range(len(data_list)):
            Insured_Address+=data_list[i]
    if Insured_Address:
        dict1['address'] = Insured_Address
        try:
            addr = dict1["address"]
            z = 0
            dict1["customer_state"] = ""
            for state in states:
                if state.upper() in Insured_Address.upper():
                    dict1["customer_state"] = state
                    z = 1
                    break
            pattern4 = re.compile(r"\d\d\d\d\d\d")
            x = pattern4.search(addr)
            pincode = x.group()
            dict1["pincode"] = pincode
            print('sdb' + pincode)
        except:
            try:
                addr = addr.upper()
                df = pd.read_csv("pincode_final.csv", engine='python')
                if dict1["customer_state"] != "":
                    df = df[df["statename"] == state]
                region = df['regionname'].unique().tolist()
                region = [x for x in region if str(x) != 'nan']
                reg = False
                dis = False
                tal = False
                k = 0
                for i in region:
                    if i in addr:
                        print("region")
                        k = 1
                        reg = True
                        break
                if k == 1:
                    df = df[df["regionname"] == i]
                district = df["Districtname"].unique().tolist()
                district = [x for x in district if str(x) != 'nan']
                k = 0
                for i in district:
                    if i in addr:
                        print("district")
                        k = 1
                        dis = True
                        break
                if k == 1:
                    df = df[df["Districtname"] == i]
                taluk = df["Taluk"].unique().tolist()
                taluk = [x for x in taluk if str(x) != 'nan']
                k = 0
                if taluk != []:
                    for i in taluk:
                        if i in addr:
                            print("taluk")
                            print(i)
                            k = 1
                            tal = True
                            break
                if k == 1:
                    df = df[df["Taluk"] == i]
                try:
                    if reg is True or dis is True or tal is True:
                        dict1["pincode"] = str(df.iloc[0]["pincode"])
                    else:
                        print("No Match")
                        dict1["pincode"] = ""
                except:
                    print("Not there")
            except:
                print("Pincode Excel")
                dict1["pincode"] = ''
    else:
        dict1['address'] = ''
    print(dict1['address'])
    print('*************************************Vehicle Details*********************************************')
    Vehicle_Details = []
    Vehicle_Details_2 = []
    final_res = []
    json_da = read_pdf(path_s, pages=int(page_no), output_format='json',silent=True,lattice=True)
    Vehicle_jsondata = json_da[0].get('data')
    for i in range(len(Vehicle_jsondata)):
        for j in range(len(Vehicle_jsondata[i])):
            Vehicle_Details.append(Vehicle_jsondata[i][j].get('text'))
    print(Vehicle_Details)
    print(len(Vehicle_Details))
    if len(Vehicle_Details) == 18:
        two_split = np.array_split(Vehicle_Details, 2)
        for array in two_split:
            Vehicle_Details_2.append(list(array))
        if len(Vehicle_Details_2) == 2:
            for i1 in range(len(Vehicle_Details_2[1])):
                final_res.append(Vehicle_Details_2[1][i1])
    print(final_res)
    print('================================================Registration Number=============================================================')
    if final_res:
        dict1['registration_no'] = final_res[0]
    else:
        dict1['registration_no'] = ''
    print(dict1['registration_no'])
    print('================================================Vehicle Make=============================================================')
    if final_res:
        dict1['make'] = final_res[2].replace('\r',' ')
    else:
        dict1['make'] = ''
    print(dict1['make'])
    print('================================================Vehicle Model=============================================================')
    if final_res:
        dict1['model'] = final_res[4].replace('- ','').replace('\r',' ')
    else:
        dict1['model'] = ''
    print(dict1['model'])
    print('================================================Cubic Capacity/ Kilowatt=============================================================')
    if final_res:
        dict1['cubic_capacity'] = final_res[5]
    else:
        dict1['cubic_capacity'] = ''
    print(dict1['cubic_capacity'])
    print('================================================Year of Manufacture=============================================================')
    if final_res:
        dict1['mfg_yr'] = final_res[6]
    else:
        dict1['mfg_yr'] = ''
    print(dict1['mfg_yr'])
    print('================================================Chassis Number=============================================================')
    print(final_res)
    if final_res:
        dict1['chassis_no'] = final_res[8].replace(' ','')
    else:
        dict1['chassis_no'] = ''
    print(dict1['chassis_no'])
    # print(
    #     '================================================Engine Number=============================================================')
    # if final_res:
    #     dict1['engine_no'] = final_res[8].replace(' ','')
    # else:
    #     dict1['engine_no'] = ''
    # print(dict1['engine_no'])

    print('================================================No Claim Bonus=============================================================')
    No_Claim_Bonus = []
    No_Claim_Bonus_temp=False
    for i in range(len(lines)):
        if str(lines[i]).__contains__("No Claim Bonus"):
            No_Claim_Bonus_temp = True
        if "Nominee Details" in lines[i]:
            break
        if not No_Claim_Bonus_temp:
            continue
        data_list = lines[i].replace('\n', '').replace(':', '').split("  ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        for i in range(len(data_list)):
            if data_list[i].__contains__('No Claim Bonus'):
                No_Claim_Bonus = (data_list[i + 1])
    if No_Claim_Bonus:
        dict1['No_Claim_Bonus'] = No_Claim_Bonus
    else:
        dict1['No_Claim_Bonus'] = ''
    print(dict1['No_Claim_Bonus'])
    print('================================================Nominee Details=============================================================')
    Nominee_Details = []
    Nominee_Details_temp = False
    nominee_for_owner_driver_nominee_name=''
    nominee_for_owner_driver_nominee_relation=''
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Nominee Details"):
            Nominee_Details_temp = True
        if "Compulsory Deductible" in lines[i]:
            break
        if not Nominee_Details_temp:
            continue
        data_list = lines[i].replace('\n', '').replace(':', '').split("  ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        print(data_list)
        for i in range(len(data_list)):
            if data_list[i].__contains__('Name') and data_list[i+1].__contains__('Relationship') :
                nominee_for_owner_driver_nominee_name=''
            if data_list[i].__contains__('Name') and data_list[i+2].__contains__('Relationship') :
                nominee_for_owner_driver_nominee_name=data_list[i+1]
            if data_list[i].__contains__('Relationship') and data_list[-1].__contains__('Relationship'):
                nominee_for_owner_driver_nominee_relation=''
            if data_list[i].__contains__('Relationship') and not data_list[-1].__contains__('Relationship'):
                nominee_for_owner_driver_nominee_relation=data_list[i+1]
    if nominee_for_owner_driver_nominee_name:
        dict1['nominee_for_owner_driver_nominee_name'] = nominee_for_owner_driver_nominee_name
    else:
        dict1['nominee_for_owner_driver_nominee_name'] = ''
    if nominee_for_owner_driver_nominee_relation:
        dict1['nominee_for_owner_driver_nominee_relation'] = nominee_for_owner_driver_nominee_relation
    else:
        dict1['nominee_for_owner_driver_nominee_relation'] = ''
    print(dict1['nominee_for_owner_driver_nominee_name'])
    print(dict1['nominee_for_owner_driver_nominee_relation'])
    print(dict1)
    name = 'CERTIFICATE_CUM_POLICY_FOR_COMMERCIAL'
    return dict1,name
def Certificate_of_Insurance(fw,file_name,path_s,page_no):
    lines = fw
    var1 = ''
    dict1 = {}

    print('*************************************Policy Number*********************************************')
    pathology = False
    tem_policy_number=''
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Policy Number"):
            pathology = True
        if "Particulars of Vehicle Insured" in lines[i]:
            break
        if not pathology:
            continue
        data_list = lines[i].replace('\n', '').split("  ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        print(data_list)
        for jj in range(len(data_list)):
            if data_list[jj].__contains__('Policy Number'):
                tem_policy_number=data_list[jj].replace('Policy Number','').replace(':','')
    if tem_policy_number:
        dict1['policy_number']=tem_policy_number
    else:
        dict1['policy_number'] = ''
    print(dict1['policy_number'])
    print('*************************************Vehicle Insured*********************************************')
    Vehicle_Details = []
    temp_didv=[]
    final_res = []
    json_da = read_pdf(path_s, pages=int(page_no), output_format='json', silent=True,lattice=True)
    print(json_da)
    Vehicle_jsondata = json_da[0].get('data')
    Vehicle_jsondata2 = json_da[1].get('data')
    for i in range(len(Vehicle_jsondata)):
        for j in range(len(Vehicle_jsondata[i])):
            Vehicle_Details.append(Vehicle_jsondata[i][j].get('text'))
    Vehicle_Details=clean_list(Vehicle_Details)
    print(len(Vehicle_Details))
    if len(Vehicle_Details)==10:
        two_split = np.array_split(Vehicle_Details, 2)
        for array in two_split:
            temp_didv.append(list(array))
        print(temp_didv)
        if len(temp_didv) == 2:
            for i1 in range(len(temp_didv[1])):
                final_res.append(temp_didv[1][i1].replace('\r', ''))
    print(final_res)
    if final_res:
        if len(final_res)==5:
            print('==========================Registration Number==========================================')
            dict1['registration_no']=final_res[0]
            print( dict1['registration_no'])
            print('==========================Engine Number==========================================')
            dict1['engine_no'] = final_res[2]
            print(dict1['engine_no'])
            print('==========================Chassis Number==========================================')
            temP_chassis_no = final_res[3]
            dict1['chassis_no'] = temP_chassis_no
            print(dict1['chassis_no'])
            print('==========================Make and Model ==========================================')
            temP_Make_Model=str(final_res[4]).replace('\r','').split('-')
            if len(temP_Make_Model)==2:
                dict1['make'] = temP_Make_Model[0]
                print(dict1['make'])
                print('==========================Model==========================================')
                dict1['model'] = temP_Make_Model[1]
                print(dict1['model'])
    else:
        dict1['registration_no']=''
        dict1['engine_no']=''
        dict1['chassis_no']=''
        dict1['make']=''
        dict1['model']=''
    print('*************************************Vehicle Insured 2*********************************************')
    Vehicle_Details_2=[]
    final_res_2=[]
    temp_didv_2=[]
    for i in range(len(Vehicle_jsondata2)):
        for j in range(len(Vehicle_jsondata2[i])):
            Vehicle_Details_2.append(Vehicle_jsondata2[i][j].get('text'))
    Vehicle_Details_2=clean_list(Vehicle_Details_2)
    if len(Vehicle_Details_2)==10:
        two_split = np.array_split(Vehicle_Details_2, 2)
        for array in two_split:
            temp_didv_2.append(list(array))
    if len(temp_didv_2)==2:
        for jj in range(len(temp_didv_2[1])):
            final_res_2.append(temp_didv_2[1][jj])
    if final_res_2:
        print('==========================Year of Mfg==========================================')
        dict1['mfg_yr']=final_res_2[1]
        print(dict1['mfg_yr'])
        print('==========================CC==========================================')
        dict1['cubic_capacity'] = final_res_2[3]
        print(dict1['cubic_capacity'])
    else:
        dict1['mfg_yr']=''
        dict1['cubic_capacity']
    print('*************************************Name and Address of Insured*********************************************')
    Name_Insured= ''
    Address_Insured=''
    Name_and_Address_ofInsured=False
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Name and Address of Insured"):
            Name_and_Address_ofInsured = True
        if "Geographical Area" in lines[i]:
            break
        if not Name_and_Address_ofInsured:
            continue
        data_list = lines[i].replace('\n', '').replace(':', '').split("  ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        for i in range(len(data_list)):
            if data_list[i].__contains__('Name and Address of Insured'):
                Name_Insured = (data_list[i + 1])
            else:
                Address_Insured +=data_list[i]
    if Name_Insured:
        dict1['insured_name']=Name_Insured
    else:
        dict1['insured_name']=''
    if Address_Insured:
        dict1['address'] = Address_Insured.replace(Name_Insured,'')
    else:
        dict1['address'] = ''
    print(dict1['insured_name'])
    print(dict1['address'])
    print('************************************Pincode*********************************************')
    if Address_Insured:
        try:
            addr = Address_Insured
            z = 0
            dict1["customer_state"] = ""
            for state in states:
                if state.upper() in Address_Insured.upper():
                    dict1["customer_state"] = state
                    z = 1
                    break
            pattern4 = re.compile(r"\d\d\d\d\d\d")
            x = pattern4.search(addr)
            pincode = x.group()
            dict1["pincode"] = pincode
            print('sdb' + pincode)
        except:
            try:
                addr = addr.upper()
                df = pd.read_csv("pincode_final.csv", engine='python')
                if dict1["customer_state"] != "":
                    df = df[df["statename"] == state]
                region = df['regionname'].unique().tolist()
                region = [x for x in region if str(x) != 'nan']
                reg = False
                dis = False
                tal = False
                k = 0
                for i in region:
                    if i in addr:
                        print("region")
                        k = 1
                        reg = True
                        break
                if k == 1:
                    df = df[df["regionname"] == i]
                district = df["Districtname"].unique().tolist()
                district = [x for x in district if str(x) != 'nan']
                k = 0
                for i in district:
                    if i in addr:
                        print("district")
                        k = 1
                        dis = True
                        break
                if k == 1:
                    df = df[df["Districtname"] == i]
                taluk = df["Taluk"].unique().tolist()
                taluk = [x for x in taluk if str(x) != 'nan']
                k = 0
                if taluk != []:
                    for i in taluk:
                        if i in addr:
                            print("taluk")
                            print(i)
                            k = 1
                            tal = True
                            break
                if k == 1:
                    df = df[df["Taluk"] == i]
                try:
                    if reg is True or dis is True or tal is True:
                        dict1["pincode"] = str(df.iloc[0]["pincode"])
                    else:
                        print("No Match")
                        dict1["pincode"] = ""
                except:
                    print("Not there")
            except:
                print("Pincode Excel")
                dict1["pincode"] = ''
        print(dict1["pincode"])
        print(dict1["customer_state"])
    else:
        dict1["pincode"]=''
        dict1["customer_state"]=''
    print('************************************Policy Inception Date and Policy Expiry Date*********************************************')
    start_and_end=False
    start_date=''
    end_date=''
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Policy Inception Date"):
            start_and_end = True
        if "Persons or Class of Persons entitled to drive" in lines[i]:
            break
        if not start_and_end:
            continue
        data_list = lines[i].replace('\n', '').split("Date:")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        print(data_list)
        for i in range(len(data_list)):
            if data_list[i].__contains__('Policy Inception'):
                start_date = (data_list[i + 1]).replace('From','').replace('Clock on','').replace('00:01','').replace("O'",'').replace(' ','')
            elif data_list[i].__contains__('Policy Expiry'):
                end_date=(data_list[i + 1]).replace('Midnight','').replace('on','').replace(' ','')
    if start_date:
        dict1['period_of_insurance_start_date']=start_date
    else:
        dict1['period_of_insurance_start_date']=''
    if end_date:
        dict1['period_of_insurance_end_date'] = end_date
    else:
        dict1['period_of_insurance_end_date'] = ''
    print(dict1['period_of_insurance_start_date'])
    print(dict1['period_of_insurance_end_date'])
    print('***********************************************Policy_Issuance_Date*****************************************')
    Policy_Issuance_Date = ''
    Policy_Issuance_Date_torf = False
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Date of issue"):
            Policy_Issuance_Date_torf = True
        if "For & On Behalf" in lines[i]:
            break
        if not Policy_Issuance_Date_torf:
            continue
        data_list = lines[i].replace('\n', '').split(":")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        for i in range(len(data_list)):
            if data_list[i].__contains__('Date of issue'):
                Policy_Issuance_Date = (data_list[i + 1])
    if Policy_Issuance_Date:
        dict1['policy_issuance_date'] = Policy_Issuance_Date
    else:
        dict1['policy_issuance_date'] = ''
    print(dict1['policy_issuance_date'])
    print('**************************************************Closed******************************************************')
    name='Certificate_of_Insurance'
    return dict1,name
def PACKAGE_POLICY_SCHEDULE(fw,file_name,path_s,page_no):
    lines = fw
    var1 = ''
    dict1 = {}

    print('*************************************Insured Name And policy number*********************************************')
    pathology = False
    Insured_Name=''
    Policy_Number=''
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Insured Name"):
            pathology = True
        if "Policy Issued on" in lines[i]:
            break
        if not pathology:
            continue
        data_list = lines[i].replace('\n', '').split("  ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        print(data_list)
        for jj in range(len(data_list)):
            if data_list[jj].__contains__('Insured Name') and not data_list[jj+1].__contains__('Policy Number') :
                Insured_Name=data_list[jj+1]
            elif data_list[jj].__contains__('Policy Number') and not data_list[-1].__contains__('Policy Number'):
                Policy_Number=data_list[jj+1]

    if Insured_Name:
        dict1['insured_name']=Insured_Name
    else:
        dict1['insured_name'] = ''
    if Policy_Number:
        dict1['policy_number'] = Policy_Number
    else:
        dict1['policy_number'] = ''
    print(dict1['insured_name'])
    print(dict1['policy_number'])
    print('*************************************Insured Address of Insured*********************************************')
    Policy_Issued_on= ''
    Address_Insured=''
    Policy_Period_start=''
    rep_2=''
    rep_1=''
    Name_and_Address_ofInsured=False
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Policy Issued on"):
            Name_and_Address_ofInsured = True
        if "Policy Period" in lines[i]:
            break
        if not Name_and_Address_ofInsured:
            continue
        data_list = lines[i].replace('\n', '').replace(':', '').split("  ")
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        for i in range(len(data_list)):
            if data_list[i].__contains__('Policy Issued on') and not data_list[-1].__contains__('Policy Issued on') :
                rep_1=data_list[i + 1]
                temp_Policy_Issued_on = (data_list[i + 1]).split(' ')
                Policy_Issued_on=temp_Policy_Issued_on[0]
            elif data_list[i].__contains__('From') and not data_list[-1].__contains__('From'):
                rep_2 = data_list[i + 1]
                temp_Policy_Period_start=(data_list[i + 1]).split(' ')
                Policy_Period_start=temp_Policy_Period_start[0]
            else:
                Address_Insured +=data_list[i]
    if Address_Insured:
        dict1['address'] = Address_Insured.replace(rep_1,'').replace(rep_2,'').replace('Address','').replace('Insured',' ')
    else:
        dict1['address'] = ''
    print(dict1['address'])
    print('************************************Pincode*********************************************')
    if Address_Insured:
        try:
            addr = Address_Insured
            z = 0
            dict1["customer_state"] = ""
            for state in states:
                if state.upper() in Address_Insured.upper():
                    dict1["customer_state"] = state
                    z = 1
                    break
            pattern4 = re.compile(r"\d\d\d\d\d\d")
            x = pattern4.search(addr)
            pincode = x.group()
            dict1["pincode"] = pincode
            print('sdb' + pincode)
        except:
            try:
                addr = addr.upper()
                df = pd.read_csv("pincode_final.csv", engine='python')
                if dict1["customer_state"] != "":
                    df = df[df["statename"] == state]
                region = df['regionname'].unique().tolist()
                region = [x for x in region if str(x) != 'nan']
                reg = False
                dis = False
                tal = False
                k = 0
                for i in region:
                    if i in addr:
                        print("region")
                        k = 1
                        reg = True
                        break
                if k == 1:
                    df = df[df["regionname"] == i]
                district = df["Districtname"].unique().tolist()
                district = [x for x in district if str(x) != 'nan']
                k = 0
                for i in district:
                    if i in addr:
                        print("district")
                        k = 1
                        dis = True
                        break
                if k == 1:
                    df = df[df["Districtname"] == i]
                taluk = df["Taluk"].unique().tolist()
                taluk = [x for x in taluk if str(x) != 'nan']
                k = 0
                if taluk != []:
                    for i in taluk:
                        if i in addr:
                            print("taluk")
                            print(i)
                            k = 1
                            tal = True
                            break
                if k == 1:
                    df = df[df["Taluk"] == i]
                try:
                    if reg is True or dis is True or tal is True:
                        dict1["pincode"] = str(df.iloc[0]["pincode"])
                    else:
                        print("No Match")
                        dict1["pincode"] = ""
                except:
                    print("Not there")
            except:
                print("Pincode Excel")
                dict1["pincode"] = ''
        print(dict1["pincode"])
        print(dict1["customer_state"])
    else:
        dict1["pincode"]=''
        dict1["customer_state"]=''
    print('***********************************************Policy_Issuance_Date*****************************************')
    if Policy_Issued_on:
        dict1['policy_issuance_date'] = Policy_Issued_on
    else:
        dict1['policy_issuance_date'] = ''
    print(dict1['policy_issuance_date'])
    print('************************************Policy Expiry Date*********************************************')
    start_and_end=False
    end_date=''
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Policy Period"):
            start_and_end = True
        if "Geographical" in lines[i]:
            break
        if not start_and_end:
            continue
        data_list = lines[i].replace('\n', '').split(':')
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        print(data_list)
        for i in range(len(data_list)):
            if data_list[i].__contains__('Policy Period'):
                end_date = (data_list[i + 1]).replace('Midnight','').replace(' ','')
    if Policy_Period_start:
        dict1['period_of_insurance_start_date']=Policy_Period_start
    else:
        dict1['period_of_insurance_start_date']=''
    if end_date:
        dict1['period_of_insurance_end_date'] = end_date
    else:
        dict1['period_of_insurance_end_date'] = ''
    print(dict1['period_of_insurance_start_date'])
    print(dict1['period_of_insurance_end_date'])
    print('************************************Previous Policy No*********************************************')
    Previous_Policy_No = False
    Previous_Policy_No_data = ''
    for i in range(len(lines)):
        if str(lines[i]).__contains__("Previous Policy No"):
            Previous_Policy_No = True
        if "Bank Reference" in lines[i]:
            break
        if not Previous_Policy_No:
            continue
        data_list = lines[i].replace('\n', '').split('No')
        if not len(data_list) > 0:
            continue
        data_list = clean_list(data_list)
        print(data_list)
        for i in range(len(data_list)):
            if data_list[i].__contains__('Previous Policy'):
                Previous_Policy_No_data = (data_list[i + 1]).replace(' ', '')
    if Previous_Policy_No_data:
        dict1['previous_policy_number'] = Previous_Policy_No_data
    else:
        dict1['previous_policy_number'] = ''
    print(dict1['previous_policy_number'])
    print('**************************************************Vechile details******************************************************')
    Vehicle_Details = []
    temp_Vechile=[]
    temp_didv=[]
    final_res = []
    json_da = read_pdf(path_s, pages=int(page_no), output_format='json', silent=True)
    Vehicle_jsondata = json_da[2].get('data')
    for i in range(len(Vehicle_jsondata)):
        for j in range(len(Vehicle_jsondata[i])):
            Vehicle_Details.append(Vehicle_jsondata[i][j].get('text'))
    output_1 = []
    temp_1 = []
    for item in Vehicle_Details:
        if item == 'NCB %':
            output_1.append(temp_1)
            temp_1 = []
        temp_1.append(item)
    if temp_1:
        output_1.append(temp_1)
    if output_1:
        if len(output_1) == 2:
            temp_Vechile = output_1[0]
    if temp_Vechile:
        if len(temp_Vechile) == 12:
            two_split = np.array_split(temp_Vechile, 2)
            for array in two_split:
                temp_didv.append(list(array))
            if len(temp_didv) == 2:
                for i1 in range(len(temp_didv[1])):
                    final_res.append(temp_didv[1][i1])
    print(final_res)
    if final_res:
        if len(final_res)==6:
            print('==========================Registration Number==========================================')
            dict1['registration_no']=final_res[0]
            print( dict1['registration_no'])
            print('==========================Engine Number==========================================')
            dict1['engine_no'] = final_res[2]
            print(dict1['engine_no'])
            print('==========================Chassis Number==========================================')
            temP_chassis_no = str(final_res[3]).replace('\r', '')
            dict1['chassis_no'] = temP_chassis_no
            print(dict1['chassis_no'])
            print('==========================Make and Model ==========================================')
            temP_Make_Model=str(final_res[4]).replace('\r','').replace('MOTO-CORP','AND').replace('-','').split('AND')
            dict1['make'] = temP_Make_Model[0]
            print(dict1['make'])
            print('==========================Model==========================================')
            dict1['model'] = temP_Make_Model[1].lstrip()
            print(dict1['model'])
    else:
        dict1['registration_no']=''
        dict1['engine_no']=''
        dict1['chassis_no']=''
        dict1['make']=''
        dict1['model']=''
    print('*************************************Vehicle Insured 2*********************************************')
    output_2 = []
    temp_2 = []
    temp_vech=[]
    VehicleInsured2=[]
    temp_didv2=[]
    final_res_2=[]
    if output_1:
        if len(output_1) == 2:
            temp_vech = output_1[1]
    if temp_vech:
        for item in temp_vech:
            if item == 'Vehicle IDV':
                output_2.append(temp_2)
                temp_2 = []
            temp_2.append(item)
        if temp_2:
            output_2.append(temp_2)
    if output_2:
        VehicleInsured2=output_2[0]
    if VehicleInsured2:
        if len(VehicleInsured2) == 12:
            two_split = np.array_split(VehicleInsured2, 2)
            for array in two_split:
                temp_didv2.append(list(array))
            if len(temp_didv2) == 2:
                for i1 in range(len(temp_didv2[1])):
                    final_res_2.append(temp_didv2[1][i1])
    if final_res_2:
        if len(final_res_2) == 6:
            print('==========================Year Of Manufacturing==========================================')
            dict1['mfg_yr'] = final_res_2[3]
            print(dict1['mfg_yr'])
            print('==========================Seating Capacity==========================================')
            dict1['cubic_capacity'] = final_res_2[1]
            print(dict1['cubic_capacity'])
    else:
        dict1['mfg_yr'] = ''
        dict1['cubic_capacity'] = ''
    print('*************************************Closed*********************************************')

    name='POLICY-PC THROUGH CSC SCHEDULE'
    return dict1,name
