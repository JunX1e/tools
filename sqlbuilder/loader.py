import csv
import pandas as pds
import numpy as np


def generate_sql_insert(excel_name):
    excel = pds.read_excel(excel_name)
    for idx, row in excel.iterrows():
        if np.isnan(row['Agent ID']):
            continue
        item_id = '14'
        value_text_source_name = row['Agency Name']
        value_currency = row["Currency"]
        value_text = f'{value_text_source_name}({value_currency})'
        real_id = int(row['Agent ID'])
        status = 1
        extended_value = '2'
        create_by = 'System'
        modify_by = ''
        order_by_id = '0'
        config_item_value_insert_sql = (
            f"INSERT INTO configitemvalue (ItemID, ValueText, RealID, Status, ExtendedValue, CreateBy, ModifyBy, OrderByID)"
            f" VALUES ('{item_id}', '{value_text}', '{real_id}', {status}, '{extended_value}', '{create_by}', '{modify_by}', '{order_by_id}');")
        print(config_item_value_insert_sql)


generate_sql_insert('../csvfile/travix45.xlsx')
