import codecs
import csv
import requests
import json
import time
from datetime import datetime

# 调用soa API，获取service的appID
def call_api(url, data):
    cookie = '_bfaStatusPVSend=1; _RSG=HsaJsRsr.P0XS6Oy8vP6S9; _RDG=28693e62b3028b27b4077a87252587a906; _RGUID=067ed766-f64e-4d91-9706-67923c606721; PRO_CCST_SECRET_ADFC=PRO-6261695f6c-d7bd1252dd324a419fd3807c670d7325; bbz_offlineLocale=zh-CN; UBT_VID=1686578245451.2zts8t; nfes_isSupportWebP=1; fltoffline_order_timeZoneOffset=8; fltoffline_order_part=3a4f6aba22f17e1d3e21f00b8887cb68; fltoffline_order_lan=zh-CN; workbench_locale=zh-CN; UBT_CID=70006203511263636495; GUID=70006203511263636495; IFS_R=067ed766f64e4d91970667923c606721; FAT_cas_principal=FAT-6261695f6c-MTcwMDY0MzM5MzI3Mw-5b1c91ca64b34123a44b681b4cb2ee25; UAT_cas_principal=UAT-6261695f6c-MTcwMDY0NzU3NTM0Ng-053f7bfb317c48f089825859c0736462; IFS_FP=BAD79A-0BA126-BD5188; Servers_Eid=S64373; PRO_Servers_Eid=S64373; PRO_cas_principal=PRO-6261695f6c-MTcwMzA0Mjk5ODQ5MQ-c506722b385c41d182269d413ff782c2; PRO_principal=bd2e01ce1b5b87dd0df38e50852ef32e-010f4394-188c-4806-b30e-80281e8b5c95; offlineTicket=_50D43F2D96FFA2B0374815183AD7261AB3AF2AECF86C29B4FDCEDDE1E911C339; _ubtstatus=%7B%22vid%22%3A%221686578245451.2zts8t%22%2C%22sid%22%3A204%2C%22pvid%22%3A8%2C%22pid%22%3A10650068765%7D; _bfi=p1%3D10650068765%26p2%3D10650068765%26v1%3D8%26v2%3D2; _bfaStatus=success; _pk_ref.111.655c=%5B%22%22%2C%22%22%2C1703211663%2C%22http%3A%2F%2Fbigeyes.ctripcorp.com%2F%22%5D; _pk_ses.111.655c=*; _bfa=1.1686578245451.2zts8t.1.1703211483029.1703211665541.207.3.10650105740; _RF1=112.65.220.253; _pk_id.111.655c=117f7a4a6bfb02f0.1688476294.169.1703213440.1703211663.; grafana_session=9498c647adf9993350d27ba5d5bdccc1'
    headers = {"Cookie": cookie, "Content-Type": "application/json", "Accept": "application/json", "charset": "UTF-8"}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.text

def call_bat_query_api(param):
    bat_query_url = "https://bat.fx.ctripcorp.com/api/ds/query"
    response_body = call_api(bat_query_url, param)
    data = json.loads(response_body)
    return data

def call_api_get_sended_msg_by_appid(appid):
    expr = "topK(100000,(sum by (subject,appid) (increase(qmq.client.pub.send.count_count{appid=~\"" + appid + "\"}))))"
    param = {
        "queries":[
            {
                "expr":expr,
                "format":"table",
                "instant":True,
                "intervalFactor":1,
                "legendFormat":"{{subject}} {{appid}}",
                "legends":[

                ],
                "refId":"A",
                "datasource":{
                    "uid":"208",
                    "type":"prometheus"
                },
                "queryType":"timeSeriesQuery",
                "exemplar":False,
                "requestId":"5A",
                "utcOffsetSec":28800,
                "interval":"",
                "datasourceId":208,
                "intervalMs":1200000,
                "maxDataPoints":542
            }
        ],
        "range":{
            "from":"2023-12-14T07:57:44.385Z",
            "to":"2023-12-21T07:57:44.385Z",
            "raw":{
                "from":"now-7d",
                "to":"now"
            }
        },
        "from":"1702540664385",
        "to":"1703145464385"
    }
    return call_bat_query_api(param)

