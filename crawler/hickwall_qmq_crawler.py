import csv

import requests
import json

base_url = 'https://bat.fx.ctripcorp.com/api/ds/query'


def call_api(url, data):
    cookie = '_RSG=HVqB9uCwZo9r2TJhihFTI8; _RDG=28f3e35d1bfdea2df414e1de0c32aa1e92; _RGUID=9ca3e8ce-092f-47d1-849d-3ebb2b4dd0b5; IFS_R=9ca3e8ce092f47d1849d3ebb2b4dd0b5; PRO_CCST_SECRET_ADFC=PRO-7869656a756e-c66ee7845d4b45fa9b1a254d4f3fffe8; Servers_Eid=TR009698; PRO_Servers_Eid=TR009698; fltoffline_order_lan=zh-CN; fltoffline_order_timeZoneOffset=8; fltoffline_order_part=3a4f6aba22f17e1d3e21f00b8887cb68; IFS_FP=B4F79A-742260-C55DAF; PRO_cas_principal=PRO-7869656a756e-MTcwMzc0Mjc5NjgzOA-6548427ecbf240cd97e5edeccf52a756; PRO_principal=87c6731d64eb83aa79b0966422f393a1-29c74e5d-ff5f-487b-af33-3997cbbd3c23; offlineTicket=_863F211EC07981C4F581817C92FF9B3470615C6FF5F7CBC734303D9F345347BB; FAT_cas_principal=FAT-7869656a756e-MTcwMzc1OTIzMTg2Mw-e52b7cab23a44b9180725476697b23ad; Union=OUID=&AllianceID=66672&SID=1693366&SourceID=&AppID=&OpenID=&exmktID=&createtime=1703764287&Expires=1704369087331; UBT_VID=1695609672067.48jis5; nfes_isSupportWebP=1; _bfaStatusPVSend=1; _ubtstatus=%7B%22vid%22%3A%221695609672067.48jis5%22%2C%22sid%22%3A180%2C%22pvid%22%3A93%2C%22pid%22%3A0%7D; _bfi=p1%3D10650061238%26p2%3D10650060568%26v1%3D93%26v2%3D39; _bfaStatus=success; _RF1=117.131.104.24; _bfa=1.1695609672067.48jis5.1.1704266983153.1704281859859.182.2.10650052332; _pk_ref.111.655c=%5B%22%22%2C%22%22%2C1704282454%2C%22http%3A%2F%2Fconf.ctripcorp.com%2F%22%5D; _pk_ses.111.655c=*; grafana_session=ad2eff3524e8bfb215218f4f628de005; _pk_id.111.655c=bbd065c6247c9838.1703233291.26.1704282668.1704282454.'
    headers = {"Cookie": cookie, "Content-Type": "application/json", "Accept": "application/json", "charset": "UTF-8"}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.text


def build_param_subject(expr):
    global param
    param = {
        "queries": [
            {
                "expr": expr,
                "format": "table",
                "instant": True,
                "intervalFactor": 1,
                "legendFormat": "{{subject}} {{appid}}",
                "legends": [
                ],
                "refId": "A",
                "datasource": {
                    "uid": "208",
                    "type": "prometheus"
                },
                "queryType": "timeSeriesQuery",
                "exemplar": False,
                "requestId": "5A",
                "utcOffsetSec": 28800,
                "interval": "",
                "datasourceId": 208,
                "intervalMs": 1200000,
                "maxDataPoints": 542
            }
        ],
        "range": {
            "from": "2023-12-01T07:57:44.385Z",
            "to": "2024-01-03T07:57:44.385Z",
            "raw": {
                "from": "now-31d",
                "to": "now"
            }
        },
        "from": "1701360000000",
        "to": "1704211200000"
    }





def find_labels_from_response_body(response_body):
    topics = []
    frames = response_body["results"]["A"]["frames"] if response_body.get("results") and response_body["results"].get(
        "A") else []
    for frame in frames:
        fields = frame["schema"]["fields"] if frame.get("schema") else []
        for field in fields:
            if field.get("labels"):
                topics.append(field["labels"])
    return topics


def get_subject_produced_by_app(app_id):
    expr = "topK(100000,(sum by (subject,appid) (increase(qmq.client.pub.send.count_count{appid=~\"" + app_id + "\"}))))"
    build_param_subject(expr)
    response_body = call_api(base_url, param)
    data = json.loads(response_body)
    labels = find_labels_from_response_body(data)
    produced_subject_list = []
    for label in labels:
        produced_subject_list.append(label["subject"])
    return produced_subject_list


