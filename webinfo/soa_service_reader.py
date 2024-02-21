import codecs
import csv
import requests
import json
import time

from webinfo.soa_client_reader import call_webinfo_api


# appid_set = []
# version_set = []
# app_owner_set = []
# app_owner_email_set = []
# app_org_name_set = []
# app_chinese_name_set = []

def read_csv_get_appid_list(filename):
    appid_version_set = []
    with codecs.open(filename, encoding='utf-8-sig') as file:
        for row in csv.DictReader(file, skipinitialspace=True):
            appid = str(row["domain"]).lower()
            version = str(row["name"]).lower()
            appid_version = {"appid": appid, "version": version}
            appid_version_set.append(appid_version)
    file.close()
    return appid_version_set


# print(appid_set.__len__())
# print(appid_set)
# print(version_set.__len__())
# print(version_set)

def call_api(url, data):
    cookie = "_bfaStatusPVSend=1; _RSG=HsaJsRsr.P0XS6Oy8vP6S9; _RDG=28693e62b3028b27b4077a87252587a906; _RGUID=067ed766-f64e-4d91-9706-67923c606721; PRO_CCST_SECRET_ADFC=PRO-6261695f6c-d7bd1252dd324a419fd3807c670d7325; Servers_Eid=S64373; PRO_Servers_Eid=S64373; bbz_offlineLocale=zh-CN; UBT_VID=1686578245451.2zts8t; nfes_isSupportWebP=1; fltoffline_order_timeZoneOffset=8; fltoffline_order_part=3a4f6aba22f17e1d3e21f00b8887cb68; fltoffline_order_lan=zh-CN; workbench_locale=zh-CN; UBT_CID=70006203511263636495; GUID=70006203511263636495; IFS_FP=1vyrs65-oqbre-2u4m5o; IFS_R=067ed766f64e4d91970667923c606721; FAT_cas_principal=FAT-6261695f6c-MTcwMDY0MzM5MzI3Mw-5b1c91ca64b34123a44b681b4cb2ee25; UAT_cas_principal=UAT-6261695f6c-MTcwMDY0NzU3NTM0Ng-053f7bfb317c48f089825859c0736462; PRO_cas_principal=PRO-6261695f6c-MTcwMTQxNjI4NDU3NA-ec30462686a844268fd104a330c497bf; PRO_principal=bd2e01ce1b5b87dd0df38e50852ef32e-ee628e23-aab7-4569-8fe1-e876d69795bb; offlineTicket=_5CAAEC5F5E87531D055B7EF037396D0F047C24A811CBF68A5A4F9B1716522FB3; principal_webInfo=PRO-6261695f6c-MTcwMTQxNjI4NDU3NA-ec30462686a844268fd104a330c497bf; Union=OUID=&AllianceID=66672&SID=1693366&SourceID=&AppID=&OpenID=&exmktID=&createtime=1702288922&Expires=1702893722153; _RF1=112.65.220.248; _pk_ses.53.8cb3=*; _bfa=1.1686578245451.2zts8t.1.1702371317339.1702371352466.183.2.10650009917; _ubtstatus=%7B%22vid%22%3A%221686578245451.2zts8t%22%2C%22sid%22%3A183%2C%22pvid%22%3A2%2C%22pid%22%3A10650009917%7D; _pk_id.53.8cb3=3a41c247f59039bc.1701421495.5.1702371352.1702371317.; _bfi=p1%3D10650009917%26p2%3D10650009917%26v1%3D2%26v2%3D1; _bfaStatus=success"
    headers = {"Cookie": cookie, "Content-Type": "application/json", "Accept": "application/json", "charset": "UTF-8"}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.text


def call_apid_then_get_appid_info(appid):
    url = "http://webinfo7.ops.ctripcorp.com/api/basicInfo"
    data = {"id": appid, "type": "application"}
    response_body = call_webinfo_api(url, data)
    data = json.loads(response_body)["data"]
    return data[0]


def get_appid_infos(appid_list):
    data_list = []
    for appid in appid_list:
        data = call_apid_then_get_appid_info(appid)
        data_list.append(data)
        time.sleep(0.5)
    return data_list


# 使用示例
# url = "http://webinfo7.ops.ctripcorp.com/api/basicInfo"
# data = {"id": "100036002", "type": "application"}
# response_body = call_api(url, data)
# data = json.loads(response_body)["data"]
# print(data[0]["app_owner"])
# print(data[0]["app_owner_email"])
# print(data[0]["app_org_name"])
# print(data[0]["app_chinese_name"])

def write_to_csv(server_appid, filename, appid_version_set):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ServerAppID", "AppID", "name", "owner", "经理组", "组织", "2023-10-30版本"])

        for appid_version in appid_version_set:
            appid = appid_version["appid"]
            version = appid_version["version"]
            data = call_apid_then_get_appid_info(appid)
            print(data)
            owner = data["app_owner"]
            email = data["app_owner_email"]
            org = data["app_org_name"]
            name = data["app_chinese_name"]
            writer.writerow([server_appid, appid, name, owner, email, org, version])


def read_csv_get_appid_list_then_write_to_csv():
    server_appid = "100024647"
    read_csv_file = '/Users/xiejun/Documents/' + server_appid + '_2.csv'
    write_csv_file = '/Users/xiejun/Documents/' + server_appid + '被其他服务调用.csv'
    # read csv
    appid_version_list = read_csv_get_appid_list(read_csv_file)
    # log
    print(appid_version_list)
    # call api get appid info
    # data_list = get_appid_infos(appid_list)
    # log
    # print(data_list)
    # write to csv
    write_to_csv(server_appid, write_csv_file, appid_version_list)


# 使用示例
read_csv_get_appid_list_then_write_to_csv()