def call_api_get_sub_msg_by_appid(appid):
    expr = "sum by (subject,appid,consumerGroup) (increase(qmq.client.sub.msg.delivery.count_count{appid=~\"" + appid + "\",consumerGroup!='__masked__11'}))"
    param = {
        "queries":[
            {
                "expr":expr,
                "format":"table",
                "instant":True,
                "intervalFactor":1,
                "legendFormat":"",
                "legends":[

                ],
                "refId":"A",
                "datasource":{
                    "uid":"208",
                    "type":"prometheus"
                },
                "queryType":"timeSeriesQuery",
                "exemplar":False,
                "requestId":"6A",
                "utcOffsetSec":28800,
                "interval":"",
                "datasourceId":208,
                "intervalMs":1200000,
                "maxDataPoints":542
            }
        ],
        "range":{
            "from":"2023-12-14T07:57:44.385Z",
            "to":"2023-12-21T07:57:44.385Z",
            "raw":{
                "from":"now-7d",
                "to":"now"
            }
        },
        "from":"1702540664385",
        "to":"1703145464385"
    }
    return call_bat_query_api(param)

def call_api_get_msg_delivery_by_message(expr):
    param = {
        "queries":[
            {
                "expr":expr,
                "format":"table",
                "instant":True,
                "intervalFactor":1,
                "legendFormat":"",
                "legends":[

                ],
                "refId":"A",
                "datasource":{
                    "uid":"208",
                    "type":"prometheus"
                },
                "queryType":"timeSeriesQuery",
                "exemplar":False,
                "requestId":"11A",
                "utcOffsetSec":28800,
                "interval":"",
                "datasourceId":208,
                "intervalMs":1200000,
                "maxDataPoints":542
            }
        ],
        "range":{
            "from":"2023-12-14T07:57:44.385Z",
            "to":"2023-12-21T07:57:44.385Z",
            "raw":{
                "from":"now-7d",
                "to":"now"
            }
        },
        "from":"1702540664385",
        "to":"1703145464385"
    }
    return call_bat_query_api(param)

def find_labels_from_response_body(response_body):
    topics = []
    frames = response_body["results"]["A"]["frames"] if response_body.get("results") and response_body["results"].get("A") else []
    for frame in frames:
        fields = frame["schema"]["fields"] if frame.get("schema") else []
        for field in fields:
            if field.get("labels"):
                topics.append(field["labels"])
    return topics

def call_webinfo_api_return_appid_info(appid):
    url = "http://webinfo7.ops.ctripcorp.com/api/basicInfo"
    data = {"id": appid, "type": "application"}
    cookie = "_bfaStatusPVSend=1; _RSG=HsaJsRsr.P0XS6Oy8vP6S9; _RDG=28693e62b3028b27b4077a87252587a906; _RGUID=067ed766-f64e-4d91-9706-67923c606721; PRO_CCST_SECRET_ADFC=PRO-6261695f6c-d7bd1252dd324a419fd3807c670d7325; Servers_Eid=S64373; PRO_Servers_Eid=S64373; bbz_offlineLocale=zh-CN; UBT_VID=1686578245451.2zts8t; nfes_isSupportWebP=1; fltoffline_order_timeZoneOffset=8; fltoffline_order_part=3a4f6aba22f17e1d3e21f00b8887cb68; fltoffline_order_lan=zh-CN; workbench_locale=zh-CN; UBT_CID=70006203511263636495; GUID=70006203511263636495; IFS_FP=1vyrs65-oqbre-2u4m5o; IFS_R=067ed766f64e4d91970667923c606721; FAT_cas_principal=FAT-6261695f6c-MTcwMDY0MzM5MzI3Mw-5b1c91ca64b34123a44b681b4cb2ee25; UAT_cas_principal=UAT-6261695f6c-MTcwMDY0NzU3NTM0Ng-053f7bfb317c48f089825859c0736462; PRO_cas_principal=PRO-6261695f6c-MTcwMTQxNjI4NDU3NA-ec30462686a844268fd104a330c497bf; PRO_principal=bd2e01ce1b5b87dd0df38e50852ef32e-ee628e23-aab7-4569-8fe1-e876d69795bb; offlineTicket=_5CAAEC5F5E87531D055B7EF037396D0F047C24A811CBF68A5A4F9B1716522FB3; principal_webInfo=PRO-6261695f6c-MTcwMTQxNjI4NDU3NA-ec30462686a844268fd104a330c497bf; Union=OUID=&AllianceID=66672&SID=1693366&SourceID=&AppID=&OpenID=&exmktID=&createtime=1702288922&Expires=1702893722153; _RF1=112.65.220.248; _pk_ses.53.8cb3=*; _bfa=1.1686578245451.2zts8t.1.1702371317339.1702371352466.183.2.10650009917; _ubtstatus=%7B%22vid%22%3A%221686578245451.2zts8t%22%2C%22sid%22%3A183%2C%22pvid%22%3A2%2C%22pid%22%3A10650009917%7D; _pk_id.53.8cb3=3a41c247f59039bc.1701421495.5.1702371352.1702371317.; _bfi=p1%3D10650009917%26p2%3D10650009917%26v1%3D2%26v2%3D1; _bfaStatus=success"
    headers = {"Cookie": cookie, "Content-Type": "application/json", "Accept": "application/json", "charset": "UTF-8"}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    data = json.loads(response.text)["data"]
    return data[0] if data else {}

