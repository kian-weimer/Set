from classes.card import Card


def setChecker(card1: Card, card2: Card, card3: Card):
    print(card1)
    c1Color, c1Fill, c1Shape, c1Number = card1.getAll()
    c2Color, c2Fill, c2Shape, c2Number = card2.getAll()
    c3Color, c3Fill, c3Shape, c3Number = card3.getAll()

    if (colorCheck(c1Color, c2Color, c3Color) and fillCheck(c1Fill, c2Fill, c3Fill) and
            shapeCheck(c1Shape, c2Shape, c3Shape) and countCheck(c1Number, c2Number, c3Number)):
        return True
    return False


def fillCheck(fill1, fill2, fill3):
    if (fill1 == fill2 and fill1 == fill3) or (fill1 != fill2 and fill2 != fill3 and fill1 != fill3):
        return True
    return False


def colorCheck(color1, color2, color3):
    if (color1 == color2 and color1 == color3) or (color1 != color2 and color2 != color3 and color1 != color3):
        return True
    return False


def countCheck(count1, count2, count3):
    if (count1 == count2 and count1 == count3) or (count1 != count2 and count2 != count3 and count1 != count3):
        return True
    return False


def shapeCheck(shape1, shape2, shape3):
    if (shape1 == shape2 and shape1 == shape3) or (shape1 != shape2 and shape2 != shape3 and shape1 != shape3):
        return True
    return False
