from tkinter import *
import pandas
import random

df_dict = {}
BACKGROUND_COLOR = "#B1DDC6"
selection = {}
# ----------------------------READING THE DICTIONARY WITH THE WORDS ------------------------------- #
try:
    df = pandas.read_csv('./data/words_to_learn.csv')
except FileNotFoundError:
    original_data = pandas.read_csv('./data/french_words.csv')
    df_dict = original_data.to_dict(orient="records")
else:
    df_dict = df.to_dict(orient="records")


# ---------------------------- Functions to generate random words and check meanings------------------------------- #

def generate_word():
    global selection, flip_timer
    window.after_cancel(flip_timer)
    selection = random.choice(df_dict)
    canvas.itemconfig(word, text=selection['French'], fill='black')
    canvas.itemconfig(language, text="French", fill="black")
    canvas.itemconfig(background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(background, image=card_back_img)
    canvas.itemconfig(word, text=selection['English'], fill='white')
    canvas.itemconfig(language, text="English", fill='white')


def is_known():
    df_dict.remove(selection)
    data = pandas.DataFrame(df_dict)
    data.to_csv("data/words_to_learn.csv", index=False)
    generate_word()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

flip_timer = window.after(3000, func=flip_card)

# canvas initialization
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="./images/card_front.png")
background = canvas.create_image(400, 263, image=card_front_img)
canvas.grid(column=0, row=0, columnspan=2)

card_back_img = PhotoImage(file="./images/card_back.png")

language = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
# button creation
right_image = PhotoImage(file="./images/right.png")
known_button = Button(image=right_image, command=is_known, highlightthickness=0)
known_button.grid(row=1, column=0)

wrong_image = PhotoImage(file="./images/wrong.png")
unknown_button = Button(image=wrong_image, command=generate_word, highlightthickness=0)
unknown_button.grid(row=1, column=1)

generate_word()
window.mainloop()
