import regex as re
from packages.bajaj.image.interpretation_bajaj import check_bajaj
import re



def common_member(a, b):
    a_set = set(a)
    b_set = set(b)
    return a_set & b_set

def clean(s):
    return s.strip(" : . ( ) ;  _ ")

def correct_alpha(a):
    x1 = {'1': 'I', '0': 'O', '8': 'B', ')': 'I', '(': 'I', '5': 'S', '~': 'N', ']': 'I', '[': 'I', '_': ''}

    for key in x1.keys():
        if key == a:
            a = x1[key]

    return a

def correct_num(a):
    x1 = {'s': '5', 'Z': '2', 'T': '1', 'S': '5', 'R': '2', 'Q': '0', 'O': '0', 'A': '4', 'G': '6', 'H': '4',
          'a': '2', 'o': '0', 'y': '4', 'z': '2', 'f': '5', 't': '1',
          'b': '6', 'F': '5', 'B': '8', 'L': '1', 'C': '0', 'D': '1', 'l': '1', 'I': '1', 'i': '1', 'j': '1',
          'J': '7', 'P': '9', ')': '1', '(': '1', 'd': '0', '.':'0','N':'0','E':'0','q':'9'}

    for key in x1.keys():
        if key == a:
            a = x1[key]

    return a

def correct_time(a1):

    # a1 = a1.strip("a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z")
    a = a1
    b = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}

    try:
        keys = b.keys()
        month = ""
        for key in keys:
            if key in a:
                # print(key)
                month = key
                break
        a = a.split(month)
        # month = b[month]
        result = ""
        if "," in a[-1]:
            date = a[-1].strip().split(",")[0]
            year = a[-1].strip(', .').split(",")[-1]
            year = year.strip().split()[0]
            result = date + "-" + month + "-" + year
        elif "." in a[-1]:
            # print("yesss")
            date = a[-1].strip().split(".")[0]
            year = a[-1].strip(', .').split(".")[-1]
            year = year.strip().split()[0]
            result = date + "-" + month + "-" + year
        else:
            date = a[-1].strip().split()[0]
            year = a[-1].strip(', .').split()[-1]
            year = year.strip().split()[0]
            result = date + "-" + month + "-" + year
        # print(a)
        # print(result)
        return result
    except:
        try:
            a = a.split('/')
            date = a[0]
            month = a[1]
            year = a[2].split()[0]
            b1 = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
                 "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}
            # keys = b1.keys()
            # for key in keys:
            #     if key in month:
            #         print(key)
            #         month = key
            #         break
            # print(date)
            # print(month)
            # print(year)
            month = b1[month]
            result = date + "-" + month + "-" + year
            # print(result)
            return result
        except:
            # print(a1)
            return a1

