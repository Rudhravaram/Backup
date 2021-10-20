from googlesearch import search
import spacy
from googlesearch import search
import icd10
def icd10_code(dieases_data):
    # dieases_data = input("diagnosis name : ")
    main_words,code_list,desc,block,block_desc = "","","","",""
    query = str(dieases_data) + " icd 10"
    list_url = []
    for i in search(query,  tld='com', lang='en', tbs='0', safe='off', num=2, start=0, stop=5, pause=1.0, country=''):
        list_url.append(i)
    for i in range(len(list_url)):
        # print(list_url[i])
        if str(list_url[i]).__contains__('icd10data'):
            try:
                    # print(list_url[i])
                my_split = str(list_url[i]).split('/')[-1]
                if "-" not in str(my_split):
                    code_val = my_split
                    code = icd10.find(my_split)
                    code_desc = code.description
                    code_block = code.block
                    code_block_desc = code.block_description
                    print(dieases_data)
                    print(code_val)
                    print(code_desc)
                    print(code_block)
                    main_words = dieases_data
                    code_list = code_val
                    desc = code_desc
                    block = code_block
                    block_desc = code_block_desc
                    break
            except:
                pass
    return main_words,code_list,desc,block,block_desc
def main_icd10(raw_text):
    nlp = spacy.load("en_core_web_trf")
    doc = nlp(raw_text)
    flag = 0
    main_words,code_list,desc,block,block_desc = [],[],[],[],[]
    for chunk in doc.noun_chunks:
        dieases_data,code_val,code_desc,code_block,code_block_desc = icd10_code(chunk.text)
        main_words.append(dieases_data)
        code_list.append(code_val)
        desc.append(code_desc)
        block.append(code_block)
        block_desc.append(code_block_desc)
    return main_words,code_list,desc,block,block_desc

main_words,code_list,desc,block,block_desc=icd10_code('Antibody Identification')#Z90.410
print("main_words",main_words)
print("code_list",code_list)
print("desc",desc)
print("block",block)
print("block_desc",block_desc)

