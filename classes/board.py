from classes.deck import Deck


class Board:

    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.positions = {(i % 4, i // 4): self.deck.draw() for i in range(12)}
        self.hand = []

    # takes in an integer (1-81) and returns the index at that card
    def check_card(self, board_position):
        return self.positions[board_position]

    def select_card(self, board_position):
        if len(self.hand) == 3:
            return False
        self.hand.append(self.check_card(board_position))
        return True

    def remove_card(self, board_position):
        self.hand.remove(self.check_card(board_position))

    def change_card(self, board_position):
        if self.deck.is_empty():
            self.deck = Deck()
            self.deck.shuffle()
        self.positions[board_position] = self.deck.draw()
