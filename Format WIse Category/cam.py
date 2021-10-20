# from tabula import read_pdf
# from tabulate import tabulate
# import camelot
# import numpy as np
# lists=[]
# list2=[]
# json_da=read_pdf(r'C:\Format WIse Category\pdf\bajaj.pdf', pages=1,output_format='json')
# jsondata=json_da[0].get('data')
# print(len(jsondata))
# for i in range(len(jsondata)):
#    for j in range(len(jsondata[i])):
#       lists.append(jsondata[i][j].get('text'))
# print(lists)
# print('****************************')
# two_split = np.array_split(lists, 5)
# for array in two_split:
#    list2.append(list(array))
# print(list2)
# final_res=[]
# if len(list2)==5:
#    for i in range(len(list2[3])):
#       final_res.append(list2[3][i] +' '+ list2[4][i])
# print(final_res)
#
#
#
# # Summary_of_Transactions={}
# # temp_list=[]
# # Summary_of_Transactions = {v: [] for v in list[:9]}
# # for i, v in enumerate(list[9:]):
# #    # print(v)
# #    # print('****************************')
# #    Summary_of_Transactions[list[i % 9]].append(v)
# # temp_list=Summary_of_Transactions['Vehicle']
# # print(temp_list)
# # liascbh=['v1','v2','v3']
# # Summary_of_Transactions1={'v1':[],'v2':[],'v3':[]}
# # for i, v in enumerate(temp_list):
# #    print(v)
# #    print('****************************')
# #    Summary_of_Transactions1[liascbh[i % 3]].append(v)
# # print(Summary_of_Transactions1)
# # del Summary_of_Transactions['Vehicle']
# # Summary_of_Transactions.update(Summary_of_Transactions1)
# # print(Summary_of_Transactions)
# import subprocess
# filename=r'C:\Format WIse Category\pdf\bajaj.pdf'
# a1='"' + filename + '"'
# # print("pdftotext -layout " + path_s + " -f "+ str(i) +" -l "+str(i)+"  "+filename+".txt")
# # subprocess.run("pdftotext -layout " + a + " -f 2 -l 2 1245xfbdfb.txt")
# subprocess.run("pdftotext −table " + a1 + " -f 1 -l 1 tablesss.txt")

# from tabula import read_pdf
# path_s=r'C:\Format WIse Category\pdf\Bajaj_! (9).pdf'
# json_da = read_pdf(path_s, pages=1, output_format='json',silent=True)
# Vehicle_jsondata = json_da[0].get('data')
# Vehicle_jsondata2 = json_da[1].get('data')
# print('######################################Result from table 1###################################################')
# print(Vehicle_jsondata)
# print('#########################################Result from table 2################################################')
# print(Vehicle_jsondata2)
# print('#########################################################################################')


