import subprocess
import pandas as pd
import regex as re
from packages.rc.Image_Interpretation_rc import check
from packages.rc.Interpretation_RC import check_rc
from packages.rc.Interpretation_RC_2 import check_rc_2
import xlrd
#from rapidfuzz import fuzz
from fuzzywuzzy import fuzz
import requests
import time
import urllib.parse, urllib.error
import re
import string

def common_member(a, b):
    a_set = set(a)
    b_set = set(b)
    return a_set & b_set

def clean(s):
    return s.strip(" : . ( ) ;  _ ")

def correct_alpha(a):
    x1 = {'1':'I','0':'O','8':'B', ')': 'I', '(': 'I','5':'S','~':'N',']':'I','[':'I','_':''}

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


# file = r"Uttar Pradesh/29.JPG"

def magic_RC(text_json, text_json1, rc_number):

    # text_json = icr_run(file)
    # text_json = [{'boundingBox': [514, 157, 910, 163, 909, 186, 513, 179], 'text': 'CERTIFICATE OF REGISTRATION', 'words': [{'boundingBox': [515, 159, 676, 160, 675, 182, 515, 179], 'text': 'CERTIFICATE'}, {'boundingBox': [686, 161, 718, 161, 718, 182, 686, 182], 'text': 'OF'}, {'boundingBox': [726, 161, 906, 164, 905, 186, 726, 183], 'text': 'REGISTRATION'}]}, {'boundingBox': [963, 167, 1111, 169, 1111, 193, 962, 191], 'text': 'NO2724607R', 'words': [{'boundingBox': [966, 168, 1111, 169, 1110, 193, 966, 191], 'text': 'NO2724607R', 'confidence': 'Low'}]}, {'boundingBox': [593, 191, 839, 194, 838, 217, 592, 213], 'text': 'JHARKHAND STATE', 'words': [{'boundingBox': [597, 192, 751, 193, 750, 215, 596, 213], 'text': 'JHARKHAND'}, {'boundingBox': [761, 193, 836, 195, 835, 218, 760, 215], 'text': 'STATE'}]}, {'boundingBox': [286, 226, 545, 231, 544, 250, 285, 245], 'text': 'Registration No. JH1983608', 'words': [{'boundingBox': [287, 227, 392, 229, 391, 247, 287, 244], 'text': 'Registration'}, {'boundingBox': [395, 230, 431, 230, 430, 248, 395, 247], 'text': 'No.'}, {'boundingBox': [446, 230, 545, 232, 545, 249, 445, 248], 'text': 'JH1983608', 'confidence': 'Low'}]}, {'boundingBox': [606, 232, 725, 234, 724, 250, 605, 248], 'text': 'Purpose ALT/', 'words': [{'boundingBox': [608, 232, 677, 234, 677, 249, 608, 248], 'text': 'Purpose'}, {'boundingBox': [687, 234, 725, 235, 725, 249, 687, 249], 'text': 'ALT/', 'confidence': 'Low'}]}, {'boundingBox': [888, 234, 1111, 235, 1110, 254, 887, 252], 'text': 'Tax Paid Up To 10/07/2019', 'words': [{'boundingBox': [890, 234, 917, 234, 917, 252, 890, 252], 'text': 'Tax'}, {'boundingBox': [921, 235, 958, 235, 958, 253, 921, 252], 'text': 'Paid'}, {'boundingBox': [962, 235, 985, 235, 985, 253, 961, 253], 'text': 'Up'}, {'boundingBox': [990, 235, 1010, 236, 1009, 253, 989, 253], 'text': 'To'}, {'boundingBox': [1024, 236, 1110, 237, 1110, 253, 1023, 253], 'text': '10/07/2019'}]}, {'boundingBox': [285, 248, 538, 252, 537, 271, 284, 267], 'text': 'Registration Date 16/01/2019', 'words': [{'boundingBox': [287, 249, 391, 250, 391, 269, 287, 267], 'text': 'Registration'}, {'boundingBox': [396, 251, 436, 251, 436, 270, 395, 269], 'text': 'Date'}, {'boundingBox': [447, 251, 538, 253, 538, 270, 446, 270], 'text': '16/01/2019'}]}, {'boundingBox': [607, 250, 840, 254, 839, 271, 606, 266], 'text': 'HDBFINANCIAL SERVICESLIMITED', 'words': [{'boundingBox': [608, 252, 713, 253, 713, 268, 608, 266], 'text': 'HDBFINANCIAL', 'confidence': 'Low'}, {'boundingBox': [716, 253, 839, 255, 838, 271, 716, 268], 'text': 'SERVICESLIMITED', 'confidence': 'Low'}]}, {'boundingBox': [889, 254, 1001, 256, 1000, 274, 888, 272], 'text': 'Regd. Validity', 'words': [{'boundingBox': [891, 255, 938, 256, 937, 274, 890, 273], 'text': 'Regd.'}, {'boundingBox': [941, 256, 1000, 257, 999, 275, 940, 274], 'text': 'Validity'}]}, {'boundingBox': [1017, 257, 1113, 256, 1114, 272, 1018, 273], 'text': '10/01/2021', 'words': [{'boundingBox': [1024, 257, 1113, 257, 1113, 273, 1024, 273], 'text': '10/01/2021'}]}, {'boundingBox': [284, 269, 512, 273, 511, 292, 283, 288], 'text': 'Manufacturing Dt 11/2018', 'words': [{'boundingBox': [286, 270, 410, 273, 409, 291, 286, 288], 'text': 'Manufacturing'}, {'boundingBox': [414, 273, 439, 273, 438, 291, 413, 291], 'text': 'Dt'}, {'boundingBox': [446, 273, 512, 274, 511, 292, 445, 292], 'text': '11/2018'}]}, {'boundingBox': [889, 275, 984, 277, 983, 294, 889, 293], 'text': 'Unladen Wt', 'words': [{'boundingBox': [891, 276, 958, 278, 957, 294, 890, 294], 'text': 'Unladen'}, {'boundingBox': [961, 278, 984, 278, 983, 294, 960, 294], 'text': 'Wt'}]}, {'boundingBox': [1021, 279, 1082, 280, 1081, 295, 1020, 294], 'text': '007400', 'words': [{'boundingBox': [1024, 280, 1082, 280, 1082, 295, 1023, 294], 'text': '007400'}]}, {'boundingBox': [890, 295, 1083, 299, 1082, 317, 889, 313], 'text': 'Cubic Capacity 005883', 'words': [{'boundingBox': [891, 297, 939, 297, 938, 314, 891, 313], 'text': 'Cubic'}, {'boundingBox': [942, 297, 1013, 299, 1013, 316, 941, 314], 'text': 'Capacity'}, {'boundingBox': [1024, 299, 1083, 301, 1083, 318, 1023, 316], 'text': '005883'}]}, {'boundingBox': [529, 323, 696, 326, 696, 343, 528, 339], 'text': 'Colour ARCTIC_WHITE', 'words': [{'boundingBox': [530, 325, 579, 325, 580, 340, 530, 339], 'text': 'Colour'}, {'boundingBox': [587, 325, 694, 327, 694, 343, 587, 340], 'text': 'ARCTIC_WHITE'}]}, {'boundingBox': [888, 317, 990, 318, 989, 335, 887, 334], 'text': 'Wheel Base', 'words': [{'boundingBox': [891, 317, 942, 319, 941, 335, 890, 333], 'text': 'Wheel'}, {'boundingBox': [945, 319, 987, 319, 986, 335, 945, 335], 'text': 'Base'}]}, {'boundingBox': [1019, 321, 1085, 322, 1084, 339, 1018, 338], 'text': '005205', 'words': [{'boundingBox': [1024, 322, 1085, 322, 1084, 339, 1024, 338], 'text': '005205'}]}, {'boundingBox': [530, 339, 640, 342, 639, 357, 529, 354], 'text': 'Fuel DIESEL', 'words': [{'boundingBox': [530, 341, 564, 341, 564, 355, 530, 354], 'text': 'Fuel'}, {'boundingBox': [586, 341, 637, 343, 637, 357, 586, 356], 'text': 'DIESEL'}]}, {'boundingBox': [890, 335, 1019, 343, 1018, 360, 889, 352], 'text': 'RLW 036000', 'words': [{'boundingBox': [892, 336, 934, 339, 933, 355, 891, 353], 'text': 'RLW'}, {'boundingBox': [959, 340, 1018, 343, 1017, 359, 959, 357], 'text': '036000'}]}, {'boundingBox': [530, 354, 750, 357, 749, 374, 529, 371], 'text': 'Vehicle Class Goods Carrier - T', 'words': [{'boundingBox': [531, 356, 582, 356, 582, 371, 531, 370], 'text': 'Vehicle'}, {'boundingBox': [584, 356, 625, 357, 625, 372, 584, 371], 'text': 'Class'}, {'boundingBox': [630, 357, 677, 357, 677, 373, 630, 372], 'text': 'Goods'}, {'boundingBox': [680, 357, 729, 358, 729, 373, 680, 373], 'text': 'Carrier'}, {'boundingBox': [732, 358, 739, 358, 739, 373, 731, 373], 'text': '-'}, {'boundingBox': [742, 358, 750, 358, 750, 373, 742, 373], 'text': 'T'}]}, {'boundingBox': [529, 372, 605, 373, 604, 389, 528, 388], 'text': 'Body Type', 'words': [{'boundingBox': [530, 373, 567, 374, 567, 389, 529, 388], 'text': 'Body'}, {'boundingBox': [571, 374, 604, 374, 604, 389, 571, 389], 'text': 'Type'}]}, {'boundingBox': [627, 373, 686, 374, 685, 389, 626, 388], 'text': 'TRUCK', 'words': [{'boundingBox': [631, 373, 680, 375, 679, 389, 631, 388], 'text': 'TRUCK'}]}, {'boundingBox': [530, 385, 766, 389, 765, 406, 529, 403], 'text': 'Manufacturar TATA MOTORS LTD', 'words': [{'boundingBox': [530, 388, 624, 389, 624, 404, 530, 402], 'text': 'Manufacturar'}, {'boundingBox': [631, 389, 667, 389, 667, 405, 631, 404], 'text': 'TATA'}, {'boundingBox': [671, 389, 735, 389, 736, 406, 671, 405], 'text': 'MOTORS'}, {'boundingBox': [738, 389, 764, 389, 765, 406, 739, 406], 'text': 'LTD'}]}, {'boundingBox': [530, 399, 798, 405, 797, 423, 529, 417], 'text': 'Chassis No MAT466457J2N27069', 'words': [{'boundingBox': [531, 400, 597, 403, 597, 419, 531, 415], 'text': 'Chassis'}, {'boundingBox': [600, 403, 623, 403, 623, 420, 600, 419], 'text': 'No'}, {'boundingBox': [630, 403, 798, 405, 798, 423, 630, 420], 'text': 'MAT466457J2N27069', 'confidence': 'Low'}]}, {'boundingBox': [526, 428, 856, 427, 857, 446, 527, 447], 'text': 'Seating Capacity 001 No Of Cyc 06', 'words': [{'boundingBox': [531, 428, 594, 428, 594, 447, 531, 446], 'text': 'Seating'}, {'boundingBox': [598, 428, 671, 428, 671, 447, 598, 447], 'text': 'Capacity'}, {'boundingBox': [684, 428, 716, 428, 716, 447, 684, 447], 'text': '001'}, {'boundingBox': [720, 428, 744, 428, 744, 447, 720, 447], 'text': 'No'}, {'boundingBox': [748, 428, 768, 428, 768, 447, 748, 447], 'text': 'Of'}, {'boundingBox': [772, 428, 805, 428, 805, 446, 772, 446], 'text': 'Cyc'}, {'boundingBox': [833, 428, 855, 428, 855, 445, 833, 446], 'text': '06'}]}, {'boundingBox': [528, 448, 853, 449, 852, 468, 527, 467], 'text': 'Standing Capacity 00 Owner Serial 01', 'words': [{'boundingBox': [531, 449, 603, 449, 603, 468, 531, 466], 'text': 'Standing'}, {'boundingBox': [607, 449, 678, 449, 678, 468, 607, 468], 'text': 'Capacity'}, {'boundingBox': [684, 449, 705, 449, 705, 468, 684, 468], 'text': '00'}, {'boundingBox': [721, 449, 775, 449, 775, 468, 721, 468], 'text': 'Owner'}, {'boundingBox': [778, 449, 829, 449, 829, 468, 778, 468], 'text': 'Serial'}, {'boundingBox': [833, 449, 853, 449, 853, 467, 833, 468], 'text': '01'}]}, {'boundingBox': [279, 468, 636, 467, 637, 485, 280, 487], 'text': 'Engine No. ISBE5.91804081L63746809', 'words': [{'boundingBox': [282, 469, 343, 469, 342, 487, 281, 487], 'text': 'Engine'}, {'boundingBox': [346, 469, 383, 469, 382, 487, 346, 487], 'text': 'No.'}, {'boundingBox': [397, 469, 636, 468, 636, 486, 396, 487], 'text': 'ISBE5.91804081L63746809'}]}, {'boundingBox': [279, 489, 369, 490, 368, 508, 278, 507], 'text': 'Model No.', 'words': [{'boundingBox': [279, 491, 334, 490, 334, 508, 279, 508], 'text': 'Model'}, {'boundingBox': [337, 490, 368, 491, 368, 508, 337, 508], 'text': 'No.'}]}, {'boundingBox': [393, 490, 661, 488, 662, 508, 394, 509], 'text': 'TATA LPT 3118 CR BD IV 8X2', 'words': [{'boundingBox': [399, 492, 447, 491, 447, 509, 399, 509], 'text': 'TATA'}, {'boundingBox': [454, 491, 491, 490, 491, 509, 454, 509], 'text': 'LPT'}, {'boundingBox': [496, 490, 539, 490, 539, 509, 496, 509], 'text': '3118'}, {'boundingBox': [544, 490, 569, 490, 569, 509, 544, 509], 'text': 'CR'}, {'boundingBox': [576, 490, 601, 490, 601, 509, 576, 509], 'text': 'BD'}, {'boundingBox': [606, 490, 623, 490, 623, 508, 606, 509], 'text': 'IV'}, {'boundingBox': [627, 490, 662, 490, 661, 508, 627, 508], 'text': '8X2'}]}, {'boundingBox': [278, 512, 569, 513, 568, 533, 277, 532], 'text': 'Owner Name BAINATH SAHU', 'words': [{'boundingBox': [280, 514, 338, 514, 338, 532, 279, 531], 'text': 'Owner'}, {'boundingBox': [342, 514, 391, 514, 391, 533, 341, 532], 'text': 'Name'}, {'boundingBox': [398, 514, 501, 514, 501, 533, 398, 533], 'text': 'BAINATH', 'confidence': 'Low'}, {'boundingBox': [511, 514, 565, 513, 565, 532, 511, 533], 'text': 'SAHU'}]}, {'boundingBox': [277, 537, 354, 536, 355, 554, 278, 555], 'text': 'SID/W of', 'words': [{'boundingBox': [281, 537, 327, 538, 327, 555, 280, 555], 'text': 'SID/W', 'confidence': 'Low'}, {'boundingBox': [338, 538, 355, 537, 354, 555, 338, 555], 'text': 'of'}]}, {'boundingBox': [395, 537, 594, 534, 594, 554, 396, 557], 'text': 'S/O LT BALO SAHU', 'words': [{'boundingBox': [398, 538, 428, 538, 429, 556, 399, 556], 'text': 'S/O'}, {'boundingBox': [438, 537, 464, 537, 465, 556, 438, 556], 'text': 'LT'}, {'boundingBox': [470, 537, 526, 536, 526, 555, 471, 556], 'text': 'BALO'}, {'boundingBox': [536, 536, 590, 535, 591, 554, 537, 555], 'text': 'SAHU'}]}, {'boundingBox': [277, 558, 352, 559, 351, 577, 276, 576], 'text': 'Address', 'words': [{'boundingBox': [279, 559, 351, 560, 351, 577, 279, 576], 'text': 'Address'}]}, {'boundingBox': [394, 557, 805, 555, 806, 574, 395, 577], 'text': 'C/O LT BALO SAHU GANESHPUR BALUMATH', 'words': [{'boundingBox': [397, 559, 427, 558, 427, 577, 397, 577], 'text': 'C/O'}, {'boundingBox': [436, 558, 461, 558, 461, 576, 436, 577], 'text': 'LT'}, {'boundingBox': [465, 558, 516, 557, 516, 576, 465, 576], 'text': 'BALO'}, {'boundingBox': [526, 557, 574, 557, 574, 575, 526, 576], 'text': 'SAHU'}, {'boundingBox': [582, 557, 695, 557, 695, 575, 581, 575], 'text': 'GANESHPUR'}, {'boundingBox': [702, 557, 802, 557, 801, 574, 702, 575], 'text': 'BALUMATH'}]}, {'boundingBox': [394, 582, 562, 579, 563, 597, 395, 601], 'text': 'Latehar JH 829202', 'words': [{'boundingBox': [395, 583, 470, 582, 470, 599, 396, 601], 'text': 'Latehar'}, {'boundingBox': [474, 581, 494, 581, 494, 599, 474, 599], 'text': 'JH'}, {'boundingBox': [501, 581, 563, 580, 563, 598, 501, 599], 'text': '829202'}]}, {'boundingBox': [611, 635, 776, 633, 777, 654, 612, 656], 'text': 'DTO-LATEHAR', 'words': [{'boundingBox': [613, 635, 774, 634, 775, 654, 613, 656], 'text': 'DTO-LATEHAR'}]}, {'boundingBox': [273, 664, 527, 660, 528, 682, 274, 685], 'text': 'Signature Of Issuing Authority', 'words': [{'boundingBox': [277, 665, 357, 664, 358, 683, 277, 685], 'text': 'Signature'}, {'boundingBox': [361, 664, 381, 664, 381, 683, 362, 683], 'text': 'Of'}, {'boundingBox': [385, 664, 446, 663, 446, 682, 385, 683], 'text': 'Issuing'}, {'boundingBox': [450, 663, 527, 661, 527, 682, 450, 682], 'text': 'Authority'}]}, {'boundingBox': [636, 655, 774, 656, 773, 673, 635, 672], 'text': 'Issuing Authority', 'words': [{'boundingBox': [637, 657, 696, 657, 696, 673, 637, 673], 'text': 'Issuing'}, {'boundingBox': [701, 657, 774, 657, 774, 673, 701, 673], 'text': 'Authority'}]}]
    print("inside magic_RC")

    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    manuf = ["MARUTI", "HYU", "MAM", "HONDA", "DATSUN", "MAHIND", "RENAULT", "TKM"]

    manufacturer = {"MARUTI": "MARUTI SUZUKI", "HYU": "HYUNDAI", "MAM": "MAHINDRA AND MAHINDRA",
                    "MAHIND": "MAHINDRA AND MAHINDRA"}

    mon = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
           "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}

    cache = ["ment of Assam", "am.Assam", "lil of Assam Cover", "elli of Assam", "Govern", "ement of Assam",
             "ement of Assam", "ement of Assam", "ill of Assam Govern", "am Governn", "Ramcal ( Aka",
             "of Assam Government of Assam", "am Governn", "of Assam Government of Assam", "ofAssammentofAssam", "amn"]

    body_type = ["SALOON", "TOURER", "SEDAN", "SEDAN", "SPORTS CAR", "STATION WAGON", "HATCHBACK", "CONVERTIBLE", "SUV",
                 "SPORT-UTILITY VEHICLE", "MINIVAN", "PICKUP TRUCK"]

    state = ["KALAHANDI", "UTTAR PRADESH", "RAPIN", "BILASPUR", "adoor", "trivandrum", "KARUNAGAPPALLY", "BETUL", "PUNE", "JHANSI", "4TNA", "SHARKHAND", "JMARKHAND",
             "Yamunanagar", "CUDDALORE", "CHENNAI", "SIRKALI", "KALLAKURICHI", "COOCH BEHAR", "COOCHBEHAR",
             "UTTAR DINAJPUR", "Garhwa", "Deoghar", "Pakur", "Godda", "Sahibganj", "Latehar", "Simdega", "Jamtara",
             "Saraikela", "Kharsawan", "Khunti", "Ramgarh", "Hazaribagh", "Daltonganj", "Dumka", "Jamshedpur",
             "Chaibasa", "Gumla", "Lohardaga", "Bokaro", "Dhanbad", "Giridih", "Koderma", "MOHALI", "HOSHIARPUR",
             "GADAG", "KOPPAL", "KODAGU", "RAMANAGARA", "HASSAN", "JALGAON", "BULDHANA", "BULDANA", "CHANDRAPUR",
             "SATARA", "TUMKUR", "UDUPI", "DHARWAD", "BELAGAVI", "SHIMOGA", "BELGAUM", "THANE", "NASHIK", "BELLARY",
             "BHANDARA", "SHIGGAON", "YADGIR", "OSMANABAD", "DHULE", "MUMBAI", "NAGPUR", "KOLHAPUR", "LATUR", "PIMPRI",
             "BEED", "BENGALURU", "BANGALORE", "TUMKUR", "SONEPAT", "BHIWANI", "GURGRAM", "GURGAON",
             "MADILYAPRADESI", "MADITYA PRADESH", "Lucknow",


             "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Delhi",  "Uttar Pradesh",
             "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand",
             "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
             "Orissa", "Odisha", "Punjab", "UNJAB", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
             "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands", "Chandigarh",
             "Dadra and Nagar Haveli", "Daman and Diu", "Lakshadweep", "National Capital Territory of Delhi",
             "Puducherry"]
    state = [elem.upper() for elem in state]
    # CHATRA
    assam = ["Guwahati", "Kamrup", "Nagaon", "Jorhat", "Sibsagar", "Golaghat", "Dibrugarh", "Lakhimpur", "Dima Hasao",
             "Karbi Anglong", "Karimganj", "Cachar", "Sonitpur", "Darrang", "Nalbari", "Barpeta", "Kokrajhar",
             "Assam new series", "Baksa", "Udalguri", "Chirang", "Kamrup Rural", "Hailakandi", "Tinsukia", "Dhemaji",
             "Marigaon", "Bongaigaon", "Goalpara", "Dhubri"]
    assam = [elem.upper() for elem in assam]
    state.extend(assam)
    jharkhand = ["Garhwa", "Deoghar", "Pakur", "Godda", "Sahibganj", "Latehar", "Simdega", "Jamtara", "Saraikela",
                 "Kharsawan", "Khunti", "Ramgarh", "Hazaribagh", "Daltonganj", "Dumka", "Jamshedpur", "Chaibasa",
                 "Gumla", "Lohardaga", "Bokaro", "Dhanbad", "Giridih", "Koderma"]
    jharkhand = [elem.upper() for elem in jharkhand]
    state.extend(jharkhand)
    karnataka = ["Uttar a Kannada","Uttar Kannada", "Chandapura", "Koramangala", "Rajajinagar", "Bangalore", "Indiranagar", "Yeshwanthpur", "Jayanagar",
                 "Tumkur", "Mysore", "Chamrajnagar", "Mandya", "Madikeri", "Hassan", "Shimoga", "Chitradurga",
                 "Davangere", "Chickmagalur", "Mangalore", "Udupi", "Puttur", "Belgaum", "Chikkodi", "Bailhongal",
                 "Dharwad", "Gadag", "Haveri", "Vijapura", "Bagalkot", "Karwar", "Sirsi", "Kalaburagi", "Yadgir",
                 "Tarikere", "Chikkamagaluru", "Dandeli", "Madhugiri", "Tumakuru", "Hubballi", "Mangaluru", "Surathkal",
                 "Marathahalli", "R.T. Nagar", "Chamrajpet", "Banashankari", "Shantinagar", "Basavakalyan",
                 "Nagamangala", "Mandya", "K.R.Puram", "Nelamangala", "Banneraghatta", "Yelhanka", "Gokak", "Jamkhandi",
                 "Bagalkote", "Honnavar", "Uttarakannada", "Sakleshpur", "Hassan", "Hunsur", "Tiptur", "Devanahalli",
                 "Ramanagar", "Kengeri", "Chikkaballapur", "Bhalki", "Bidar", "Raichur", "Hospet", "Bellary"]   # "Kolar"
    karnataka = [elem.upper() for elem in karnataka]
    state.extend(karnataka)
    maharashtra = ["Mumbai", "Kalyan", "Sindhudurg", "Kolhapur", "Satara", "Solapur", "Ahmednagar", "Dhule",
                   "Aurangabad", "Parbhani", "Latur", "Nanded", "Yavatmal", "Gadchiroli", "Gondia", "Washim",
                   "Nandurbar", "Malegaon", "Nashik", "Akluj", "Solapur", "Ratnagiri", "Karad", "Vasai", "Virar",
                   "Panvel", "Ambejogai", "Beed", "Baramati", "Wadi", "Hingoli", "Bhandara", "Chandrapur", "Wardha",
                   "Akola", "Buldana", "Amravati", "Osmanabad", "Jalna", "Jalgaon", "Shrirampur", "Sangli", "Raigad",
                   "Thane"]
    maharashtra = [elem.upper() for elem in maharashtra]
    state.extend(maharashtra)
    punjab = ["Taxis", "Amritsar", "Bathinda", "Faridkot", "Gurdaspur", "Hoshiarpur", "Jalandhar", "Kapurthala",
              "Ludhiana", "Patiala", "Ropar", "Sangrur", "Ajnala", "Abohar", "Anandpur", "Bakala", "Batala", "Barnala",
              "Balachaur", "Dasuya", "Fazilka", "Fatehgarh", "Garhshankar", "Jagraon", "Kharar", "Malerkotla", "Moga",
              "Muktsar", "Nawanshahr", "Nakodar", "Nabha", "Pathankot", "Phagwara", "Phillaur", "Ahmedgarh", "Lehra",
              "Tappa Mandi", "Patran", "Chamkaur", "Dera Bassi", "Bagha Purana", "Dhar Kalan", "Shahkot",
              "Nihal Singh Wala", "Mohali", "Moonak", "Khadoor Sahib", "Jaitu", "Jalalabad", "Gidderbaha", "Dhuri",
              "Dera Baba Nanak", "Bhulath", "Raikot", "Mukerian", "Malout", "Bassi Pathana", "Jhunir", "Sardulgarh",
              "Budhlada", "Khamano", "Amloh", "Tarn Taran", "Talwandi Sabo", "Samrala", "Sultanpur Lodhi",
              "Rampura Phul", "Rajpura"]
    punjab = [elem.upper() for elem in punjab]
    state.extend(punjab)
    haryana = ["Ambala", "Yamuna Nagar", "Panchkula", "Karnal", "Panipat", "Kurukshetra", "Kaithal", "Guhla", "Sonepat",
               "Gohana", "Rohtak", "Bahadurgarh", "Jhajjar", "Meham", "Bhiwani", "Siwani", "Loharu", "Charkhi Dadri",
               "Hisar", "Fatehabad", "Tohana", "Sirsa", "Dabwali", "Gurgaon", "Ferozepur Jhirka", "Barara", "Bawal",
               "Adampur", "Barwala", "Kharkhoda", "Hatin", "Faridabad", "Sahabad", "Hodal", "Beri", "Kalka", "Pataudi",
               "Tosham", "Indri", "Rewari", "Mewat", "Rohtak", "Palwal", "Ellenabad", "Karnal",
               "Chandigarh", "Kosli", "Ganaur", "Sonipat", "Pehowa", "Panchkula", "Assandh", "Panipat", "Narnaul",
               "Faridabad", "Kaithal", "Rewari", "Fatehabad", "Samalkha", "Mohindergarh", "Safidon", "Narwana", "Ratia",
               "Jagadhari", "Palwal", "Sirsa", "Ballabgarh"]
    haryana = [elem.upper() for elem in haryana]
    state.extend(haryana)
    westb = ["Dakshin Dinajpur", "KOLKATA", "Diamond Harbour", "Salt Lake", "Howrah", "Howrah", "Uluberia", "Hooghly",
             "Chandannagar", "Alipore", "24 Parganas", "Barrackpore", "Barasat", "Tamluk", "Contai", "Midnapur",
             "Asansol", "Durgapur", "Burdwan", "Kalna", "Asansol", "Darjeeling", "Baruipur", "Jangipur (Murshidabad)",
             "Islampur", "Kalyani", "	Mathabhanga", "Raghunathpur", "Kalimpong", "Darjeeling", "Siliguri",
             "Jalpaiguri", "Alipurduar", "Bankura", "Malda", "	Cooch Behar", "Balurghat", "Raiganj", "Murshidabad",
             "Purulia", "Birbhum", "Nadia", "Bolpur", "Kalna"]
    westb = [elem.upper() for elem in westb]
    state.extend(westb)
    bihar = ["Patna", "Gaya", "Bhojpur", "Chapra", "Motihari", "Muzaffarpur", "Darbhanga", "Munger", "Begusarai",
             "Bhagalpur", "Purnea", "Saharsa", "Nalanda", "Bettiah", "Dehri", "Jehanabad", "Aurangabad", "Nawada",
             "Gopalganj", "Siwan", "Sheohar", "Lakhisarai", "Sheikhpura", "Banka", "Supaul", "Jamui", "Bhabua", "Buxar",
             "Madhepura", "Katihar", "Araria", "Kishanganj", "Khagaria", "Samastipur", "Samastipur",
             "Vaishali district", "Sitamarhi"]
    bihar = [elem.upper() for elem in bihar]
    state.extend(bihar)
    tamilnadu = ["TAMBARAM", "POONAMALLE", "AMBATTUR", "SHOLINGANALLUR", "ULUNDURPET", "KALLAKURICHI", "TINDIVANAM",
                 "GINGEE", "REDHILLS", "GUMIDIPOONDI", "CHENGALPATTU", "MADURANTAKAM", "THIRUTHANI", "KANCHEEPURAM",
                 "SRIPERUMBUDUR", "MEENAMBAKKAM", "VELLORE", "GUDIYATHAM", "KRISHNAGIRI", "TIRUVANNAMALAI", "CHEYYAR",
                 "ARANI", "NAMAKKAL", "RASIPURAM", "DHARMAPURI", "PALACODE", "PALACODE", "SALEM", "OMALUR", "CUDDALORE",
                 "PANRUTI", "VILLUPURAM", "ERODE", "TIRUCHENCODE", "GOBICHETTIPALAYAM", "BHAVANI", "SATHIYAMANGALAM",
                 "COIMBATORE", "SULUR", "COIMBATORE", "TIRUPPUR", "AVINASHI", "METTUPALAYAM", "POLLACHI", "VALPARAI",
                 "TIRUPUR", "KANGAYAM", "OOTY", "GUDALUR", "TIRUCHIRAPALLI", "MANAPPARAI", "PERAMBALUR", "KARUR",
                 "MANMANGALAM", "ARAVAKURICHI", "KULITHALAI", "SRIRANGAM", "LALGUDI", "MUSIRI", "THURAIYUR",
                 "THANJAVUR", "PATTUKOTTAI", "THIRUVARUR", "THIRUTHRAIPOONDI", "MANNARGUDI", "NAGAPATTINAM", "SANGARI",
                 "METTUR", "SALEM", "PUDUKOTTAI", "ILLUPPUR", "ARANTHANGI", "PERUNDURAI", "DINDIGUL", "OTTANCHATRAM",
                 "VADASANDUR", "BATALAGUNDU", "PALANI", "MADURAI", "USILAMPATTI", "THIRUMANGALAM", "MADURAI",
                 "VADIPATTI", "MELUR", "THENI", "UTHAMAPALAYAM", "ARIYALUR", "SIVAGANGA", "KARAIKUDI", "MADURAI",
                 "RAMANATHPURAM", "PARAMAKUDI", "COIMBATORE", "VIRUDHUNAGAR", "ARUPPUKOTTAI", "KUMBAKONAM", "TUTICORIN",
                 "KOVILPATTI", "HOSUR", "TIRUNELVELI", "VALLIOOR", "RANIPET", "ARAKONAM", "NAGERCOIL", "MARTHANDAM",
                 "TENKASI", "AMBASAMUTHIRAM", "ATTUR", "VALAPADI", "DHARAPURAM", "UDUMALPET", "SANKARANKOIL",
                 "TIRUCHIRAPALLI", "THIRUVERUMBUR", "MAYILADUTHURAI", "SIRKALI", "VANIYAMBADI", "THIRUPATTUR",
                 "SRIVILIPUTHUR", "SIVAKASI", "KUNDRATHUR", "ERODE", "SRIPERUMBUDUR", "NAMAKKAL", "PARAMATHI VELUR",
                 "SALEM", "CHIDAMBARAM", "NEYVELI", "VRIDDHACHALAM", "TIRUCHENDUR", "METTUR"]
    tamilnadu = [elem.upper() for elem in tamilnadu]
    state.extend(tamilnadu)
    odisha = ["Balasore", "Bhubaneswar", "Balangir", "Chandikhole", "Cuttack", "Dhenkanal", "Ganjam", "Kalahandi",
              "Keonjhar", "Koraput", "Mayurbhanj", "Phulabani", "Puri", "Rourkela", "Sambalpur", "Sundergarh",
              "Baragarh", "Jajpur", "Bhanjanagar", "Sonepur", "Malkangiri", "Kendrapada", "Debagarh", "Boudh",
              "Nuapada", "Nayagarh", "Nabarangpur", "Jharsuguda", "Bhadrak", "Jagatsinghpur", "Gajapati", "Angul",
              "Rayagada"]
    odisha = [elem.upper() for elem in odisha]
    state.extend(odisha)
    chhattisgarh = ["Chhattisgarh", "Raipur", "Dhamtari", "Dhamtari", "Rajnandgaon", "Kabirdham", "Bilaspur",
                   "Janjgir-Champa", "Korba", "Raigarh", "Jashpur", "Sarguja", "Balrampur", "Surajpur", "Mungeli", "Kondagaon",
                   "Sukma", "Bemetara", "Balod", "Gariyaband", "Baloda Bazar", "Narayanpur", "Bijapur", "Kanker", "Dantewada", "Jagdalpur", "Koriya"] # , "Durg"
    chhattisgarh = [elem.upper() for elem in chhattisgarh]
    state.extend(chhattisgarh)
    kerla = ["Kollam", "Pathanamthitta", "Alappuzha", "Kottayam", "Idukki", "Ernakulam", "Thrissur", "Palakkad", "Malappuram",
             "Kozhikode", "Wayanad", "Kannur", "Kasargode", "Kerala", "Attingal", "Muvattupuzha", "Vadakara", "Parassala", "Neyyattinkara",
             "Nedumangad", "Kazhakkoottam", "Karunagapally", "Guruvayur", "Irinjalakuda", "Kothamangalam", "Mattancherry", "North Paravur",
             "Aluva", "Perumbavoor", "Thripunithura", "Thodupuzha", "Vandiperiyar", "Vaikom", "Kanjirappally", "Changanassery", "Cherthala",
             "Mavelikara", "Chengannur", "Kayamkulam", "Mallappally", "Thiruvalla", "Adoor", "Punalur", "Kottarakara", "Kodungallur",
             "Wadakkancherry", "Alathur", "Mannarghat", "Ottappalam", "Pattambi", "Perinthalmanna", "Ponnani", "Tirur", "Koyilandi",
             "Koduvally", "Thalassery", "Taliparamba", "Kanhangad", "Kunnathur", "Ranni", "Angamaly", "Chalakkudy", "Thirurangadi", "Kuttanadu",
             "Uzhavoor", "Devikulam", "Udumbanchola"] # , "Pala"
    kerla = [elem.upper() for elem in kerla]
    state.extend(kerla)

    # print(state)

    rto_code = {"OD": "ODISHA", "TN": "TAMIL NADU", "BR": "BIHAR", "WB": "WEST BENGAL", "HR": "HARYANA", "PB": "PUNJAB",
                "MH": "MAHARASHTRA", "KA": "KARNATAKA", "JH": "JHARKHAND", "AS": "ASSAM"}

    st = ""
    for i in range(len(text_json)-1, -1, -1):
        for j in state:
            if j in text_json[i].get("text").upper():
                st = j
                break
        if st != "":
            break
    print(st)

    result = {}
    try:
        if st == "UTTAR PRADESH" or st == "LUCKNOW" or st == "JHANSI":
            st = "UTTAR PRADESH"
            print("In if condn")
            result = check(text_json, "UP1", st, 0)
            if len(text_json1) != 0:
                print("no")
                result1 = check(text_json1, "UP1", st, 1)
                result.update(result1)
        elif st == "BIHAR" or st in bihar:
            st = "BIHAR"
            result = check(text_json, "BR1", st, 0)
            if len(text_json1) != 0:
                result1 = check(text_json1, "BR1", st, 1)
                result.update(result1)
        elif st == "MADHYA PRADESH" or st == "4TNA" or st == "MADITYA PRADESH" or st == "MADILYAPRADESI" or st == "BETUL":
            st = "MADHYA PRADESH"
            result = check_rc(text_json, "MP", st, 0)
            if len(text_json1) != 0:
                result1 = check_rc(text_json1, "MP", st, 1)
                result.update(result1)
        elif st == "TAMIL NADU" or st == "CHENNAI" or st == "KALLAKURICHI" or st == "SIRKALI" or st == "CUDDALORE" or st in tamilnadu:
            st = "TAMIL NADU"
            maha = "TN"
            type = "Type 1"
            if len(text_json) > 70:
                type = "Type 2"
                maha = "TN_2"
            result = check_rc(text_json, maha, st, 0)
            # result2 = check_rc_2(text_json)
            # result.update(result2)
            if len(text_json1) != 0:
                result1 = check_rc(text_json1, "TN", st, 1)
                result.update(result1)
        elif st == "ASSAM" or st in assam:
            st = "ASSAM"
            result = check_rc(text_json, "Assam", st, 0)
            if len(text_json1) != 0:
                result1 = check_rc(text_json1, "Assam", st, 1)
                result.update(result1)
        elif st == "CHATTISGARH" or st == "CHHATTISGARH" or st == "BILASPUR" or st == "RAPIN" or st in chhattisgarh:
            st = "CHHATTISGARH"
            result = check_rc(text_json, "Chattisgarh", st, 0)
            if len(text_json1) != 0:
                result1 = check_rc(text_json1, "Chattisgarh", st, 1)
                result.update(result1)
        elif st == "KERALA" or st == "KARUNAGAPPALLY" or st == "TRIVANDRUM" or st == "ADOOR" or st in kerla:
            st = "KERALA"
            result = check_rc(text_json, "Kerla", st, 0)
            if len(text_json1) != 0:
                result1 = check_rc(text_json1, "Kerla", st, 1)
                result.update(result1)
        elif st == "PUNJAB" or st == "UNJAB" or st == "HOSHIARPUR" or st == "MOHALI" or st in punjab:
            st = "PUNJAB"
            result = check_rc(text_json, "Punjab", st, 0)
            if len(text_json1) != 0:
                result1 = check_rc(text_json1, "Punjab", st, 1)
                result.update(result1)
        elif st == "JHARKHAND" or st == "SHARKHAND" or st == "RANCHI" or st == "JMARKHAND" or st in jharkhand:
            maha = "Jharkhand"
            st = "JHARKHAND"
            if len(text_json) > 66:
                maha = "Jharkhand2"
            result = check_rc(text_json, maha, st, 0)
            if len(text_json1) != 0:
                result1 = check_rc(text_json1, maha, st, 1)
                result.update(result1)
        elif st == "HARYANA" or st == "YAMUNANAGAR" or st == "GURGAON" or st == "GURGRAM" or st == "BHIWANI" or st == "SONEPAT" or st in haryana:
            st = "HARYANA"
            result = check_rc(text_json, "Haryana", st, 0)
            if len(text_json1) != 0:
                result1 = check_rc(text_json1, "Haryana", st, 1)
                result.update(result1)
        elif st == "KARNATAKA" or st == "TUMKU" or st == "GADAG" or st == "KOPPAL" or st == "KODAGU" or st == "RAMANAGARA" or st == "HASSAN" or st == "TUMKUR" or st == "UDUPI" or st == "DHARWAD" or st == "BELAGAVI" or st == "SHIMOGA" or st == "BELGAUM" or st == "BELLARY" or st == "BANGALORE" or st == "BENGALURU" or st == "TUMKUR" or st == "YADGIR" or st == "SHIGGAON" or st in karnataka:
            st = "KARNATAKA"
            result = check_rc(text_json, "Karnataka_1", "KARNATAKA", 0)
            if len(text_json1) != 0:
                result1 = check_rc(text_json1, "Karnataka_1", "KARNATAKA", 1)
                result.update(result1)
        elif st == "RAJASTHAN":
            st = "RAJASTHAN"
            result = check_rc(text_json, "Rajasthan", "RAJASTHAN", 0)
            if len(text_json1) != 0:
                result1 = check_rc(text_json1, "Rajasthan", "RAJASTHAN", 1)
                result.update(result1)
        elif st == "ORISSA" or st == "ODISHA" or st in odisha:
            st = "ODISHA"
            maha = "OD_1"
            for i in range(10):
                if text_json[i].get("text").__contains__("GOVERNMENT OF ODISHA"):
                    print("2")
                    maha = "OD_2"
            result = check_rc(text_json, maha, st, 0)
            if len(text_json1) != 0:
                result1 = check_rc(text_json1, maha, st, 1)
                result.update(result1)
        elif st =="MAHARASHTRA" or st == "JALGAON" or st == "BULDHANA" or st == "BULDANA" or st == "CHANDRAPUR" or st == "SATARA" or st == "THANE" or st == "NASHIK" or st == "BHANDARA" or st == "OSMANABAD" or st == "MUMBAI" or st == "MAHARASTRA" or st == "BEED" or st == "PIMPRI" or st == "PUNE" or st == "LATUR" or st == "KOLHAPUR" or st == "NAGPUR" or st == "DHULE" or st in maharashtra:
            st = "MAHARASHTRA"
            maha = "Maharastra_1"
            type = "TYPE 1"
            for i in range(10):
                if text_json[i].get("text").__contains__("GOVERNMENT") and text_json[i].get("text").__contains__("MAHA"):   # or text_json[i].get("text").__contains__("GOVERNMENT")
                    # print("noooo")
                    type = "TYPE 2"
                    maha = "Maharastra_2"
                    break
                elif text_json[i].get("text").__contains__("15A") or text_json[i].get("text").__contains__("FORM"):
                    type = "TYPE 3"
                    maha = "Maharastra_1"
                    break
            print(type)
            result = check_rc(text_json, maha, st, 0)
            if type == "TYPE 3":
                result2 = check_rc_2(text_json)
                result.update(result2)
            if len(text_json1) != 0:
                result1 = check_rc(text_json1, maha, st, 1)
                result.update(result1)
        elif st =="WEST BENGAL" or st == "COOCHBEHAR" or st == "UTTAR DINAJPUR" or st == "COOCH BEHAR" or st in westb:
            st = "WEST BENGAL"
            maha = "WB_1"
            type = "TYPE 1"
            if len(text_json) > 65:
                type = "TYPE 3"
                maha = "WB_3"
                for i in range(10):
                    if text_json[i].get("text").upper().__contains__("STATE") and text_json[i].get("text").upper().__contains__("TRANSPORT"):
                        type = "TYPE 2"
                        maha = "WB_2"
                        break
            print(type)
            result = check_rc(text_json, maha, st, 0)
            if len(text_json1) != 0:
                result1 = check_rc(text_json1, maha, st, 1)
                result.update(result1)
        else:
            st = ""
            result = {}
    except:
        print(result)

    if "Registration Number" in result.keys():
        if result["Registration Number"] != "":
            result["Registration Number"] = clean(result["Registration Number"])
            result["Registration Number"] = result["Registration Number"].split("E. NO")[0]
            result["Registration Number"] = result["Registration Number"].split("E NO")[0]
            reg = result["Registration Number"].replace(":", "").replace(".", "").replace("-", "").replace(",", "").replace(" ", "").strip() #[0:4]
            x = reg[0:4]
            # print(x)
            x = x[0:2] + "-" + x[2:4]
            a = x[0]
            b = x[1]
            c = x[3]
            d = x[4]
            a = correct_alpha(a)
            b = correct_alpha(b)
            c = correct_num(c)
            d = correct_num(d)
            x = a + b + c + d + reg[4:]
            result["Registration Number"] = x

    if st == "BIHAR" or st == "UTTAR PRADESH":
        try:
            if "S/W/D" in result:
                z = result["S/W/D"]
                # print(z)
                z = z.replace("man's", "")
                z = z.strip()
                result["S/W/D"] = z
        except:
            print("S/W/D")
        try:
            if "Registration Number" in result:
                z = result["Registration Number"]
                # print(z)
                z = z.rstrip("L")
                z = clean(z)
                z = z.replace("/", "").replace("$", "S").replace("Registration No", "").replace(":", "1")
                result["Registration Number"] = z
                try:
                    if rc_number[0:2] in rto_code.keys():
                        if rc_number[-4:].isnumeric() and rc_number[2:4].isnumeric() and len(rc_number) >= 9 and len(
                                rc_number) <= 11:
                            x = fuzz.partial_ratio(rc_number, z)
                            if x > 80:
                                print("good rc_number")
                                #result["Registration Number"] = rc_number
                            elif len(z) > 11 or len(z) < 8 or (z[0].isnumeric() and z[1].isnumeric() or ((not z[2].isnumeric()) and (not z[3].isnumeric()))):
                                print(z)
                                result["Registration Number"] = rc_number
                except:
                    print("rc_number")
        except:
            print("Registration Number")
        try:
            if "Mfg Yr" in result:
                z = result["Mfg Yr"]
                del result["Mfg Yr"]
                # print(z)
                z = z.split('am')[0]
                z = z.strip()
                n = len(z)
                z = z.replace("-", "").replace("$", "0").replace("um Government al Asta", "")
                z = clean(z)
                result["Mfg Yr"] = z[-4:n]
        except:
            print("Mfg Yr")
        try:
            if "Date of Registration" in result:
                z = result["Date of Registration"]
                # print(len(z))
                del result["Date of Registration"]
                z = z.split("Class")[0]
                z = z.split("Cubic")[0]
                z = z.replace("Owner's Serial", "").replace("A439", "Aug")
                z = z.strip(" - ")
                z = z.lstrip(":")
                z = z.replace(" ", "-")
                z = z.replace(",", "").replace(".", "").replace("-", "").replace("/", "").replace(" ", "")
                z = z.replace("Dot", "Dec").replace("Now", "Nov")
                z = clean(z)
                # print(z)
                if len(z) == 8:
                    z = z.replace("D", "0").replace("y", "9").replace("Z", "7")
                    m = z[2:4]
                    mo = mon[m]
                    z = z[:2] + "-" + mo + "-" + z[4:]
                elif len(z) == 7:
                    z = z.replace("D", "0").replace("y", "9").replace("Z", "7")
                    m = z[1:3]
                    mo = mon[m]
                    z = z[0] + "-" + mo + "-" + z[3:]
                elif len(z) == 9:
                    # print("yesss")
                    mo = ""
                    s1 = z[2:5]
                    for i in month:
                        # print("Nooooo")
                        # print(fuzz.partial_ratio(s1.lower(), i.lower()) + " %%%%%%")
                        if fuzz.partial_ratio(s1.lower(), i.lower()) > 80:
                            # print("yess")
                            mo = i
                            break
                    z = z[:2] + "-" + mo + "-" + z[5:]
                elif len(z) == 10:
                    z = z[:2] + "-" + z[2:6] + "-" + z[6:]
                else:
                    z = z
                result["Date of Registration"] = z

        except:
            print("Date of Registration")
        try:
            if "Manufacturer with Make" in result and result["Manufacturer with Make"] != "":
                z = result["Manufacturer with Make"]
                del result["Manufacturer with Make"]
                # print(z)
                z = clean(z)
                z = z.replace("AM ANEVA CRISTA 24", "TKM INNOVA CRYSTA 2.0").replace("10OOOO", "")
                mak = z.split(" ")
                make = ""
                # print(mak)
                # if make.isdigit():
                #     make = mak[1]
                for i in mak:
                    if i.upper() in manuf:
                        make = i
                        break
                try:
                    make1 = manufacturer[make]
                    make = make1
                except:
                    print("make1")
                result["Make"] = make
                result["Model - Variant"] = z
        except:
            print("Manufacturer with Make")
        try:
            if result["Manufacturer with Make"] == "":
                del result["Manufacturer with Make"]
        except:
            print("Manufacturer with Make")

        try:
            if "Cubic Capacity" in result:
                z = result["Cubic Capacity"]
                del result["Cubic Capacity"]
                z = z.replace(" ", ".")
                t = ""
                if z.__contains__("."):
                    p = z.split(".")
                    z = p[0]
                    t = p[-1]
                # print(t)
                z = clean(z)

                if len(z) > 4:
                    z = z.lstrip("0")

                if len(z) == 0:
                    z = "0000"
                elif len(z) == 2:
                    z = "00" + z
                elif len(z) == 3:
                    z = "0" + z

                # if t:
                #     z = z + "." + t

                if len(z) > 4:
                    result["Cubic Capacity"] = z[-4:]
                elif t:
                    result["Cubic Capacity"] = z + "." + t
                else:
                    result["Cubic Capacity"] = z

        except:
            print("Cubic Capacity")

        try:
            if "Seating Capacity" in result:
                z = result["Seating Capacity"]
                z = z.replace("B", "8").replace("C", "0").replace("O", "0")
                z = z.lstrip("0")
                z = clean(z)
                if len(z) > 2:
                    if z[-1].isdigit():
                        z = z[-2:]
                    else:
                        for d in z:
                            if d.isdigit():
                                # print(d)
                                z = d
                                break

                if len(z) > 2:
                    z = z.lstrip("0")

                if len(z) == 0:
                    z = "00"
                elif len(z) == 1:
                    z = "0" + z

                # print(z)
                result["Seating Capacity"] = z
        except:
            print("Seating Capacity")

        try:
            if "Chassis No" in result:
                z = result["Chassis No"]
                del result["Chassis No"]
                z = z.replace("/", "7").replace(" ", "").replace("?", "7").replace(":", "1")
                result["Chassis No"] = z
        except:
            print("Chassis No")
        try:
            if "Gross Vehicle Weight" in result:
                z = result["Gross Vehicle Weight"]
                z = z.replace("kgs", "").replace(" ", "").replace("kg", "").replace("kq", "").replace("Mos",
                                                                                                      "").replace("KO",
                                                                                                                  "").replace(
                    "Pge", "")
                z = clean(z)
                z = z[-5:]

                if len(z) > 5:
                    z = z.lstrip("0")

                if len(z) == 0:
                    z = "00000"
                elif len(z) == 3:
                    z = "00" + z
                elif len(z) == 4:
                    z = "0" + z
                result["Gross Vehicle Weight"] = z
        except:
            print("Gross Vehicle Weight")

        try:
            if "Insured Name" in result:
                z = result["Insured Name"]
                del result["Insured Name"]
                # print(z)
                z = z.split("Son/wife")[0]
                z = z.replace("we for wake", "").replace("Permanent", "").replace(")", "").replace(",", "").replace(":",
                                                                                                                    "").replace(
                    "416-1 WITH 31 71 49 (", "")
                result["Insured Name"] = clean(z)
        except:
            print("Insured Name")

        try:
            if "Address" in result:
                z = result["Address"]
                del result["Address"]
                z = z.split("Unladen Weight")[0]
                z = z.split("Seating Capacity")[0]
                z = z.replace("Permanent", "").replace(")", "").replace(",", "").replace(":", "").replace(
                    "Somlwife daughter of", "").replace("No. of Cylinders", "").replace("BOCCIS", "")
                z = z.replace("Laden Weight", "").replace("(Current", "").replace("Dealer's Name & Address",
                    "").replace("Name & Address","").replace("(","").replace("aler's", "").replace("Full Addroos", "")
                z = z.replace("WITAR PRADESH", "UTTAR PRADESH")
                z = z.strip()
                try:
                    pattern2 = re.compile("[0-9]{2}-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\-\d{4}")
                    x = pattern2.search(z)
                    date = x.group()
                    # print(date)
                    if date:
                        z = z.replace(date, "")
                except:
                    print("No date")
                result["Address"] = z
        except:
            print("Address")

        try:
            if "Engine No" in result:
                z = result["Engine No"]
                del result["Engine No"]
                z = z.replace("No of Cylinders", "")
                result["Engine No"] = z
        except:
            print("Engine No")
        try:
            if "Make" in result:
                z = result["Make"]
                # print(z)
                z = z.replace(",", " ").replace(";", " ").replace("Wheel Base", "")
                result["Make"] = clean(z)
        except:
            print("Make")
        try:
            if "Model - Variant" in result:
                z = result["Model - Variant"]
                # print(z)
                z = z.strip()
                if z.__contains__("DRUM"):
                    z = z.split("DRUM")[0]
                    z = z + "DRUM-CAST"
                if z.__contains__("("):
                    if not z[-1].__contains__(")"):
                        z = z + ")"

                result["Model - Variant"] = z
        except:
            print("Model - Variant")

        try:
            if "FINANCIER_NAME" in result:
                z = result["FINANCIER_NAME"]
                z = z.replace("1) Financer Type", "")
                result["FINANCIER_NAME"] = z
        except:
            print("FINANCIER_NAME")

    if st == "CHHATTISGARH" or st == "KERALA" or st == "TAMIL NADU" or st == "WEST BENGAL" or st == "ASSAM" or st == "MADHYA PRADESH" or st == "PUNJAB" or st == "KARNATAKA" or st == "JHARKHAND" or st == "HARYANA" or st == "MAHARASHTRA" or st == "ODISHA":  ### 11sagen
        try:
            if "Engine No" in result:
                z = result["Engine No"]
                del result["Engine No"]
                z = z.replace("Chassis No", "")
                z = z.lstrip(".")
                z = z.lstrip(":")
                z = z.replace(" ", "").replace("-", "").replace("*", "K").replace(":", "1").replace("<", "K").replace(
                    "$", "S").replace("(", "C").replace("Pre", "").replace("/", "7")
                result["Engine No"] = z
        except:
            print("Engine No")

        try:
            if "Insured Name" in result:
                z = result["Insured Name"]
                del result["Insured Name"]
                z = z.replace(",", " ").replace("owner", "").replace("Wheel Base", "").replace("/s", "").replace(
                    "WENT TO", "").replace("PIR'S", "MRS")
                z = z.split("Owner")[0]
                z = z.split("Serial")[0]
                z = z.split("Son/wife")[0]

                # print(z)
                if len(z) > 50:
                    result["Insured Name"] = ""
                else:
                    result["Insured Name"] = clean(z)
        except:
            print("Insured Name")

        try:
            if "Registration Number" in result:
                z = result["Registration Number"]
                del result["Registration Number"]
                z = z.split("Unladen Weight")[0]
                z = z.split("Inladen Weight")[0]
                z = z.split("nladen")[0]
                z = z.split("GOVERNMENT")[0]
                z = z.split("E. NO")[0]
                z = z.replace("/", "").replace("$", "S").replace("Registration No", "").replace("IN", "TN").replace(
                    "Registered Number", "").replace("<", "")
                z = clean(z)

                result["Registration Number"] = z
                try:
                    pattern = re.compile("[0-9]{2}-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\-\d{4}")
                    x = pattern.search(z)
                    if x.group():
                        reg_date = x.group()
                        result["Date of Registration"] = reg_date
                        result["Registration Number"] = z.replace(reg_date, "")
                    else:
                        result["Registration Number"] = z
                except:
                    print("Registration Number")

                result["Registration Number"] = z
                try:
                    if rc_number[0:2] in rto_code.keys():
                        if rc_number[-4:].isnumeric() and rc_number[2:4].isnumeric() and len(rc_number) >= 9 and len(
                                rc_number) <= 11:
                            x = fuzz.partial_ratio(rc_number, z)
                            if x > 80:
                                print("good rc_number")
                                # result["Registration Number"] = rc_number
                            elif len(z) > 11 or len(z) < 8 or (z[0].isnumeric() and z[1].isnumeric() or (
                                    (not z[2].isnumeric()) and (not z[3].isnumeric()))):
                                print(z)
                                result["Registration Number"] = rc_number
                except:
                    print("rc_number")
        except:
            print("Registration Number")
        try:
            if "Make/Model" in result and result["Make/Model"] != "":
                z = result["Make/Model"]
                del result["Make/Model"]
                # print(z)
                z = clean(z)
                make = z.split("/")[0]
                result["Make"] = clean(make)
                result["Model - Variant"] = clean(z.replace(make, ""))
        except:
            print("Make/Model")
        try:
            if result["Make/Model"] == "":
                del result["Make/Model"]
        except:
            print("Make/Model")

        try:
            if "Make" in result:
                z = result["Make"]
                # print(z)
                del result["Make"]
                z = z.split("Color")[0]
                z = z.replace(",", " ").replace(";", " ").replace("Dealer Name &",
                                                                  "")  # .replace("Govern", "").replace("ement of Assam", "")
                z = z.lstrip("an")
                for c in cache:
                    if z.__contains__(c):
                        z = z.replace(c, "")

                z = z.strip()
                # print(z)
                if z == "SMW":
                    z = "BMW"
                if z.__contains__("("):
                    if not z[-1].__contains__(")"):
                        z = z + ")"

                if z.__contains__("/"):
                    result["Make"] = z.split("/")[0]
                    p = z.replace(result["Make"], "")
                    result["Model - Variant"] = p
                else:
                    result["Make"] = z

        except:
            print("Make")

        try:
            if "Date of Registration" in result:
                z = result["Date of Registration"]
                # print(len(z))
                del result["Date of Registration"]
                z = z.split("Class")[0]
                z = z.split("Cubic")[0]
                z = z.split("CLAS")[0]
                z = z.split("and the Temporary")[0]
                z = z.strip(" - ")
                z = z.replace(" ", "-").replace(":", "").replace("Date", "")
                z = z.replace(",", "").replace(".", "").replace("-", "").replace("/", "").replace(" ", "").replace("$", "")
                z = clean(z)
                # print(z)
                if len(z) == 8:
                    z = z.replace("D", "0").replace("y", "9").replace("Z", "7").replace("C", "0")
                    m = z[2:4]
                    if int(m) > 12:
                        m = m.replace("9", "0")
                    mo = mon[m]
                    z = z[:2] + "-" + mo + "-" + z[4:]
                elif len(z) == 7:  # 15-02-20-2 (exception)
                    # print("yesss")
                    z = z.replace("D", "0").replace("y", "9").replace("Z", "7")
                    m = "0" + z[2]
                    mo = mon[m]
                    # print(mo)
                    z = z[:2] + "-" + mo + "-" + z[3:]
                elif len(z) == 9:
                    if z[2:5] == "301":
                        z = z[:2] + "-" + "Jul" + "-" + z[5:]
                    else:
                        mo = ""
                        s1 = z[2:5]
                        for i in month:
                            if fuzz.ratio(s1.lower(), i.lower()) > 70:
                                # print("yess")
                                mo = i
                                break
                        z = z[:2] + "-" + mo + "-" + z[5:]
                elif len(z) == 10:
                    z = z[:2] + "-" + z[2:6] + "-" + z[6:]
                else:
                    z = z
                result["Date of Registration"] = z

        except:
            print("Date of Registration")

        try:
            if "Model - Variant" in result:
                z = result["Model - Variant"]
                del result["Model - Variant"]
                # print(z)
                z = z.split("Registration")[0]
                z = z.split("Wheel")[0]
                z = z.replace("Month & Yr.of Mig", "").replace("Owner Name", "").replace("$", "S").replace(";", " ")  # .replace("(", "").replace(")", "")
                z = z.replace("Month & Yr. of Mig", "").replace("r's Classiffication", "").replace("!", "I")
                # print(z)
                result["Model - Variant"] = z
                for c in cache:
                    if z.__contains__(c):
                        z = z.replace(c, "")
                z = z.strip()
                # print(z)
                if z.__contains__("("):
                    if not z[-1].__contains__(")"):
                        z = z + ")"
                # print(z)
                result["Model - Variant"] = z
        except:
            print("Model - Variant")

        try:
            if "Mfg Yr" in result:
                z = result["Mfg Yr"]
                del result["Mfg Yr"]
                # print(z)
                z = z.split('am')[0]
                z = z.strip()
                # n = len(z)
                z = z.replace("-", "").replace("$", "0").replace("um Government al Asta", "").replace("FG.", "")
                z = z.replace("20017", "2017")
                z = clean(z)
                # print(z)
                # if z[1] == "0":
                #     z = z.replace("0", "9", 1)
                if len(z) > 4:
                    z = z[-4:]

                if z[-4] == "2":
                    result["Mfg Yr"] = z[-4] + "0" + z[-2:]
                elif z[-4] == "1":
                    if z[-3] == "0":
                        z = z[-4] + "9" + z[-2:]
                        result["Mfg Yr"] = z
                else:
                    result["Mfg Yr"] = z[-4:]
        except:
            print("Mfg Yr")

        try:
            if "Name & Add" in result and result["Name & Add"] != "":
                z = result["Name & Add"]
                del result["Name & Add"]
                # z = z.replace("SIMON FERNANDES", "")
                Name = z.split(",")[0]
                Add = z.replace(Name, "").replace("$", "S")
                # print(Add)
                result["Insured Name"] = Name
                result["Address"] = Add
        except:
            print("Name & Add")
        try:
            if result["Name & Add"] == "":
                del result["Name & Add"]
        except:
            print("Name & Add")
        try:
            if "Make & Model" in result and result["Make & Model"] != "":
                z = result["Make & Model"]
                del result["Make & Model"]
                z = clean(z)
                p = z.split(";")
                while ("" in p):
                    p.remove("")
                # print(p)
                z = ";".join(p)
                # print(z)
                make = z.split(";")[0]
                model = z.replace(make, "")
                model = clean(model)
                model = model.split(";")[0]
                # print(model)
                body = model.split(";")[-1]
                # print(body)
                body = body.upper()
                # print(body)
                for b in body_type:
                    if b == body:
                        # print(b)
                        model = model.replace(b, "")
                result["Make"] = make
                result["Model - Variant"] = model.replace(";", " ")
        except:
            print("Make & Model")
        try:
            if result["Make & Model"] == "":
                del result["Make & Model"]
        except:
            print("Make & Model")
        try:
            if "Seating/Standing" in result and result["Seating/Standing"] != "":
                z = result["Seating/Standing"]
                del result["Seating/Standing"]
                if len(z) > 2:
                    z = z.lstrip("0")
                # print(z)
                if len(z) == 1:
                    z = "0" + z
                result["Seating Capacity"] = z[:3]
        except:
            print("Seating/Standing")
        try:
            if result["Seating/Standing"] == "":
                del result["Seating/Standing"]
        except:
            print("Seating/Standing")
        try:
            if "Address" in result:
                z = result["Address"]
                del result["Address"]
                z = z.split("Purpose")[0]
                z = z.split("DTO")[0]
                z = z.split("DY. RTO")[0]
                z = z.split("DY.RTO")[0]
                z = z.split("Identification")[0]
                z = z.split("Full Address: (Temporary )")[0]
                z = z.split("Motor Car")[0]
                z = z.split("HPI/LEASE")[0]
                z = z.split("Seating")[0]
                z = z.split("Re Registering")[0]
                z = z.upper().split("VELTICLO CLASS")[0]
                z = z.upper().split("VEHICLE CLASS")[0]
                z = z.split("REF. MFG")[0]
                z = z.replace("REDMI NOTE 6 PRO MI DUAL CAMERA", "").replace("District Transport Officer", "").\
                    replace("Fail Address", "").replace("Temp. Address", "").replace("O.A.W", "").replace("JOIES", "").\
                    replace("MOB. NO.", "").replace("MOB. NO", "")
                # print(z)
                z = z.replace("Full :", "").replace("R.L.W", "").replace("HPILEASE", "").replace("HP/LEASE", ""). \
                    replace(":", "").replace(";", ",").replace("b)", "").replace("(", "").replace(")", "")
                z = z.replace("Audio", "").replace("Video", "").replace("No", "").replace("N0", "").replace("Yes",
                                                                                                            "").replace(
                    "EMISSION NORMS", "").replace("BHARAT STAGE-IV", "").replace("TEMPORARY", "")  # .replace("NO", "")
                # print(z)
                z = z.replace("FAIL ADDRESS", "").replace("FULL ADDRESS", "").replace("TEMP", "").replace("ADDRESS",
                                                                                                          "").replace(
                    "DISTRICT TRANSPORT OFFICER", "").replace("MARUTI", "")
                z = z.replace("LECT FROM", "").replace("WITH EFFECT FROM", "").replace("HDFC BANK LTD", "").replace(
                    "WITH AFFECT FROM", "").replace("STATE BANK OF INDIA", "").replace("SMW", "").replace("STANDING CAPACITY", "").replace("PERMANENT", "")
                z = z.replace("BATHING", "BATHINDA").replace("CANDAM", "GANJAM").replace("486 JAGADISHPUR", "JAGADISHPUR").replace("1 MJOB. NO.", "").replace("GAJANAN", "").replace("FINANCIER", "")
                z = z.replace(",,,", " ").replace(",,", " ").replace("MOB NO", "").replace("AUDIO", "").replace("YES", "").replace(",,", "")
                z = z.split("SI.NO")[0]
                z = z.split("MODEL NAME")[0]
                z = z.split("IS FINANCED")[0]
                z = z.split("-,COVE")[0]
                z = z.split("E. NO")[0]
                z = z.split("SHOT ON")[0]
                z = z.split("TIKAMENT")[0]
                z = z.split("CUSTOMER ")[0]
                # print(z)
                try:
                    pattern2 = re.compile("\d{2}\/\d{2}\/\d{4}")
                    date2 = pattern2.search(z)
                    if date2.group():
                        z = z.replace(date2.group(), "")

                    pattern = re.compile("\d{2}\s\d{2}\s\d{4}")
                    date = pattern.search(z)
                    if date.group():
                        z = z.replace(date.group(), "")

                    # pattern3 = re.compile("\d{1}\-\d{2}\-\d{4}")
                    # date3 = pattern3.search(z)
                    # if date3.group():
                    #     z = z.replace(date3.group(), "")
                except:
                    print("date")
                try:
                    pattern = re.compile("(0/91)?[6-9][0-9]{9}")
                    x = pattern.search(z)
                    if x.group():
                        z = z.replace(",", "").replace(x.group(), "")
                except:
                    print("No Mob")
                    # temp_add = temp_add.replace(",", "").replace(" ", "")

                result["Address"] = z
                if result["Address"].__contains__(result["Insured Name"]):
                    result["Address"] = clean(result["Address"].split(result["Insured Name"])[-1])
                if result["Address"].__contains__(result["S/D/W"]):
                    result["Address"] = clean(result["Address"].split(result["S/D/W"])[-1])
        except:
            print("Address")

        try:
            if "Chassis No" in result:
                z = result["Chassis No"]
                del result["Chassis No"]
                # print(z)
                z = z.split("REGD")[0]
                z = z.replace("Engine No", "")
                z = z.lstrip(".")
                z = z.lstrip(":")
                z = z.replace("*", "K").replace(":", "1").replace("$", "S").replace("/", "7").replace(".", "")
                result["Chassis No"] = z

                p = result["Engine No"]
                p = p.strip()
                if p[0] == "M" and p[1] != "C":
                    q = result["Chassis No"]
                    result["Engine No"] = q
                    result["Chassis No"] = p
        except:
            print("Chassis No")

        try:
            if "Gross Vehicle Weight" in result:
                z = result["Gross Vehicle Weight"]
                del result["Gross Vehicle Weight"]
                # print(z)
                z = z.split("/")[-1]
                z = z.replace("kgs", "").replace(" ", "").replace("Kg", "").replace("kg", "").replace("kq", "").replace("Mos",
                                                                                                      "").replace("Kgs",
                                                                                                                  "").replace(
                    "xg", "")
                z = z.replace("C", "0").replace("O", "0").replace("c", "0").replace("o", "0").replace("U", "0").replace(
                    "t", "0").replace("$", "1").replace("r", "")
                z = clean(z)
                z = z[-5:]
                result["Gross Vehicle Weight"] = z
                if len(z) > 4:
                    z = z.lstrip("0")

                if len(z) == 0:
                    z = "00000"
                elif len(z) == 3:
                    z = "00" + z
                elif len(z) == 4:
                    z = "0" + z
                # print(z)
                try:
                    if int(z) > 10000:
                        z = "0" + z[1:]
                    result["Gross Vehicle Weight"] = z
                except:
                    print("Int pro GVW")
        except:
            print("Gross Vehicle Weight")

        try:
            if "Seating Capacity" in result:
                z = result["Seating Capacity"]
                del result["Seating Capacity"]
                # print(z)
                z = z.strip()
                z = z.replace("Including Driver", "").replace("1+1", "2").replace("6+1", "7")
                z = z.split("including")[0]
                z = z.split("Including")[0]
                z = z.split("Inchiding")[0]
                z = z.split("U.Weight")[0]
                z = z.split("No")[0]
                z = z.split("Owner")[0]
                z = z.split("/")[0]
                z = z.split("+")[0]
                # print(z)
                z = z.replace("a", "").replace("s", "").replace("p", "0").replace("o", "0").replace("s", "5").replace(
                    "S", "5").replace("great", "").replace("!", "2").replace("i", "0").replace("f", "5")
                z = z.replace("(", "").replace(")", "").replace("'", "").replace("70", "01")
                z = clean(z)

                if len(z) > 2:
                    if z.__contains__("+"):
                        z = z[-3:]
                    elif z[-1].isdigit():
                        z = z[-2:]
                    else:
                        for d in z:
                            if d.isdigit():
                                # print(d)
                                z = d
                                break

                if len(z) > 2:
                    z = z.lstrip("0")
                # print(z)

                if len(z) == 0:
                    z = "00"
                elif len(z) == 1:
                    z = "0" + z

                result["Seating Capacity"] = z
        except:
            print("Seating Capacity")

        try:
            if "Cubic Capacity" in result:
                z = result["Cubic Capacity"]
                del result["Cubic Capacity"]
                # print(z)
                z = z.replace(" ", "")
                z = z.replace("CC", "").replace("cc", "").replace("GC", "").replace("D", "0")
                for c in cache:
                    if z.__contains__(c):
                        z = z.replace(c, "")
                # print(z)
                z = z.replace("C", "0").replace("O", "0").replace("c", "0").replace("o", "0").replace("/", "7").replace(
                    "G", "6")
                z = z.replace(",", ".").replace(" ", ".")
                z = z.strip()
                z = z.strip("a b c d e f g h i j k l m n o p q r s t u v w x y z")
                # print(z)
                p = z.split(".")
                # print(p)
                z = p[0]
                t = ""
                if len(p) > 1:
                    t = p[-1]
                # print(t)
                z = clean(z)

                if len(z) > 4:
                    z = z.lstrip("0")

                if len(z) == 0:
                    z = "0000"
                elif len(z) == 1:
                    z = "000" + z
                elif len(z) == 2:
                    z = "00" + z
                elif len(z) == 3:
                    z = "0" + z

                if len(z) > 4:
                    result["Cubic Capacity"] = z[-4:]
                elif t:
                    result["Cubic Capacity"] = z + "." + t
                else:
                    result["Cubic Capacity"] = z
        except:
            print("Cubic Capacity")

        try:
            if "FINANCIER_NAME" in result:
                z = result["FINANCIER_NAME"]
                del result["FINANCIER_NAME"]
                z = z.replace("T 1)", "")
                z = z.replace("Seating(in all)/Standing/Sleeping Capacity", "")
                if z.__contains__(","):
                    temp = z.split(",")
                    if len(temp) > 1:
                        result["FINANCIER_NAME"] = temp[0]
                        result["FINANCIER_BRANCH"] = temp[1]
                    else:
                        result["FINANCIER_NAME"] = z
                elif z.__contains__("/"):
                    temp = z.split("/")
                    if len(temp) > 1:
                        result["FINANCIER_NAME"] = temp[0]
                        result["FINANCIER_BRANCH"] = temp[1]
                    else:
                        result["FINANCIER_NAME"] = z

                else:
                    result["FINANCIER_NAME"] = z
                    # result["FINANCIAL_BRANCH"] = ""

        except:
            print("FINANCIER_NAME")


    else:
        if "Cubic Capacity" in result.keys():
            result["Cubic Capacity"] = result["Cubic Capacity"].strip(
                "a b c d e f g h j  k l i m n o p q r s t u v w x y z")

        if "Seating Capacity" in result.keys():
            result["Seating Capacity"] = result["Seating Capacity"].split("No Of Cyc")[0]
    result["CUSTOMER_STATE"] = ""
    try:
        if "Address" in result.keys():
            result["Address"] = result["Address"].replace("Full Address", "").replace("Temporary", "").replace(
                "Fail Address: ( ", "")  # .replace("Son/wife/daughter of", "")
            result["Address"] = clean(result["Address"].lstrip(","))
            # print(result["Address"])
            if result["Address"].upper().__contains__("SON/WIF"):
                if result["Address"].__contains__(result["S/W/D"]):
                    if result["Address"].split()[-1] == result["S/W/D"]:
                        result["Address"] = result["Address"].split(result["S/W/D"])[0]
                        result["Address"] = result["Address"].split("Son/wife/daughter of")[-1]
                    else:
                        result["Address"] = result["Address"].split(result["S/W/D"])[-1]
                else:
                    result["Address"] = result["Address"].split("Son/wife/daughter of")[-1]
            # print(result["Address"])
            if len(result["Address"].split()[0]) > 5:
                if (not result["Address"].__contains__(",")) and (not result["Address"].__contains__("/")):
                    result["Address"] = result["Address"].lstrip(', 0 1 2 3 4 5 6 7 8 9 : ( )')
            else:
                result["Address"] = result["Address"].lstrip(', : ( )')
            # print(result["Address"])
            result["Address"] = result["Address"].replace("Full Address", "").replace("Temporary",
                                                                                      "")  # .replace("Son/wife/daughter of", "")
            # result["Address"] = result["Address"].lstrip(', 0 1 2 3 4 5 6 7 8 9 : ( )')
            # print(result["Address"])
            temp_add = result["Address"].replace(" ", "")
            try:
                pattern = re.compile("(0/91)?[6-9][0-9]{9}")
                x = pattern.search(temp_add)
                mobile = x.group()
                temp_add = result["Address"].replace(",", "").replace(mobile, "")
            except:
                # print("No Mobile")
                temp_add = temp_add.replace(",", "").replace(" ", "")
            try:
                pattern2 = re.compile("(\d{2})[/.-](\d{2})[/.-](\d{4})$")
                x = pattern2.search(temp_add)
                date = x.group()
                temp_add = temp_add.replace(",", "").replace(date, "")
            except:
                print("No Date")
                temp_add = temp_add.replace(",", "").replace(" ", "")
            try:
                # print(temp_add)
                pattern3 = re.compile(r"\d\d\d\d\d\d\d")
                x = pattern3.search(temp_add)
                # print(x)
                date = x.group()
                temp_add = temp_add.replace(",", "").replace(date, "")
            except:
                print("No Garbage")
                temp_add = temp_add.replace(",", "").replace(" ", "")
            try:
                # print(temp_add)
                pattern4 = re.compile(r"\d\d\d\d\d\d\d")
                x = pattern4.search(temp_add)
                # print(x)
                date = x.group()
                temp_add = temp_add.replace(",", "").replace(date, "")
            except:
                print("No Garbage2")
                temp_add = temp_add.replace(",", "").replace(" ", "")
            try:
                pattern5 = re.compile("[0-9]{6}|[0-9]{3}\s[0-9]{3}")  # ^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$")  #(^((?!RAM).)*$)
                x = pattern5.search(temp_add)
                result["Pincode"] = x.group()
                result["Address"] = result["Address"].split(result["Pincode"])[0]  # + " " + result["Pincode"]
            except:
                print("Pincode")
    except:
        print("Address")
    if result["CUSTOMER_STATE"] == "":
        result["CUSTOMER_STATE"] = st
    try:
        data = pd.read_excel("packages/all_rto_det.xlsx")
        df = pd.DataFrame(data, columns=['Vehicle RTO Codes', 'District/Region'])
    except:
        print("major")

    ask = ["Registration Number", "Date of Registration", "Insured Name", "Address", "Make", "Mfg Yr", "Chassis No",
           "Engine No", "Cubic Capacity", "Model - Variant", "Gross Vehicle Weight", "Seating Capacity",
           "CUSTOMER_STATE",
           "Pincode", "HYPOTHECATION", "FINANCIER_NAME", "FINANCIER_BRANCH", "Carrying Capacity", "RTO", "product_type"]

    for h in ask:
        if h not in result.keys():
            result[h] = ""
            print("empty")
        else:
            ct = 0
            # print(result[h])

    try:
        if "RTO" in result.keys():
            if result["RTO"] == "":
                if "Registration Number" in result.keys():
                    if result["Registration Number"] != "":
                        x = result["Registration Number"].replace(":", "").replace(".", "").replace("-", "").replace(
                            ",", "").replace(" ", "").strip()[0:4]
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
                        z = df[df['Vehicle RTO Codes'] == x]['District/Region'].item()
                        result["RTO"] = z
                        x = a+b+c+d+result["Registration Number"][4:]
                        result["Registration Number"] = x
    except:
        print("RTO")
        result["RTO"] = ""

    if result["Pincode"] == "" or result["Pincode"][0] == "0" or len(result["Pincode"]) != 6:
        try:
            print("I m there")
            result["Address"] = result["Address"].upper()
            df = pd.read_csv("packages/pincode_final.csv", engine='python')
            df = df[df["statename"] == result["CUSTOMER_STATE"]]
            region = df['regionname'].unique().tolist()
            region = [x for x in region if str(x) != 'nan']
            reg = False
            dis = False
            tal = False
            k = 0
            for i in region:
                if i in result["Address"]:
                    print("region")
                    k = 1
                    reg = True
                    break
            if k == 1:
                df = df[df["regionname"] == i]
            district = df["Districtname"].unique().tolist()
            district = [x for x in district if str(x) != 'nan']
            k = 0
            for i in district:
                if i in result["Address"]:
                    print("district")
                    k = 1
                    dis = True
                    break
            if k == 1:
                df = df[df["Districtname"] == i]
            taluk = df["Taluk"].unique().tolist()
            taluk = [x for x in taluk if str(x) != 'nan']
            k = 0
            if taluk != []:
                for i in taluk:
                    if i in result["Address"]:
                        print("taluk")
                        print(i)
                        k = 1
                        tal = True
                        break
            if k == 1:
                df = df[df["Taluk"] == i]
            try:
                if reg is True or dis is True or tal is True:
                    result["Pincode"] = str(df.iloc[0]["pincode"])
                else:
                    print("No Match")
            except:
                print("Not there")
        except:
            print("Pincode Excel")
    try:
        temp = {}
        temp["Make"] = result["Make"]
        temp["Model"] = result["Model - Variant"]
    except:
        pass
    try:
        make = result["Make"]
        if make == "MSI" or make == "MARUTI SUZUKI INDIA LTD" or "MARUTI" in make or make == "HSI" or make == "LIS I" or make == "MS" or make == "MUL":
            make = "Maruti"
        if make == "MAM" or "MAHINDRA AND MAHINDRA" in make or make == "MAH & MAH" or "MAHINDRA & MAHINDRA" in make or "MAHENDRA & MAHINDRA" in make or "MAHINDRA" in make or make == "M&M":
            make = "Mahindra"
        if make == "HYU" or make == "HYUMOT" or "HYUNDAI MOTOR" in make:
            make = "Hyundai"
        if "OYOTA KIRLOSKAR MOTOR" in make or "TOYOTA KIRIOSKAR MOTOR" in make or "TOYOTA KIRKOGEAR MOTOR" in make or make == "TOTKML" or make == "TKM":
            make = "Toyota"
        if make == "TATA MOTORS LTD" or "TATA MOTORS" in make or "TATAMOTOR" in make or make == "TML":
            make = "Tata"
        if make == "BMW INDIA PVT LTD" or make == "SMW" or make == "BMWIN":
            make = "BMW"
        if make == "RENAULT NOAPIT LTD":
            make = "Renault"
        if make == "HONDA CARS INDIA LTD" or make == "HIS":
            make = "Honda"
        if make == "VOLVO AUTO INDIA PVT LTD":
            make = "Volvo"
        if make == "JAGUAR LAND ROVER INDIA":
            make = "Jaguar Land Rover"
        if make == "MERCED":
            make = "Mercedes"
        if "RENALT" in make:
            make = "Renault"


        #bikes
        if "HERO" in make or "HENO MOTOCORP LTD" in make or "HEAD MOTOCORP LTD" in make or make == "HHML" or make == "HMCL":
            make = "Hero"
        if "HONDA MOTORCYCLE AND" in make or make == "HONDAMCTIC" or make == "HONMCY":
            make = "Honda"
        if "ROYAL-ENFIELD" in make or "ROYAL ENFIELD" in make:
            make = "Royal Enfield"
        if "TVS MOTOR" in make:
            make = "TVS"
        if "BAJAJ AUTO LTD" in make or make == "BAJ  W":
            make = "Bajaj"
        if "SUZUKI MOTORCYCLE INDIA" in make or make == "SUZMCY":
            make = "Suzuki"

        print(make)
        make1 = make
        make2 = make
        model = result["Model - Variant"]
        model1 = model
        model2 = model
        cc = ""
        cc = str(result["Cubic Capacity"])
        # print(cc)
        sx = ""
        cc1 = ""
        cc2 = ""
        # print(model)
        if "." in cc:
            cx = cc.split(".")
            cc1 = cx[0]
            cc2 = cx[1]
            if not (int(cc1) < 50):   # or not (int(cc1) > 2500)
                cc = cc1
        # print(cc2)
        for c in list(cc):
            sx = sx + correct_num(c)
        cc = sx
        if cc == "":
            cc = "0"
        seat = str(result["Seating Capacity"])
        sx = ""
        for c in list(seat):
            sx = sx + correct_num(c)
        seat = sx
        if seat == "":
            seat = "0"
        weight = str(result["Gross Vehicle Weight"])
        sx = ""
        for c in list(weight):
            sx = sx + correct_num(c)
        weight = sx
        if weight == "":
            weight = "0"

        loc = "packages/final_car.xlsx"
        wb = xlrd.open_workbook(loc)
        make_names = wb.sheet_names()
        make_names.remove("Entire List ")
        make_names.remove("Others")
        print(make_names)

        others_list = ["VOLKSWAGEN", "BMW", "AUDI", "LEXUS"]

        name = ""
        thre = 70
        for z in make_names:
            x = fuzz.ratio(clean(make1).upper(), clean(z).upper())
            # print(z)
            # print(x)
            if x >= thre:
                thre = x
                make = z
                # print(make)
                # print(thre)
                name = z

        other = 0
        if name != "":
            sheet = wb.sheet_by_name(make)
            result["Make"] = name
            result["product_type"] = "Four Wheeler"
        else:
            other = 1
            sheet = wb.sheet_by_name("Others")
            result["Make"] = make1
            model = make1 + " " + model
            # result["product_type"] = "Private Car"
        # print(model)
        # print(make + "####")
        # print(model + " $$$$")
        xcv = -1
        thre = 68    # 55
        name = ""

        for i in range(sheet.nrows):
            x = clean(str(sheet.cell_value(i, 0))).upper()
            if x == "BRAND":
                continue
            x = x.replace(make.upper(), "")
            model1 = model1.upper()
            model1 = model1.replace(make.upper(), "")
            z = fuzz.ratio(model1, x)
            # print(model1)
            # print(x)
            # print(z)
            if z >= thre and z > 0:
                thre = z
                model = x
                # print(model)
                # print(thre)
                name = x
                xcv = i
                result["product_type"] = "Four Wheeler"

        i = xcv
        if name != "" and i != -1:
            result["Model - Variant"] = model
            try:
                if int(cc) < 600 or int(cc) > 5000:
                    result["Cubic Capacity"] = sheet.cell_value(i, 2)
                else:
                    if int(cc) - int(sheet.cell_value(i, 2)) < 300:
                        result["Cubic Capacity"] = cc
                    else:
                        result["Cubic Capacity"] = sheet.cell_value(i, 2)
            except:
                print("cubic_capacity_car")

            try:
                if int(seat) <= 1 or int(seat) == 4 or int(seat) > 15:
                    result["Seating Capacity"] = str(sheet.cell_value(i, 1)).split(".")[0].split("-")[0]
                else:
                    if int(seat) - int(str(sheet.cell_value(i, 1)).split(".")[0].split("-")[0]) < 2:
                        result["Seating Capacity"] = seat
                    else:
                        result["Seating Capacity"] = str(sheet.cell_value(i, 1)).split(".")[0].split("-")[0]
            except:
                print("seating_capcity_car")

            try:
                if float(weight) < 10 or float(weight) > 10000:
                    # print("yesssss")
                    result["Gross Vehicle Weight"] = str(sheet.cell_value(i, 3))
                else:
                    if float(weight) - float(str(sheet.cell_value(i, 3))) < 10:
                        result["Gross Vehicle Weight"] = weight
                    else:
                        result["Gross Vehicle Weight"] = str(sheet.cell_value(i, 3))
            except:
                print("gvw_car")
        else:
            if other == 1:
                for x in others_list:
                    if x.upper() in model:
                        result["make"] = x.upper()
                        result["product_type"] = "Four Wheeler"
            result["Model - Variant"] = model
            result["Cubic Capacity"] = cc
            result["Seating Capacity"] = seat

            ###   BIKES

            loc = "packages/Bike.xlsx"
            wb = xlrd.open_workbook(loc)
            make_names = wb.sheet_names()
            # print(make_names)

            name = ""
            thre = 75
            for z in make_names:
                x = fuzz.ratio(clean(make2).upper(), clean(z).upper())
                # print(z)
                # print(x)
                if x > thre:
                    thre = x
                    make1 = z
                    # print(make1)
                    # print(thre)
                    name = z

            other = 0
            if name != "":
                sheet = wb.sheet_by_name(make1)
                result["Make"] = name
                result["product_type"] = "Two Wheeler"
            else:
                other = 1

            if other == 0:
                xcv = -1
                thre = 65
                # print("$$$$$$$$$$$$$$$")
                name = ""
                for i in range(sheet.nrows):
                    x = str(sheet.cell_value(i, 0)).upper()
                    x = x.replace(make.upper(), "")
                    z = fuzz.ratio(model2.upper().replace(make.upper(), ""), x)
                    # print(x)
                    # print(z)
                    if z >= thre:
                        thre = z
                        model1 = x
                        # print(model1)
                        # print(thre)
                        name = x
                        xcv = i
                # print("@@@@@@@@@@@@@@@@@@@@@@@")
                # print(name)
                # print(xcv)
                i = xcv
                if name != "" and i != -1:
                    # print("######")
                    result["Model - Variant"] = model1
                    # print("@@@@@@@@@@@@@@@@@@@@@@@")
                    # cc = cc.lstrip("0")
                    try:
                        if int(cc) < 50 or int(cc) > 2500:
                            # print("yesss")
                            result["Cubic Capacity"] = sheet.cell_value(i, 2)
                            print("#######################3")
                        else:
                            # print("yesssss")
                            if int(cc) - int(sheet.cell_value(i, 2)) < 150:
                                result["Cubic Capacity"] = cc
                            else:
                                result["Cubic Capacity"] = sheet.cell_value(i, 2)
                    except:
                        print("Cubic_Capacity_Bike")

                    try:
                        if int(seat) <= 1 or int(seat) > 3:
                            result["Seating Capacity"] = str(sheet.cell_value(i, 1))
                        else:
                            if int(seat) - int(str(sheet.cell_value(i, 1))) < 2:
                                result["Seating Capacity"] = seat
                            else:
                                result["Seating Capacity"] = str(sheet.cell_value(i, 1))
                    except:
                        seating_capacity_bike = 0

                    # print(weight)
                    # print(float(weight) < 10 or float(weight) > 500)
                    # print(sheet.cell_value(i, 3))
                    try:
                        if float(weight) < 10 or float(weight) > 500:
                            # print("yesssss")
                            result["Gross Vehicle Weight"] = str(sheet.cell_value(i, 3))
                        else:
                            if float(weight) - float(str(sheet.cell_value(i, 3))) < 15:
                                result["Gross Vehicle Weight"] = weight
                            else:
                                result["Gross Vehicle Weight"] = str(sheet.cell_value(i, 3))
                    except:
                        print("gvw_bike")
        if cc2:
            result["Cubic Capacity"] = result["Cubic Capacity"] + "." + cc2

    except:
        print("Make Model Excel")

    car_list = ["Maruti", "Renault", "Hyundai", "Toyota", "Audi", "BMW", "Mercedes", "Hyundi", "Kia", "Tata", "Chevrolet", "Ford", "Mahindra", "Mitsubishi & HM", "Skoda", "MG Hector", "Volvo"]
    bike_list = ["Bajaj", "Hero", "Royal Enfield", "TVS motors", "Yamaha", "Piaggio", "Aprilia", "Hero Honda"]
    model_four = ["Bolero", "Scorpio", "BEAT", "Etios", "Kwid", "Figo", "Toyota", "Tata"]
    if "No of Cylinders" in result.keys():
        del result["No of Cylinders"]

    if "S/W/D" in result.keys():
        del result["S/W/D"]

    try:
        if "Cubic Capacity" in result.keys():
            result["Cubic Capacity"] = str(result["Cubic Capacity"])
            while len(result["Cubic Capacity"]) < 4:
                result["Cubic Capacity"] = "0" + result["Cubic Capacity"]
        if "Gross Vehicle Weight" in result.keys():
            result["Gross Vehicle Weight"] = str(result["Gross Vehicle Weight"])
            while len(result["Gross Vehicle Weight"]) < 5:
                result["Gross Vehicle Weight"] = "0" + result["Gross Vehicle Weight"]
        if "Seating Capacity" in result.keys():
            result["Seating Capacity"] = str(result["Seating Capacity"])
            while len(result["Seating Capacity"]) < 2:
                result["Seating Capacity"] = "0" + result["Seating Capacity"]
    except:
        print("Numeric Case")

    for key in result.keys():
        try:
            result[key] = str(result[key]).strip(". : / | ,")
        except:
            print("Issue here")

    ask1 = ["registration_no", "date_of_registration", "insured_name", "address", "make", "mfg_yr", "chassis_no",
            "engine_no", "cubic_capacity", "model", "gross_vehicle_weight", "seating_capacity", "customer_state",
            "pincode", "hypothecation", "financier_name", "financier_branch", "carrying_capacity", "rto", "product"]

    for i in range(len(ask)):
        a = ask[i]
        b = ask1[i]
        result[b] = result[a]
        del result[a]
    try:
        result["model"] = result["model"].replace(result["make"], "").strip()
    except:
        print("clean_model")

    result["product_type"] = result["product"]
    del result["product"]

    try:
        # print(result["make"])
        thresh = 70
        max = ""
        for car in car_list:
            r = fuzz.ratio(car.upper().replace("INDIA", "").replace("MOTOR", ""), clean(result["make"]).upper().replace("INDIA", "").replace("MOTOR", ""))
            if r > thresh:
                thresh = r
                max = car
        if max:
            result["product_type"] = "Four Wheeler"
            print("private_car_00")
        else:
            thresh = 70
            max = ""
            for bike in bike_list:
                r = fuzz.ratio(bike.upper(), clean(result["make"]).upper())
                if r > thresh:
                    thresh = r
                    max = bike
            if max:
                result["product_type"] = "Two Wheeler"
                print("bike_00")
    except:
        print("product_type0")
    try:
        result["make"] = temp["Make"]
        result["model"] = temp["Model"]
    except:
        pass
    print("Last Line of Routing_Sheet")

    if result["product_type"].strip() == "":
        for i in range(len(text_json)):
            for j in model_four:
                print(text_json[i].get("text"), j)
                if text_json[i].get("text").upper().__contains__(j.upper()):
                    result["product_type"] = "Four Wheeler"
                    break
            if result["product_type"].strip() != "":
                break

        if result["product_type"].strip() == "":
            for i in range(len(text_json1)):
                for j in model_four:
                    print(text_json1[i].get("text"), j)
                    if text_json1[i].get("text").upper().__contains__(j.upper()):
                        result["product_type"] = "Four Wheeler"
                        break
                if result["product_type"].strip() != "":
                    break

    return result
