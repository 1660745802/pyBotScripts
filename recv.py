from poker.player import *
from utils.q_send import *
from utils.send import *
from utils.get import *
from user.user_op import *
from nokia.nokia import gen_img
import anime.bangumi as bangumi
from anime.lolicon import setu, moyu

q_talk = { # 不可带参数 ==
    "摸鱼": moyu,
    "氵": moyu,
}
q_command = { # 可带参数 .startswith 函数默认参数 message
    "来点涩图": setu,
    "新番": bangumi.bangumi_list,
    "我要看": bangumi.bangumi_watch,
    "无内鬼": gen_img,
    "有内鬼": gen_img,
}


async def recv(websocket, recv_text):

    print(recv_text)
    message = get_message_paint(recv_text)
    at_target = get_at_target(recv_text)

    # if 192616427 in at_target:
    #     await recv_at(websocket, recv_text, message)

    # else:
    #     # 戳一戳
    #     for target in at_target:
    #         await send_stamp(websocket, target, get_group_id(recv_text))

    if message == "bot":
        # text = 'bot 命令集:\n"积分命令", "德扑"\n"摸鱼/氵", "来点涩图", "新番", "有内鬼/无内鬼"'
        text = "bot 命令集:\n"
        for i in q_talk:
            text += i + "，"
        text = text[:-1] + "\n"
        for i in q_command:
            text += i + "，"
        await q_send(websocket, recv_text, text[:-1])
        return

    # q_talk
    for key in q_talk:
        if message == key:
            await q_send(websocket, recv_text, q_talk[key]())
            return
    # q_command
    for key in q_command:
        if message.startswith(key):
            await q_send(websocket, recv_text, q_command[key](message))
            return

    score_command1 = {
        #"积分命令": user_commands,
        #"积分": get_score,
        #"签到": sign,
    }
    for key in score_command1:
        if message == key:
            await score_command1[key](websocket, recv_text)
            return
    score_command2 = {
        "送": give_score,
    }
    for key in score_command2:
        if message.startswith(key):
            await score_command2[key](websocket, recv_text)
            return

    poker_command1 = {
        #"德扑": show_commands,
        #"牌局": show_table_info,
        # "上桌": enter_table,
        #"下桌": leave_table,
        #"开始": start,
        #"跟": call_score,
        #"过": call_score,
        #"弃牌": fold_card,
    }      
    poker_command2 = {
        #"下": call_score,
        #"加": call_score,
    }
    if get_message_type(recv_text) == "GroupMessage":
        for key in poker_command1:
            if message == key:
                await poker_command1[key](websocket, recv_text)
                return

        for key in poker_command2:
            if message.startswith(key):
                await poker_command2[key](websocket, recv_text)
                return



# async def recv_at(websocket, recv_text, message):
#     await send_stamp(websocket, get_id(recv_text), get_group_id(recv_text))