# temp_didv=[['Registration Number', 'Place of Registration', 'Engine Number', 'Chassis Number', 'Make & Model'], ['JH04N3407', 'DUMKA', 'GRHF59001', 'MA1WY2GRKH5F05\r010', 'MAHINDRA AND\rMAHINDRA -\rBOLERO']]
# Temp_bajaj_pdfs=str(temp_didv[1][3]).replace(r'\r','')
# print(Temp_bajaj_pdfs)
# # for i in range(len(temp_didv[1])):
# #     tem_var = r'' + temp_didv[1][i] + ''.replace(r'\r', '')
# #     print(tem_var)
sentence=[[], [], ['Products Recall Exclusion'], ['As per Master Policy Wording'], [], ['Duty to Defend Endorsement'], ['It is understood and agreed that, notwithstanding anything contained in this Policy to the contrary, the Company shall not be called upon to assume'], ['charge of investigation, settlement or defense of any claim made, or suit brought, or proceedings instituted against the Insured with respect to bodily'], ['injury or property damage occurring in and/or any claim therefrom is brought in any territory where the Company is not legally allowed to assume charge'], ['of investigation, settlement or defense of any claim made, or suit brought, or proceedings instituted against the Insured, but shall have the right and'], ['be given the opportunity to be associated in the defense and trial of any such claims, suits or proceedings relative to any occurrence which, in the'], ['opinion of the Company, may create liability on the part of the Company under the terms of this policy.'], [], ['Absolute Pollution exclusion'], ['NOTWITHSTANDING anything to the contrary mentioned in the policy, it is hereby understood and agreed that COVERAGE A – BODILY INJURY AND PROPERTY'], ['DAMAGE LIABILITY Exclusion 2 f. is deleted in its entirety and replaced with the following (1) "Bodily injury" or "property damage" arising out of the'], ['actual, alleged or threatened discharge, dispersal, seepage, migration, release or escape of "pollutants" (a) At or from any premises, site or'], ['location which is or was at any time owned or occupied by, or rented or loaned to, any insured. (b) At or from any premises, site or location which is'], ['or was at any time used by or for any insured or others for the handling, storage, disposal, processing or treatment of waste (c) Which are or were at'], ['any time transported, handled, stored, treated, disposed of, or processed as waste by or for (i) Any insured or (ii) Any person or organization for'], ['whom you may be legally responsible or (d) At or from any premises, site or location on which any insured or any contractors or subcontractors working'], ['directly or indirectly on any insureds behalf are performing operations if the "pollutants" are brought on or to the premises, site or location in'], ['connection with such operations by such insured, contractor or subcontractor. At or from any premises, site or location on which any insured or any'], ['contractors or subcontractors working directly or indirectly on any insureds behalf are performing operations if the operations are to test for,'], ['monitor, clean up, remove, contain, treat, detoxify or neutralize, or in any way respond to, or assess the effects of, "pollutants". (2) Any loss, cost'], ['or expense arising out of any (a) Request, demand, order or statutory or regulatory requirement that any insured or others test for, monitor, clean'], ['up, remove, contain, treat, detoxify or neutralize, or in any way respond to, or assess the effects of, "pollutants" or (b) Claim or suit by or on'], ['behalf of a governmental authority for damages because of testing for, monitoring, cleaning up, removing, containing, treating, detoxifying or'], ['neutralizing, or in any way responding to, or assessing the effects of, "pollutants". All other terms and conditions remain unchanged.'], [], ['Definition of Aircraft Endorsement'], ['It is hereby understood and agreed that Definitions under General Liability Insurance Policy Provisions are amended by the addition of the following'], ['definition. “Aircraft” means any machine that can derive support in the atmosphere from the reactions of the air other than the reactions of the air'], ['against the earths surface and that is invented, used, or designed to navigate, or fly in the air, including, but not limited to, any aerospatial'], ['device, any airborne craft or vessel, unmanned aerial vehicle and/or any equipment which a person cannot structurally get on and can fly by remote'], ['control or auto-pilot stipulated in Civil Aeronautics Act of Japan. The definition aforementioned in this endorsement shall apply for interpretation'], ['of any coverage part and/or endorsements incorporated in this policy. The provisions of the General Liability Insurance Policy Provisions, the'], ['Coverage Part(s) and endorsement(s) attached to the policy shall be applied to all other matters than those stipulated in this endorsement in so far as'], ['such provisions are not inconsistent with the intent of the provisions of this endorsement.'], [], ['Cost Inclusive Endorsement'], ['As per Master Policy Wording'], [], ['Waiver of Subrogation Rights Endorsement'], ['It is hereby understood and agreed that the paragraph 6. Subrogation of the CONDITIONS of the General Liability Insurance Policy Provisions does not'], ['apply to the person or the party specified in the Declaration attached to the policy. Waiver of Subrogation Named Insured GE Company and its'], ['affiliates'], [], ['Flat Premium Endorsement'], ['It is hereby understood and agreed that notwithstanding Paragraph 1. Premium of CONDITIONS of General Liability Insurance Policy Provisions, the'], ['premium for this policy is a flat charge of the total premium specified in the Declaration attached to the policy and shall not be subject to any final'], ['audit.'], [], [], [], [], ['Page 21'], []]


output = []
Temp_bajaj_pdfs = []
for item in sentence:
    if len(item)==0:
        output.append(Temp_bajaj_pdfs)
        Temp_bajaj_pdfs = []
    Temp_bajaj_pdfs.append(item)
if Temp_bajaj_pdfs:
    output.append(Temp_bajaj_pdfs)
print(output)

# import os
# def create_folder():
#     path = "New_format_test/tmp"
#     try:
#         os.mkdir(path)
#     except OSError:
#         print("Creation of the directory %s failed" % path)
#     else:
#         print("Successfully created the directory %s " % path)
# create_folder()