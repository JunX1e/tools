import datetime



def sql_build(table_name,target):
    start_date = datetime.date(2022, 1, 1)
    end_date = start_date + datetime.timedelta(days=700)
    interval = datetime.timedelta(days=15)
    while start_date < end_date:
        next_date = start_date + interval
        # 生成查询语句
        query = f"SELECT '{table_name}',i.OrderID \
        FROM {target} i \
        JOIN {table_name} d ON i.checkingid = d.checkingid \
        WHERE i.userdata_location <> d.userdata_location \
        AND i.DataChange_LastTime >= '{start_date}' \
        AND i.DataChange_LastTime < '{next_date}' \
        AND i.userdata_location <> 'GB_90009' \
        AND d.userdata_location <> 'GB_90009';"
        print(query)
        start_date = next_date


table_list = [
    'issuebilldetail',
    'issuebilldetailextend',
    'issuebillaccount',
    'issuebillassignoperator',
    'issuebillextend',
]



table_list_ticket = [
    'tichecking',
    'issuebillticketnodetail',
    'issuebillticketnoextend'
]
sql_build("ticheckingdetail", "tichecking")
