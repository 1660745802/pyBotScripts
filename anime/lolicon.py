import requests
import json

def setu(message):
    message = message[4:].strip()
    try:
        r = requests.get("https://api.lolicon.app/setu/v2?tag={}".format(message)).text
        r = json.loads(r)
        r = r["data"][0]["urls"]["original"].replace("https://i.pixiv.cat/", "https://api.pixiv.moe/image/i.pximg.net/")
        message_chain = [False, {"type": "Image", "url": r}]
    except:
        return [True, {"type": "Plain", "text": " 搜不到哦！"}]
    else:
        return message_chain


def moyu():
    r = requests.get("https://api.vvhan.com/api/moyu?type=json").text
    r = json.loads(r)
    r = r["url"]
    message_chain = [False, {"type": "Image", "url": r}]
    return message_chain

if __name__ == "__main__":
    moyu()
