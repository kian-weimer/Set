import tkinter as tk
from tkinter import *
from classes.board import Board
from functools import partial
import _thread as thread
import time

from functions.property_checker import property_checker
from functions.setChecker import *
from winsound import *
from functions.wiki_info import wiki_text, example_sets

root = tk.Tk()
root.attributes("-topmost", True)

canvas = tk.Canvas(root, width=1000, height=600, bg='#ff4733', highlightthickness=0)
root.configure(bg='#ff4733')
card_buttons = []
high_scores = []
card_windows = []
high_score_windows = []
example_images = []  # stores example set images for the how to page
enable_audio=True
enable_cheats=False

current_menu = "homePage"


def select_card(position):
    """
    Select on unselect a single card on the board.
        No more than three cards can be selected at one time
    :param position: the position of the card on the board 0-11
    :return: None
    """
    thread.start_new_thread(play, ('sounds/Click.wav',))
    row = position % 4
    column = position // 4

    # unselect a card if already selected
    if card_buttons[position].cget('bg') == "#fcff66":
        board.remove_card((row, column))

        # change the colors of various objects
        card_buttons[position].configure(bg='white')
        canvas.configure(bg='white')
        root.configure(bg='white')
        score_label.configure(bg='white', fg='black')
        wiki.configure(bg='white', fg='black')
        settings_button.configure(bg='white')
        settings_label.configure(bg='white')
        canvas.itemconfigure(settings_background, fill='white')

    # otherwise select the card if there is not already three cards in the players 'hand'
    else:
        if board.select_card((row, column)):  # enters if the card select was successful

            # change the colors of various objects
            card_buttons[position].configure(bg="#fcff66")
            score_label.configure(bg=board.check_card((row, column)).getColor(), fg='white')
            wiki.configure(bg=board.check_card((row, column)).getColor(), fg='white')
            canvas.configure(bg=board.check_card((row, column)).getColor())
            root.configure(bg=board.check_card((row, column)).getColor())
            settings_button.configure(bg=board.check_card((row, column)).getColor())
            settings_label.configure(bg=board.check_card((row, column)).getColor())
            canvas.itemconfigure(settings_background, fill=board.check_card((row, column)).getColor())


def end_game(early_end=False):
    """
    Ends the current game and displays score
    :param early_end: If True displays additional message stating that game ended early
    :return: None
    """
    rank = 1

    # construct end game message
    end_message = f"Game Over!\n" + early_end * "There are no possible sets on the board.\n" + \
                  f"You are rank {rank} with score {board.score}"

    # create end game windows and modify buttons to allow for more exit options
    message_label = tk.Label(font=("Helvetica", 15), bg='#ffef5e', borderwidth=7, relief="raised")
    message_label.configure(text=end_message)
    message_label_window = canvas.create_window(500, 250, window=message_label)
    submit_button.configure(text="Exit", command=lambda: reset(message_label_window))
    backButton.configure(command=lambda: reset(message_label_window))


def set():
    """
    Checks if a set has been made and updates the score accordingly.
        Three cards on the board must be selected
    :return: None
    """
    if enable_cheats:
        for row, column in board.is_a_set_on_board(board.positions.values(), True):
            position = column * 4 + row
            if card_buttons[position].cget("bg") == "teal":
                card_buttons[position].configure(bg="white")

    thread.start_new_thread(play, ('sounds/Click.wav',))  # playing a sound in a new thread allows for overlap

    # create a location for reply message to be displayed
    message_label = tk.Label(font=("Helvetica", 15), bg='#ffef5e', borderwidth=7, relief="raised")

    # requires player to select three
    if len(board.hand) != 3:
        message_label.configure(text="Select Three Cards!")

    # if players 'hand' is a valid set, increase score and swap out cards
    elif setChecker(*board.hand):
        thread.start_new_thread(play, ('sounds/Victory.wav',))  # play victory sound
        message_label.configure(text="Correct")
        hand = board.hand
        board.change_cards(hand)

        # swap the selected cards out with new ones
        for player_card in hand:
            row, column = player_card.position
            position = column * 4 + row
            player_card = board.check_card((row, column))
            if player_card is not None:
                player_card.img = PhotoImage(file=player_card.image_file)
                card_buttons[position].configure(image=player_card.img, bg="white",
                                                 command=partial(select_card, position))
            else:
                card_buttons[position].configure(image=pix, bg="white", width=200, height=150, compound="c",
                                                 state='disabled')

        # clear hand and reset the score
        board.hand = []
        board.score += 1

        # end the game if there are no valid sets remaining on the board
        if not board.is_a_set_on_board(board.positions.values()):
            end_game(True)
            return

    # if players 'hand' is an invalid set, decrease score
    else:
        thread.start_new_thread(play, ('sounds/Boo.wav',))  # play failure sound
        message_label.configure(text=property_checker(board.hand))
        if board.score > 0:
            board.score -= 1

    if enable_cheats:
        for row, column in board.is_a_set_on_board(board.positions.values(), True):
            position = column * 4 + row
            card_buttons[position].configure(bg="teal")

    message_label_window = canvas.create_window(500, 250, window=message_label)
    thread.start_new_thread(hide_after_seconds, (message_label_window, 2))  # message disappears after two seconds
    score_label.configure(text=f"Score: {board.score}")  # update score