def write_to_csv(type, labels, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["appid", "name", "owner", "组织", "consumerGroup", "subject", "确认是否可以开启SHA-SIN双向同步", "单元生产", "单元消费", "备注"])
        for label in labels:
            appid = label["appid"] if label.get("appid") else ""
            # get appid info from webinfo api
            appid_info = call_webinfo_api_return_appid_info(appid)
            name = appid_info["app_chinese_name"]
            owner = appid_info["app_owner"]
            org = appid_info["app_org_name"]
            # get consumerGroup and subject from label
            consumerGroup = label["consumerGroup"] if label.get("consumerGroup") else ""
            subject = label["subject"] if label.get("subject") else ""
            # get is_produce and is_consume from type
            is_produce = (type == "pub" and "生产" or "")
            is_consume = (type == "sub" and "消费" or "")
            # write to csv
            writer.writerow([appid, name, owner, org, consumerGroup, subject, "", is_produce, is_consume, ""])

def collect_infos_to_csv_100011366():
    appid = "100011366"
    # 获取当前appid下所有生产的subject
    pub_response_body = call_api_get_sended_msg_by_appid(appid)
    pub_lables = find_labels_from_response_body(pub_response_body)
    write_to_csv("pub", pub_lables, "/Users/bellynn/ctripcode/personnal/" + appid + "生产的Q.csv")
    # 获取当前appid下所有消费的subject、consumerGroup
    sub_response_body = call_api_get_sub_msg_by_appid(appid)
    sub_lables = find_labels_from_response_body(sub_response_body)
    write_to_csv("sub", sub_lables, "/Users/bellynn/ctripcode/personnal/" + appid + "消费的Q.csv")
    # 获取当前appid下所生产Q的消费组列表
    pub_expr = "sum by (subject,consumerGroup,appid) (increase(qmq.client.sub.msg.delivery.count_count{subject=~\"(flight\\\\.ctrip\\\\.flight\\\\.reimbursement\\\\.tryredeinvoice|flight\\\\.reimbursement\\\\.xproductcalculate|flight\\\\.reimbursement\\\\.xrebook\\\\.success|flight\\\\.reimbursement\\\\.orderedmessage|flight\\\\.reimbursement\\\\.xrebook\\\\.failed)\",consumerGroup!=\"__masked__11\",consumerGroup!=\"<masked>11\",consumerGroup!~'qmq-mirror-.*'}))"
    msg_delivery_response_body = call_api_get_msg_delivery_by_message(pub_expr)
    msg_delivery_labels = find_labels_from_response_body(msg_delivery_response_body)
    write_to_csv("sub", msg_delivery_labels, "/Users/bellynn/ctripcode/personnal/" + appid + "生产Q的消费组列表.csv")
    # 获取当前appid下所消费Q的消费组列表
    sub_expr = "sum by (subject,consumerGroup,appid) (increase(qmq.client.sub.msg.delivery.count_count{subject=~\"(ctrip\\\\.flight\\\\.integrationservice\\\\.mnotify\\\\.change\\\\.submitted|ctrip\\\\.flight\\\\.integrationservice\\\\.mnotify\\\\.change\\\\.changed|ctrip\\\\.flight\\\\.integrationservice\\\\.mnotify\\\\.xorder\\\\.submitted|flight\\\\.xreschedule\\\\.status|ctrip\\\\.flight\\\\.integrationservice\\\\.mnotify\\\\.change\\\\.paid|ctrip\\\\.flight\\\\.integrationservice\\\\.mnotify\\\\.change\\\\.failed|flight\\\\.onex\\\\.postprocessing\\\\.postprocess\\\\.discountfirstactivity\\\\.activitystatus\\\\.changed|flight\\\\.xproduct\\\\.postprocess\\\\.usedstatus\\\\.change|ctrip\\\\.flight\\\\.integrationservice\\\\.payment\\\\.changpaymentway|ctrip\\\\.flight\\\\.xRefund\\\\.statuschange|flight\\\\.reimbursement\\\\.datachange\\\\.config|ctrip\\\\.flight\\\\.ticket\\\\.issue\\\\.ticketNoPrice|ctrip\\\\.flight\\\\.integrationservice\\\\.mnotify\\\\.xproduct\\\\.issuefailed|flight\\\\.onex\\\\.postprocessing\\\\.postprocess\\\\.hotelcrossdiscount\\\\.activitystatus\\\\.changed|ctrip\\\\.flight\\\\.reschedule\\\\.payment\\\\.refunded|ctrip\\\\.flight\\\\.integrationservice\\\\.mnotify\\\\.refund\\\\.moneyrefunded|ctrip\\\\.flight\\\\.integrationservice\\\\.mnotify\\\\.xorder\\\\.canceled|ctrip\\\\.flight\\\\.integrationservice\\\\.mnotify\\\\.change\\\\.cancelled|ctrip\\\\.flight\\\\.integrationservice\\\\.mnotify\\\\.order\\\\.cancelled|ctrip\\\\.flight\\\\.integrationservice\\\\.mnotify\\\\.refund\\\\.submitted|ctrip\\\\.flight\\\\.integrationservice\\\\.mnotify\\\\.order\\\\.paid|ctrip\\\\.flight\\\\.integrationservice\\\\.mnotify\\\\.xproduct\\\\.issued|flight\\\\.reimbursement\\\\.orderedmessage|ctrip\\\\.flight\\\\.integrationservice\\\\.mnotify\\\\.refund\\\\.cancelled|ctrip\\\\.flight\\\\.ticket\\\\.issue\\\\.orderstatus8)\",consumerGroup!=\"__masked__11\",consumerGroup!=\"<masked>11\",consumerGroup!~'qmq-mirror-.*'}))"
    msg_delivery_response_body = call_api_get_msg_delivery_by_message(pub_expr)
    msg_delivery_labels = find_labels_from_response_body(msg_delivery_response_body)
    write_to_csv("sub", msg_delivery_labels, "/Users/bellynn/ctripcode/personnal/" + appid + "所消费Q的消费组列表.csv")

