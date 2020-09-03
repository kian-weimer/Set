import tkinter as tk
from tkinter import *
from classes.board import Board
from functools import partial
import _thread as thread
import time

from functions.property_checker import property_checker
from functions.setChecker import *
from winsound import *

root = tk.Tk()
root.attributes("-topmost", True)

canvas = tk.Canvas(root, width=1000, height=600, bg='#ff4733', highlightthickness=0)
root.configure(bg='#ff4733')
card_buttons = []
high_scores = []
card_windows = []
high_score_windows = []
board = Board()


def select_card(position):
    thread.start_new_thread(play, ('sounds/Click.wav',))
    row = position % 4
    column = position // 4

    if card_buttons[position].cget('bg') == "#fcff66":
        card_buttons[position].configure(bg='white')
        board.remove_card((row, column))
        canvas.configure(bg='white')
        root.configure(bg='white')
        score_label.configure(bg='white', fg='black')
        wiki.configure(bg='white', fg='black')

    else:
        if board.select_card((row, column)):
            card_buttons[position].configure(bg="#fcff66")
            score_label.configure(bg=board.check_card((row, column)).getColor(), fg='white')
            wiki.configure(bg=board.check_card((row, column)).getColor(), fg='white')
            canvas.configure(bg=board.check_card((row, column)).getColor())
            root.configure(bg=board.check_card((row, column)).getColor())


def end_game(score, early_end=False):
    rank = 1
    end_message = f"Game Over!\n" + early_end*"There are no possible sets on the board.\n" + \
                  f"You are rank {rank} with score {score}"
    message_label = tk.Label(font=("Helvetica", 15), bg='#ffef5e', borderwidth=7, relief="raised")
    message_label.configure(text=end_message)
    message_label_window = canvas.create_window(500, 250, window=message_label)
    submit_button.configure(text="Exit", command=lambda: reset(message_label_window))
    backButton.configure(command=lambda: reset(message_label_window))

def reset(window):
    backButton.configure(text="<--Back", command=homePage)
    submit_button.configure(text="Set!", command=set)
    canvas.itemconfigure(window, state='hidden')
    homePage()

def set():
    thread.start_new_thread(play, ('sounds/Click.wav',))
    message_label = tk.Label(font=("Helvetica", 15), bg='#ffef5e', borderwidth=7, relief="raised")

    if len(board.hand) != 3:
        message_label.configure(text="Select Three Cards!")

    elif setChecker(*board.hand):
        thread.start_new_thread(play, ('sounds/Victory.wav',))
        message_label.configure(text="Correct")
        hand = board.hand
        board.change_cards(hand)

        for card in hand:
            row, column = card.position
            position = column * 4 + row
            card = board.check_card((row, column))
            if card is not None:
                card.img = PhotoImage(file=card.image_file)
                card_buttons[position].configure(image=card.img, bg="white", command=partial(select_card, position))
            else:
                card_buttons[position].configure(image=pix, bg="white", width=200, height=150, compound="c",
                                                 state='disabled')

        board.hand = []
        board.score += 1
        board.is_a_set_on_board(board.positions.values())

    else:
        thread.start_new_thread(play, ('sounds/Boo.wav',))
        message_label.configure(text=property_checker(board.hand))
        if board.score > 0:
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
    canvas.itemconfigure(submit_button_window, state='normal')
    canvas.itemconfigure(back_button_window, state='normal')
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


    board.is_a_set_on_board(board.positions.values())

def play(sound_file_name):
    return PlaySound(sound_file_name, SND_ASYNC)


def howToPlay():
    thread.start_new_thread(play, ('sounds/Click.wav',))
    canvas.itemconfigure(start_button_window, state='hidden')
    canvas.itemconfigure(multiplayer_button_window, state='hidden')
    canvas.itemconfigure(how_to_button_window, state='hidden')
    canvas.itemconfigure(back_button_window, state='normal')
    canvas.itemconfigure(wiki_window, state='normal')
    canvas.itemconfigure(example_background, state='normal')
    for image in example_images:
        canvas.itemconfigure(image[0], state='normal')

def highScore():
    global high_score_windows
    file = open("scores/HighScores", "r")
    high_score_number = 0
    high_score_windows = []

    for highScore in file:
        high_score_number += 1
        high_scores.append(highScore)
        high_score_label = tk.Label(text = highScore,  font = ('helvetica',20),bg = canvas['background'])

        high_score_window = canvas.create_window(500, 50 + 50*high_score_number, window=high_score_label)
        high_score_windows.append(high_score_window)
    file.close()

    thread.start_new_thread(play, ('sounds/Click.wav',))
    canvas.itemconfigure(start_button_window, state = 'hidden')
    canvas.itemconfigure(multiplayer_button_window, state='hidden')
    canvas.itemconfigure(how_to_button_window, state='hidden')
    canvas.itemconfigure(back_button_window, state='normal')