def hide_after_seconds(window, seconds):
    """
    Will hide a given window after x seconds. To be ran in a new thread.
    :param window: the window to hide
    :param seconds: The number of seconds to wait before hiding the window
    :return: None
    """
    time.sleep(seconds)
    canvas.itemconfigure(window, state='hidden')


def startGame():
    """
    Actual gameplay menu. Sets up the board gui and makes the game playable.
    :return: None
    """
    global current_menu
    global board

    reset()  # clears the menu that was previously open

    current_menu = "startGame"  # set this page as the new current menu
    thread.start_new_thread(play, ('sounds/Click.wav',))  # plays button click sound

    # create a new board
    board = Board()

    # Creates the initial twelve cards on the board
    for j in range(12):
        row = j % 4
        column = j // 4
        card = board.check_card((row, column))
        img = PhotoImage(file=card.image_file)
        card.image = img
        card_button = tk.Button(image=img, bg="white")
        card_button.configure(command=partial(select_card, j))
        card_buttons.append(card_button)

        single_card_window = canvas.create_window(row * 200 + 100, column * 150, window=card_button, anchor=NW)
        card_windows.append(single_card_window)

    if enable_cheats:
        for row, column in board.is_a_set_on_board(board.positions.values(), True):
            position = column * 4 + row
            print(position)
            card_buttons[position].configure(bg="teal")

    # end the game if there are no valid sets remaining on the board
    if not board.is_a_set_on_board(board.positions.values()):
        end_game(True)
        return

    # make buttons visible
    make_visible([submit_button_window, back_button_window, score_label_window])


def play(sound_file_name):
    """
    plays a sound
    :param sound_file_name: The file location of the desired sound
    :return: The sound object created
    """
    if enable_audio:
        return PlaySound(sound_file_name, SND_ASYNC)


def make_visible(windows: []):
    """
    Makes all windows in the given list visible
    :param windows: a list of windows
    :return: None
    """
    for window in windows:
        canvas.itemconfigure(window, state='normal')


def howToPlay():
    """
    A wiki containing info on how to play the game
    :return: None
    """
    global current_menu

    reset()  # clears the menu that was previously open
    canvas.itemconfigure(settings_button_window, state='hidden')

    current_menu = "howToPlay"  # set this page as the new current menu
    thread.start_new_thread(play, ('sounds/Click.wav',))  # plays button click sound

    # makes wiki windows visible
    make_visible([back_button_window, wiki_window, example_background, *[image[0] for image in example_images]])


def highScore():
    """
    Menu which saves the top 10 highest scores
    :return: None
    """
    global current_menu
    global high_score_windows

    reset()  # clears the menu that was previously open

    current_menu = "highScore"  # set this page as the new current menu
    thread.start_new_thread(play, ('sounds/Click.wav',))  # plays button click sound

    high_score_number = 0

    with open("scores/HighScores", "r") as file:
        for highScore in file:
            high_score_number += 1
            high_scores.append(highScore)
            high_score_label = tk.Label(text=highScore, font=('helvetica', 20), bg=canvas['background'])

            high_score_window = canvas.create_window(500, 50 + 50 * high_score_number, window=high_score_label)
            high_score_windows.append(high_score_window)

    make_visible([back_button_window])


