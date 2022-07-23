import sqlite3
import datetime

con = sqlite3.connect("user/db/user.db")
cur = con.cursor()


def insert(id, score = 1000, date = ""):
    if date == "":
        date = datetime.datetime.now().strftime("%Y-%m-%d")
    sql = 'insert into user_info values({}, {}, "{}")'.format(id, score, date)
    cur.execute(sql)
    con.commit()

def update_score(ids):
    for [id, score] in ids:
        sql = 'update user_info set score = {} where user_id = {}'.format(score, id)
        cur.execute(sql)
    con.commit()

def update_date(id):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    sql = 'update user_info set sign_date = "{}" where user_id = {}'.format(date, id)
    cur.execute(sql)
    con.commit()

def quary_score(ids):
    ans = []
    for id in ids:
        sql = "select score from user_info where user_id = {}".format(id)
        cur.execute(sql)
        ans.append(cur.fetchall()[0][0])
    return ans

def quary_date(id):
    sql = "select sign_date from user_info where user_id = {}".format(id)
    cur.execute(sql)
    return cur.fetchall()[0][0]

def quary_all():
    sql = "select * from user_info"
    cur.execute(sql)
    return cur.fetchall()[0]

def has_user(id):
    sql = "select * from user_info where user_id = {}".format(id)
    cur.execute(sql)
    return cur.fetchall() != []

def check_sign_day_is_today(id):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    return quary_date(id) == date


if __name__ == "__main__":
    sql = '''
         create table user_info(
             user_id varchar(15) primary key not null,
             score integer not null,
             sign_date date not null
         )
    '''
    cur.execute(sql)
