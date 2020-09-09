from classes.card import Card


# checks to see if there is a set between 3 cards calls the smaller methods to check each attribute
def set_checker(card1: Card, card2: Card, card3: Card):
    if (color_check(card1, card2, card3) and fill_check(card1, card2, card3) and
            shape_check(card1, card2, card3) and count_check(card1, card2, card3)):
        return True
    return False


# checks if the fills are either all the same or all different
def fill_check(card1, card2, card3):
    fill1 = card1.get_fill()
    fill2 = card2.get_fill()
    fill3 = card3.get_fill()
    if (fill1 == fill2 and fill1 == fill3) or (fill1 != fill2 and fill2 != fill3 and fill1 != fill3):
        return True
    return False


# checks if the colors are either all the same or all different
def color_check(card1, card2, card3):
    color1 = card1.get_color()
    color2 = card2.get_color()
    color3 = card3.get_color()
    if (color1 == color2 and color1 == color3) or (color1 != color2 and color2 != color3 and color1 != color3):
        return True
    return False


# checks if the counts are either all the same or all different
def count_check(card1, card2, card3):
    count1 = card1.get_count()
    count2 = card2.get_count()
    count3 = card3.get_count()
    if (count1 == count2 and count1 == count3) or (count1 != count2 and count2 != count3 and count1 != count3):
        return True
    return False


# checks if the shapes are either all the same or all different
def shape_check(card1, card2, card3):
    shape1 = card1.get_shape()
    shape2 = card2.get_shape()
    shape3 = card3.get_shape()
    if (shape1 == shape2 and shape1 == shape3) or (shape1 != shape2 and shape2 != shape3 and shape1 != shape3):
        return True
    return False
