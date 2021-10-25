import os
import camelot
import pandas as pd
cwd = os.path.abspath('')
files = os.listdir(cwd)
file=r"D:\Backup\Backup\camelot\N0679_Hospital Rates_11thJul19.pdf"
tables2=camelot.read_pdf(file, flavor='lattice', pages='144')#stream#lattice
print(tables2)
tables2.export('144.csv', f='csv', compress=True)


