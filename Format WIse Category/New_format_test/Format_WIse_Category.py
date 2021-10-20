import os
from Get_the_Result import Transcript_of_Proposal,Coverage_opted,CERTIFICATE_CUM_POLICY,pdf_to_img,Certificate_of_Insurance,PACKAGE_POLICY_SCHEDULE,Transcript_of_Proposal_for_Commercial,CERTIFICATE_CUM_POLICY_FOR_COMMERCIAL

Transcript_of_Proposal_data={}
Coverage_opted_data={}
CERTIFICATE_CUM_POLICY_data={}
Certificate_of_Insurance_data={}
PACKAGE_POLICY_SCHEDULE_data={}

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

def Get_Final_data():
    dict_result = {}
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
    print(dict_result)
    return dict_result

if __name__ == '__main__':
    file_name=r'Policy (6).pdf'
    folder = 'txtx'
    path_s = os.path.join(os.getcwd(), "pdf", str(folder), str(file_name))
    pdf_to_img(file_name, folder)
    idct = {}
    if os.path.exists(os.path.join(os.getcwd(), 'pdf', folder)):
        entries = os.listdir("pdf/" + str(folder))
        for i in range(len(entries)):
            if entries[i].endswith('txt'):
                page_no=i
                # print(entries[i], folder + str(i) + ".txt")
                file_names=file_name.replace('.pdf','').replace('PDF','').replace('.','')
                # print(file_names + str(i))
                Format_Wise_main(os.path.join(os.getcwd(), "pdf", folder, file_names + str(i) + ".txt"),path_s,page_no)
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        Get_Final_data()