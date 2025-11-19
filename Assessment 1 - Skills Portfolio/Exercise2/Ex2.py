import tkinter as tk
import random

#The function is loading for getting jokes from file
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

# The function to displaying  a new  setup of joke 
def TellingOfJoke():
    global JokeOfCurrent
    JokeOfCurrent = random.choice(jokes)
    joke_text.set(JokeOfCurrent[0])  # Showing the setup
    TextWithPunchline.set("")  # To clearing the  punchline

#The  Function is to displaying punchline
def show_punchline(event=None):  # Adding the key press handling event
    if JokeOfCurrent:
        TextWithPunchline.set(JokeOfCurrent[1])

#  Code of the quit of application
def quit_app():
    IfInRoot.destroy()

# The file from where the jokes load 
jokes = JokesWithLoad()
JokeOfCurrent = None

# The set up of the main application window 
IfInRoot = tk.Tk()
IfInRoot.title("Alexa Tell Me a Joke")
IfInRoot.geometry("800x800")  #To Accommodate the new label The adjustment of height 
IfInRoot.config(bg='#ffd6ff')  # Making the setting of background color in light #ffd6ff

# making The string variables for punchline and setup 
joke_text = tk.StringVar()
TextWithPunchline = tk.StringVar()

#  creation of border with an outer frame 
LayoutOfOuterFrame = tk.Frame(IfInRoot, bg='#ffd6ff', bd=5, relief='solid')  # Border added to the outer frame
LayoutOfOuterFrame.pack(padx=10, pady=10, fill='both', expand=True)

#  The widgets
LabelingOfJoke = tk.Label(LayoutOfOuterFrame, textvariable=joke_text, wraplength=350, font=("Arial", 24), bg='#ffd6ff', bd=2, relief="solid")
LabelOfPunchline = tk.Label(LayoutOfOuterFrame, textvariable=TextWithPunchline, wraplength=350, font=("Arial", 24, "italic"), bg='#ffd6ff', bd=2, relief="solid")
ButtonIsTellingJoke = tk.Button(LayoutOfOuterFrame, text="Tell me a Joke", command=TellingOfJoke, width=30,font=("Arial", 24, "italic"), relief="raised", bg='#d9a7f1', borderwidth=3)
ButtonOfQuit = tk.Button(LayoutOfOuterFrame, text="Quit", command=quit_app, width=30,font=("Arial", 24, "italic"), relief="raised", bg='#d9a7f1', borderwidth=3)

# For the instruction make new label
LabelingOfInstructions = tk.Label(LayoutOfOuterFrame, text="Press Enter for answer", font=("Arial", 20, "italic"), bg='#ffd6ff')

# The layout of the frame 
LabelingOfJoke.pack(pady=20, padx=10)   #The padding of layout 
LabelOfPunchline.pack(pady=20, padx=10)
ButtonIsTellingJoke.pack(pady=10)
ButtonOfQuit.pack(pady=5)
LabelingOfInstructions.pack(pady=20)  # Pack of the new instructions which are label

# Bind key for showing punchline (e.g., Enter key) # For showing the punchline binds a key
IfInRoot.bind('<Return>', show_punchline)

# The tkinter loop is start
IfInRoot.mainloop()
