from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import sys
import game


class Window(QWidget):

    def __init__(self):
        super().__init__()

        # Klasy potrzebne do prowadzenia rozgrywki
        # karty, karty gracza, karty krupiera

        self.deck = game.Cards()
        self.hand = game.Hand()
        self.dealer_hand = game.DealerHand()
        self.chips = game.Chips()

        # Ustawienia okna z grą

        self.setWindowTitle("Blackjack")
        self.setGeometry(100, 100, 900, 900)

        self.first_game = True

        # Wygląd stołu

        self.setStyleSheet("background: ForestGreen")

        '''PRZYCISKI'''

        # Hit, kładzie kartę

        self.hit = QPushButton(self)
        self.hit.move(650, 700)
        self.hit.setFixedSize(100, 100)
        self.hit.setText("Hit")
        self.hit.setStyleSheet("border-radius : 50px; border : 2px solid black; background: Red;\
                                            font-family: 'Courier New', monospace; font-size: 30px")

        self.hit.clicked.connect(self.put_player_card)
        self.hit.setDisabled(True)

        # Stand, rezugnuje z rozgrywki

        self.stand = QPushButton(self)
        self.stand.move(700, 550)
        self.stand.setFixedSize(100, 100)
        self.stand.setText("Stand")
        self.stand.setStyleSheet("border-radius : 50px; border : 2px solid black; background: Red; \
                                                font-family: 'Courier New', monospace; font-size: 30px")
        self.stand.clicked.connect(self.player_stand)
        self.stand.setDisabled(True)

        # New game, rozpoczuna kolejną rozgrywkę

        self.new_game_button = QPushButton("New game", self)
        self.new_game_button.move(125, 200)
        self.new_game_button.setFixedSize(200, 50)
        self.new_game_button.setStyleSheet("border : 2px solid black; background: Red; \
                                                        font-family: 'Courier New', monospace; font-size: 30px")
        self.new_game_button.clicked.connect(self.new_game)

        self.add = QPushButton(self)
        self.add.move(130, 280)
        self.add.setFixedSize(40, 40)
        self.add.setStyleSheet("font-family: 'Courier New', monospace; font-size: 50px; background: LightGreen")
        self.add.setText("+")
        self.add.clicked.connect(self.add_bet)

        self.sub = QPushButton(self)
        self.sub.move(70, 280)
        self.sub.setFixedSize(40, 40)
        self.sub.setStyleSheet("font-family: 'Courier New', monospace; font-size: 50px; background: IndianRed")
        self.sub.setText("-")
        self.sub.clicked.connect(self.sub_bet)

        '''ETYKIETY'''

        # etykieta z punktami gracza

        self.player_score = QLabel(self)
        self.player_score.setFixedSize(100, 100)
        self.player_score.move(75, 450)
        self.player_score.setText("0")
        self.player_score.setStyleSheet("font-family: 'Courier New', monospace; font-size: 50px;")

        # etykieta z punktami krupiera

        self.dealer_score = QLabel(self)
        self.dealer_score.setFixedSize(100, 100)
        self.dealer_score.move(400, 50)
        self.dealer_score.setText("0")
        self.dealer_score.setStyleSheet("font-family: 'Courier New', monospace; font-size: 50px;")

        # etykieta w której pojawi się wynik rozgrywki

        self.result = QLabel(self)
        self.result.move(65, 100)
        self.result.setFixedSize(300, 100)
        self.result.setStyleSheet("font-family: 'Courier New', monospace; font-size: 62px;")

        # Etykieta z pieniędzmi gracza

        self.money = QLabel(self)
        self.money.move(60, 400)
        self.money.setFixedSize(300, 75)
        self.money.setText("Money: " + str(self.chips.chips) + "$")
        self.money.setStyleSheet("font-family: 'Courier New', monospace; font-size: 35px;")
        # Etykieta z obecnym zakładem

        self.bet = QLabel(self)
        self.bet.move(60, 325)
        self.bet.setFixedSize(300, 75)
        self.bet.setText("Bet: " + str(self.chips.bet_chips) +"$")
        self.bet.setStyleSheet("font-family: 'Courier New', monospace; font-size: 35px;")

        # miejsca na karty gracza, numerowane [1-7]

        self.spot1 = QLabel(self)
        self.spot2 = QLabel(self)
        self.spot3 = QLabel(self)
        self.spot4 = QLabel(self)
        self.spot5 = QLabel(self)
        self.spot6 = QLabel(self)
        self.spot7 = QLabel(self)

        self.player_cards_queue = [self.spot1, self.spot2, self.spot3, self.spot4, self.spot5, self.spot6, self.spot7]
        self.player_cards_counter = 0

        # miejsca na karty krupiera, numerowane [11-17]

        self.spot11 = QLabel(self)
        self.spot12 = QLabel(self)
        self.spot13 = QLabel(self)
        self.spot14 = QLabel(self)
        self.spot15 = QLabel(self)
        self.spot16 = QLabel(self)
        self.spot17 = QLabel(self)

        self.dealer_cards_queue = [self.spot11, self.spot12, self.spot13, self.spot14, self.spot15, self.spot16, self.spot17]
        self.dealer_cards_counter = 0

        self.show()

    # dodanie karty gracza sa stół
    # i sprawdzenie czy liczba punktów nie przekracza 21

    def put_player_card(self):
        next_card = self.hand.add_card(self.deck)
        self.hand.adjust_aces()

        place = self.player_cards_queue[self.player_cards_counter]
        x = 75 + 50 * self.player_cards_counter
        y = 550 + 15 * self.player_cards_counter
        place.setFixedSize(200, 240)
        place.setPixmap(QPixmap(self.get_image(next_card)))
        place.move(x, y)
        self.player_cards_counter += 1
        self.set_player_score()

        if self.hand.value > 21:
            self.player_bust()

    # dobranie karty przez krupiera, pierwsza jest zakryta na czas trwania rozgrywki

    def put_dealer_card(self):
        next_card = self.dealer_hand.add_card(self.deck)
        self.dealer_hand.adjust_aces()

        place = self.dealer_cards_queue[self.dealer_cards_counter]
        x = 400 + 50 * self.dealer_cards_counter
        y = 150 + 15 * self.dealer_cards_counter
        place.setFixedSize(200, 240)
        place.move(x, y)
        # Zakrycie karty
        if place == self.dealer_cards_queue[0]:
            place.setPixmap(QPixmap("images/1x/back-navy.png"))
        else:
            place.setPixmap(QPixmap(self.get_image(next_card)))
        self.dealer_cards_counter += 1
        self.set_dealer_score()

    # stand, zakończenie rozgrywki przez gracza, podjęcie decyzji przez krupiera czy dobrać karty
    # + sprawdzenie wyniku

    def player_stand(self):
        while self.dealer_hand.value < 17:
            self.put_dealer_card()
        if self.dealer_hand.value > 21:
            self.dealer_bust()
        elif self.dealer_hand.value > self.hand.value:
            self.dealer_wins()
        elif self.dealer_hand.value < self.hand.value:
            self.player_wins()
        elif self.dealer_hand.value == self.hand.value:
            self.draw()
        else:
            self.player_bust()

    # odświeżanie wyników wypisywanych na planszy

    def set_player_score(self):
        self.player_score.setText(str(self.hand.value))

    def set_dealer_score(self):
        self.dealer_score.setText(str(self.dealer_hand.value_public))

    def set_money(self):
        self.money.setText(str("Money: " + str(self.chips.chips) + "$"))

    def set_bet(self):
        self.bet.setText(str("Bet: " + str(self.chips.bet_chips) + "$"))

    # rozdanie po dwóch kart na początek

    def begin(self):
        self.put_player_card()
        self.put_player_card()
        self.put_dealer_card()
        self.put_dealer_card()

    def end(self):
        pass

    # pozyskanie z obiektu typu karta ścieżki do obrazku

    @staticmethod
    def get_image(card):
        return "images/1x/" + card.color + "_" + card.rank + ".png"

    # możliwe wyniki rozgrywki
    # wypisanie wyniku, odsłonięcie karty krupiera, zablokowanie i doblokowanie przycisków
    # sprawdzenie żetonów gracza

    def player_bust(self):
        self.result.setText("You lost!")  # player_bust
        self.spot11.setPixmap(QPixmap(self.get_image(self.dealer_hand.cards[0])))
        self.dealer_score.setText(str(self.dealer_hand.value))
        self.new_game_button.setDisabled(False)
        self.hit.setDisabled(True)
        self.stand.setDisabled(True)
        self.chips.lose_bet()
        self.set_money()
        self.set_bet()
        self.add.setDisabled(False)
        self.sub.setDisabled(False)
        self.check_if_zero_chips()

    def player_wins(self):
        self.result.setText("You win!")
        self.spot11.setPixmap(QPixmap(self.get_image(self.dealer_hand.cards[0])))
        self.dealer_score.setText(str(self.dealer_hand.value))
        self.new_game_button.setDisabled(False)
        self.hit.setDisabled(True)
        self.stand.setDisabled(True)
        self.chips.win_bet()
        self.set_money()
        self.set_bet()
        self.add.setDisabled(False)
        self.sub.setDisabled(False)
        self.check_if_zero_chips()

    def dealer_wins(self):
        self.result.setText("You lost!")
        self.spot11.setPixmap(QPixmap(self.get_image(self.dealer_hand.cards[0])))
        self.dealer_score.setText(str(self.dealer_hand.value))
        self.new_game_button.setDisabled(False)
        self.hit.setDisabled(True)
        self.stand.setDisabled(True)
        self.chips.lose_bet()
        self.set_money()
        self.set_bet()
        self.add.setDisabled(False)
        self.sub.setDisabled(False)
        self.check_if_zero_chips()

    def dealer_bust(self):
        self.result.setText("You win!")
        self.spot11.setPixmap(QPixmap(self.get_image(self.dealer_hand.cards[0])))
        self.dealer_score.setText(str(self.dealer_hand.value))
        self.new_game_button.setDisabled(False)
        self.hit.setDisabled(True)
        self.stand.setDisabled(True)
        self.chips.win_bet()
        self.set_money()
        self.set_bet()
        self.add.setDisabled(False)
        self.sub.setDisabled(False)
        self.check_if_zero_chips()

    def draw(self):
        self.result.setText("Draw!")
        self.spot11.setPixmap(QPixmap(self.get_image(self.dealer_hand.cards[0])))
        self.dealer_score.setText(str(self.dealer_hand.value))
        self.new_game_button.setDisabled(False)
        self.hit.setDisabled(True)
        self.stand.setDisabled(True)
        self.chips.draw_bet()
        self.set_money()
        self.set_bet()
        self.add.setDisabled(False)
        self.sub.setDisabled(False)
        self.check_if_zero_chips()

    def check_if_zero_chips(self):
        if self.chips.chips <= 0:
            self.bet.setText("No more chips.")
            self.money.setText("You lost.")

    # Rozpoczęcie nowej partii

    def new_game(self):

        # Zablokowanie możliwości obstawiania, odblokowanie możliwości gry

        self.hit.setDisabled(False)
        self.stand.setDisabled(False)
        self.new_game_button.setDisabled(True)
        self.add.setDisabled(True)
        self.sub.setDisabled(True)

        if self.first_game:
            # self.result.setText("New Game")
            self.first_game = False
            self.begin()

        else:   # Jeśli nie jest to pierwsza partia to należy wyczyścić stół

            for spot in self.player_cards_queue:
                spot.move(0, 0)
                spot.setFixedSize(1, 1)
                spot.clear()

            for spot in self.dealer_cards_queue:

                spot.move(0, 0)
                spot.setFixedSize(1, 1)
                spot.clear()

            self.deck = game.Cards()
            self.hand = game.Hand()
            self.dealer_hand = game.DealerHand()

            self.player_score.setText("0")
            self.dealer_score.setText("0")
            self.result.setText("")

            self.player_cards_counter = 0
            self.dealer_cards_counter = 0

            self.set_bet()

            self.begin()

    # Obstawianie żetonów

    def add_bet(self):
        if self.chips.chips > 0:
            self.chips.bet(100)
            self.set_bet()
            self.set_money()

    def sub_bet(self):
        if self.chips.bet_chips > 0:
            self.chips.unbet(100)
            self.set_bet()
            self.set_money()


def main():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

