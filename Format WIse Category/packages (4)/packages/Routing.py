import subprocess
import pandas as pd1
import regex as re
from packages.hdfc.pdf.Interpretation import magic
import os
from packages.hdfc.pdf.Routing_Sheet import final_run
from packages.Routing_for_image import main_interpretation_run_image
from packages.icici.pdf.ICICI_pdf import icici_pdf
from packages.cloud_connection import upload_to_aws, image_presigned_url
from packages.bajaj.pdf.bajaj_image import main_run_bajaj
import logging


def pdftotext(path, output_file):
    #Generate a text rendering of a PDF file in the form of a list of lines.
    args = ['pdftotext', '-layout', path, output_file]
    cp = subprocess.run(
      args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
      check=True, text=True
    )
    return cp.stdout


def main_interpretation_run(file_name,vech_number):
    logging.info('uploaded pdf')
    upload_to_aws('uploads/' + str(vech_number) + '/' + str(file_name), str(vech_number) + '/' + str(file_name))
    file = "uploads/" + str(file_name).replace(".PDF","").replace(".pdf","")
    # try:
    print(file)
    try:
        pdftotext(file + '.pdf', file.replace(".PDF", "").replace(".pdf", "") + '.txt')
    except:
        pdftotext(file + '.PDF', file.replace(".PDF", "").replace(".pdf", "") + '.txt')
    f = open(file.replace(".PDF", "").replace(".pdf", "") + ".txt")
    # except:
    # print("File Not found")
    count = ""
    z = []
    s = ""
    for line in f:
        if not (line == '\n' or line == ''):
            z.append(line)
            s = s + line
    for line in z:
        if line.upper().__contains__("RELIANCE"):
            count = "reliance"
            print("RELIANCE")
            break
        elif line.upper().__contains__("ICICI"):
            count = "icici"
            print("ICICI")
            break
        elif line.upper().__contains__("BAJAJ"):
            count = "bajaj"
            print("BAJAJ")
            break
        elif line.upper().__contains__("HDFC"):
            count = "hdfc"
            print("HDFC")
            break
    try:
        if count == "reliance":
            print("passing to Image")
            result = main_interpretation_run_image(vech_number, file_name)
            return result
        elif count == "bajaj":
            print("passing to bajaj pdf")
            result = main_run_bajaj(file_name)
            return result
        elif count == "icici":
            print("Entering ICICI")
            result = icici_pdf(z, s)
            print("Completed ICICI")
        elif count == "hdfc":
            print("HDFC PDF")
            result = final_run(z, s)
    except:
        print("Couldnt process pdf. Sending to image")
        result = main_interpretation_run_image(vech_number, file_name)
        return result
    os.remove('uploads/' + str(file_name))
    os.remove('uploads/' + str(file_name).replace('.pdf', '').replace('.PDF', '') + '.txt')
    return result