def get_subject_consumed_by_app(app_id):
    expr = "sum by (subject,appid,consumerGroup) (increase(qmq.client.sub.msg.delivery.count_count{appid=~\"" + app_id + "\",consumerGroup!='__masked__11'}))"

    build_param_subject(expr)
    response_body = call_api(base_url, param)
    data = json.loads(response_body)
    labels = find_labels_from_response_body(data)
    consumed_subject_list = []
    for label in labels:
        consumed_subject_list.append(label["subject"])
    return consumed_subject_list


def call_webinfo_api(url, data):
    cookie = 'UBT_VID=1703233274693.db14uNqpJKXW; IFS_FP=B4F79A-B0823D-E519C7; _RF1=112.65.220.253; _RSG=HVqB9uCwZo9r2TJhihFTI8; _RDG=28f3e35d1bfdea2df414e1de0c32aa1e92; _RGUID=9ca3e8ce-092f-47d1-849d-3ebb2b4dd0b5; IFS_R=9ca3e8ce092f47d1849d3ebb2b4dd0b5; PRO_cas_principal=PRO-7869656a756e-MTcwMzIzMzI4OTY1OQ-f55b6820d78b4334bfa8f0f2fba2afd4; PRO_principal=87c6731d64eb83aa79b0966422f393a1-e4441d2c-bf3d-4c0e-84a9-52f6a0265fa0; offlineTicket=_863F211EC07981C4F581817C92FF9B345A25AC456A71895213185BA31235BF66; PRO_CCST_SECRET_ADFC=PRO-7869656a756e-c66ee7845d4b45fa9b1a254d4f3fffe8; Servers_Eid=TR009698; PRO_Servers_Eid=TR009698; principal_webInfo=PRO-7869656a756e-MTcwMzIzMzI4OTY1OQ-f55b6820d78b4334bfa8f0f2fba2afd4; _pk_ses.53.8cb3=*; _bfaStatusPVSend=1; _bfi=p1%3D10650009917%26p2%3D10650009917%26v1%3D2%26v2%3D4; _bfaStatus=success; _pk_id.53.8cb3=2db788fdcff3ed10.1703235036.1.1703235051.1703235036.; _bfa=1.1703233274693.db14uNqpJKXW.1.1703235035821.1703235051142.1.3.10650009917; _ubtstatus=%7B%22vid%22%3A%221703233274693.db14uNqpJKXW%22%2C%22sid%22%3A1%2C%22pvid%22%3A3%2C%22pid%22%3A10650009917%7D'
    headers = {"Cookie": cookie, "Content-Type": "application/json", "Accept": "application/json", "charset": "UTF-8"}
    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    return response.text


# 'app_org_name' = 组织, 'app_owner' = owner , 'app_chinese_name' = name
def call_apid_then_get_appid_info(appid):
    url = "http://webinfo7.ops.ctripcorp.com/api/basicInfo"
    data = {"id": appid, "type": "application"}
    response_body = call_webinfo_api(url, data)
    data = json.loads(response_body)["data"]
    return data[0] if data else {}


def collect_qmq_message(app_id_list):
    all_subject_list = []
    for app_id in app_id_list:
        produced_subject_list = get_subject_produced_by_app(app_id)
        consumed_subject_list = get_subject_consumed_by_app(app_id)
        print(app_id)
        print(produced_subject_list)
        print(consumed_subject_list)
        all_subject_list = all_subject_list + produced_subject_list + consumed_subject_list
    subject = "|".join(all_subject_list)
    query_consumer_expr = 'sum by (subject,consumerGroup,appid) (increase(qmq.client.sub.msg.delivery.count_count{subject=~"(' + subject + ')",consumerGroup!="__masked__11",consumerGroup!="<masked>11",consumerGroup!~\'qmq-mirror-.*\'}))'
    build_param_subject(query_consumer_expr)
    response_body = call_api(base_url, param)
    data = json.loads(response_body)
    labels = find_labels_from_response_body(data)
    file_name = '/Users/xiejun/Documents/报销凭证单元所有QMQ依赖整理.csv'
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["appid", "name", "owner", "组织", "consumerGroup", "subject"])
        for label in labels:
            co_app_id = label["appid"]
            if co_app_id:
                co_app_info = call_apid_then_get_appid_info(co_app_id)
            else:
                print(label)
            write_to_csv(writer, label, co_app_info)


def write_to_csv(writer, label, co_app_info):
    appid = label["appid"]
    name = co_app_info["app_chinese_name"]
    owner = co_app_info["app_owner"]
    org = co_app_info["app_org_name"]
    co_group = label["consumerGroup"]
    subject = label["subject"]
    writer.writerow([appid, name, owner, org, co_group, subject])


app_id_list = ["100015188", "100026327", "100028781", "100011366", "100012233", "100016491", "100016492", "100017236",
               "100010934"]
collect_qmq_message(app_id_list)
