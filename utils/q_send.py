
from email import message
from utils.get import *
from utils.send import *
from random import choice
face_code = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 41, 42, 43, 46, 49, 53, 54, 55, 56, 57, 59, 60, 61, 63, 64, 66, 67, 69, 74, 75, 76, 77, 78, 79, 85, 86, 89, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 136, 137, 138, 140, 144, 145, 146, 147, 148, 151, 158, 168, 169, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 187, 188, 190, 192, 193, 194, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 210, 211, 212, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324]

async def q_send(websocket, recv_text, text):
    target = ""
    message_chain = []
    message_type = get_message_type(recv_text)
    if isinstance(text, list):
        if text[0] and message_type == "GroupMessage":
            message_chain.append({"type": "At", "target": get_id(recv_text)})
        for obj in text[1:]:
            message_chain.append(obj)
    else:
        message_chain = [{"type": "MiraiCode", "code": text}]

    if message_type == "GroupMessage":
        target = get_group_id(recv_text)
        await send_group_message(websocket, target, message_chain)
    elif message_type == "FriendMessage":
        target = get_id(recv_text)
        await send_friend_message(websocket, target, message_chain)
    elif message_type == "TempMessage":
        target = [get_id(recv_text), get_group_id(recv_text)]
        await send_temp_message(websocket, target, message_chain)
    
async def q_send_at_message(websocket, recv_text, text, b = False):
    message_chain = []
    message_chain.append({"type": "At", "target": get_id(recv_text)})
    message_chain.append({"type": "MiraiCode", "code": " " + text})
    if b:
        message_chain.append({"type": "MiraiCode", "code": "[mirai:face:{}] ".format(choice(face_code))})
    await send_group_message(websocket, get_group_id(recv_text), message_chain)
