import glob
import os
from os.path import basename
from Get_the_Result import Transcript_of_Proposal,Coverage_opted,CERTIFICATE_CUM_POLICY,pdf_to_img,Certificate_of_Insurance,PACKAGE_POLICY_SCHEDULE,Transcript_of_Proposal_for_Commercial,CERTIFICATE_CUM_POLICY_FOR_COMMERCIAL
import pandas as pd
from shutil import copyfile

Transcript_of_Proposal_data={}
Coverage_opted_data={}
CERTIFICATE_CUM_POLICY_data={}
Certificate_of_Insurance_data={}
PACKAGE_POLICY_SCHEDULE_data={}
product_type='Four Wheeler'

def Format_Wise_main(file_name,path_s,page_no):
    global Transcript_of_Proposal_data
    global Coverage_opted_data
    global CERTIFICATE_CUM_POLICY_data
    global PACKAGE_POLICY_SCHEDULE_data
    file = str(file_name)
    print(file)
    f = open(file, 'r',encoding='utf-8')
    z = []
    s = ""
    for line in f:
        if not (line == '\n' or line == ''):
            z.append(line)
            s = s + line
    global product_type
    if s.upper().__contains__("TWO WHEELER"):
        product_type='Two Wheeler'
    print(product_type)
    if s.__contains__("Transcript of Proposal") and (s.replace('-',' ').upper().__contains__("FOR TWO WHEELER") or s.__contains__("for Motor Comprehensive") or s.__contains__("For Private Car")) :
        Transcript_of_Proposal_data,name=Transcript_of_Proposal(z,file_name,path_s,page_no)
        print(name)
    if s.__contains__("Transcript of Proposal") and s.upper().__contains__("FOR COMMERCIAL VEHICLE") :
        Transcript_of_Proposal_data,name=Transcript_of_Proposal_for_Commercial(z,file_name,path_s,page_no)
        print(name)
    if s.__contains__("Coverage opted")  :
        Coverage_opted_data,name = Coverage_opted(z,file_name,path_s,page_no)
        print(name)
    if s.__contains__("CERTIFICATE CUM POLICY") and not s.__contains__("COMMERCIAL VEHICLE"):
        CERTIFICATE_CUM_POLICY_data,name = CERTIFICATE_CUM_POLICY(z,file_name,path_s,page_no)
        print(name)
    if s.__contains__("CERTIFICATE CUM POLICY") and  s.__contains__("COMMERCIAL VEHICLE"):
        CERTIFICATE_CUM_POLICY_data,name = CERTIFICATE_CUM_POLICY_FOR_COMMERCIAL(z,file_name,path_s,page_no)
        print(name)
    if s.__contains__("Certificate of Insurance"):
        CERTIFICATE_CUM_POLICY_data,name=Certificate_of_Insurance(z,file_name,path_s,page_no)
        print(name)
        print(Certificate_of_Insurance_data)
    if s.__contains__("POLICY-PC THROUGH CSC SCHEDULE") or s.__contains__("PACKAGE POLICY SCHEDULE") :
        PACKAGE_POLICY_SCHEDULE_data,name=PACKAGE_POLICY_SCHEDULE(z,file_name,path_s,page_no)
        print(name)
        print(PACKAGE_POLICY_SCHEDULE_data)
    return
