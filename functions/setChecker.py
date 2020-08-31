from classes.card import Card


def setChecker(card1: Card, card2: Card, card3: Card):

    if (colorCheck(card1, card2, card3) and fillCheck(card1, card2, card3) and shapeCheck(card1, card2, card3) and countCheck(card1, card2, card3)):
        return True
    return False

def fillCheck(card1, card2, card3):
    fill1 = card1.getFill()
    fill2 = card2.getFill()
    fill3 = card3.getFill()
    if (fill1 == fill2 and fill1 == fill3) or (fill1 != fill2 and fill2 != fill3 and fill1 != fill3):
        return True
    return False

def colorCheck(card1, card2, card3):
    color1 = card1.getColor()
    color2 = card2.getColor()
    color3 = card3.getColor()
    if (color1 == color2 and color1 == color3) or (color1 != color2 and color2 != color3 and color1 != color3):
        return True
    return False

def countCheck(card1, card2, card3):
    count1 = card1.getCount()
    count2 = card2.getCount()
    count3 = card3.getCount()
    if (count1 == count2 and count1 == count3) or (count1 != count2 and count2 != count3 and count1 != count3):
        return True
    return False

def shapeCheck(card1, card2, card3):
    shape1 = card1.getShape()
    shape2 = card2.getShape()
    shape3 = card3.getShape()
    if (shape1 == shape2 and shape1 == shape3) or (shape1 != shape2 and shape2 != shape3 and shape1 != shape3):
        return True
    return False
