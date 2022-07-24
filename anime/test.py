import requests
import json
import opencc


bangumi = [[] for i in range(7)]

addr = "https://bangumi.online/api/schedule"
info = requests.post(addr)
info = json.loads(info.text)["data"]
for i in range(7):
    for bg in info[i]:
        time = int(bg)
        time += 28800
        for dic in info[i][bg]:
            bangumi_list[i if time < 86400 else (i + 1) % 7].append({
                "time": time if time < 86400 else time - 86400,
                "cover": dic["cover"],
                "title": dic["title_cn"],
                "vid": dic["vid"]
            })
for i in range(7):
    bangumi_list[i] = sorted(bangumi_list[i], key=lambda item:item["time"])

