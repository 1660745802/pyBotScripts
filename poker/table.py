import random
from poker.cmphands import calc_winner_hands
from user.user_info import update_score

color = ["♥", "♠", "♣", "♦"]
value = ["2 ","3 ","4 ","5 ","6 ","7 ","8 ","9 ","10","J ","Q ","K ","A "]
class Poker_Table:
    
    def __init__(self, group, players):
    
        self.group = group
        self.players = list(players.keys())
        self.player_score = players
        self.player_score_c = dict(zip(self.players, [2] * len(self.players)))
        self.deck = [co + va + "" for co in color for va in value]
        self.data = {"deck_pos": 0, "player_pos": 0, "tmp" : "", "tot_score": 2 * len(self.players), "lst_score": 0, "turns": 0}
        self.hands = {}
        self.table = []

    def next_player(self):
        while True:
            self.data["player_pos"] = self.data["player_pos"] + 1
            if self.data["player_pos"] == len(self.players):
                self.data["player_pos"] = 0
            if self.hands[self.players[self.data["player_pos"]]] != []:
                break
        return "[mirai:at:{}] 到你下注了".format(self.players[self.data["player_pos"]])
    
    def turns_one(self):
        random.shuffle(self.players)
        random.shuffle(self.deck)
        for player in self.players:
            self.hands[player] = [self.deck[self.data["deck_pos"]], self.deck[self.data["deck_pos"] + 1]]
            self.data["deck_pos"] += 2
        self.data["deck_pos"] += 2
        self.data["tmp"] = self.players[0]
        self.data["turns"] = 1
        return self.hands
    
    def turns_two(self):
        self.data["player_pos"] = len(self.players) - 1
        self.data["lst_score"] = 0
        self.data["turns"] = 2
        msg = self.next_player()
        for i in range(self.data["deck_pos"], self.data["deck_pos"] + 3):
            self.table.append(self.deck[i])
        self.data["deck_pos"] += 3
        self.data["tmp"] = self.players[self.data["player_pos"]]
        
        return "第一轮发牌 " + self.table[0] + " " + self.table[1] + " " + self.table[2] + "\n" + msg
    
    def turns_last(self):
        self.data["player_pos"] = len(self.players) - 1
        self.data["lst_score"] = 0
        self.data["turns"] += 1
        msg = self.next_player()
        self.data["deck_pos"] += 1
        self.data["tmp"] = self.players[self.data["player_pos"]]
        self.table.append(self.deck[self.data["deck_pos"]])
        return "本轮发牌 " + self.table[self.data["turns"]] + "\n" + msg
    
    def check_player(self, player, socre = -1):
        if self.hands[player] == []:
            return "[mirai:at:{}] 你已经弃牌了".format(player)
        if player != self.players[self.data["player_pos"]]:
            return "[mirai:at:{}] 还没轮到你呢".format(player)
        return ""

    def check_player_nums(self):
        cnt = 0
        for hand in self.hands:
            if self.hands[hand] != []:
                cnt += 1
        return cnt
        
    def call_score(self, player, score, add = False):

        message = self.check_player(player, score)
        if message != "":
            return message
        if add:
            score += self.data["lst_score"]
        elif score < self.data["lst_score"]:
            return "不可以这样操作哦"

        self.data["tot_score"] += score
        self.player_score_c[player] += score
        nxt_player = self.next_player()
        if self.data["lst_score"] != score:
            self.data["tmp"] = player
        elif nxt_player[10:-7] == str(self.data["tmp"]):
            nxt_player = "over"
        self.data["lst_score"] = score
        if nxt_player != "over":
            nxt_player += "，最低下注: {}".format(score)
        return nxt_player
    
    def fold_card(self, player):
        message = self.check_player(player)
        if message != "":
            return message
        self.hands[player] = []
        
        if self.check_player_nums() == 1:
            return "over"
        return(self.next_player())

    def calc_winner(self):
        if self.check_player_nums() == 1:
            for hand in self.hands:
                if self.hands[hand] != []:
                    return [[hand, "", []]]

        return calc_winner_hands(self.hands, self.table)
    
    def handle_over(self):
        winner_info = self.calc_winner()
        winner = []
        score_change = []
        msg = "游戏结束\n"
        for tmp in winner_info:
            player = tmp[0]
            winner.append(player)
            self.player_score[player] += self.data["tot_score"] // len(winner) - self.player_score_c[player]
            score_change.append([player, self.player_score[player]])
            msg += "[mirai:at:{}] 获胜，牌型：".format(player) + tmp[1] + "\n "
            for ccc in tmp[2]:
                msg += " " + ccc
            msg += "\n  赢得{}积分\n".format(self.data["tot_score"] // len(winner_info) - self.player_score_c[player])
        for player in self.players:
            if player not in winner:
                self.player_score[player] -= self.player_score_c[player]
                score_change.append([player, self.player_score[player]])
                msg += "[mirai:at:{}] 失败，失去{}积分\n".format(player, self.player_score_c[player])
        update_score(score_change)
        return msg[:-1]


if __name__ == "__main__":
    table = Poker_Table(0, ["1", "2", "3"])
    print(table.turns_one())
        
        
