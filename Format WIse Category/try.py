# from tabula import read_pdf
# path_s=r'D:\Format WIse Category\Temp_bajaj_pdfs\JH01CE1936.pdf'
# json_da = read_pdf(path_s, pages=1, output_format='json',silent=True,lattice=True)
# Vehicle_Details=[]
# Vehicle_Details1=[]
# # Vehicle_jsondata = json_da[0].get('data')
# Vehicle_jsondata2 = json_da[1].get('data')
# print('============================================================================================')
# # for i in range(len(Vehicle_jsondata)):
# #     for j in range(len(Vehicle_jsondata[i])):
# #         Vehicle_Details.append(Vehicle_jsondata[i][j].get('text'))
# # print(len(Vehicle_Details))
# # print(Vehicle_Details)
# print('============================================================================================')
# for i in range(len(Vehicle_jsondata2)):
#     for j in range(len(Vehicle_jsondata2[i])):
#         Vehicle_Details1.append(Vehicle_jsondata2[i][j].get('text'))
# print(len(Vehicle_Details1))
# print(Vehicle_Details1)
# print('============================================================================================')


tem='BLHA10BS\rGHH42583'
just=tem.split('\r')
print(just)