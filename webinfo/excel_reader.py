import pandas as pd

df = pd.read_excel('/Users/xiejun/Documents/单元所有SOA客户端升级.xlsx')
names = []
appids = []
orgs = []
versions = []
deadlines = []

for index, row in df.iterrows():
    email = row['经理组']
    name = email.split('@')[0]
    version = row['2023-10-30版本']
    appid = row['AppID']
    if  not appids.__contains__(appid) and version != 'java-2.24.28' and version != 'java-2.24.35':

        appids.append(row['AppID'])
        orgs.append(row['组织'])
        names.append(name)
        versions.append(version)
        deadlines.append('2024-02-29')




data = {'AppId': appids,
         'Owner': names,
        '组织': orgs,
        '客户端版本':versions,
        '截止时间':deadlines}
df = pd.DataFrame(data)

# 将 DataFrame 写入 Excel 文件
df.to_excel('/Users/xiejun/Documents/单元所有SOA客户端升级清单.xlsx', index=False)