import os
import sys
import numpy as np

class CardTools():
    ranks = [str(n) for n in range(2, 10)] + list('TJQKA')
    suits = list('cdhs')
    
    def __init__(self):
        self._card_to_id = {}
        self._id_to_card = []
        counter = 0
        for rank in self.ranks:
            for suit in self.suits:
                card_str = rank + suit
                self._id_to_card.append(card_str)
                self._card_to_id[card_str] = counter
                counter += 1
        self._hand_to_id = {}
        self._id_to_hand = []
        hand_counter = 0
        for card1 in range(counter):
            for card2 in range(card1 + 1, counter):
                hand_str = (self._id_to_card[card1], self._id_to_card[card2])
                hand_str2 = (self._id_to_card[card2], self._id_to_card[card1])
                self._id_to_hand.append(hand_str)
                self._hand_to_id[hand_str] = hand_counter
                self._hand_to_id[hand_str2] = hand_counter
                hand_counter += 1

    def card_to_id(self, card):
        return self._card_to_id[card]
    
    def id_to_card(self, cid):
        return self._id_to_card[cid]

    def hand_to_id(self, hand):
        return self._hand_to_id[tuple(hand)]
    
    def id_to_hand(self, hid):
        return self._id_to_hand[hid]

    def evaluate(self, hands):
        rank = self.hand_rank[ hands[ : , 0 ] + 54 ]
        for c in range(1, hands.shape[1]):
            rank = self.hand_rank[ hands[ : , c ] + rank + 1 ]
        return rank

card_tools = CardTools()

class Lookup():    
    
    def __init__(self):
        pass 

    def check(self, a, b):
        if b == None or a == None:
            return False
        for x in a:
            if x in b:
                return True
        return False

    def find(self, hand1, hand2, board = None):
        if board == []:
            board = None
        if (self.check(hand1, hand2) or self.check(hand1, board) or self.check(hand2, board)):
            return -1
        if board == None:
            hand_str1 = ''.join(hand1)
            hand_str2 = ''.join(hand2)
            command = "./pokerstove/build/bin/ps-eval " + hand_str1 + " " + hand_str2
            # print(command)
            a = os.popen(command).read().split("\n")
            wp = float(a[0].split(' ')[4]) / 100
        else:
            hand_str1 = ''.join(hand1)
            hand_str2 = ''.join(hand2)
            board_str = ''.join(board)
            command = "./poker_server/eval/ps-eval " + hand_str1 + " " + hand_str2  + " --board " + board_str
            a = os.popen(command).read().split("\n")
            wp = float(a[0].split(' ')[4]) / 100
        return wp

    def make_table(self, hand_id):
        hand1 = card_tools.id_to_hand(hand_id)
        result = np.zeros((1326, ))
        for i in range(10):
            hand2 = card_tools.id_to_hand(i)
            wp = self.find(hand1, hand2)
            result[i] = wp
        name = ''.join(hand1)
        np.save(name + ".npy", result)
    
Lookup().make_table(int(sys.argv[1]))

