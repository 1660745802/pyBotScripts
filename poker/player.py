from curses.ascii import isdigit
from email import message
from hashlib import new
from re import T
from tokenize import group
from poker.table import Poker_Table
from utils.get import get_id, get_group_id
from utils.q_send import q_send, q_send_at_message
from utils.send import send_temp_message, send_group_message
from utils.get import get_message_paint
from user.user_info import quary_score, has_user
from random import choice

table_info = {}
player_info = {}


async def show_commands(websocket, recv_text):
    text = '德州扑克 命令集:\n"牌局", "上桌", "下桌", "开始"\n"下 X", "加 X", "跟", "过", "弃牌"'
    await q_send(websocket, recv_text, text)


async def show_table_info(websocket, recv_text):
    group_id = get_group_id(recv_text)
    message = ""
    if group_id not in player_info.keys() or table_info[group_id] == "":
        message += "游戏尚未开始，"
    else:
        message += "游戏进行中，"
    if group_id in player_info.keys():
        
        if table_info[group_id] != "":
            message += "底池: {} 分\n".format(table_info[group_id].data["tot_score"])
            message += "牌面: "
            for card in table_info[group_id].table:
                message += card + " "
            message += "\n"
            for player in player_info[group_id]:
                if table_info[group_id].hands[player] == []:
                    message += "[mirai:at:{}] 已弃牌\n".format(player)
                else:
                    message += "[mirai:at:{}] 已下注 {} 分\n".format(player, table_info[group_id].player_score_c[player])
        else:
            message += "当前玩家:\n"
            for player in player_info[group_id]:
                message += "[mirai:at:{}]\n".format(player)
    await q_send(websocket, recv_text, message[:-1])


async def enter_table(websocket, recv_text):
    id = get_id(recv_text)
    group_id = get_group_id(recv_text)
    
    if group_id not in player_info.keys():
        player_info[group_id] = []
        table_info[group_id] = ""
        
    if table_info[group_id] != "":
        await q_send_at_message(websocket, recv_text, "游戏还在进行中")
    elif not has_user(id) or quary_score([id])[0] < 2:
        await q_send_at_message(websocket, recv_text, "你的积分不够哦")
    elif id in player_info[group_id]:
        li = ["你已经在桌上了"]
        await q_send_at_message(websocket, recv_text, choice(li), True)
    else:
        player_info[group_id].append(id)
        li = ["ok", "上桌成功"]
        await q_send_at_message(websocket, recv_text, choice(li), True)


async def leave_table(websocket, recv_text):
    id = get_id(recv_text)
    group_id = get_group_id(recv_text)
    if group_id in player_info.keys() and id in player_info[group_id]:
        if table_info[group_id] != "":
            await q_send_at_message(websocket, recv_text, "游戏还在进行中")
        else:
            player_info[group_id].remove(id)
            li = ["玩不起就别玩", "下桌成功"]
            await q_send_at_message(websocket, recv_text, choice(li), True)
    else:
        li = ["你TM来都没来", "你还没上桌呢"]
        await q_send_at_message(websocket, recv_text, choice(li), True)


async def start(websocket, recv_text):
    id = get_id(recv_text)
    group_id = get_group_id(recv_text)
    if group_id in player_info.keys() and table_info[group_id] != "":
        await q_send_at_message(websocket, recv_text, "游戏正在进行中")
    elif group_id not in player_info.keys() or id not in player_info[group_id]:
        li = ["你TM来都没来", "你先上桌再说"]
        await q_send_at_message(websocket, recv_text, choice(li), True)
    elif len(player_info[group_id]) < 2:
        li = ["人太少了", "人不够啊", "再叫点人"]
        await q_send_at_message(websocket, recv_text, choice(li), True)
    elif len(player_info[group_id]) > 10:
        await q_send_at_message(websocket, recv_text, "人太多, 超出限制了", True)
    else:
        table_info[group_id] = Poker_Table(group_id, dict(zip(player_info[group_id], quary_score(player_info[group_id]))))
        await q_send(websocket, recv_text, "游戏开始，底分: 2")
        hands = table_info[group_id].turns_one()
        for player in hands:
            await send_temp_message(websocket, [player, group_id], [{"type": "MiraiCode", "code": hands[player][0] + " " + hands[player][1]}])
        await send_group_message(websocket, group_id, [{"type": "MiraiCode", "code": "[mirai:at:{}] 到你下注了".format(table_info[group_id].players[0])}])

def check_over(group_id):
    if table_info[group_id].check_player_nums() == 1 or table_info[group_id].data["turns"] == 4:
        msg = game_over(group_id)
    elif table_info[group_id].data["turns"] == 1:
        msg = table_info[group_id].turns_two()
    elif table_info[group_id].data["turns"] in [2, 3]:
        msg = table_info[group_id].turns_last()
    return msg

async def call_score(websocket, recv_text):
    id = get_id(recv_text)
    group_id = get_group_id(recv_text)
    message = get_message_paint(recv_text)
    if (message[0] == "下" or message[0] == "加") and (group_id not in table_info.keys() or table_info[group_id] == ""):
        return
    elif group_id not in player_info.keys() or table_info[group_id] == "":
        await q_send_at_message(websocket, recv_text, "游戏还没开始")
        return
    elif group_id not in player_info.keys() or id not in player_info[group_id]:
        return
    try:
        if message[0] == "下":
            msg = table_info[group_id].call_score(id, int(message[1:].strip()))
        elif message[0] == "跟":
            msg = table_info[group_id].call_score(id, 0, True)
        elif message[0] == "加":
            msg = table_info[group_id].call_score(id, int(message[1:].strip()), True)
        elif message[0] == "过":
            msg = table_info[group_id].call_score(id, 0)
    
        if msg == "over":
            msg = check_over(group_id)
    
        await q_send(websocket, recv_text, msg)
    except:
        return

async def fold_card(websocket, recv_text):
    id = get_id(recv_text)
    group_id = get_group_id(recv_text)
    if group_id not in player_info.keys() or table_info[group_id] == "":
        await q_send_at_message(websocket, recv_text, "游戏还没开始")
        return
    elif group_id not in player_info.keys() or id not in player_info[group_id]:
        return
    
    msg = table_info[group_id].fold_card(id)
    if msg == "over":
        msg = check_over(group_id)
    
    await q_send(websocket, recv_text, msg)

def game_over(group_id):
    msg = table_info[group_id].handle_over()
    table_info[group_id] = ""
    player_info[group_id] = []
    return msg
