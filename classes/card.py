class Card:

    def __init__(self, color, shape, fill, number):
        self.color = color
        self.fill = shape
        self.shape = fill
        self.number = number
        self.image_file = f"CardImages/{color} {shape} {fill}{number}.gif"
        self.image = None
        self.position = None

    # create the methods for getting the properties of the card
    def getColor(self):
        return self.color

    def getFill(self):
        return self.fill

    def getShape(self):
        return self.shape

    def getNumber(self):
        return self.number

    def getAll(self):
        return (self.color, self.fill, self.shape, self.number)