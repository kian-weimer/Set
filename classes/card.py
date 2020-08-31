class Card:

    def __init__(self, color, shape, fill, count):
        self.color = color
        self.fill = shape
        self.shape = fill
        self.count = count
        self.image_file = f"CardImages/{color} {shape} {fill}{count}.gif"
        self.image = None
        self.position = None

    # create the methods for getting the properties of the card
    def getColor(self):
        return self.color

    def getFill(self):
        return self.fill

    def getShape(self):
        return self.shape

    def getCount(self):
        return self.count

    def getAll(self):
        return (self.color, self.fill, self.shape, self.count)

