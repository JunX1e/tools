import json

class WebsiteInfo:
    def __init__(self, failOpTip, failOpWebSite, accountName, accountPwd, scene, bookingAccountName, bookingAccountPwd):
        self.failOpTip = failOpTip
        self.failOpWebSite = failOpWebSite
        self.accountName = accountName
        self.accountPwd = accountPwd
        self.scene = scene
        self.bookingAccountName = bookingAccountName
        self.bookingAccountPwd = bookingAccountPwd

class WebsiteInfoEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, WebsiteInfo):
            return obj.__dict__
        return super().default(obj)

def json_test():
    original_website_info = WebsiteInfo("2", "test", "", "", "I", None, None)
    to_update_web_dic = {"websiteInfoList": [original_website_info]}
    to_update_web_dic["websiteInfoList"].append(WebsiteInfo("2", "test2", "", "", "I", None, None))
    serialized_data = json.dumps(to_update_web_dic, cls=WebsiteInfoEncoder)
    print(serialized_data)

# test

def serialize_json(List):
    return json.dumps({"websiteInfoList": [List]} , cls=WebsiteInfoEncoder)



def deserialize_json(json_str):
    # 解析JSON字符串为字典
    data = json.loads(json_str)
    # 提取websiteInfoList列表
    website_info_list = data["websiteInfoList"]
    # 创建WebsiteInfo对象列表
    website_info_objects = []
    for website_info_dict in website_info_list:
        website_info = WebsiteInfo(
            website_info_dict["failOpTip"],
            website_info_dict["failOpWebSite"],
            website_info_dict["accountName"],
            website_info_dict["accountPwd"],
            website_info_dict["scene"],
            website_info_dict["bookingAccountName"],
            website_info_dict["bookingAccountPwd"]
        )
        website_info_objects.append(website_info)

    return website_info_objects



