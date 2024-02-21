import csv
import pandas as pds

date = pds.read_excel('/Users/xiejun/Documents/2024年自动入库日期.xlsx', header=None)


with open('/Users/xiejun/Documents/2024年自动入库日期qconfig.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'StorageDate'])  # 写入表头
        for i, date in enumerate(date[0], start=1):
            writer.writerow([str(i), date.strftime('%Y/%m/%d')])


