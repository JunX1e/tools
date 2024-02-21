import pandas as pds
import numpy as np
import json

from webinfo_json import WebsiteInfo, deserialize_json, serialize_json


def global_load():
    # 需要新增的链接
    global new_web_url_and_account
    # 基础配置
    global booking_channel
    global flight_agency
    booking_channel = 'TF-WS'
    flight_agency = '-1'
    website_info_issue = WebsiteInfo(
        "",
        "https://ibe.travelfusion.com",
        "",
        "",
        "I",
        "ctriplivesearch.admin",
        "zHSQXr9py"
    )
    website_info_rebook = WebsiteInfo(
        "",
        "https://ibe.travelfusion.com",
        "",
        "",
        "I",
        "shzfglz",
        "Wsxc2023."
    )
    new_web_url_and_account = [website_info_issue, website_info_rebook]


def generate_sql_update(excel_name):
    global_load()
    excel = pds.read_excel(excel_name)
    for idx, row in excel.iterrows():
        # 用于更新的列表
        to_update_web_list = list([])
        # 如果有老json优先用老json
        original_web_site_json = row['WebSiteInfo']
        original_web_site = row['FailOpWebSite']
        flight_agency = row["FlightAgency"]
        if isinstance(flight_agency , int) and flight_agency == 4755 :
            continue
        if not isinstance(original_web_site_json, float):
            website_info_objects = deserialize_json(original_web_site_json)
            # 老节点保留
            to_update_web_list.append(website_info_objects)
        else:
            if not isinstance(original_web_site, float):
                original_website_info = WebsiteInfo("2", original_web_site, None, None, "I", None, None)
                to_update_web_list.append(original_website_info)
        # 这里保证了老节点在前
        to_update_web_list.append(new_web_url_and_account)
        toupdate_webinfo_json = serialize_json(to_update_web_list)
        config_item_value_insert_sql = (
            f"INSERT INTO issuebillautofailopconfig (BooKingChannel, FlightAgency, FailType, FailOpTip, FailOpWebSite, WebSiteInfo)"
            f" VALUES ('{booking_channel}', '{flight_agency}', 2, '', '{original_web_site}', '{toupdate_webinfo_json}');")
        print(config_item_value_insert_sql)


generate_sql_update("../csvfile/tfwebinfo.xlsx")
