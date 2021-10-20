code_matche_list= [['E87.71'], ['E87.71'], ['E87.71'], ['E87.71'], ['30233H0', 'E87.71']]
code_matches_Name= ['transfusion', 'exchange tranfusion', 'blood transfusion package', 'transfusion workup', 'whole blood with replacement(transfusion']
matches= [('exchange tranfusion', 97), ('transfusion', 71), ('transfusion workup', 58), ('blood transfusion package', 53), ('whole blood with replacement(transfusion', 53)]
TepM_out_list=[]
final_Temp_match = [match[0] for match in matches]
print('final_Temp_match',final_Temp_match)
for match in final_Temp_match:
    for i in range(len(code_matches_Name)):
        if str(code_matches_Name[i]).lower().strip()==str(match).lower().strip():
            TepM_out_list.append(code_matche_list[i])
            break
print("TepM_out_list",TepM_out_list)