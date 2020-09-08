from classes.deck import Deck
from functions.setChecker import set_checker


class Board:

    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.positions = {(i % 4, i // 4): self.deck.draw((i % 4, i // 4)) for i in range(12)}
        self.hand = []
        self.score = 0

    # takes in an integer (1-81) and returns the index at that card
    def check_card(self, board_position):
        return self.positions[board_position]

    def select_card(self, board_position):
        if len(self.hand) == 3:
            return False
        self.hand.append(self.check_card(board_position))
        return True

    def remove_card(self, board_position):
        card = self.check_card(board_position)
        # card.position = None
        self.hand.remove(card)

    def change_cards(self, cards: []):
        for card in cards:
            card_position = card.position
            if self.deck.is_empty():
                self.positions[card_position] = None
            else:
                self.positions[card_position] = self.deck.draw(card_position)

    def is_a_set_on_board(self, cards:[], return_positions=False):
        for card1 in cards:
            for card2 in cards:
                for card3 in cards:
                    if (card1 is not None and card2 is not None and card3 is not None) and set_checker(card1, card2, card3) and card1 != card2 and card1 != card3 and card2 != card3:
                        if return_positions:
                            return card1.position, card2.position, card3.position
                        else:
                            return True
        return False