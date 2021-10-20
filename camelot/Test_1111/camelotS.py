import camelot
import os
import pandas as pd
import pikepdf
cwd = os.path.abspath('')
files = os.listdir(cwd)
file= r"D:\camelot\Top 51-80 Providers\51-80 Rank Hospitals@ Tariff's\N0048\N0048_Vasuclar Additional_Aug15.pdf"
pdf = pikepdf.Pdf.open(file)
print(pdf)

# tables2=camelot.read_pdf(pdf, flavor='lattice', pages='all')#stream#lattice
# print(tables2)
# tables2.export(r"D:\camelot\Top 51-80 Providers\51-80 Rank Hospitals@ Tariff's\N0048\Results\TRY", f='csv',compress=True)#,compress=True


