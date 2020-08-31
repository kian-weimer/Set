import tkinter as tk
from tkinter import *
from classes.board import Board
from functools import partial

from functions.setChecker import setChecker

root = tk.Tk()

canvas = tk.Canvas(root, width=1000, height=500)
canvas.configure(bg= '#ff4733')
card_buttons = []
card_windows = []
board = Board()

def select_card(position):
    row = position % 4
    column = position // 4

    if card_buttons[position].cget('bg') == "#fcff66":
        card_buttons[position].configure(bg='white')
        board.remove_card((row,column))
        canvas.configure(bg = 'white')

    else:
        if board.select_card((row, column)):
            card_buttons[position].configure(bg="#fcff66")
            canvas.configure(bg=board.check_card((row,column)).getColor())

def set():
    if len(board.hand) != 3:
        print("Select Three Cards!")

    elif setChecker(*board.hand):
        print("Correct")
        hand = board.hand
        board.change_cards(hand)

        for card in hand:
            row, column = card.position
            position = column*4 + row
            card = board.check_card((row, column))
            card.img = PhotoImage(file=card.image_file)
            card_button = tk.Button(image=card.img, bg="white")
            card_button.configure(command=partial(select_card, position))
            card_buttons[position] = card_button

            card_window = canvas.create_window(row * 200 + 100, column * 150, window=card_button, anchor=NW)
            card_windows[position] = card_window

            board.hand = []
            canvas.pack()

    else:
        print("Wrong!")

def startGame():
    startButton.forget()
    howToButton.forget()
    multiplayerButton.forget()
    canvas.itemconfigure(submit_button_window, state='normal')
    canvas.itemconfigure(back_button_window, state = 'normal')

    for i in range(12):
        row = i % 4
        column = i // 4
        card = board.check_card((row, column))
        img = PhotoImage(file=card.image_file)
        card.image = img
        card_button = tk.Button(image=img, bg="white")
        card_button.configure(command=partial(select_card, i))
        card_buttons.append(card_button)

        card_window = canvas.create_window(row * 200 + 100, column * 150, window=card_button, anchor=NW)
        card_windows.append(card_window)

def howToPlay():
    canvas.itemconfigure(start_button_window, state='hidden')
    canvas.itemconfigure(multiplayer_button_window, state='hidden')
    canvas.itemconfigure(how_to_button_window, state='hidden')
    canvas.itemconfigure(back_button_window, state='normal')

def multiplayer():
    canvas.itemconfigure(start_button_window, state = 'hidden')
    canvas.itemconfigure(multiplayer_button_window, state='hidden')
    canvas.itemconfigure(how_to_button_window, state='hidden')
    canvas.itemconfigure(back_button_window, state = 'normal')

def homePage():
    for card_window in card_windows:
        canvas.itemconfigure(card_window, state = 'hidden')

    canvas.itemconfigure(submit_button_window, state = 'hidden')

    canvas.itemconfigure(back_button_window, state = 'hidden')
    canvas.itemconfigure(start_button_window, state='normal')
    canvas.itemconfigure(multiplayer_button_window, state='normal')
    canvas.itemconfigure(how_to_button_window, state='normal')

startButton = tk.Button(command=startGame, text='Start Game', width = 20, height = 2, bg = '#ffef5e')
multiplayerButton = tk.Button(command=multiplayer, text='Multiplayer', width = 20, height = 2, bg = '#ffef5e')
howToButton = tk.Button(command=howToPlay, text='How To Play', width = 20, height = 2, bg = '#ffef5e')
backButton = tk.Button(command=homePage, text='<--Back', bg = '#ffef5e')

start_button_window = canvas.create_window(505,150, window = startButton)
multiplayer_button_window = canvas.create_window(505,250, window = multiplayerButton)
how_to_button_window = canvas.create_window(505,350, window = howToButton)
back_button_window = canvas.create_window(40,40, window = backButton, state = 'hidden')
submit_button = tk.Button(command=set, text='Set!', bg='#ffef5e', width = 10, height = 1, font = ('helvetica',18))
submit_button_window = canvas.create_window(500, 475, window=submit_button)
canvas.itemconfigure(submit_button_window, state='hidden')
canvas.pack()


root.mainloop()