def magic_bajaj(text_json):

    # wheel = 0
    pre_insurer = 0
    for i in range(len(text_json)):
        # print(i)
        # print(text_json[i].get('text'))  # str(i) + " " +
        # print(text_json[i].get('boundingBox'))
        # print("######################")
        # if text_json[i].get("text").upper().__contains__("WO WHEELER") or text_json[i].get("text").upper().__contains__("TUP WHEELER") or \
        #         text_json[i].get("text").upper().__contains__("O WHEEL") or text_json[i].get("text").upper().__contains__("MOTORCYCLE") or \
        #         text_json[i].get("text").upper().__contains__("MOTO") or text_json[i].get("text").upper().__contains__("HYUNDAI"):
        #     # print("yesss")
        #     wheel = 1
        if text_json[i].get("text").upper().__contains__("BAJAJ") and text_json[i].get("text").upper().__contains__(
                "ALLIANZ"):
            pre_insurer = 1


    state = ["Andhra Pradesh", "Arunachal Pradesh ", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana",
             "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh",
             "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Orissa", "Odisha", "Punjab", "Rajasthan",
             "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
             "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli", "Daman and Diu", "Lakshadweep",
             "National Capital Territory of Delhi", "Puducherry", "Delhi"]

    # print(text_json)
    text_json1 = []

    result = {}

    sheet = ""
    bck = 0

    for i in range(20 ):  # len(text_json)
        if text_json[i].get("text").upper().__contains__("CERTIFICATE OF INSURANCE") or \
                text_json[i].get("text").upper().__contains__("CUM POLICY SCHEDULE"):
            sheet = "T1"
            # print("T1")
            result = check_bajaj(text_json, "T1", bck)
            break
        if text_json[i].get("text").upper().__contains__("INSURED DETAILS"):
            sheet = "T2"
            # print("T2")
            result = check_bajaj(text_json, "T2", bck)
            break

    # if wheel == 0:   # shan
    #     result["product_type"] = "Four Wheeler"
    # else:
    #     result["product_type"] = "Two Wheeler"

    # print(pre_insurer)
    if pre_insurer == 1:
        result["previous_insurer_name"] = "BAJAJ ALLIANZ"

    keys = result.keys()

    try:
        if "insured_name" in keys:
            result["insured_name"] = result["insured_name"].replace("Zone", "")
    except:
        pass

    try:
        if "insured_name2" in keys:
            # print(result["insured_name"])
            z = result["insured_name2"]
            del result["insured_name2"]

            z = clean(z)
            p = z.split(";")
            dump = ""
            if len(p[1]) < 7:
                result["insured_name"] = p[0] + "-" + p[1]
                dump = p[0] + ";" + p[1]
                result["address"] = z.replace(dump, "")
            else:
                result["insured_name"] = p[0]
                result["address"] = z.replace(p[0], "")
    except:
        pass

    make_name = ["HERO HONDA"]
    model_name = ["PASSION PRO"]

    try:
        if "registration_no" in keys:
            result["registration_no"] = result["registration_no"].replace("CAST", "").replace("DRUM", "")
            if result["make"] == "":
                for l in make_name:
                    if l in result["registration_no"]:
                        result["make"] = l
                        result["registration_no"] = result["registration_no"].replace(l, "")
            if result["model"] == "":
                for l in model_name:
                    if l in result["registration_no"]:
                        result["model"] = l
                        result["registration_no"] = result["registration_no"].replace(l, "")

            result["registration_no"] = result["registration_no"].replace(" ", "")
    except:
        pass

    try:
        if "previous_policy_number" in keys:
            result["previous_policy_number"] = result["previous_policy_number"].replace("-", "")
    except:
        pass

    try:
        if "policy_issuance_date" in keys:
            if "PM" in result["policy_issuance_date"] or "AM" in result["policy_issuance_date"]:
                result["policy_issuance_date"] = result["policy_issuance_date"].split(" ")[0]
                result["policy_issuance_date"] = result["policy_issuance_date"].rstrip()
            result["policy_issuance_date"] = result["policy_issuance_date"].replace("Fob", "Feb").replace("Fee", "Feb")
    except:
        pass

    try:
        if "gstin" in keys:
            result["gstin"] = result["gstin"].replace(" ", "")
    except:
        pass


    state_code = { "Maharashtra": "MH", "Jharkhand": "JK", "Karnataka": "KA"}
    num = ""
    try:
        if "customer_state" in keys:
            z = result["customer_state"]
            z = z.replace(".", "-")
            z = z.replace("State", "").replace("NAME", "").replace("/", "")
            z = clean(z)
            # print(z)
            result["customer_state"] = z.split("-")[-1]
            num = z.split("-")[0]
            result["customer_state"] = result["customer_state"].replace("Mahalashaia", "Maharashtra").replace("thankhand", "Jharkhand")
            result["customer_state"] = clean(result["customer_state"])
    except:
        pass

    try:
        data = pd.read_excel("packages/all_rto_det.xlsx")
        df = pd.DataFrame(data, columns=['Vehicle RTO Codes', 'District/Region'])
    except:
        pass

    try:
        if "registration_no" in result.keys():
            if result["registration_no"] != "" and result["registration_no"] != "NEW":
                x = result["registration_no"].replace(":", "").replace(".", "").replace("-", "").replace(
                    ",", "").replace("IN", "TN").replace(" ", "").strip()[0:4]
                x = x[0:2] + "-" + x[2:4]
                a = x[0]
                b = x[1]
                c = x[3]
                d = x[4]
                a = correct_alpha(a)
                b = correct_alpha(b)
                c = correct_num(c)
                d = correct_num(d)
                x = a + b + '-' + c + d
                # print(x)
                z = df[df['Vehicle RTO Codes'] == x]['District/Region'].item()
                result["rto"] = z
                x = a + b + c + d + result["registration_no"][4:]
                result["registration_no"] = x

            elif num != "":
                num = clean(num)
                for code in state_code:
                    if code.upper() == result["customer_state"].upper():
                        x = state_code[code] + "-" + num
                        a = x[0]
                        b = x[1]
                        c = x[3]
                        d = x[4]
                        a = correct_alpha(a)
                        b = correct_alpha(b)
                        c = correct_num(c)
                        d = correct_num(d)
                        x = a + b + '-' + c + d
                        # print(x)
                        z = df[df['Vehicle RTO Codes'] == x]['District/Region'].item()
                        result["rto"] = z

    except:
        pass

    try:
        if "mfg_yr" in keys:
            result["mfg_yr"] = result["mfg_yr"].replace("%", "7")
    except:
        pass

    try:
        if "make" in keys:
            result["make"] = clean(result["make"])
            result["make"] = result["make"].replace("-", "").replace(";", "-").replace("CAST WHEEL", "")
    except:
        pass

    try:
        if "model" in keys:
            result["model"] = clean(result["model"])
            result["model"] = result["model"].replace("CO 100", "CD 100").replace(";", "-")
            result["model"] = result["model"].replace(";", "-").replace("Trailer", "")
            if result["model"] == "PLUS":
                result["model"] = result["subtype"].split(" ")[-1] + " " + result["model"]
            result["model"] = result["model"].rstrip("-")
    except:
        pass

    try:
        if "chassis_no" in keys:
            result["chassis_no"] = result["chassis_no"].lstrip(";")
            result["chassis_no"] = result["chassis_no"].replace(";", " ").lstrip("No")
            result["chassis_no"] = result["chassis_no"].split("LIABILITY")[0]
            result["chassis_no"] = clean(result["chassis_no"])
            # print(result["chassis_no"])
            p = result["chassis_no"].split(" ")
            # print(p)
            if len(p) == 2:
                if len(p[0]) > 5 and len(p[1]) > 5:
                    result["engine_no"] = p[1] + result["engine_no"]
                    result["chassis_no"] = result["chassis_no"].replace(p[1], "")
                    result["chassis_no"] = result["chassis_no"].replace(" ", "")
            elif len(p) > 2:
                if len(p[0]) > 5 and len(p[1]) > 5 and (len(p[2]) < 5):
                    result["chassis_no"] = result["chassis_no"].replace(p[1], "")
                    result["chassis_no"] = result["chassis_no"].replace(" ", "")
                    result["engine_no"] = p[1] + result["engine_no"]
                elif len(p[0]) > 5 and len(p[2]) > 5 and (len(p[1]) < 5):
                    result["engine_no"] = p[2] + result["engine_no"]
                    result["chassis_no"] = result["chassis_no"].replace(p[2], "")
                    result["chassis_no"] = result["chassis_no"].replace(" ", "")
                elif len(p[0]) > 5 and len(p[2]) > 5 and (len(p[1]) == 5):
                    result["engine_no"] = p[2] + result["engine_no"]
                    result["chassis_no"] = result["chassis_no"].replace(p[2], "")
                    result["chassis_no"] = result["chassis_no"].replace(" ", "")
                elif len(p[0]) > 5 and len(p[2]) > 5 and (len(p[1]) == 6):
                    result["engine_no"] = p[2] + result["engine_no"]
                    result["chassis_no"] = result["chassis_no"].replace(p[2], "")
                    result["chassis_no"] = result["chassis_no"].replace(" ", "")
                elif len(p[0]) > 5 and len(p[2]) > 5 and (len(p[1]) > 5):
                    result["engine_no"] = p[1] + p[2] + result["engine_no"]
                    result["chassis_no"] = result["chassis_no"].replace(p[1], "").replace(p[2], "")
                    result["chassis_no"] = result["chassis_no"].replace(" ", "")
                else:
                    result["chassis_no"] = result["chassis_no"].replace(" ", "")
    except:
        pass

    try:
        if "chassis_no2" in keys:
            result["chassis_no"] = result["chassis_no2"].replace(";", "").replace("$", "S")
            result["chassis_no"] = result["chassis_no"].rstrip()

            del result["chassis_no2"]
    except:
        pass

    try:
        if "engine_no" in keys:
            result["engine_no"] = result["engine_no"].replace(";", "").replace(" ", "")
    except:
        pass

    try:
        if "Make & Model" in keys:
            z = result["Make & Model"]
            # print(z)
            del result["Make & Model"]

            # z = z.replace(";", "")
            z = clean(z)
            z = z.lstrip(";")
            z = z.lstrip("el;")
            # print(z)

            if " " in z:
                result["make"] = z.split(" ")[0]
                result["make"] = clean(result["make"])

                result["model"] = z.split(" ")[-1]
                result["model"] = result["model"].replace(";", "")
                result["model"] = clean(result["model"])
            else:
                result["make"] = z.split(";")[0]
                result["make"] = clean(result["make"])

                result["model"] = z.split(";")[-1]
                result["model"] = clean(result["model"])
    except:
        pass

    try:
        if "hypothecation" in keys:
            result["hypothecation"] = result["hypothecation"].replace("Policy Status", "")
    except:
        pass

    try:
        if "ncb" in keys:
            result["ncb"] = result["ncb"].replace("%%", "%")
    except:
        pass

    result["period_of_insurance_start_date"] = ""
    result["period_of_insurance_end_date"] = ""
    per_of_ins = {"Jut": "Jul", "te": "To", "Te": "To", "Map": "May", "mm": "To", "to": "To"}
    try:
        if "Period of Insurance" in keys:
            for key in per_of_ins:
                if key in result["Period of Insurance"]:
                    result["Period of Insurance"] = result["Period of Insurance"].replace(key, per_of_ins[key])
            # print(result["Period of Insurance"])

            if result["Period of Insurance"].__contains__("To"):
                result["period_of_insurance_start_date"] = result["Period of Insurance"].split("To")[0].lstrip(";").lstrip("From ")
                result["period_of_insurance_end_date"] = result["Period of Insurance"].split("To")[1].lstrip(" ")

                result["period_of_insurance_start_date"] = result["period_of_insurance_start_date"].replace("Sup", "Sep").replace("OD:", "")
                result["period_of_insurance_start_date"] = clean(result["period_of_insurance_start_date"])
                result["period_of_insurance_start_date"] = result["period_of_insurance_start_date"].split(" ")[0]
                # result["period_of_insurance_start_date"] = correct_time(result["period_of_insurance_start_date"])
                result["period_of_insurance_start_date"] = result["period_of_insurance_start_date"].replace("--", "-").replace("Nay", "Nov").lstrip("-")

                result["period_of_insurance_end_date"] = result["period_of_insurance_end_date"].replace(":", "").replace("Of", "06")
                result["period_of_insurance_end_date"] = result["period_of_insurance_end_date"].split("Mi")[0]
                result["period_of_insurance_end_date"] = clean(result["period_of_insurance_end_date"]).split(";")[0]
                # print(result["Period of Insurance End date"])
                result["period_of_insurance_end_date"] = result["period_of_insurance_end_date"].replace("Aor", "Apr").replace(" ", "-")
                # result["period_of_insurance_end_date"] = correct_time(result["period_of_insurance_end_date"])
                result["period_of_insurance_end_date"] = result["period_of_insurance_end_date"].replace("--", "-").lstrip("-")

                del result["Period of Insurance"]

    except:
        # print("Period of Insurance")
        del result["Period of Insurance"]

    try:
        if "registration no" in keys:
            result["registration no"] = result["registration no"].replace(" ", "").replace("-", "")
            if len(result["registration no"]) == 10:
                a = correct_alpha(result["registration no"][0])
                b = correct_alpha(result["registration no"][1])

                c = correct_num(result["registration no"][2])
                d = correct_num(result["registration no"][3])

                e = correct_alpha(result["registration no"][4])
                f = correct_alpha(result["registration no"][5])

                g = correct_num(result["registration no"][6])
                h = correct_num(result["registration no"][7])
                i = correct_num(result["registration no"][8])
                j = correct_num(result["registration no"][9])

                result["registration no"] = a + b + c + d + e + f + g + h + i + j

            if len(result["registration no"]) == 9:
                a = correct_alpha(result["registration no"][0])
                b = correct_alpha(result["registration no"][1])

                c = correct_num(result["registration no"][2])
                d = correct_num(result["registration no"][3])

                e = correct_alpha(result["registration no"][4])

                f = correct_num(result["registration no"][5])
                g = correct_num(result["registration no"][6])
                h = correct_num(result["registration no"][7])
                i = correct_num(result["registration no"][8])

                result["registration no"] = a + b + c + d + e + f + g + h + i

    except:
        pass

    try:
        if "address" in keys:
            result["address"] = result["address"].replace("Cubic Capacity/Watts", "").replace("Cubic Capacity", "").replace("elephone No", "")
            # print(result["Address"])

            result["address"] = result["address"].lstrip(" ,").lstrip(";")
            # if result["gstin"] != "":
            #     if result["gstin"] in result["Address"]:
            #         result["Address"] = result["Address"].replace(result["gstin"], "")

            result["address"] = result["address"].lstrip(', 0 1 2 3 4 5 6 7 8 9 ')

            Pattern = re.compile("[0-9]{6}|[0-9]{3}\s[0-9]{3}")  # ^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$")
            x = Pattern.search(result["address"].replace(" ", ""))
            try:
                result["pincode"] = x.group()
            except:
                pass

            if x.group():
                result["address"] = result["address"].split(result["pincode"])[0] + " " + result["pincode"]

            result["address"] = result["address"].replace(";", " ")

            state = [elem.upper() for elem in state]
            # print(result["Insured Name"])
            for i in state:
                if result["customer_state"] == "":
                    if i in result["address"].upper():
                        result["customer_state"] = i
                        # print(result["CUSTOMER_STATE"])
                        break

    except:
        pass

    result["source_system"] = ""
    if result["source_system"] == "":
        result["source_system"] = "OCR"

    if "Period of Insurance" in keys:
        del result["Period of Insurance"]
    if "subtype" in keys:
        del result["subtype"]

    if "gstin" in keys:
        del result["gstin"]

    try:
        loc = "packages/bajaj/image/Bikes_2.xlsx"
        # loc = "Bike.xlsx"
        wb = xlrd.open_workbook(loc)
        make_names = wb.sheet_names()
        # print(make_names)

        make = result["make"]
        if "HERO" in make or "HENO MOTOCORP LTD" in make or "HEAD MOTOCORP LTD" in make or make == "HHML" or make == "HMCL":
            make = "Hero"

        make2 = make
        model2 = result["model"]

        name = ""
        model = ""
        thre = 75
        for z in make_names:
            x = fuzz.ratio(clean(make2).upper(), clean(z).upper())
            # print(z)
            # print(x)
            if x > thre:
                thre = x
                make2 = z
                # print(make1)
                # print(thre)
                name = z

        other = 0
        if name != "":
            sheet = wb.sheet_by_name(make2)

            thre2 = 68
            z = 0
            for i in range(sheet.nrows):
                x = clean(str(sheet.cell_value(i, 0))).upper()
                if x == "BRAND":
                    continue
                x = x.replace(make2.upper(), "")

                model = model2.upper()
                model1 = model.replace(make2.upper(), "")

                z = fuzz.ratio(model1, x)

            if z >= thre2 and z > 0:
                result["product_type"] = "Two Wheeler"
            else:
                result["product_type"] = "Four Wheeler"

        else:
            result["product_type"] = "Four Wheeler"
    except:
        pass


    try:
        ask2 = ["make", "model", "previous_policy_number", "registration_no", "rto", "policy_issuance_date", "chassis_no",
    "cubic_capacity", "mfg_yr", "engine_no", "email_id", "ncb", "address", "period_of_insurance_start_date",
    "period_of_insurance_end_date", "pincode", "mobile", "insured_name", "salutation", "customer_state",
    "nominee_for_owner_driver_nominee_relation", "nominee_for_owner_driver_nominee_name", "hypothecation",
    "financier_name", "financier_branch", "date_of_registration", "source_system", "product_type",
    "previous_policy_type", "previous_insurer_name", "ncb"]
        for h in ask2:
            if h not in keys:
                result[h] = ""
    except:
        pass
    for key in result.keys():
        try:
            result[key] = result[key].strip((". : / | ,"))
        except:
            pass

    # print("Last Line of Routing_Sheet")

    return result