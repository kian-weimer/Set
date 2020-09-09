from functions.setChecker import *


def property_checker(hand):
    incorrect_label = ""

    if not fill_check(*hand):
        incorrect_label += "The fills are invalid"

    if not color_check(*hand):
        if incorrect_label == "":
            incorrect_label += "The colors are invalid"
        else:
            incorrect_label += " + the colors are invalid"

    if not count_check(*hand):
        if incorrect_label == "":
            incorrect_label += "The counts are invalid"
        else:
            incorrect_label += " + the counts are invalid"

    if not shape_check(*hand):
        if incorrect_label == "":
            incorrect_label += "The shapes are invalid"
        else:
            incorrect_label += " + the shapes are invalid"

    return incorrect_label