def collect_infos_to_csv_100017236():
    appid = "100017236"
    # 获取当前appid下所有生产的subject
    pub_response_body = call_api_get_sended_msg_by_appid(appid)
    pub_lables = find_labels_from_response_body(pub_response_body)
    write_to_csv("pub", pub_lables, "/Users/bellynn/ctripcode/personnal/" + appid + "生产的Q.csv")
    # 获取当前appid下所有消费的subject、consumerGroup
    sub_response_body = call_api_get_sub_msg_by_appid(appid)
    sub_lables = find_labels_from_response_body(sub_response_body)
    write_to_csv("sub", sub_lables, "/Users/bellynn/ctripcode/personnal/" + appid + "消费的Q.csv")
    # 获取当前appid下所生产Q的消费组列表
    pub_expr = "sum by (subject,consumerGroup,appid) (increase(qmq.client.sub.msg.delivery.count_count{subject=~\"(flight\\\\.reimbursement\\\\.addfullskill|flt\\\\.reimbursement\\\\.einvoiceapply|flight\\\\.ctrip\\\\.flight\\\\.reimbursement\\\\.tryredeinvoice|flight\\\\.reimbursement\\\\.invoice\\\\.numberchange|flight\\\\.reimbursement\\\\.sendreimbursementemail|flight\\\\.reimbursement\\\\.packageresult|flight\\\\.reimbursement\\\\.nodeliverystatus)\",consumerGroup!=\"__masked__11\",consumerGroup!=\"<masked>11\",consumerGroup!~'qmq-mirror-.*'}))"
    msg_delivery_response_body = call_api_get_msg_delivery_by_message(pub_expr)
    msg_delivery_labels = find_labels_from_response_body(msg_delivery_response_body)
    write_to_csv("sub", msg_delivery_labels, "/Users/bellynn/ctripcode/personnal/" + appid + "生产Q的消费组列表.csv")
    # 获取当前appid下所消费Q的消费组列表
    sub_expr = "sum by (subject,consumerGroup,appid) (increase(qmq.client.sub.msg.delivery.count_count{subject=~\"()\",consumerGroup!=\"__masked__11\",consumerGroup!=\"<masked>11\",consumerGroup!~'qmq-mirror-.*'}))"
    msg_delivery_response_body = call_api_get_msg_delivery_by_message(pub_expr)
    msg_delivery_labels = find_labels_from_response_body(msg_delivery_response_body)
    write_to_csv("sub", msg_delivery_labels, "/Users/bellynn/ctripcode/personnal/" + appid + "所消费Q的消费组列表.csv")


