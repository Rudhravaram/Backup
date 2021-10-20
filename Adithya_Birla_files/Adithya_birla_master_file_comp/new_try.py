import openpyxl
wb = openpyxl.Workbook()
Sheet_name = wb.sheetnames
wb.save(filename='Test.xlsx')