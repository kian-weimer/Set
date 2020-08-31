import tkinter as tk
from tkinter import *
from classes.board import Board
from functools import partial
import _thread as thread
import time


from functions.setChecker import setChecker

root = tk.Tk()
root.attributes("-topmost", True)

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
    message_label = tk.Label(text="Wrong", font=("Helvetica", 32))

    if len(board.hand) != 3:
        message_label.configure(text="Select Three Cards!")

    elif setChecker(*board.hand):
        message_label.configure(text="Correct")
        hand = board.hand
        board.change_cards(hand)

        for card in hand:
            row, column = card.position
            position = column*4 + row
            card = board.check_card((row, column))
            card.img = PhotoImage(file=card.image_file)
            card_buttons[position].configure(image=card.img, bg="white", command=partial(select_card, position))

        board.hand = []
        board.score += 1

    else:
        message_label.configure(text="Wrong!")
        board.score -= 1

    message_label_window = canvas.create_window(500, 250, window=message_label)
    canvas.itemconfigure(message_label_window, state='normal')
    thread.start_new_thread(hide_after_seconds, (message_label_window, 2))
    score_label.configure(text=f"Score: {board.score}")

def hide_after_seconds(window, seconds):
    time.sleep(seconds)
    canvas.itemconfigure(window, state='hidden')

def startGame():
    card_buttons.clear()
    card_windows.clear()
    startButton.forget()
    howToButton.forget()
    multiplayerButton.forget()
    canvas.itemconfigure(submit_button_window, state='normal')
    canvas.itemconfigure(back_button_window, state = 'normal')
    canvas.itemconfigure(score_label_window, state='normal')

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
    global board

    for card_window in card_windows:
        canvas.itemconfigure(card_window, state = 'hidden')

    board = Board()

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

score_label = tk.Label(text=f"Score: {board.score}", font=("Helvetica", 32))
score_label_window = canvas.create_window(750, 475, window=score_label, state='hidden')

root.mainloop()

