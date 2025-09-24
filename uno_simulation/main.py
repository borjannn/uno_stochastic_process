import random
import os
import csv
from random import shuffle, randint
from statistics import stdev, mean
from concurrent.futures import ProcessPoolExecutor, as_completed


class Card:
    def __init__(self, num, suit):
        self.num = num
        self.suit = suit

    def __str__(self):
        return f'{self.num}:{self.suit}'


class Player:
    def __init__(self, starting_hand):
        self.hand = starting_hand

    def __str__(self):
        return f'{self.hand}'


class Game:
    def __init__(self, num_players, num_cards, num_colours, num_starting_cards, reverse, skip, draw2, draw4,
                 shuffle_level="high"):
        self.shuffle_level = shuffle_level
        self.turn_of_player = 0
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
                self.deck.append(Card(num + 1, suit + 1))
        self.partial_shuffle(self.shuffle_level)
        self.players = []
        self.num_players = num_players
        self.num_cards = num_cards
        self.num_colours = num_colours
        for i in range(num_players):
            starting_hand = self.deck[:self.num_starting_cards]
            self.deck = self.deck[self.num_starting_cards:]
            self.players.append(Player(starting_hand))
        self.last_card = self.deck.pop(0)

    def best_card(self, hand):

        if self.last_card.num in (7, 14):
            pass

    def draw_cards(self, player, n):
        if n == 0:
            return
        if n >= len(self.deck):
            n = n - len(self.deck)
            player.hand += self.deck
            self.deck = self.thrown_deck[:]
            self.thrown_deck = []
            self.partial_shuffle(self.shuffle_level)
            player.hand += self.deck[:n]
        else:
            player.hand += self.deck[:n]
        self.deck = self.deck[n:]

    def card_action(self, card):
        if card.num == 7 and self.draw2:
            self.next_draw = 2
        elif card.num == 14 and self.draw4:
            self.next_draw = 4
        elif card.num == 10 and self.reverse:
            self.order *= -1
        elif (card.num == 1 or card.num == 8) and self.skip:
            self.turn_of_player += self.order

    def partial_shuffle(self, quality='high'):
        if quality == 'high':
            shuffle(self.deck)
        elif quality == 'medium':
            for _ in range(25):
                i, j = randint(0, len(self.deck) - 1), randint(0, len(self.deck) - 1)
                self.deck[i], self.deck[j] = self.deck[j], self.deck[i]
        elif quality == 'low':
            for _ in range(7):
                i, j = randint(0, len(self.deck) - 1), randint(0, len(self.deck) - 1)
                self.deck[i], self.deck[j] = self.deck[j], self.deck[i]
        elif quality == 'none':
            pass

    def try_throw_card(self, card, player):
        if card.num == self.last_card.num or card.suit == self.last_card.suit:
            player.hand.remove(card)
            self.thrown_deck.append(self.last_card)
            self.last_card = card
            self.card_action(card)
            return True
        return False

    def play(self):
        while self.turns < 10000:
            self.turns += 1
            player = self.players[self.turn_of_player]

            self.draw_cards(player, self.next_draw)
            self.next_draw = 0

            flag = False
            for card in player.hand:
                if self.try_throw_card(card, player):
                    flag = True
                    break

            if not flag:
                self.draw_cards(player, 1)

            if len(player.hand) == 0:
                break
            self.turn_of_player = (self.turn_of_player + self.order) % self.num_players


# 1-92    2-50    3-43.5    4-44.25    5-47.5    6-51.35
# {1: 91.9103, 2: 50.3073, 3: 43.4577, 4: 44.49545, 5: 47.4441, 6: 51.73825, 7: 56.48335}
#
# primeroci1 = {}
# primeroci2 = {}
# for np in range(2, 8):
#     primerok = []
#     for j in range(50000):
#         game = Game(num_players=np, num_cards=14, num_colours=4, num_starting_cards=6, reverse=True, skip=True,
#                     draw2=True, draw4=True)
#         game.play()
#         if game.turns != -1:
#             primerok.append(game.turns)
#     primeroci1[np] = primerok
#
# for np in range(2, 8):
#     primerok = []
#     for j in range(1000):
#         game = Game(num_players=np, num_cards=14, num_colours=4, num_starting_cards=6, reverse=False, skip=False,
#                     draw2=False, draw4=False)
#         game.play()
#         if game.turns != -1:
#             primerok.append(game.turns)
#     primeroci2[np] = primerok
#
# for np in primeroci1:
#     primerok1 = primeroci1[np]
#     primerok2 = primeroci2[np]
#     print(np)
#     print("standardna devijacija", stdev(primerok1), stdev(primerok2))
#     print("prosek", mean(primerok1), mean(primerok2))
#     print("maks", max(primerok1), max(primerok2))
#     print("min", min(primerok1), min(primerok2))
#     print()

def run_game(seed, np, with_specials=True):
    random.seed(seed)
    game = Game(
        num_players=np,
        num_cards=14,
        num_colours=4,
        num_starting_cards=6,
        reverse=with_specials,
        skip=with_specials,
        draw2=with_specials,
        draw4=with_specials,
    )
    game.play()
    return {
        "seed": seed,
        "num_players": np,
        "num_cards": 14,
        "num_colours": 4,
        "shuffle_level": "high",  # could be param
        "specials": with_specials,
        "turns": game.turns,
        "winner": game.turn_of_player,  # winner index
    }


def run_batch(np, n_runs=1000, with_specials=True, workers=None):
    results = []
    workers = workers or os.cpu_count()
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(run_game, seed, np, with_specials)
            for seed in range(n_runs)
        ]
        for f in as_completed(futures):
            turns = f.result()
            if turns is not None:
                results.append(turns)
    return results


def save_results(rows, filename="results.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        if not file_exists:
            writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    primeroci1 = {}
    primeroci2 = {}

    for np in range(2, 8):
        primeroci1[np] = run_batch(np, n_runs=20000, with_specials=True)
        save_results(primeroci1[np], filename="results_with_specials.csv")

    for np in range(2, 8):
        primeroci2[np] = run_batch(np, n_runs=20000, with_specials=False)
        save_results(primeroci2[np], filename="results_no_specials.csv")

    # Print stats
    for np in primeroci1:
        primerok1 = primeroci1[np]
        primerok2 = primeroci2[np]
        print(f"\nPlayers = {np}")
        print("standardna devijacija", stdev([r["turns"] for r in primerok1]),
              stdev([r["turns"] for r in primerok2]))
        print("prosek", mean([r["turns"] for r in primerok1]),
              mean([r["turns"] for r in primerok2]))
        print("maks", max([r["turns"] for r in primerok1]),
              max([r["turns"] for r in primerok2]))
        print("min", min([r["turns"] for r in primerok1]),
              min([r["turns"] for r in primerok2]))

