import pandas as pd
import copy


def clean(s):
    return s.strip(' " : .  - * # ')


def diff(x, y, z, df):
    xx = ["x0", "x1",  "x6", "x7", "x2", "x3", "x4", "x5"]
    for xc in xx:
        if not df.loc[z, xc] == "None":
            if abs(x[int(xc[-1])] - y[int(xc[-1])]) > df.loc[z, xc]:
                return False
    return True


def check_bajaj(text_json, sheet1, bck):  # , state, bck

    # st = state
    # print(st)

    data = pd.read_excel(r'packages/bajaj/image/directives_bajaj.xlsx', sheet_name=sheet1)
    df = pd.DataFrame(data, columns=['Key', 'Available', 'Value Navigation', 'Front Breaking', 'Reverse Breaking', 'Name',
                                     'x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'Cols', 'Ignore', "REGEX", "Not IN", "INIT2", "Counters", "Name2"])

    result = {}
    for j in range(df.shape[0]):
        if df.loc[j, "Available"] == 'Y':
            result[df.loc[j, "Name"]] = ""

    counters = {}
    visited = {}

    # try:
    #     result["Vehicle Class"] = ""
    #     for i in range(len(text_json)):
    #         s = text_json[i].get("text")
    #         if "LMV" in s:
    #             result["Vehicle Class"] = result["Vehicle Class"] + ", " + "LMV"
    #         if "MCWG" in s:
    #             result["Vehicle Class"] = result["Vehicle Class"] + ", " + "MCWG"
    #         if "TRANS" in s:
    #             result["Vehicle Class"] = result["Vehicle Class"] + ", " + "TRANS"
    # except:
    #     print("Prime Vehicle Class")

    for i in range(df.shape[0]):
        visited[df.loc[i, "Name"]] = False

    flag = 0
    # print(len(text_json))

    for i in range(len(text_json)):
        for j in range(df.shape[0]):
            # if fuzz.token_set_ratio(df.loc[j, "Key"].upper(), text_json[i].get('text').upper()) > 86:
            #     print(df.loc[j, "Key"].upper())
            #     print(text_json[i].get('text').upper())
            #     print(fuzz.token_set_ratio(df.loc[j, "Key"].upper(), text_json[i].get('text').upper()))
            #     print(i)

            # print(df.loc[j, "Key"])

            # if df.loc[j, "Key"] in text_json[i].get("text"):
            #     print(df.loc[j, "Key"])
            #     print(text_json[i].get("text"))
            #     print("$$$$$$$$")

            if (df.loc[j, "Available"] == 'Y') and (((df.loc[j, "Key"] in text_json[i].get("text")) and (df.loc[j, "Not IN"] not in text_json[i].get("text")))\
                    and ((visited[df.loc[j, "Name"]] == False) or (result[df.loc[j, "Name"]].strip(" ") == ""))):
                try:
                    if df.loc[j, "Value Navigation"] == 'R':
                        # print(df.loc[j, "Key"])
                        x = text_json[i].get("boundingBox")
                        for z in range(i+1, len(text_json)):
                            if df.loc[j, "Front Breaking"] in text_json[z].get("text"):
                                break
                            if text_json[z].get("text").strip(". : ,") == "":
                                continue
                            if df.loc[j, "Name"] == "chassis_no" or df.loc[j, "Name"] == "engine_no":
                                if text_json[z].get("text").__contains__("IDV"):
                                    break
                            if diff(x, text_json[z].get("boundingBox"), j, df):
                                result[df.loc[j, "Name"]] = str(clean(text_json[z].get("text"))).replace(df.loc[j, "Ignore"], "").strip()

                                if df.loc[j, "Name"] == "previous_policy_number":
                                    z = result["previous_policy_number"]
                                    z = clean(z)
                                    if len(z) > 30:
                                        visited[df.loc[j, "Name"]] = False
                                        result["previous_policy_number"] = ""
                                        continue
                                    if not z[-3:].isdigit():
                                        visited[df.loc[j, "Name"]] = False
                                        result["previous_policy_number"] = ""
                                        continue
                                if df.loc[j, "Name"] == "registration_no":
                                    z = result["registration_no"]
                                    z = clean(z)
                                    if len(z) < 5 and z != "NEW":
                                        visited[df.loc[j, "Name"]] = False
                                        result["registration_no"] = ""
                                        continue
                                    if len(z) > 47:
                                        visited[df.loc[j, "Name"]] = False
                                        result["registration_no"] = ""
                                        continue
                                if df.loc[j, "Name"] == "policy_issuance_date":
                                    z = result["policy_issuance_date"]
                                    z = clean(z)
                                    if z.__contains__("Cover Note") or z.__contains__("From"):
                                        visited[df.loc[j, "Name"]] = False
                                        result["policy_issuance_date"] = ""
                                        continue
                                #     if z.__contains__("Body") or z.__contains__("Yr"):
                                #         visited[df.loc[j, "Name"]] = False
                                #         result["model"] = ""
                                #         continue
                                if df.loc[j, "Name"] == "chassis_no":
                                    z = result["chassis_no"]
                                    z = clean(z)
                                    # print(result["engine_no"])
                                    if z == result["registration_no"] or z == result["engine_no"]:
                                        visited[df.loc[j, "Name"]] = False
                                        result["chassis_no"] = ""
                                        continue
                                if df.loc[j, "Name"] == "mfg_yr":
                                    z = result["mfg_yr"]
                                    z = z.replace("%", "7")
                                    z = clean(z)
                                    if len(z) < 4 and z != "201" and z != "200":
                                        visited[df.loc[j, "Name"]] = False
                                        result["mfg_yr"] = ""
                                        continue
                                    if len(z) > 4:
                                        visited[df.loc[j, "Name"]] = False
                                        result["mfg_yr"] = ""
                                        continue
                                    if not z[-2:].isdigit() or z == result["cubic_capacity"]:
                                        visited[df.loc[j, "Name"]] = False
                                        result["mfg_yr"] = ""
                                        continue
                                if df.loc[j, "Name"] == "customer_state":
                                    z = result["customer_state"]
                                    z = clean(z)
                                    if z.__contains__("State Code") or z.__contains__("NAME"):
                                        visited[df.loc[j, "Name"]] = False
                                        result["customer_state"] = ""
                                        continue
                                if df.loc[j, "Name"] == "hypothecation":
                                    z = result["hypothecation"]
                                    z = clean(z)
                                    if z.__contains__("Supply"):
                                        visited[df.loc[j, "Name"]] = False
                                        result["hypothecation"] = ""
                                        continue
                                if df.loc[j, "Name"] == "cubic_capacity":
                                    z = result["cubic_capacity"]
                                    z = clean(z)
                                    if len(z) < 2 or len(z) > 5:
                                        visited[df.loc[j, "Name"]] = False
                                        result["cubic_capacity"] = ""
                                        continue
                                    if not z[:2].isdigit() or z == result["mfg_yr"]:
                                        visited[df.loc[j, "Name"]] = False
                                        result["cubic_capacity"] = ""
                                        continue
                                if df.loc[j, "Name"] == "ncb":
                                    z = result["ncb"]
                                    z = z.replace("%", "")
                                    z = clean(z)
                                    if len(z) > 3:
                                        visited[df.loc[j, "Name"]] = False
                                        result["ncb"] = ""
                                        continue
                                    if not z[0].isdigit():
                                        visited[df.loc[j, "Name"]] = False
                                        result["ncb"] = ""
                                        continue

                            if len(result[df.loc[j, "Name"]]) == 0:
                                # print(df.loc[j, "Key"])
                                # print(text_json[z].get("text"))
                                continue
                            else:
                                visited[df.loc[j, "Name"]] = True
                                break

                        if df.loc[j, "Name"] == "previous_policy_number" and visited["previous_policy_number"] == False:
                            # print("yesss")
                            cvb = i - 5
                            for z in range(i - 1, cvb, -1):
                                if not clean(text_json[z].get("text"))[-3:].isdigit():
                                    continue
                                if diff(x, text_json[z].get("boundingBox"), j, df):
                                    # print(text_json[z].get("text"))
                                    result[df.loc[j, "Name"]] = clean(text_json[z].get("text")).replace(df.loc[j, "Ignore"], "")
                                    visited[df.loc[j, "Name"]] = True
                                    break
                        if df.loc[j, "Name"] == "policy_issuance_date" and visited["policy_issuance_date"] == False:
                            # print("yesss")
                            cvb = i - 5
                            for z in range(i - 1, cvb, -1):
                                # if clean(text_json[z].get("text"))[:2].isdigit() or z.__contains__("@"):
                                #     continue
                                if diff(x, text_json[z].get("boundingBox"), j, df):
                                    # print(text_json[z].get("text"))
                                    result[df.loc[j, "Name"]] = clean(text_json[z].get("text")).replace(df.loc[j, "Ignore"], "")
                                    visited[df.loc[j, "Name"]] = True
                                    break

                    elif df.loc[j, "Value Navigation"] == 'INIT':
                        # print(df.loc[j, "Key"])
                        x = text_json[i].get("text")
                        x = x.split(df.loc[j, "Key"])[1].strip()
                        data = x.replace(df.loc[j, "Ignore"], "").strip(" - ? ; . , ").split(df.loc[j, "Front Breaking"])[0]

                        z = x.replace(data, "")
                        init2 = z.split(df.loc[j, "INIT2"]) #[1].strip()
                        # print(init2)
                        if len(init2) > 1:
                            data2 = init2[1].strip()
                            result[df.loc[j, "Name2"]] = clean(data2)

                        result[df.loc[j, "Name"]] = clean(data)

                        if df.loc[j, "Name"] == "mobile":
                            z = result["mobile"]
                            z = clean(z)
                            if len(z) < 4:
                                visited[df.loc[j, "Name"]] = False
                                result["mobile"] = ""
                                continue

                        # print(result["Engine No"])

                        if len(result[df.loc[j, "Name"]]) == 0:
                            # print(df.loc[j, "Key"])
                            continue
                        else:
                            visited[df.loc[j, "Name"]] = True
                            break

                    elif df.loc[j, "Value Navigation"] == 'BML':
                        try:
                            result[df.loc[j, "Name"]] = ""
                            x = text_json[i].get("boundingBox")
                            xc = i + 1
                            count = 0
                            counter = 0
                            # print(df.loc[j, "Key"])
                            while df.loc[j, "Front Breaking"] not in text_json[xc].get("text"):
                                if df.loc[j, "Name"] == "chassis_no" or df.loc[j, "Name"] == "engine_no" or df.loc[j, "Name"] == "model":
                                    if text_json[xc].get("text").__contains__("IDV"):
                                        break
                                if diff(x, text_json[xc].get("boundingBox"), j, df):
                                    count = count + 1
                                    # if df.loc[j, "Key"] == "Addr":
                                    # print(text_json[xc].get("text"))
                                    if df.loc[j, "Name"] == "address":
                                        if text_json[xc].get("text").__contains__("Address") or text_json[xc].get("text").isnumeric() and len(text_json[xc].get("text")) != 6:
                                            counter = counter + 1
                                            xc = xc + 1
                                            continue
                                    if df.loc[j, "Name"] == "insured_name2":
                                        if text_json[xc].get("text").__contains__("Insured") or text_json[xc].get("text").__contains__("Address"):
                                            counter = counter + 1
                                            xc = xc + 1
                                            continue
                                    if df.loc[j, "Name"] == "Period of Insurance":
                                        if text_json[xc].get("text").__contains__("Policy"):
                                            xc = xc + 1
                                            continue
                                    if df.loc[j, "Name"] == "model":
                                        if text_json[xc].get("text").__contains__("Type"):
                                            xc = xc + 1
                                            continue
                                    if df.loc[j, "Name"] == "engine_no":
                                        if text_json[xc].get("text").__contains__("Chassis"):
                                            xc = xc + 1
                                            continue
                                    if df.loc[j, "Name"] == "chassis_no":
                                        # print(result["engine_no"])
                                        if text_json[xc].get("text") in result["engine_no"] or text_json[xc].get("text") == result["mfg_yr"] or len(text_json[xc].get("text")) == 1:
                                            xc = xc + 1
                                            continue
                                    data = text_json[xc].get("text")
                                    result[df.loc[j, "Name"]] = result[df.loc[j, "Name"]] + ";" + clean(data.replace(df.loc[j, "Ignore"], ""))
                                    x = text_json[xc].get("boundingBox")
                                xc = xc + 1
                            if ((not result["Period of Insurance"].__contains__("To")) or
                                (not result["Period of Insurance"].__contains__("From"))) and result["Period of Insurance"] != "":
                                cvb = i - 5
                                p = ""
                                for z in range(i - 1, cvb, -1):
                                    # if not clean(text_json[z].get("text"))[-2:].isdigit():
                                    #     continue
                                    if diff(x, text_json[z].get("boundingBox"), j, df):
                                        if text_json[z].get("text").__contains__("To") or text_json[z].get("text").__contains__("From"):
                                            # print(text_json[z].get("text"))
                                            result["Period of Insurance"] = clean(text_json[z].get("text")).replace(
                                                df.loc[j, "Ignore"], "") + result["Period of Insurance"]
                                            # visited[df.loc[j, "Name"]] = True
                                            break

                            if df.loc[j, "Name"] == "Address":
                                # print(count - counter)
                                # print(result["Address"])
                                count = count - counter
                                if count == 1:  # or count == 2
                                    cvb = i - 5
                                    p = ""
                                    for z in range(i - 1, cvb, -1):
                                        if clean(text_json[z].get("text")).__contains__("Insurance"):
                                            continue
                                        if diff(x, text_json[z].get("boundingBox"), j, df):
                                            # print(text_json[z].get("text"))
                                            result["Address"] = clean(text_json[z].get("text")) + result["Address"]
                                            # visited[df.loc[j, "Name"]] = True
                                            break

                            visited[df.loc[j, "Name"]] = True
                        except:
                            # + df.loc[j, "Name"]+ " " + result[df.loc[j, "Name"]])
                            pass
                        # print(result["Address"])
                        break

                    elif df.loc[j, "Value Navigation"] == 'TBML':
                        # print(df.loc[j, "Key"] + "$$$$$")
                        try:
                            result[df.loc[j, "Name"]] = ""
                            x = text_json[i].get("boundingBox")
                            y = x
                            xc = i

                            while df.loc[j, "Front Breaking"] not in text_json[xc].get("text"):

                                if diff(y, text_json[xc].get("boundingBox"), j, df):
                                    # print(text_json[xc].get("text"))

                                    if df.loc[j, "Name"] == "Period of Insurance":
                                        if text_json[xc].get("text").__contains__("Policy"):
                                            xc = xc + 1
                                            continue

                                    result[df.loc[j, "Name"]] = result[df.loc[j, "Name"]] + " " + clean(text_json[xc].get("text").replace(df.loc[j, "Ignore"], "").split(df.loc[j, "Key"])[-1])

                                    y = text_json[xc].get("boundingBox")

                                    # visited[df.loc[j, "Name"]] = True
                                xc = xc + 1
                            # print(result["Period of Insurance"])
                            if ((not result["Period of Insurance"].__contains__("To")) or (not result["Period of Insurance"].__contains__("From"))) and result["Period of Insurance"] != "":
                                # print("yesss")
                                cvb = i - 5
                                p = ""
                                for z in range(i - 1, cvb, -1):
                                    # print(text_json[z].get("text"))
                                    # if not clean(text_json[z].get("text"))[-2:].isdigit():
                                    #     continue
                                    if diff(x, text_json[z].get("boundingBox"), j, df):
                                        # print(text_json[z].get("text"))
                                        if text_json[z].get("text").__contains__("To") or text_json[z].get("text").__contains__("From"):
                                            # print(text_json[z].get("text"))
                                            result["Period of Insurance"] = clean(text_json[z].get("text")).replace(
                                                df.loc[j, "Ignore"], "") + result["Period of Insurance"]
                                            # visited[df.loc[j, "Name"]] = True
                                            break

                            if len(result[df.loc[j, "Name"]]) == 0:
                                # print(df.loc[j, "Key"])
                                continue
                            else:
                                visited[df.loc[j, "Name"]] = True
                                break
                        except:
                            pass
                        break


                except:
                    pass

    result1 = copy.deepcopy(result)
    if bck == 1:
        for key in result1.keys():
            if result1[key] == "":
                del result[key]

    return result