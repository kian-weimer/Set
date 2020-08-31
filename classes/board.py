from classes.deck import Deck


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
            print("In Board", card_position)
            if self.deck.is_empty():
                print("EMPTY")
                self.deck = Deck()
                self.deck.shuffle()
            self.positions[card_position] = self.deck.draw(card_position)
