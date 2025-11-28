import tkinter as tk
import random

def JokesWithLoad(filename="randomJokes.txt"):
    jokes = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                if '?' in line:
                    setup, punchline = line.strip().split('?')
                    jokes.append((setup + "?", punchline))
    except FileNotFoundError:
        jokes.append(("Joke file not found!", "Please check the file path."))
    return jokes

def TellingOfJoke():
    global JokeOfCurrent
    JokeOfCurrent = random.choice(jokes)
    joke_text.set(JokeOfCurrent[0])
    TextWithPunchline.set("")

def show_punchline(event=None):
    if JokeOfCurrent:
        TextWithPunchline.set(JokeOfCurrent[1])

def quit_app():
    IfInRoot.destroy()

jokes = JokesWithLoad()
JokeOfCurrent = None
 
IfInRoot = tk.Tk()
IfInRoot.title("Alexa Tell Me a Joke")
IfInRoot.geometry("800x800")
IfInRoot.config(bg='#ffd6ff')

joke_text = tk.StringVar()
TextWithPunchline = tk.StringVar()

LayoutOfOuterFrame = tk.Frame(IfInRoot, bg='#ffd6ff', bd=5, relief='solid')
LayoutOfOuterFrame.pack(padx=10, pady=10, fill='both', expand=True)

LabelingOfJoke = tk.Label(LayoutOfOuterFrame, textvariable=joke_text, wraplength=350, font=("Arial", 24), bg='#ffd6ff', bd=2, relief="solid")
LabelOfPunchline = tk.Label(LayoutOfOuterFrame, textvariable=TextWithPunchline, wraplength=350, font=("Arial", 24, "italic"), bg='#ffd6ff', bd=2, relief="solid")
ButtonIsTellingJoke = tk.Button(LayoutOfOuterFrame, text="Tell me a Joke", command=TellingOfJoke, width=30,font=("Arial", 24, "italic"), relief="raised", bg='#d9a7f1', borderwidth=3)
ButtonOfQuit = tk.Button(LayoutOfOuterFrame, text="Quit", command=quit_app, width=30,font=("Arial", 24, "italic"), relief="raised", bg='#d9a7f1', borderwidth=3)


LabelingOfInstructions = tk.Label(LayoutOfOuterFrame, text="Press Enter for answer", font=("Arial", 20, "italic"), bg='#ffd6ff')


LabelingOfJoke.pack(pady=20, padx=10) 
LabelOfPunchline.pack(pady=20, padx=10)
ButtonIsTellingJoke.pack(pady=10)
ButtonOfQuit.pack(pady=5)
LabelingOfInstructions.pack(pady=20)


IfInRoot.bind('<Return>', show_punchline)


IfInRoot.mainloop()
