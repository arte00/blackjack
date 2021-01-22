from collections import namedtuple
from random import choice


class Cards:

    Card = namedtuple('Card', ['Color', 'Value'])

    def __init__(self):
        self.values = [i for i in range(2, 11)] + list("JQKA")
        self.colors = ["Pik", "Trefl", "Kier", "Karo"]
        self.cards = [self.Card(color, str(value)) for color in self.colors for value in self.values]

    def __getitem__(self, item):
        return self.cards[item]

    def show_cards(self):
        # print(self.values)
        # print(self.colors)
        print(self.cards)

    def __len__(self):
        return len(self.cards)

    def points(self):
        return self.cards


def evaluate(_cards: Cards, _hand: list):
    points1 = 0
    points2 = 0

    for card in _hand:
        if card.Value in ['J', 'Q', 'K', 'A']:
            points1 += 10
        else:
            points1 += int(card.Value)

    for card in _hand:
        if card.Value in ['J', 'Q', 'K']:
            points2 += 10
        elif card.Value == 'A':
            points2 += 1
        else:
            points2 += int(card.Value)

    return points1, points2


def deal(_deck: Cards, _hand: list):
    draw(_deck, _hand)
    draw(_deck, _hand)


def draw(_deck: Cards, _hand: list):
    _hand.append(choice(_deck))


def show_hand(_hand: list):
    print(_hand)


def check(_deck: Cards, _hand: list):
    v1, v2 = evaluate(_deck, _hand)
    if v1 > 21 & v2 > 21:
        return 1
    return 0


def engine(deck: Cards):
    hand = []
    deal(deck, hand)

    while True:
        v1, v2 = evaluate(deck, hand)
        show_hand(hand)
        print("Your score is " + str(v1) + " or " + str(v2))
        if v1 > 21 and v2 > 21:
            flag = input("You lost. Do you want to play again? Y/N").lower()
            if flag == "n":
                break
            else:
                engine(deck)

        decision = input("Hit or stand? H/S").lower()
        if decision == "h":
            draw(deck, hand)
        elif decision == "s":
            print("You stand")
        else:
            print("There is no option like that.")
    print("End! Thank you for playing")


def main():
    cards = Cards()
    engine(cards)


if __name__ == "__main__":
    main()

"""
List of classes:
Cards / deck -> all cards
Engine -> is responsible for checking if your score, value of cards etc
Game -> game loop
AI -> computer, takes its hand as argument and hand of player and evaluates possible moves
Graphics -> Takes info from all classes and prints it on boards
Settings -> stores settings like visuals, difficulty, 
Also there is need for folder with images of cards
"""