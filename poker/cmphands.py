


mp_v = {"2 ": 2, "3 ": 3,"4 ": 4, "5 ": 5, "6 ": 6, "7 ": 7, "8 ": 8, "9 ": 9 ,"10": 10, "J ": 11, "Q ": 12, "K ": 13, "A ": 14}
mp_name = ["高牌", "一对", "两对", "三条", "顺子", "同花", "葫芦", "四条", "同花顺", "皇家同花顺"]

def pd_list(li1, li2):
    length = min(len(li1), len(li2))
    for i in range(length):
        if li1[i] > li2[i]:
            return 1
        elif li1[i] < li2[i]:
            return -1
    return 0

def pd_color(combo):
    flag = True
    for i in range(4):
        if combo[i][0] != combo[i + 1][0]:
            flag = False
            break
    return flag

def pd_unmber(combo):
    tmp = []
    for i in combo:
        tmp.append(mp_v[i[1:]])
    return sorted(tmp)

def pd_value(combo):
    col = pd_color(combo)
    combo = pd_unmber(combo)
    if col and combo[0] + 1 == combo[1] and combo[1] + 1 == combo[2] and combo[2] + 1 == combo[3] and combo[3] + 1 == combo[4]:
        if combo[4] == 14:
            return [9]
        else:
            return [8, combo[4]]
    if combo[0] == combo[3]:
        return [7, combo[0], combo[4]]
    if combo[1] == combo[4]:
        return [7, combo[4], combo[0]]
    if combo[0] == combo[2] and combo[3] == combo[4]:
        return [6, combo[0], combo[4]]
    if combo[0] == combo[1] and combo[2] == combo[4]:
        return [6, combo[4], combo[0]]
    if col:
        return [5, combo[4], combo[3], combo[2], combo[1], combo[0]]
    if combo[0] + 1 == combo[1] and combo[1] + 1 == combo[2] and combo[2] + 1 == combo[3] and combo[3] + 1 == combo[4]:
        return [4, combo[4]]
    if combo[0] == combo[2]:
        return [3, combo[0], combo[4], combo[3]]
    if combo[1] == combo[3]:
        return [3, combo[1], combo[4], combo[0]]
    if combo[2] == combo[4]:
        return [3, combo[4], combo[1], combo[0]]
    if combo[0] == combo[1] and combo[2] == combo[3]:
        return [2, combo[2], combo[0], combo[4]]
    if combo[0] == combo[1] and combo[3] == combo[4]:
        return [2, combo[4], combo[0], combo[2]]
    if combo[1] == combo[2] and combo[3] == combo[4]:
        return [2, combo[4], combo[2], combo[0]]
    if combo[0] == combo[1]:
        return [1, combo[0], combo[4], combo[3], combo[2]]
    if combo[1] == combo[2]:
        return [1, combo[1], combo[4], combo[3], combo[0]]
    if combo[2] == combo[3]:
        return [1, combo[3], combo[4], combo[1], combo[0]]
    if combo[3] == combo[4]:
        return [1, combo[4], combo[2], combo[1], combo[0]]
    return [0, combo[4], combo[3], combo[2], combo[1]]
    

def pd_combo(mx, li):
    li1 = pd_value(mx)
    li2 = pd_value(li)
    return pd_list(li1, li2)

def calc_max_combo(all_combo):
    mx = []
    for li in all_combo:
        if mx == [] or pd_combo(mx, li) == -1:
            mx = li
    return mx

def compare(hands):
    all_combo = []
    for i in range(6):
        for j in range(i + 1, 7):
            tmp = []
            for k in range(7):
                if k == i or k == j:
                    continue
                tmp.append(hands[k])
            all_combo.append(tmp)
    return calc_max_combo(all_combo)

def calc_winner_hands(dic, table):
    for player in dic:
        if dic[player] == []:
            continue
        for tmp in table:
            dic[player].append(tmp)
        dic[player] = compare(dic[player])
    winner = []
    for player in dic:
        if dic[player] == []:
            continue
        if winner == [] or pd_combo(dic[player], winner[0][2]) == 0:
            winner.append([player, mp_name[pd_value(dic[player])[0]], dic[player]])
        elif pd_combo(dic[player], winner[0][2]) == 1:
            winner = [[player, mp_name[pd_value(dic[player])[0]], dic[player]]]
    return winner

if __name__ == "__main__":
    # print(compare(["♥2 ", "♥3 ", "♥4 ", "♥5 ", "♥6 ", "♣9 ", "♣10"]))
    combo = ["♥6 ", "♣9 ", "♥A ", "♥5 ", "♣10"]
    # print(pd_value(combo))
    print(calc_winner_hands({"1": ["♥2 ", "♥3 "], "2": ["♥5 ", "♥6 "],}, combo))
