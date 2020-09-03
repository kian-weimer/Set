from functions.setChecker import *


def property_checker(hand):
    incorrectLabel = ""

    if not fillCheck(*hand):
        incorrectLabel += "The fills don't match"

    if not colorCheck(*hand):
        if incorrectLabel == "":
            incorrectLabel += "The colors don't match"
        else:
            incorrectLabel += " + the colors don't match"

    if not countCheck(*hand):
        if incorrectLabel == "":
            incorrectLabel += "The counts don't match"
        else:
            incorrectLabel += " + the counts don't match"

    if not shapeCheck(*hand):
        if incorrectLabel == "":
            incorrectLabel += "The shapes don't match"
        else:
            incorrectLabel += " + the shapes don't match"

    return incorrectLabel