def homePage():
    """
    Home menu which directs the user to all other menus
    :return: None
    """
    global board
    global current_menu

    reset()  # clears the menu that was previously open

    current_menu = "homePage"  # set this page as the new current menu
    if enable_audio:
        PlaySound('sounds/MusicTrack.wav', SND_LOOP | SND_ASYNC)  # Title screen music

    make_visible([start_button_window, multiplayer_button_window, how_to_button_window])


def reset(window=None):
    """
    Hides all windows on the canvas, determined by global variable current_menu
    :param window: Will hide an additional window if passed (used to hide non-global windows)
    :return: None
    """
    # close the settings window if it is open
    if settings_open:
        settings()

    # hide any additional windows passed
    if window is not None:
        canvas.itemconfigure(window, state='hidden')

    # clear high score windows
    if current_menu == "highScore":
        for high_score_window in high_score_windows:
            canvas.itemconfigure(high_score_window, state='hidden')
        canvas.itemconfigure(back_button_window, state='hidden')
        high_score_windows.clear()

    # clear homePage windows
    if current_menu == "homePage":
        canvas.itemconfigure(start_button_window, state='hidden')
        canvas.itemconfigure(multiplayer_button_window, state='hidden')
        canvas.itemconfigure(how_to_button_window, state='hidden')

    # clear howToPlay windows
    if current_menu == "howToPlay":
        canvas.itemconfigure(settings_button_window, state='normal')
        canvas.itemconfigure(wiki_window, state='hidden')
        canvas.itemconfigure(example_background, state='hidden')
        canvas.itemconfigure(back_button_window, state='hidden')
        for image in example_images:
            canvas.itemconfigure(image[0], state='hidden')

    # clear startGame windows
    # this must be the last check since it can include a homePage function call
    if current_menu == "startGame":
        # clear high score windows
        for card_window in card_windows:
            canvas.itemconfigure(card_window, state='hidden')
        canvas.itemconfigure(score_label_window, state='hidden')
        canvas.itemconfigure(submit_button_window, state='hidden')
        canvas.itemconfigure(back_button_window, state='hidden')

        # empty the lost of card buttons and windows
        card_buttons.clear()
        card_windows.clear()

        # occurs if a game has ended
        if submit_button.cget("text") != "Set!":
            backButton.configure(text="<--Back", command=homePage)
            submit_button.configure(text="Set!", command=set)
            homePage()


# doesn't follow typical menu structure since it is a pop up
settings_open = False

def settings():
    """
    Popup menu containing game settings
    :return:
    """
    global current_menu
    global settings_open
    global card_window

    # closes settings pop up if already open
    if settings_open:
        canvas.itemconfigure(settings_background, state='hidden')
        canvas.itemconfigure(audio_button_window, state='hidden')
        canvas.itemconfigure(cheat_button_window, state='hidden')
        settings_open = False
        if len(card_windows):
            canvas.itemconfigure(card_windows[3], state='normal')
            canvas.itemconfigure(card_windows[7], state='normal')

        canvas.itemconfigure(settings_label_window, state='hidden')

    # otherwise opens the settings menu
    else:
        if len(card_windows) > 0:
            canvas.itemconfigure(card_windows[3], state='hidden')
            canvas.itemconfigure(card_windows[7], state='hidden')

        canvas.itemconfigure(settings_background, state='normal')
        canvas.itemconfigure(audio_button_window, state='normal')
        canvas.itemconfigure(cheat_button_window, state='normal')
        canvas.itemconfigure(settings_label_window, state='normal')
        settings_open = True


def toggle_audio():
    global enable_audio
    play(None)
    enable_audio = bool(not enable_audio)
    if enable_audio:
        audio_button.configure(text="Disable Audio")
        if current_menu == "homePage":
            PlaySound('sounds/MusicTrack.wav', SND_LOOP | SND_ASYNC)  # Title screen music
    else:
        audio_button.configure(text="Enable Audio")


