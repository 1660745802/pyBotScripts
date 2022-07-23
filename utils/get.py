
def get_id(recv_text):
    return recv_text["data"]["sender"]["id"]


def get_group_id(recv_text):
    if get_message_type(recv_text) != "GroupMessage" and get_message_type(recv_text) != "TempMessage":
        return ""
    return recv_text["data"]["sender"]["group"]["id"]


def get_message_paint(recv_text):
    message = ""
    if "messageChain" in recv_text["data"].keys():
        for msg in recv_text["data"]["messageChain"]:
            if msg["type"] == "Plain":
                message = message + msg["text"]
    return message.strip()


def get_message_type(recv_text):
    return recv_text["data"]["type"]


def get_at_target(recv_text):
    target = []
    if "messageChain" in recv_text["data"].keys():
        for msg in recv_text["data"]["messageChain"]:
            if msg["type"] == "At":
                target.append(msg["target"])
    return target
