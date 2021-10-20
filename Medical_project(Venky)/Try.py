import pandas as pd

def get_dataframe(file_name):
    str_ = 'TOYOTA CAMRY V1'
    list_1 = []
    list_2 = []
    list_3 = []
    temp = ''
    df = pd.read_excel(file_name, index_col=False)
    list_1 = df['Make_Name'].unique().tolist()
    print(list_1)
    for i in list_1:
        if i in str_:
            if str_.__contains__('MAHINDRA & MAHINDRA'):
                fin_st = 'MAHINDRA & MAHINDRA'
            else:
                fin_st = i
    df = df[df["Make_Name"] == fin_st]
    list_2 = df['Model_Name'].unique().tolist()
    for j in list_2:
        if j in str_:
            Model_Name = j
    df = df[df["Model_Name"] == Model_Name]
    list_3 = df['Variant_Name'].unique().tolist()
    print(list_3)
    for z in list_3:
        if z in str_:
            Variant_Names = z
    df = df[df["Variant_Name"] == Variant_Names]
    df_reset = df.reset_index()
    temp = df_reset
    return temp

def get_list_dataframeSet1(temp,file_name):
    df12=pd.DataFrame()
    list_1 = temp['Set1_id'].tolist()
    list_4 = temp['Make_Name'].tolist()
    df = pd.read_excel(file_name,sheet_name='To be Mapp - set 1',index_col=False)
    for i in range(len(list_1)):
        temp_id=list_1[i].replace(' ','').split(',')
        modl_=list_4[i]
        print(temp_id)
        for ij in temp_id:
            df1 = (df[df["Id"] == int(ij)])
            print(df1)
            df12 = df12.append(df1)
    temP_vad=df12.drop_duplicates()
    temP_vad.reset_index()
    temP_vad.to_excel('temp_.xlsx')
    print(df12)

def get_list_dataframeSet2(temp,file_name):
    df12=pd.DataFrame()
    list_1 = temp['Set2_id'].tolist()
    df = pd.read_excel(file_name,sheet_name='To be Mapp - set 2',index_col=False)
    for i in range(len(list_1)):
        temp_id=list_1[i].replace(' ','').split(',')
        print(temp_id)
        for ij in temp_id:
            df1 = (df[df["Vehicle Code"] == int(ij)])
            print(df1)
            df12 = df12.append(df1)
    temP_vad=df12.drop_duplicates()
    temP_vad.reset_index()
    temP_vad.to_excel('Fi_gdv.xlsx')
    print(df12)

if __name__ == '__main__':
    file_name='Sample - Copy.xlsx'
    temp=get_dataframe(file_name)
    get_list_dataframeSet1(temp,file_name)
    get_list_dataframeSet2(temp,file_name)
