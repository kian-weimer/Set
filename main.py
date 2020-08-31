import tkinter as tk
from tkinter import *
from classes.board import Board
from functools import partial
import _thread as thread
import time
from functions.setChecker import *
from winsound import *

root = tk.Tk()
root.attributes("-topmost", True)

canvas = tk.Canvas(root, width=1000, height=600, bg= '#ff4733', highlightthickness=0)
root.configure(bg = '#ff4733')
card_buttons = []
card_windows = []
board = Board()

def select_card(position):
    thread.start_new_thread(play, ('sounds/Click.wav',))
    row = position % 4
    column = position // 4

    if card_buttons[position].cget('bg') == "#fcff66":
        card_buttons[position].configure(bg='white')
        board.remove_card((row,column))
        canvas.configure(bg = 'white')
        root.configure(bg= 'white')

    else:
        if board.select_card((row, column)):
            card_buttons[position].configure(bg="#fcff66")
            score_label.configure(bg=board.check_card((row, column)).getColor())
            canvas.configure(bg = board.check_card((row,column)).getColor())
            root.configure(bg = board.check_card((row,column)).getColor())

def set():

    message_label = tk.Label(text="Wrong", font=("Helvetica", 15), bg = '#ffef5e', borderwidth = 7, relief = "raised")

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
        thread.start_new_thread(play, ('sounds/Boo.wav',))
        incorrectLabel = ""
        if not fillCheck(*board.hand):
            incorrectLabel += "The fills don't match"

        if not colorCheck(*board.hand):
            if incorrectLabel == "":
                incorrectLabel += "The colors don't match"
            else:
                incorrectLabel += "+ the colors don't match"

        if not countCheck(*board.hand):
            if incorrectLabel == "":
                incorrectLabel += "The counts don't match"
            else:
                incorrectLabel += "+ the counts don't match"

        if not shapeCheck(*board.hand):
            if incorrectLabel == "":
                incorrectLabel += "The shapes don't match"
            else:
                incorrectLabel += "+ the shapes don't match"
        message_label.configure(text=incorrectLabel)
        board.score -= 1

    message_label_window = canvas.create_window(500, 250, window=message_label)
    canvas.itemconfigure(message_label_window, state='normal')
    thread.start_new_thread(hide_after_seconds, (message_label_window, 2))
    score_label.configure(text=f"Score: {board.score}")

def hide_after_seconds(window, seconds):
    time.sleep(seconds)
    canvas.itemconfigure(window, state='hidden')

def startGame():
    thread.start_new_thread(play, ('sounds/Click.wav',))
    score_label.configure(text=f"Score: {board.score}")
    card_buttons.clear()
    card_windows.clear()
    startButton.forget()
    howToButton.forget()
    multiplayerButton.forget()
    canvas.itemconfigure(submit_button_window, state='normal')
    canvas.itemconfigure(back_button_window, state = 'normal')
    canvas.itemconfigure(score_label_window, state='normal')
    canvas.itemconfigure(start_button_window, state='hidden')
    canvas.itemconfigure(multiplayer_button_window, state='hidden')
    canvas.itemconfigure(how_to_button_window, state='hidden')

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

def play(sound_file_name):
    return PlaySound(sound_file_name, SND_FILENAME)

def howToPlay():
    thread.start_new_thread(play, ('sounds/Click.wav',))
    canvas.itemconfigure(start_button_window, state='hidden')
    canvas.itemconfigure(multiplayer_button_window, state='hidden')
    canvas.itemconfigure(how_to_button_window, state='hidden')
    canvas.itemconfigure(back_button_window, state='normal')

def multiplayer():
    thread.start_new_thread(play, ('sounds/Click.wav',))
    canvas.itemconfigure(start_button_window, state = 'hidden')
    canvas.itemconfigure(multiplayer_button_window, state='hidden')
    canvas.itemconfigure(how_to_button_window, state='hidden')
    canvas.itemconfigure(back_button_window, state = 'normal')

def homePage():
    global board

    thread.start_new_thread(play, ('sounds/Click.wav',))

    for card_window in card_windows:
        canvas.itemconfigure(card_window, state = 'hidden')

    canvas.itemconfigure(score_label_window, state = 'hidden')

    board = Board()

    canvas.itemconfigure(submit_button_window, state = 'hidden')

    canvas.itemconfigure(back_button_window, state = 'hidden')
    canvas.itemconfigure(start_button_window, state='normal')
    canvas.itemconfigure(multiplayer_button_window, state='normal')
    canvas.itemconfigure(how_to_button_window, state='normal')


startButton = tk.Button(command=startGame, text='Start Game', width = 20, height = 2, bg = '#ffef5e', font = ('helvetica',18))
multiplayerButton = tk.Button(command=multiplayer, text='Multiplayer', width = 20, height = 2, bg = '#ffef5e', font = ('helvetica',18))
howToButton = tk.Button(command=howToPlay, text='How To Play', width = 20, height = 2, bg = '#ffef5e', font = ('helvetica',18))
backButton = tk.Button(command=homePage, text='<--Back', bg = '#ffef5e')

start_button_window = canvas.create_window(500,150, window = startButton)
multiplayer_button_window = canvas.create_window(500,300, window = multiplayerButton)
how_to_button_window = canvas.create_window(500,450, window = howToButton)
back_button_window = canvas.create_window(40,40, window = backButton, state = 'hidden')
submit_button = tk.Button(command=set, text='Set!', bg='#ffef5e', width = 10, height = 1, font = ('helvetica',18))
submit_button_window = canvas.create_window(500, 525, window=submit_button)

canvas.itemconfigure(submit_button_window, state='hidden')

canvas.pack()

score_label = tk.Label(text=f"Score: {board.score}", font=("Helvetica", 32), bg = '#ff4733', foreground = 'white')
score_label_window = canvas.create_window(800, 525, window=score_label, state='hidden', width = 300)

root.mainloop()

