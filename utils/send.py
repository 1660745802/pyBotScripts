import json

async def send_friend_message(websocket, target, messageChain):
    msg = {
        "syncId": "",
        "command": "sendFriendMessage",
        "subCommand": "",
        "content": {
            "target": target,
            "messageChain": messageChain
        }
    }
    await websocket.send(json.dumps(msg))

async def send_group_message(websocket, target, messageChain):
    msg = {
        "syncId": "",
        "command": "sendGroupMessage",
        "subCommand": "",
        "content": {
            "target": target,
            "messageChain": messageChain
        }
    }
    await websocket.send(json.dumps(msg))

async def send_temp_message(websocket, target, messageChain):
    msg = {
        "syncId": "",
        "command": "sendTempMessage",
        "subCommand": "",
        "content": {
            "qq":target[0],
            "group":target[1],
            "messageChain": messageChain
        }
    }
    await websocket.send(json.dumps(msg))

async def send_stamp(websocket, target, subject):
    msg = {
        "syncId": "",
        "command": "sendNudge",
        "subCommand": "",
        "content": {
            "target": target,
            "subject": subject,
            "kind":"Group"
        }
    }
    await websocket.send(json.dumps(msg))