def settings():
    pass

def homePage():
    global board

    for high_score_window in high_score_windows:
        canvas.itemconfigure(high_score_window, state = 'hidden')

    # need to fix this so that the button sound still plays with the music
    # may need to switch to pygame mixer...
    # thread.start_new_thread(play, ('sounds/Click.wav',))

    # Title screen music
    PlaySound('sounds/MusicTrack.wav', SND_FILENAME | SND_LOOP | SND_ASYNC)
    # thread.start_new_thread(play, ('sounds/MusicTrack.wav',))

    for card_window in card_windows:
        canvas.itemconfigure(card_window, state='hidden')

    canvas.itemconfigure(score_label_window, state='hidden')

    board = Board()

    canvas.itemconfigure(submit_button_window, state='hidden')

    canvas.itemconfigure(back_button_window, state='hidden')

    canvas.itemconfigure(wiki_window, state='hidden')
    canvas.itemconfigure(example_background, state='hidden')
    for image in example_images:
        canvas.itemconfigure(image[0], state='hidden')

    canvas.itemconfigure(start_button_window, state='normal')
    canvas.itemconfigure(multiplayer_button_window, state='normal')
    canvas.itemconfigure(how_to_button_window, state='normal')

# Title screen music
PlaySound('sounds/MusicTrack.wav', SND_FILENAME | SND_LOOP | SND_ASYNC)
pix = tk.PhotoImage(width=1, height=1)  # used to make an empty card space

startButton = tk.Button(command=startGame, text='Start Game', width = 20, height = 2, bg = '#ffef5e',
                        font = ('helvetica',18), relief=RAISED, cursor="hand2")
highScoreButton = tk.Button(command=highScore, text='High Scores', width = 20, height = 2, bg ='#ffef5e',
                            font = ('helvetica',18), relief=RAISED, cursor="hand2")
howToButton = tk.Button(command=howToPlay, text='How To Play', width = 20, height = 2, bg = '#ffef5e',
                        font = ('helvetica',18), relief=RAISED, cursor="hand2")
backButton = tk.Button(command=homePage, text='<--Back', bg = '#ffef5e', relief=RAISED, cursor="hand2")

settings_button = tk.Button(command=settings, text='Start Game', width=2, height=2, bg='#ffef5e',
                            font=('helvetica', 18), relief=RAISED, cursor="hand2", anchor=NE)
settings_button_window = canvas.create_window(985, 0, window=settings_button)

start_button_window = canvas.create_window(500, 150, window=startButton)
multiplayer_button_window = canvas.create_window(500, 300, window=highScoreButton)
how_to_button_window = canvas.create_window(500, 450, window=howToButton)
back_button_window = canvas.create_window(40, 40, window=backButton, state='hidden')
submit_button = tk.Button(command=set, text='Set!', bg='#ffef5e', width=10, height=1,
                          font=('helvetica', 18), relief=RAISED, cursor="hand2")
submit_button_window = canvas.create_window(500, 525, window=submit_button)

canvas.itemconfigure(submit_button_window, state='hidden')

canvas.pack()

score_label = tk.Label(text=f"Score: {board.score}", font=("Helvetica", 32), bg='#ff4733', foreground='white')
score_label_window = canvas.create_window(800, 525, window=score_label, state='hidden', width=300)

wiki_text = "Rules: \nThe purpose of this game is to get as many 'Sets' as possible.\n" \
            "Tweleve cards are laid out on a board.\n" \
            "Each card has four properties:\n" \
            "Color: red, blue, green\n" \
            "Shape: circle, triangle, square\n" \
            "Fill: solid, shaded, clear\n" \
            "Count: one, two, three\n" \
            "A 'Set' is made if for each property all three cards match or all three cards are disjoint.\n" \
            "One point is added for each correct 'Set' and one point is deducted for each invalid 'Set.'\n" \
            "Example Sets:"
example_images = []
example_sets = [
    ("CardImages/blue solid triangle1.gif",
     "CardImages/blue solid triangle2.gif",
     "CardImages/blue solid triangle3.gif"),
    ("CardImages/blue solid circle2.gif",
     "CardImages/red shaded triangle2.gif",
     "CardImages/green clear square2.gif"),
]

example_background = canvas.create_rectangle(200, 275, 800, 575, fill='white', state='hidden')
for i, e_set in enumerate(example_sets):
    for j, card in enumerate(e_set):
        img = PhotoImage(file=card)
        example_images.append(
            (canvas.create_image(j * 200 + 200, i * 150 + 275, image=img, state='hidden', anchor=NW), img))

wiki = tk.Label(text=wiki_text, bg='#ff4733', font=("Helvetica", 15), foreground='white')
wiki_window = canvas.create_window(500, 150, window=wiki, state='hidden')

root.mainloop()
