
import time
import datetime
from utils.send import send_group_message

img_url = [
    "http://konghonglee.top/upload/2022/05/8-b80952d590ee43019231e31ceea2644a.png",
    "http://konghonglee.top/upload/2022/05/10-52e96a823afe439e8b6d892a70ad713a.png",
    "http://konghonglee.top/upload/2022/05/9-36d9d9cc943f4417a54495f2715a2a6b.png",
    "http://konghonglee.top/upload/2022/05/11-e0e367b391724976af63e70d40d8bf93.png",
    "http://konghonglee.top/upload/2022/05/3-d578b870db9749a6b573e809deccfab6.png",
    "http://konghonglee.top/upload/2022/05/5-36ee1c125ac54d5d8ad106f92c1c3438.png",
    "http://konghonglee.top/upload/2022/05/4-f02508a603cd4fa0a192658cf34fd41d.png",
    "http://konghonglee.top/upload/2022/05/6-b040990cf9a14531b378a05e9cc1253a.png",
    "http://konghonglee.top/upload/2022/05/0-37b98ee1c1184949a7a4efef4b8c701c.png",
    "http://konghonglee.top/upload/2022/05/2-4aff05a038ab4ea88816a425c088d73e.png",
    "http://konghonglee.top/upload/2022/05/1-b7b2c1504ae94fc6805781fcf96f1abf.png",
    "http://konghonglee.top/upload/2022/05/7-eab81804784747528810f7bbb79a9a23.png"
]


async def what_time_now(websocket):
    h = int(datetime.datetime.now().strftime("%H"))
    t = h - 1
    while True:
        time.sleep(5)
        h = int(datetime.datetime.now().strftime("%H"))
        if h != t:
            t = h
            if h > 12:
                h -= 12
            if h == 0:
                h = 12
            h -= 1
            message_chain = [{"type": "Image", "url": img_url[h]}]
            await send_group_message(websocket, 546296895, message_chain)