def collect_infos_to_csv_100015188():
    appid = "100015188"
    # 获取当前appid下所有生产的subject
    pub_response_body = call_api_get_sended_msg_by_appid(appid)
    pub_lables = find_labels_from_response_body(pub_response_body)
    write_to_csv("pub", pub_lables, "/Users/bellynn/ctripcode/personnal/" + appid + "生产的Q.csv")
    # 获取当前appid下所有消费的subject、consumerGroup
    sub_response_body = call_api_get_sub_msg_by_appid(appid)
    sub_lables = find_labels_from_response_body(sub_response_body)
    write_to_csv("sub", sub_lables, "/Users/bellynn/ctripcode/personnal/" + appid + "消费的Q.csv")
    # 获取当前appid下所生产Q的消费组列表
    pub_expr = "sum by (subject,consumerGroup,appid) (increase(qmq.client.sub.msg.delivery.count_count{subject=~\"(flight\\\\.reimbursement\\\\.nodeliverystatus|flight\\\\.reimbursement\\\\.packagecalculate|flt\\\\.reimbursement\\\\.einvoiceapply|flight\\\\.reimbursement\\\\.packageresult|flight\\\\.reimbursement\\\\.calculation\\\\.printtime|flight\\\\.reimbursement\\\\.packageprovide|flight\\\\.reimbursement\\\\.checkthenrefundsendticketfee|flight\\\\.reimbursement\\\\.calculate\\\\.deliverytimerange|flight\\\\.ctrip\\\\.flight\\\\.reimbursement\\\\.tryredeinvoice|flight\\\\.ctrip\\\\.flight\\\\.reimbursement\\\\.refundsendticketfeesuccessfully|flt\\\\.reimbursement\\\\.batchcreatepackage|flight\\\\.reimbursement\\\\.redinvoice|flight\\\\.reimbursement\\\\.digitalinvoiceredissue)\",consumerGroup!=\"__masked__11\",consumerGroup!=\"<masked>11\",consumerGroup!~'qmq-mirror-.*'}))"
    msg_delivery_response_body = call_api_get_msg_delivery_by_message(pub_expr)
    msg_delivery_labels = find_labels_from_response_body(msg_delivery_response_body)
    write_to_csv("sub", msg_delivery_labels, "/Users/bellynn/ctripcode/personnal/" + appid + "生产Q的消费组列表.csv")
    # 获取当前appid下所消费Q的消费组列表
    sub_expr = "sum by (subject,consumerGroup,appid) (increase(qmq.client.sub.msg.delivery.count_count{subject=~\"(flight\\\\.reimbursement\\\\.package\\\\.distribute|flight\\\\.reimbursement\\\\.redinvoice|flt\\\\.reimbursement\\\\.batchcreatepackage|flight\\\\.reimbursement\\\\.packageupdate|bbz\\\\.delivery\\\\.traces|flight\\\\.reimbursement\\\\.replaceexpresscompany|flight\\\\.ctrip\\\\.flight\\\\.reimbursement\\\\.tryredeinvoice|flight\\\\.reimbursement\\\\.digitalinvoiceredissue)\",consumerGroup!=\"__masked__11\",consumerGroup!=\"<masked>11\",consumerGroup!~'qmq-mirror-.*'}))"
    msg_delivery_response_body = call_api_get_msg_delivery_by_message(pub_expr)
    msg_delivery_labels = find_labels_from_response_body(msg_delivery_response_body)
    write_to_csv("sub", msg_delivery_labels, "/Users/bellynn/ctripcode/personnal/" + appid + "所消费Q的消费组列表.csv")

def main():
    # collect_infos_to_csv_100011366()
    # collect_infos_to_csv_100017236()
    # collect_infos_to_csv_100015188()
    print("暂不执行")

# 使用示例
main()