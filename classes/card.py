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
    def get_color(self):
        return self.color

    def get_fill(self):
        return self.fill

    def get_shape(self):
        return self.shape

    def get_count(self):
        return self.count

    def get_all(self):
        return self.color, self.fill, self.shape, self.count
