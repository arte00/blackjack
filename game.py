from random import choice


# każda karta ma kolor i wartość
class Card:

    def __init__(self, color, rank):
        self.color = color
        self.rank = rank

    def __int__(self):
        if self.rank in ["jack", "queen", "king"]:
            return 10
        elif self.rank == "1":
            return 11
        else:
            return int(self.rank)


class Cards:

    def __init__(self):
        self.values = [str(i) for i in range(1, 11)] + ["jack", "queen", "king"]
        self.colors = ["club", "diamond", "heart", "spade"]
        self.cards = [Card(color, value) for color in self.colors for value in self.values]

    # przy zaindeksowaniu kart jest ona od razu usuwana z tali, by się nie powtórzyła

    def __getitem__(self, item):
        card = self.cards.pop(item)
        return card

    def __len__(self):
        return len(self.cards)


class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, _deck):
        added_card = choice(_deck)
        self.cards.append(added_card)
        self.value += int(added_card)
        if added_card.rank == "1":
            self.aces += 1
        return added_card

    # as liczy się jako 11, lub jako 1 gdy punkty gracza przekroczą 21

    def adjust_aces(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class DealerHand:

    # Dla gracza widoczna jest liczba punktów krupiera bez liczenia pierwszej karty, gdyż jest zakryta
    # Są zatem dwie zmienne określające liczbę punktów krupiera

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
        self.value_public = 0
        self.first_card = True

    def add_card(self, _deck):
        added_card = choice(_deck)
        self.cards.append(added_card)
        if self.first_card:
            self.value += int(added_card)
            self.first_card = False
        else:
            self.value += int(added_card)
            self.value_public += int(added_card)
        if added_card.rank == "1":
            self.aces += 1
        return added_card

    def adjust_aces(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


# Żetony

class Chips:

    def __init__(self):
        self.chips = 1000
        self.bet_chips = 0

    def bet(self, number):
        self.chips -= number
        self.bet_chips += number

    def unbet(self, number):
        self.chips += number
        self.bet_chips -= number

    def lose_bet(self):
        self.bet_chips = 0

    def win_bet(self):
        self.chips += 2 * self.bet_chips
        self.bet_chips = 0

    def draw_bet(self):
        self.chips += self.bet_chips
        self.bet_chips = 0



