import codecs
import csv
import requests
import json

from util.utility import check_node_not_none


class ServiceDetail:
    def __init__(self, service, avg, qps ,appid):
        self.service = service
        self.avg = avg
        self.qps = qps
        self.appid = appid


# 读取csv文件，获取
def read_csv_get_operation_list(filename):
    service_list = []
    service_detail = None
    with codecs.open(filename, encoding='utf-8-sig') as file:
        for row in csv.DictReader(file, skipinitialspace=True):
            service = str(row["Name"]).lower()
            avg = str(row["Avg(ms)"])
            qps = str(row["Qps"])
            appid = str(row["AppId"])
            service_detail = ServiceDetail(service, avg, qps, appid)  # 实例化对象
            service_list.append(service_detail)
    file.close()
    return service_list


# 调用soa API，获取service的appID
def call_api(url, data):
    cookie = 'UBT_VID=1703233274693.db14uNqpJKXW; IFS_FP=B4F79A-B0823D-E519C7; _RF1=112.65.220.253; _RSG=HVqB9uCwZo9r2TJhihFTI8; _RDG=28f3e35d1bfdea2df414e1de0c32aa1e92; _RGUID=9ca3e8ce-092f-47d1-849d-3ebb2b4dd0b5; IFS_R=9ca3e8ce092f47d1849d3ebb2b4dd0b5; _bfa=1.1703233274693.db14uNqpJKXW.1.1703233274738.1703233289375.1.1.10650008581; PRO_cas_principal=PRO-7869656a756e-MTcwMzIzMzI4OTY1OQ-f55b6820d78b4334bfa8f0f2fba2afd4; PRO_principal=87c6731d64eb83aa79b0966422f393a1-e4441d2c-bf3d-4c0e-84a9-52f6a0265fa0; offlineTicket=_863F211EC07981C4F581817C92FF9B345A25AC456A71895213185BA31235BF66; PRO_CCST_SECRET_ADFC=PRO-7869656a756e-c66ee7845d4b45fa9b1a254d4f3fffe8; Servers_Eid=TR009698; PRO_Servers_Eid=TR009698; UserImageHash=b924bd659e4c20d2c61f12bf9333f6cc; UserName=xiejun; EmployeeCode=TR009698; SoaPortalToken="3MumQ/fv/yJ8vc0yl+EYvdQbSTh27D/Wl1sF+dyiYkTzy3KbxR4xO81j94i4ibG/CvoOFXKu9zSGIK23Sugkq9MmV7e/sACGIfoM0dt9PQs="; JSESSIONID=875297B853E5C50B5F43F00D6353C9D4'
    token = '"3MumQ/fv/yJ8vc0yl+EYvdQbSTh27D/Wl1sF+dyiYkTzy3KbxR4xO81j94i4ibG/CvoOFXKu9zSGIK23Sugkq9MmV7e/sACGIfoM0dt9PQs="'
    headers = {"Cookie": cookie, "Content-Type": "application/json", "Accept": "application/json", "charset": "UTF-8",
               "X-Soa-Portal-Token": token}
    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    return response.text


def call_apid_then_get_serivce_info(serviceid):
    url = "http://gov.soa.fx.ctripcorp.com/forward/pro/api/service/get-service-instances"
    data = {"serviceId": serviceid}
    response_body = call_api(url, data)
    data = json.loads(response_body)
    return data


def count_substring(s, substring):
    return s.count(substring)


def split_string(s, delimiter, maxsplit):
    return delimiter.join(s.rsplit(delimiter, maxsplit)[:maxsplit])


def write_to_csv(detail_list, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["服务", "appid", "owner", "平均耗时(ms)", "QPS", "SIN环境是否Ready（上云/虫洞）"])

        for detail in detail_list:
            operation = detail.service
            appid = detail.appid
            # call api get service's appids
            if not appid:
                continue
            else:
                # 判断logicalInstances节点是否存在zoneId为SIN的节点
                # call api get appid owner
                appid_info = call_apid_then_get_appid_info(appid)
                print(appid)
                if appid_info.get("app_owner"):
                    owner = appid_info["app_owner"]
                    writer.writerow([operation, appid, owner, detail.avg, detail.qps, ""])


def call_webinfo_api(url, data):
    cookie = 'UBT_VID=1703233274693.db14uNqpJKXW; IFS_FP=B4F79A-B0823D-E519C7; _RF1=112.65.220.253; _RSG=HVqB9uCwZo9r2TJhihFTI8; _RDG=28f3e35d1bfdea2df414e1de0c32aa1e92; _RGUID=9ca3e8ce-092f-47d1-849d-3ebb2b4dd0b5; IFS_R=9ca3e8ce092f47d1849d3ebb2b4dd0b5; PRO_cas_principal=PRO-7869656a756e-MTcwMzIzMzI4OTY1OQ-f55b6820d78b4334bfa8f0f2fba2afd4; PRO_principal=87c6731d64eb83aa79b0966422f393a1-e4441d2c-bf3d-4c0e-84a9-52f6a0265fa0; offlineTicket=_863F211EC07981C4F581817C92FF9B345A25AC456A71895213185BA31235BF66; PRO_CCST_SECRET_ADFC=PRO-7869656a756e-c66ee7845d4b45fa9b1a254d4f3fffe8; Servers_Eid=TR009698; PRO_Servers_Eid=TR009698; principal_webInfo=PRO-7869656a756e-MTcwMzIzMzI4OTY1OQ-f55b6820d78b4334bfa8f0f2fba2afd4; _pk_ses.53.8cb3=*; _bfaStatusPVSend=1; _bfi=p1%3D10650009917%26p2%3D10650009917%26v1%3D2%26v2%3D4; _bfaStatus=success; _pk_id.53.8cb3=2db788fdcff3ed10.1703235036.1.1703235051.1703235036.; _bfa=1.1703233274693.db14uNqpJKXW.1.1703235035821.1703235051142.1.3.10650009917; _ubtstatus=%7B%22vid%22%3A%221703233274693.db14uNqpJKXW%22%2C%22sid%22%3A1%2C%22pvid%22%3A3%2C%22pid%22%3A10650009917%7D'
    headers = {"Cookie": cookie, "Content-Type": "application/json", "Accept": "application/json", "charset": "UTF-8"}
    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    return response.text


def call_apid_then_get_appid_info(appid):
    url = "http://webinfo7.ops.ctripcorp.com/api/basicInfo"
    data = {"id": appid, "type": "application"}
    response_body = call_webinfo_api(url, data)
    data = json.loads(response_body)["data"]
    return data[0] if data else {}


def main():
    client_appid = "100018273"
    read_csv_file = '/Users/xiejun/Documents/' + client_appid + '_1.csv'
    write_csv_file = '/Users/xiejun/Documents/' + client_appid + '调用其他服务.csv'
    # read csv
    detail_list = read_csv_get_operation_list(read_csv_file)
    # log
    print(detail_list)
    # write to csv
    write_to_csv(detail_list, write_csv_file)


# 使用示例
main()