def toggle_cheats():
    global enable_cheats

    enable_cheats = bool(not enable_cheats)
    if enable_cheats:
        cheat_button.configure(text="Disable Cheats")
        for row, column in board.is_a_set_on_board(board.positions.values(), True):
            position = column * 4 + row
            if card_buttons[position].cget("bg") == "white":
                card_buttons[position].configure(bg="teal")


    else:
        cheat_button.configure(text="Enable Cheats")
        for row, column in board.is_a_set_on_board(board.positions.values(), True):
            position = column * 4 + row
            if card_buttons[position].cget("bg") == "teal":
                card_buttons[position].configure(bg="white")


PlaySound('sounds/MusicTrack.wav', SND_FILENAME | SND_LOOP | SND_ASYNC)  # Title screen music
pix = tk.PhotoImage(width=1, height=1)  # used to make an empty card space

startButton = tk.Button(command=startGame, text='Start Game', width=20, height=2, bg='#ffef5e',
                        font=('helvetica', 18), relief=RAISED, cursor="hand2")
highScoreButton = tk.Button(command=highScore, text='High Scores', width=20, height=2, bg='#ffef5e',
                            font=('helvetica', 18), relief=RAISED, cursor="hand2")
howToButton = tk.Button(command=howToPlay, text='How To Play', width=20, height=2, bg='#ffef5e',
                        font=('helvetica', 18), relief=RAISED, cursor="hand2")
backButton = tk.Button(command=homePage, text='<--Back', bg='#ffef5e', relief=RAISED, cursor="hand2")
settings_button = tk.Button(command=settings, text='⚙', width=2, height=1, bg='#ff4733', fg='black',
                            font=('helvetica', 25), cursor="hand2", anchor=NE, relief=FLAT, activebackground='#ff4733')
audio_button = tk.Button(command=toggle_audio, text='Disable Audio', width=12, height=2, bg='#ffef5e',
                         font=('helvetica', 12), relief=RAISED, cursor="hand2")
cheat_button = tk.Button(command=toggle_cheats, text='Enable Cheats', width=12, height=2, bg='#ffef5e',
                         font=('helvetica', 12), relief=RAISED, cursor="hand2")
submit_button = tk.Button(command=set, text='Set!', bg='#ffef5e', width=10, height=1,
                          font=('helvetica', 18), relief=RAISED, cursor="hand2")
settings_label = tk.Label(font=("Helvetica", 15), bg=settings_button.cget('bg'), text="Settings:")


start_button_window = canvas.create_window(500, 150, window=startButton)
multiplayer_button_window = canvas.create_window(500, 300, window=highScoreButton)
how_to_button_window = canvas.create_window(500, 450, window=howToButton)
back_button_window = canvas.create_window(40, 40, window=backButton, state='hidden')
settings_button_window = canvas.create_window(985, 30, window=settings_button)
settings_label_window = canvas.create_window(850, 25, window=settings_label, state='hidden')
audio_button_window = canvas.create_window(850, 75, window=audio_button, state='hidden')
cheat_button_window = canvas.create_window(850, 150, window=cheat_button, state='hidden')
submit_button_window = canvas.create_window(500, 525, window=submit_button, state='hidden')

canvas.pack()

score_label = tk.Label(text=f"Score: {0}", font=("Helvetica", 32), bg='#ff4733', foreground='white')
score_label_window = canvas.create_window(800, 525, window=score_label, state='hidden', width=300)

example_background = canvas.create_rectangle(200, 275, 800, 575, fill='white', state='hidden')
settings_background = canvas.create_rectangle(700, 0, 1000, 300, fill='#ff4733', state='hidden')

for i, e_set in enumerate(example_sets):
    for j, card in enumerate(e_set):
        img = PhotoImage(file=card)
        example_images.append(
            (canvas.create_image(j * 200 + 200, i * 150 + 275, image=img, state='hidden', anchor=NW), img))

wiki = tk.Label(text=wiki_text, bg='#ff4733', font=("Helvetica", 15), foreground='white')
wiki_window = canvas.create_window(500, 150, window=wiki, state='hidden')

root.mainloop()
