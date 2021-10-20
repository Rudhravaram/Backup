import pandas as pd
import os

def get_final(BILL_TYPE,SUB_BILL_TYPE):
    print("BILL_TYPE:",BILL_TYPE)
    print("SUB_BILL_TYPE:",SUB_BILL_TYPE)
    file_name='Bill type- UAT Vs LIVE proposed.XLSX'
    excel_file=os.path.join(os.getcwd(),file_name)
    bill_type_id=''
    sub_bill_type_id=''
    for sheet in pd.ExcelFile(excel_file).sheet_names:
        print(sheet)
        if str(sheet).lower()=='uat':
            uat_df: pd.DataFrame = pd.read_excel(excel_file, sheet_name=sheet)
            uat_df = uat_df.fillna("")
            uat_df = uat_df.replace(to_replace="NaN", value="")
            print(uat_df)
            bill_type_id,sub_bill_type_id=get_UAR_df_data(uat_df,BILL_TYPE,SUB_BILL_TYPE)
            break
    print("bill_type_id",bill_type_id)
    print("sub_bill_type_id",sub_bill_type_id)
    return bill_type_id,sub_bill_type_id


def get_UAR_df_data(uat_df,bill_type,sub_bill_type):
    bill_type=str(bill_type).strip()
    sub_bill_type = str(sub_bill_type).strip()
    pd_uat_fin=uat_df
    uat_df_indexes = uat_df.index.tolist()
    print("UAT_df_indexes",uat_df_indexes)
    sub_bill_types = uat_df["SUB_BILL_TYPE"].str.lower().tolist()
    bill_type_list = uat_df["BILL_TYPE"].unique().tolist()
    fin_st=''
    temp_str=''
    for i in bill_type_list:
        if str(i).lower() in str(bill_type).lower():
            fin_st = i
    print("fin_st",fin_st)
    uat_df = uat_df[uat_df["BILL_TYPE"] == fin_st]
    sub_bill_type_top = uat_df["SUB_BILL_TYPE"].str.lower().tolist()
    for i in sub_bill_type_top:
        if str(i).lower() in  str(sub_bill_type).lower():
            temp_str = i
    print("temp_str",temp_str)
    master_index=''
    val1=''
    val2=''
    if temp_str:
        master_index = sub_bill_types.index(temp_str)
        master_index = int(uat_df_indexes[master_index])
    if master_index:
        print("master_index", master_index)
        val1 = pd_uat_fin["BILL_TYPE_ID"][master_index]
        val2 = pd_uat_fin["SUB_BILL_TYPE_ID"][master_index]
        print("val1", val1)
        print("val2", val2)
    return val1,val2






get_final("KD Anesthetist Charges","KD Local Anesthetist Charges")

