from functions.setChecker import *


def property_checker(hand):
    incorrectLabel = ""

    if not fill_check(*hand):
        incorrectLabel += "The fills are invalid"

    if not color_check(*hand):
        if incorrectLabel == "":
            incorrectLabel += "The colors are invalid"
        else:
            incorrectLabel += " + the colors are invalid"

    if not count_check(*hand):
        if incorrectLabel == "":
            incorrectLabel += "The counts are invalid"
        else:
            incorrectLabel += " + the counts are invalid"

    if not shape_check(*hand):
        if incorrectLabel == "":
            incorrectLabel += "The shapes are invalid"
        else:
            incorrectLabel += " + the shapes are invalid"

    return incorrectLabel
