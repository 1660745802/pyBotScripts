
from utils.get import get_id, get_message_paint, get_at_target
from user.user_info import check_sign_day_is_today, insert, has_user, update_date, quary_score, update_score
from utils.q_send import q_send, q_send_at_message

async def user_commands(websocket, recv_text):
    text = '积分命令:\n"签到", "积分", "送 @N X"'
    await q_send(websocket, recv_text, text)

async def sign(websocket, recv_text):
    id = get_id(recv_text)
    if not has_user(id):
        insert(id)
        await q_send_at_message(websocket, recv_text, "签到成功", True)
    elif check_sign_day_is_today(id):
        await q_send_at_message(websocket, recv_text, "你今天已经签过到了", True)
    else:
        update_date(id)
        update_score([[id, quary_score([id])[0] + 1000]])
        await q_send_at_message(websocket, recv_text, "签到成功", True)


async def get_score(websocket, recv_text):
    id = get_id(recv_text)
    if not has_user(id):
        await q_send_at_message(websocket, recv_text, "当前积分: 0")
    else:
        await q_send_at_message(websocket, recv_text, "当前积分: {}".format(quary_score([id])[0]))

async def give_score(websocket, recv_text):
    id = get_id(recv_text)
    msg = get_message_paint(recv_text)
    try:    
        target = get_at_target(recv_text)[0]
        score = msg[1:].strip()
        score = int(score)
    except:
        return
    if score < 0:
        await q_send_at_message(websocket, recv_text, "爬 ", True)
        return
    if not has_user(id) or score > quary_score([id])[0]:
        await q_send_at_message(websocket, recv_text, "你的积分不够哦", True)
        return
    update_score([[id, quary_score([id])[0] - score]])
    if not has_user(target):
        insert(target, score=0, date="2008-08-08")
    update_score([[target, quary_score([target])[0] + score]])
    await q_send_at_message(websocket, recv_text, "赠送成功")

if __name__ == "__main__":
    pass
