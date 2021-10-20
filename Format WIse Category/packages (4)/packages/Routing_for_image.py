from packages.hdfc.image.Routing_image import main_image_run
from packages.reliance.image.Reliance_12421 import magic_reliance
from packages.icici.image.routing_sheet_icici import magic_icici
from packages.bajaj.image.bajaj_image import bajaj
from pdf2image import convert_from_path
from packages.icr_connection import icr_run
from packages.cloud_connection import upload_to_aws, image_presigned_url
import os
import logging


def converting_to_image_pdf(file_name):
    file_name_temp = []
    my_image_name = str(file_name).replace(".pdf","").replace(".PDF","")
    print(os.path.exists('uploads/' + str(my_image_name)))
    if os.path.exists('uploads/' + str(my_image_name)):
        print("folder")
    else:
        os.mkdir('uploads/' + str(my_image_name))
    pages = convert_from_path("uploads/" + file_name, 400)
    no_of_pages = len(pages)
    for i in range(len(pages)):
        file_name_temp.append("uploads/" + str(my_image_name) + '/' + str(my_image_name) + '-' + str(i) + '.jpeg')
        pages[i].save("uploads/" + str(my_image_name) + '/' + str(my_image_name) + '-' + str(i) + '.jpeg', 'JPEG')
    return no_of_pages,file_name_temp


def main_interpretation_run_image(vech_number, filename):
    if filename.split(".")[-1].upper() == "PDF":
        pages, files = converting_to_image_pdf(filename)
        filename = files[0]
        logging.info('uploaded image')
        upload_to_aws(str(filename), str(vech_number) + '/' + str(filename))
        url_icr_process = image_presigned_url(str(vech_number) + '/' + str(filename))
        print('icr', url_icr_process)
        #os.remove('uploads/' + str(vech_number) + '/' + str(filename))
        #os.rmdir('uploads/' + str(vech_number))
    else:
        logging.info('uploaded image')
        upload_to_aws('uploads/' + str(vech_number) + '/' + str(filename), str(vech_number) + '/' + str(filename))
        url_icr_process = image_presigned_url(str(vech_number) + '/' + str(filename))
        print('icr', url_icr_process)
        os.remove('uploads/' + str(vech_number) + '/' + str(filename))
        os.rmdir('uploads/' + str(vech_number))
    text_json = icr_run(url_icr_process)
    print('data model')
    count = ""
    result = {}
    for i in range(len(text_json)):
        if "reliance" in text_json[i].get("text").lower():
            count = "reliance"
            break
        elif "icici" in text_json[i].get("text").lower():
            count = "icici"
            break
        elif "bajaj" in text_json[i].get("text").lower():
            count = "bajaj"
            break
        elif "hdfc" in text_json[i].get("text").lower():
            count = "hdfc"
            break

    try:
        if count == "reliance":
            print("######RELIANCE              ##############")
            result = magic_reliance(text_json)
        elif count == "icici":
            print("######ICICI              ##############")
            result = magic_icici(text_json)
        elif count == "bajaj":
            print("######bajaj              ##############")
            result = bajaj(text_json)
        elif count == "hdfc":
            print("######hdfc               ##############")
            result = main_image_run(text_json)
    except:
        result = {}

    return result