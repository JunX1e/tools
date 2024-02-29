import csv

import requests
import json

base_url = 'https://bat.fx.ctripcorp.com/api/ds/query'


def call_api(url, data):
    cookie = 'UID=9ca3e8ce-092f-47d1-849d-3ebb2b4dd0b5; _RSG=HVqB9uCwZo9r2TJhihFTI8; _RDG=28f3e35d1bfdea2df414e1de0c32aa1e92; UBT_VID=1695609672067.48jis5; IFS_R=9ca3e8ce092f47d1849d3ebb2b4dd0b5; PRO_CCST_SECRET_ADFC=PRO-7869656a756e-09c04738644c41ac82bede57de1a9abd; Servers_Eid=TR009698; PRO_Servers_Eid=TR009698; fltoffline_order_timeZoneOffset=8; fltoffline_order_part=3a4f6aba22f17e1d3e21f00b8887cb68; bbz_offlineLocale=zh-CN; FAT_cas_principal=FAT-7869656a756e-MTcwNjc5MDg1ODY1Mg-9ac9522b2ce94c5b8531244ea2b38bf7; fltoffline_order_lan=zh-CN; _bfaStatusPVSend=1; nfes_isSupportWebP=1; IFS_FP=58379A-742260-446C75; PRO_cas_principal=PRO-7869656a756e-MTcwODU5MDQyMDI5NQ-fddcf783b4724a0e8b56fcc4fb0a6e4c; offlineTicket=_EB19C57770A664F282426CFD36A6874AA5E0DD504C61323DC0F98656B0CEAC00; Union=OUID=&AllianceID=66672&SID=1693366&SourceID=&AppID=&OpenID=&exmktID=&createtime=1708678691&Expires=1709283490500; _ubtstatus=%7B%22vid%22%3A%221695609672067.48jis5%22%2C%22sid%22%3A260%2C%22pvid%22%3A15%2C%22pid%22%3A0%7D; _bfaStatus=send; workbench_locale=zh-CN; _bfa=1.1695609672067.48jis5.1.1709195956918.1709195968889.262.4.10650105742; _RF1=180.163.115.222; _pk_ref.111.655c=%5B%22%22%2C%22%22%2C1709208148%2C%22http%3A%2F%2Fconf.ctripcorp.com%2F%22%5D; _pk_ses.111.655c=*; grafana_session=63d782fdb843811e602ed28ebfd4292c; _pk_id.111.655c=bbd065c6247c9838.1703233291.101.1709208160.1709208148.'
    headers = {"Cookie": cookie, "Content-Type": "application/json", "Accept": "application/json", "charset": "UTF-8"}
    response = requests.post(url, headers=headers, data=json.dumps(data) ,verify=False)
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
            "from": "2024-02-25T07:57:44.385Z",
            "to": "2024-02-28T07:57:44.385Z",
            "raw": {
                "from": "now-3d",
                "to": "now"
            }
        },
        "from": "1708790400000",
        "to": "1709049600000"
    }





def find_labels_from_response_body(response_body):
    topics = []
    frames = response_body["results"]["A"]["frames"] if response_body.get("results") and response_body["results"].get(
        "A") else []
    if not frames :
        print(frames)
        return topics
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
    cookie = '_RGUID=9ca3e8ce-092f-47d1-849d-3ebb2b4dd0b5; _RSG=HVqB9uCwZo9r2TJhihFTI8; _RDG=28f3e35d1bfdea2df414e1de0c32aa1e92; UBT_VID=1695609672067.48jis5; IFS_R=9ca3e8ce092f47d1849d3ebb2b4dd0b5; PRO_CCST_SECRET_ADFC=PRO-7869656a756e-09c04738644c41ac82bede57de1a9abd; Servers_Eid=TR009698; PRO_Servers_Eid=TR009698; fltoffline_order_timeZoneOffset=8; fltoffline_order_part=3a4f6aba22f17e1d3e21f00b8887cb68; bbz_offlineLocale=zh-CN; FAT_cas_principal=FAT-7869656a756e-MTcwNjc5MDg1ODY1Mg-9ac9522b2ce94c5b8531244ea2b38bf7; fltoffline_order_lan=zh-CN; _bfaStatusPVSend=1; nfes_isSupportWebP=1; IFS_FP=58379A-742260-446C75; PRO_cas_principal=PRO-7869656a756e-MTcwODU5MDQyMDI5NQ-fddcf783b4724a0e8b56fcc4fb0a6e4c; offlineTicket=_EB19C57770A664F282426CFD36A6874AA5E0DD504C61323DC0F98656B0CEAC00; Union=OUID=&AllianceID=66672&SID=1693366&SourceID=&AppID=&OpenID=&exmktID=&createtime=1708678691&Expires=1709283490500; workbench_locale=zh-CN; _RF1=180.163.115.222; principal_webInfo=PRO-7869656a756e-MTcwODU5MDQyMDI5NQ-fddcf783b4724a0e8b56fcc4fb0a6e4c; _pk_ses.53.8cb3=*; _bfi=p1%3D10650009917%26p2%3D10650009917%26v1%3D4%26v2%3D3; _bfaStatus=success; _bfa=1.1695609672067.48jis5.1.1709209427991.1709209451721.263.5.10650009917; _ubtstatus=%7B%22vid%22%3A%221695609672067.48jis5%22%2C%22sid%22%3A263%2C%22pvid%22%3A5%2C%22pid%22%3A10650009917%7D; _pk_id.53.8cb3=3ba2a442ea606002.1709208705.1.1709209452.1709208705.'
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
    labels = []
    for app_id in app_id_list:
        produced_subject_list = get_subject_produced_by_app(app_id)
        consumed_subject_list = get_subject_consumed_by_app(app_id)
        print(app_id)
        print(produced_subject_list)
        print(consumed_subject_list)
        all_subject_list = all_subject_list + produced_subject_list + consumed_subject_list
    for i in range(0, len(all_subject_list), 10):
        subject = "|".join(all_subject_list[i:i + 10])
        query_consumer_expr = 'sum by (subject,consumerGroup,appid) (increase(qmq.client.sub.msg.delivery.count_count{subject=~"(' + subject + ')",consumerGroup!="__masked__11",consumerGroup!="<masked>11",consumerGroup!~\'qmq-mirror-.*\'}))'
        build_param_subject(query_consumer_expr)
        response_body = call_api(base_url, param)
        data = json.loads(response_body)
        labels.extend(find_labels_from_response_body(data))
    file_name = '/Users/xiejun/Documents/QMQ依赖整理.csv'
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


app_id_list = ["100013318"]
collect_qmq_message(app_id_list)
