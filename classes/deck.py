from classes.card import Card
import random


class Deck:

    def __init__(self):
        self.cardList = []
        self.colorList = ['red', 'blue', 'green']
        self.fillList = ['solid', 'shaded', 'clear']
        self.shapeList = ['circle', 'triangle', 'square']
        self.numList = ['1', '2', '3']

        for color in self.colorList:
            for fill in self.fillList:
                for shape in self.shapeList:
                    for number in self.numList:
                        self.cardList.append(Card(color, fill, shape, number))

        # self.cardList = self.cardList[:12]

    def is_empty(self):
        return not len(self.cardList)

    # takes in an integer (1-81) and returns the index at that card
    def draw(self, board_position):
        card = self.cardList.pop()
        card.position = board_position
        print(card.position)
        return card

    # shuffle method with three shuffles
    def shuffle(self):
        random.shuffle(self.cardList)
        random.shuffle(self.cardList)
        random.shuffle(self.cardList)
        return self.cardList