def Get_Final_data():
    dict_result = {}
    dict_result['document_type'] = "Policy"
    dict_result['previous_policy_number'] = ''
    dict_result['document_format']="pdf"
    dict_result['previous_insurer_name'] = 'Bajaj Allianz General Insurance Company Ltd.'
    dict_result['date_of_registration']=''
    dict_result['rto'] = ''
    dict_result['registration_no']=''
    dict_result['financier_branch']=''
    dict_result['financier_name'] = ''
    dict_result['hypothecation'] = ''
    dict_result['ncb'] = ''
    dict_result['previous_policy_number'] = ''
    dict_result['previous_policy_type'] = ''
    dict_result['product_type'] = product_type
    dict_result['rto'] = ''
    dict_result['salutation'] = ''
    dict_result['source_system'] = 'OCR'
    dict_result['previous_policy_number']=''
    dict_result['policy_number']=''
    Transcript_of_Proposal_data_final={}
    CERTIFICATE_CUM_POLICY_data_Final={}
    PACKAGE_POLICY_SCHEDULE_data_Final = {}
    temp1=Transcript_of_Proposal_data
    temp2=Coverage_opted_data
    temp3=CERTIFICATE_CUM_POLICY_data
    temp4=PACKAGE_POLICY_SCHEDULE_data
    if temp1 and temp2:
        temp1.update(temp2)
        Transcript_of_Proposal_data_final=temp1
        print('1')
    elif temp1 and not temp2:
        Transcript_of_Proposal_data_final = Transcript_of_Proposal_data
        print('2')
    if temp3:
        CERTIFICATE_CUM_POLICY_data_Final = temp3
        print('3')
    if temp4:
        PACKAGE_POLICY_SCHEDULE_data_Final=temp4
        print('4')
    if Transcript_of_Proposal_data_final and CERTIFICATE_CUM_POLICY_data_Final and PACKAGE_POLICY_SCHEDULE_data_Final:
        print('5')
        for dict_ in (Transcript_of_Proposal_data_final, CERTIFICATE_CUM_POLICY_data_Final,PACKAGE_POLICY_SCHEDULE_data_Final):
            for key, val in dict_.items():
                if not val == 'NA' or not val == '':
                    filtered_dict = {key: val}
                    dict_result.update(filtered_dict)
    elif Transcript_of_Proposal_data_final and CERTIFICATE_CUM_POLICY_data_Final and not PACKAGE_POLICY_SCHEDULE_data_Final:
        print('6')
        for dict_ in (Transcript_of_Proposal_data_final, CERTIFICATE_CUM_POLICY_data_Final):
            for key, val in dict_.items():
                if not val == 'NA' or not val == '':
                    filtered_dict = {key: val}
                    dict_result.update(filtered_dict)
    elif not Transcript_of_Proposal_data_final and CERTIFICATE_CUM_POLICY_data_Final and  PACKAGE_POLICY_SCHEDULE_data_Final:
        print('7')
        for dict_ in (PACKAGE_POLICY_SCHEDULE_data_Final, CERTIFICATE_CUM_POLICY_data_Final):
            for key, val in dict_.items():
                if not val == 'NA' or not val == '':
                    filtered_dict = {key: val}
                    dict_result.update(filtered_dict)
    elif  Transcript_of_Proposal_data_final and not CERTIFICATE_CUM_POLICY_data_Final and  PACKAGE_POLICY_SCHEDULE_data_Final:
        print('8')
        for dict_ in (PACKAGE_POLICY_SCHEDULE_data_Final, Transcript_of_Proposal_data_final):
            for key, val in dict_.items():
                if not val == 'NA' or not val == '':
                    filtered_dict = {key: val}
                    dict_result.update(filtered_dict)
    elif Transcript_of_Proposal_data_final and not CERTIFICATE_CUM_POLICY_data_Final and not PACKAGE_POLICY_SCHEDULE_data_Final:
        dict_result.update(Transcript_of_Proposal_data_final)
        print('9')
    elif not Transcript_of_Proposal_data_final and CERTIFICATE_CUM_POLICY_data_Final and not PACKAGE_POLICY_SCHEDULE_data_Final:
        dict_result.update(CERTIFICATE_CUM_POLICY_data_Final)
        print('10')
    elif not Transcript_of_Proposal_data_final and not CERTIFICATE_CUM_POLICY_data_Final and  PACKAGE_POLICY_SCHEDULE_data_Final:
        dict_result.update(PACKAGE_POLICY_SCHEDULE_data_Final)
        print('11')

    rto=''
    if dict_result['registration_no']:
        temp_rto=dict_result['registration_no']
        rto=temp_rto[0:4]
    else:
        dict_result['rto']=''
    if rto:
        os.path.join(os.getcwd(), 'static', 'RTO.xlsx')
        df = pd.read_excel(os.path.join(os.getcwd(), 'static', 'RTO.xlsx'))
        if rto!= "":
            df = df[df["RegNo"] == rto]
            region = df['Place'].unique().tolist()
            if dict_result['customer_state']== "":
                stat=df['State'].unique().tolist()
                dict_result['customer_state']=stat[0]
        dict_result['rto']=region[0]
        print(dict_result['rto'])
    if dict_result['previous_policy_number']=='' and dict_result['policy_number']:
        dict_result['previous_policy_number']=dict_result['policy_number']
    print(dict_result)
    return dict_result

def create_folder(folder):
    path_s = os.path.join(os.getcwd(), str(folder))
    try:
        os.mkdir(path_s)
    except OSError:
        print("Creation of the directory %s failed" % path_s)
    else:
        print("Successfully created the directory %s " % path_s)

def main_run(file_name):
    folder = "Temp_bajaj_pdfs"
    dict_result={}
    print(file_name)
    if not os.path.exists(os.path.join(os.getcwd(), folder)):
        create_folder(folder)
    copyfile(file_name,os.path.join(os.getcwd(), str(folder),basename(file_name)))
    path_s = os.path.join(os.getcwd(), str(folder), basename(file_name))
    pdf_to_img(path_s, folder)
    idct = {}
    if os.path.exists(os.path.join(os.getcwd(), folder)):
        entries = os.listdir(str(folder))
        for i in range(len(entries)):
            if entries[i].endswith('txt'):
                page_no = i
                file_names = path_s.replace('.pdf', '').replace('PDF', '').replace('.', '')
                Format_Wise_main(os.path.join(os.getcwd(), folder, file_names + str(i) + ".txt"), path_s,
                                 page_no)
                os.remove(os.path.join(os.getcwd(), folder, file_names + str(i) + ".txt"))
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        dict_result=Get_Final_data()
    os.remove(os.path.join(os.getcwd(), folder,path_s))
    return dict_result
if __name__ == '__main__':
    file_name=r'C:\Format WIse Category\pdf\1\bajaj.pdf'
    main_run(file_name)