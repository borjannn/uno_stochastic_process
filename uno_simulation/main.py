import time
from statistics import *
from random import shuffle, randint
from concurrent.futures import ProcessPoolExecutor
from functools import partial


class Card:
    def __init__(self, num, suit):
        self.num = num
        self.suit = suit

    def __str__(self):
        return f'{self.num}:{self.suit}'


class Player:
    def __init__(self, starting_hand):
        self.hand = starting_hand

    def draw_cards(self, deck, n):
        self.hand += deck[:min(n, len(deck))]
        return deck[n:]

    def __str__(self):
        return f'{self.hand}'


class Game:
    def __init__(self, num_players, num_cards, num_colours, num_starting_cards, reverse, skip, draw2, draw4):
        self.reverse = reverse
        self.skip = skip
        self.draw2 = draw2
        self.draw4 = draw4
        self.num_starting_cards = num_starting_cards
        self.next_draw = 0
        self.order = 1
        self.turns = 0
        self.deck = []
        self.thrown_deck = []
        for num in range(num_cards):
            for suit in range(num_colours):
                self.deck.append(Card(num, suit))
        shuffle(self.deck)
        self.players = []
        self.num_players = num_players
        self.num_cards = num_cards
        self.num_colours = num_colours
        for i in range(num_players):
            starting_hand = self.deck[:self.num_starting_cards]
            self.deck = self.deck[self.num_starting_cards:]
            self.players.append(Player(starting_hand))
        self.last_card = self.deck.pop(0)

    def partial_shuffle(self, quality='high'):
        if quality == 'high':
            shuffle(self.deck)
        elif quality == 'medium':
            for _ in range(20):  # Fewer swaps
                i, j = randint(0, len(self.deck) - 1), randint(0, len(self.deck) - 1)
                self.deck[i], self.deck[j] = self.deck[j], self.deck[i]
        elif quality == 'low':
            for _ in range(5):  # Minimal randomization
                i, j = randint(0, len(self.deck) - 1), randint(0, len(self.deck) - 1)
                self.deck[i], self.deck[j] = self.deck[j], self.deck[i]
        elif quality == 'none':
            pass

    def next_person_draw_n(self, player):
        for k in range(self.next_draw):
            self.deck = player.draw_cards(self.deck, 1)
            if len(self.deck) == 0:
                self.deck = self.thrown_deck[:]
                shuffle(self.deck)
                self.thrown_deck = []

    def play(self):
        i = 0

        while True:
            self.turns += 1
            player = self.players[i]
            # print("player", i, "turn")
            # print("top card:", self.last_card, "player hand:", [str(card) for card in player.hand])

            if self.next_draw != 0:
                self.next_person_draw_n(player)
                self.next_draw = 0

            flag = False
            for card in player.hand:
                if card.num == self.last_card.num or card.suit == self.last_card.suit:
                    player.hand.remove(card)
                    self.thrown_deck.append(self.last_card)
                    self.last_card = card
                    if card.num == 6 and self.draw2:
                        self.next_draw = 2
                    elif card.num == 13 and self.draw4:
                        self.next_draw = 4
                    elif card.num == 10 and self.reverse:
                        self.order *= -1
                    elif (card.num == 0 or card.num == 7) and self.skip:
                        i += self.order
                    flag = True
                    break

            if flag is False:
                self.deck = player.draw_cards(self.deck, 1)
                if len(self.deck) == 0:
                    if len(self.thrown_deck) == 0:
                        self.turns = -1
                        return
                    self.deck = self.thrown_deck[:]
                    shuffle(self.deck)
                    self.thrown_deck = []

            if len(player.hand) == 0:
                # print("Player", i, "won the game!")
                # print(self.turns)
                break
            i += self.order
            i %= self.num_players
            # time.sleep(0.1)


# 1-92    2-50    3-43.5    4-44.25    5-47.5    6-51.35
# {1: 91.9103, 2: 50.3073, 3: 43.4577, 4: 44.49545, 5: 47.4441, 6: 51.73825, 7: 56.48335}

primeroci1 = {}
primeroci2 = {}
for np in range(2, 8):
    primerok = []
    for j in range(50000):
        game = Game(num_players=np, num_cards=14, num_colours=4, num_starting_cards=6, reverse=True, skip=True, draw2=True, draw4=True)
        game.play()
        if game.turns != -1:
            primerok.append(game.turns)
    primeroci1[np] = primerok

for np in range(2, 8):
    primerok = []
    for j in range(50000):
        game = Game(num_players=np, num_cards=14, num_colours=4, num_starting_cards=6, reverse=False, skip=False, draw2=False, draw4=False)
        game.play()
        if game.turns != -1:
            primerok.append(game.turns)
    primeroci2[np] = primerok

for np in primeroci1:
    primerok1 = primeroci1[np]
    primerok2 = primeroci2[np]
    print(np)
    print("standardna devijacija", stdev(primerok1), stdev(primerok2))
    print("prosek", mean(primerok1), mean(primerok2))
    print("maks", max(primerok1), max(primerok2))
    print("min", min(primerok1), min(primerok2))
    print()
