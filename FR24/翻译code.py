import openpyxl
from openpyxl import Workbook

# 创建一个新的Excel工作簿
wb = Workbook()

sheet = wb.create_sheet("Airport Data")

# 设置表头
sheet.append(["机场代码", "机场名称", "机场所在地"])

# 读取airport CODE中的数据
with open("airport CODE.txt", "r", encoding="utf-8") as f:
    for line in f:
        code, name, country = line.strip().split('\t')
        # 将数据添加到Excel表格中
        sheet.append([code, name, country])

# 保存Excel文件
wb.save("airport CODE.xlsx")