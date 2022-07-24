import re
import datetime
from openpyxl import load_workbook
from random import choice
import requests, json, opencc


url = "https://hmacg.cn/bangumi/xfb-dl.php?dl=202204&type=all&ext=xlsx"

face_code = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 41, 42, 43, 46, 49, 53, 54, 55, 56, 57, 59, 60, 61, 63, 64, 66, 67, 69, 74, 75, 76, 77, 78, 79, 85, 86, 89, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 136, 137, 138, 140, 144, 145, 146, 147, 148, 151, 158, 168, 169, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 187, 188, 190, 192, 193, 194, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 210, 211, 212, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324]

wb = load_workbook(filename="anime/data/bangumitime.xlsx")
sheets = wb.get_sheet_names()
sheet_first = sheets[0]
ws = wb.get_sheet_by_name(sheet_first)

def get_days(message):
    days = []
    if re.search("周一", message):
        days.append("周一")
    if re.search("周二", message):
        days.append("周二")
    if re.search("周三", message):
        days.append("周三")
    if re.search("周四", message):
        days.append("周四")
    if re.search("周五", message):
        days.append("周五")
    if re.search("周六", message):
        days.append("周六")
    if re.search("周日", message):
        days.append("周日")
    if len(days) == 0:
        d = datetime.datetime.now().weekday()
        li = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        days.append(li[d])
    return days

def bangumi_list(message):
    text = ""
    days_list = get_days(message)
    rows = ws.rows
    for row in rows:
        line = [col.value for col in row]
        if line[3] in days_list:
            text += "[mirai:face:{}] ".format(choice(face_code))
            text += line[2] + "\n" + line[3] + " " + str(line[4]).strip() + "\ntags: " + line[13] + "\n\n"
    return text[:-2]

bg_list = [[] for i in range(7)]

def update_bg_list():
    addr = "https://bangumi.online/api/schedule"
    info = requests.post(addr)
    info = json.loads(info.text)["data"]
    for i in range(7):
        for bg in info[i]:
            time = int(bg)
            time += 28800
            for dic in info[i][bg]:
                if dic["title_cn"] == None:
                    continue
                bg_list[i if time < 86400 else (i + 1) % 7].append({
                    "time": time if time < 86400 else time - 86400,
                    "cover": dic["cover"],
                    "title": dic["title_cn"],
                    "vid": dic["vid"]
                })
    for i in range(7):
        bg_list[i] = sorted(bg_list[i], key=lambda item:item["time"])

update_bg_list()
def bangumi_watch(message):
    message = opencc.OpenCC("s2t").convert(message[3:].strip()).lower()
    for i in bg_list:
        for j in i:
            if j["title"].lower().find(message) != -1:
                message_chain = []
                message_chain.append(True)
                message_chain.append({"type": "Image", "url": j["cover"]})
                message_chain.append({"type": "Plain", "text": "https://bangumi.online/watch/" + j["vid"]})
                return message_chain
    return ""


