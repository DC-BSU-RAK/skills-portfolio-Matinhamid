import tkinter as tk
from tkinter import messagebox, Toplevel
import random
import threading
import os
from PIL import Image, ImageTk

BG_IMAGE_FILE = "background1.jpg"

# --- Absolute Paths ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BG_IMAGE_PATH = os.path.join(SCRIPT_DIR, BG_IMAGE_FILE)

if not os.path.exists(BG_IMAGE_PATH):
    print(f"Warning: Background image not found at: {BG_IMAGE_PATH}")
    BG_IMAGE_PATH = None

# --- Global Variables ---
SCORE = 0
QUESTION_COUNT = 0
MAX_QUESTIONS = 10
DIFFICULTY = 0
CURRENT_ANSWER = 0
ATTEMPTS_LEFT = 2
PROBLEM_STRING = ""
USER_NAME = ""
INSTITUTION = ""
answer_entry = None
feedback_label = None
CURRENT_HINT = ""
BG_LABEL = None
ORIGINAL_BG_IMAGE = None
BG_PHOTO = None

# --- Colors (Soft Pink Pastel Theme) ---
COLOR_PALETTE = {
    "BG_PRIMARY": "#00C4FA",      
    "BG_SECONDARY": "#00D5FF",
    "FG_PRIMARY": "#000000", 
    "FG_SECONDARY": "#000000",    
    "ACCENT_PRIMARY": "#00098D",  
    "ACCENT_SUCCESS": "#FF0000",  
    "ACCENT_FAIL": "#000000",     
    "ENTRY_BG": "#FFFFFF",        
    "ACCENT_BLACK": "#000000" 
}

# --- Difficulty Map ---
DIFFICULTY_MAP = {
    1: (0, 9, "Single-Digit (0-9)"),
    2: (10, 99, "Double-Digit (10-99)"),
    3: (1000, 9999, "Four-Digit (1000-9999)")
}


# --- Utility ---
def clear_frame(frame):
    for widget in frame.winfo_children():
        if widget != BG_LABEL:
            widget.destroy()

def randomInt(min_val, max_val):
    return random.randint(min_val, max_val)

def decideOperation():
    return random.choice(['+', '-'])

def get_rank(final_score):
    if final_score >= 90: return "A+"
    elif final_score >= 80: return "A"
    elif final_score >= 70: return "B"
    elif final_score >= 60: return "C"
    else: return "D"

def get_hint(num1, num2, operation):
    return "Hint: Addition problem." if operation=='+' else "Hint: Subtraction problem."

def generateProblem():
    global CURRENT_ANSWER, PROBLEM_STRING, ATTEMPTS_LEFT
    min_val, max_val, _ = DIFFICULTY_MAP.get(DIFFICULTY, (0,9,""))
    num1 = randomInt(min_val, max_val)
    num2 = randomInt(min_val, max_val)
    operation = decideOperation()
    CURRENT_ANSWER = num1+num2 if operation=='+' else num1-num2
    PROBLEM_STRING = f"{num1} {operation} {num2} ="
    ATTEMPTS_LEFT = 2
    return PROBLEM_STRING, num1, num2, operation

def isCorrect(user_answer, current_answer):
    try:
        return int(user_answer) == current_answer
    except:
        return False

def quitQuizEarly():
    if messagebox.askyesno("Exit Quiz", "Are you sure you want to quit?"):
        window.quit()

# --- Background Image ---
def resize_background(event):
    global ORIGINAL_BG_IMAGE, BG_PHOTO, BG_LABEL
    if ORIGINAL_BG_IMAGE and BG_LABEL:
        new_width = event.width
        new_height = event.height
        resized_image = ORIGINAL_BG_IMAGE.resize((new_width, new_height), Image.Resampling.LANCZOS)
        BG_PHOTO = ImageTk.PhotoImage(resized_image)
        BG_LABEL.config(image=BG_PHOTO)
        BG_LABEL.image = BG_PHOTO

def set_background(frame):
    global ORIGINAL_BG_IMAGE, BG_LABEL
    if not BG_IMAGE_PATH:
        return
    if ORIGINAL_BG_IMAGE is None:
        ORIGINAL_BG_IMAGE = Image.open(BG_IMAGE_PATH)
    if BG_LABEL is None:
        BG_LABEL = tk.Label(frame)
        BG_LABEL.place(x=0,y=0,relwidth=1,relheight=1)
        BG_LABEL.lower()
        frame.bind('<Configure>', resize_background)
    class DummyEvent:
        def __init__(self, width, height):
            self.width = width
            self.height = height
    resize_background(DummyEvent(frame.winfo_width(), frame.winfo_height()))

# --- GUI Screens ---
def displayWelcomeScreen():
    clear_frame(main_frame)
    window.title("Ultimate Math Challenge")
    main_frame.config(bg=COLOR_PALETTE["BG_PRIMARY"])
    set_background(main_frame)
    
    card = tk.Frame(main_frame, bg=COLOR_PALETTE["BG_SECONDARY"], padx=40,pady=40)
    card.pack(pady=70,padx=20)
    tk.Label(card,text="Ultimate Arithmetic Quiz", font=('Inter',22,'bold'),
             fg=COLOR_PALETTE["ACCENT_PRIMARY"], bg=COLOR_PALETTE["BG_SECONDARY"]).pack(pady=(10,20))
    tk.Label(card,text="Test your addition and subtraction skills across three difficulty levels!",
             font=('Inter',12), fg=COLOR_PALETTE["FG_PRIMARY"], bg=COLOR_PALETTE["BG_SECONDARY"], wraplength=380, justify='center').pack(pady=20)
    tk.Button(card,text="Start Registration", command=displayStartScreen, font=('Inter',14,'bold'),
              bg=COLOR_PALETTE["ACCENT_PRIMARY"], fg="white", relief='flat', padx=20, pady=10, width=20).pack(pady=10)

def displayStartScreen():
    clear_frame(main_frame)
    window.title("Quiz Registration")
    main_frame.config(bg=COLOR_PALETTE["BG_PRIMARY"])
    set_background(main_frame)
    
    card = tk.Frame(main_frame, bg=COLOR_PALETTE["BG_SECONDARY"], padx=40,pady=40)
    card.pack(pady=70,padx=20)
    
    tk.Label(card,text="Math Quiz Registration", font=('Inter',20,'bold'), fg=COLOR_PALETTE["ACCENT_PRIMARY"], bg=COLOR_PALETTE["BG_SECONDARY"]).pack(pady=15)
    
    tk.Label(card,text="Your Name:", anchor='w', font=('Inter',12), fg=COLOR_PALETTE["FG_PRIMARY"], bg=COLOR_PALETTE["BG_SECONDARY"]).pack(fill='x', pady=(15,5))
    global name_entry
    name_entry = tk.Entry(card, font=('Inter',14), width=30, bd=1, relief='solid', fg=COLOR_PALETTE["FG_PRIMARY"], bg=COLOR_PALETTE["ENTRY_BG"], insertbackground=COLOR_PALETTE["FG_PRIMARY"])
    name_entry.pack(pady=(0,15))
    
    tk.Label(card,text="Institution:", anchor='w', font=('Inter',12), fg=COLOR_PALETTE["FG_PRIMARY"], bg=COLOR_PALETTE["BG_SECONDARY"]).pack(fill='x', pady=(15,5))
    global inst_entry
    inst_entry = tk.Entry(card, font=('Inter',14), width=30, bd=1, relief='solid', fg=COLOR_PALETTE["FG_PRIMARY"], bg=COLOR_PALETTE["ENTRY_BG"], insertbackground=COLOR_PALETTE["FG_PRIMARY"])
    inst_entry.pack(pady=(0,30))
    
    tk.Button(card,text="Start Quiz", command=processStartDetails, font=('Inter',14,'bold'),
              bg=COLOR_PALETTE["ACCENT_SUCCESS"], fg=COLOR_PALETTE["FG_PRIMARY"], relief='flat', padx=20, pady=10, width=20).pack(pady=10)

def processStartDetails():
    global USER_NAME, INSTITUTION
    name = name_entry.get().strip()
    institution = inst_entry.get().strip()
    if not name or not institution:
        messagebox.showerror("Input Error","Please enter both Name and Institution.")
        return
    USER_NAME = name
    INSTITUTION = institution
    displayMenu()

def displayMenu():
    clear_frame(main_frame)
    window.title("Math Quiz | Select Difficulty")
    main_frame.config(bg=COLOR_PALETTE["BG_PRIMARY"])
    set_background(main_frame)
    
    card = tk.Frame(main_frame, bg=COLOR_PALETTE["BG_SECONDARY"], padx=40,pady=40)
    card.pack(pady=70,padx=20)
    tk.Label(card,text="Select Difficulty", font=('Inter',20,'bold'), fg=COLOR_PALETTE["ACCENT_PRIMARY"], bg=COLOR_PALETTE["BG_SECONDARY"]).pack(pady=15)
    
    for level, (_,_,desc) in DIFFICULTY_MAP.items():
        tk.Button(card,text=f"{level}. {desc}", command=lambda l=level: startQuiz(l), width=25,
                  font=('Inter',14), bg=COLOR_PALETTE["ACCENT_PRIMARY"], fg="white").pack(pady=10)

def startQuiz(level):
    global DIFFICULTY, SCORE, QUESTION_COUNT
    DIFFICULTY = level
    SCORE = 0
    QUESTION_COUNT = 0
    
    displayProblem()

def displayProblem():
    global QUESTION_COUNT, answer_entry, feedback_label, CURRENT_HINT
    clear_frame(main_frame)
    window.title(f"Math Quiz | Question {QUESTION_COUNT+1}")
    main_frame.config(bg=COLOR_PALETTE["BG_PRIMARY"])
    set_background(main_frame)
    
    control_frame = tk.Frame(main_frame, bg=COLOR_PALETTE["BG_PRIMARY"])
    control_frame.pack(fill='x', padx=10, pady=5)
    tk.Button(control_frame,text="❌ Quit Test", command=quitQuizEarly, bg=COLOR_PALETTE["ACCENT_FAIL"], fg="white").pack(side=tk.RIGHT)
    tk.Label(control_frame,text=f"Score: {SCORE} | Question: {QUESTION_COUNT+1} of {MAX_QUESTIONS}",
             bg=COLOR_PALETTE["BG_PRIMARY"], fg=COLOR_PALETTE["FG_SECONDARY"]).pack(side=tk.LEFT)
    
    problem_card = tk.Frame(main_frame, bg=COLOR_PALETTE["BG_SECONDARY"], padx=30,pady=30)
    problem_card.pack(pady=10)
    
    problem_text, num1, num2, operation = generateProblem()
    CURRENT_HINT = get_hint(num1,num2,operation)
    
    tk.Label(problem_card,text=problem_text, font=('Inter',40,'bold'), bg=COLOR_PALETTE["BG_SECONDARY"], fg=COLOR_PALETTE["FG_PRIMARY"]).pack(pady=20)
    
    answer_entry = tk.Entry(problem_card, font=('Inter',20), width=15, justify='center', bd=2, relief='solid', bg=COLOR_PALETTE["ENTRY_BG"], fg=COLOR_PALETTE["FG_PRIMARY"], insertbackground=COLOR_PALETTE["FG_PRIMARY"])
    answer_entry.pack(pady=15)
    answer_entry.focus_set()
    
    feedback_label = tk.Label(main_frame,text="", font=('Inter',14), bg=COLOR_PALETTE["BG_PRIMARY"])
    feedback_label.pack()
    
    tk.Button(problem_card,text="Submit Answer", command=submitAnswer, bg=COLOR_PALETTE["ACCENT_PRIMARY"], fg="white").pack(pady=20)

def submitAnswer():
    global SCORE, QUESTION_COUNT, ATTEMPTS_LEFT
    user_input = answer_entry.get().strip()
    feedback_label.config(text="")
    if not user_input:
        feedback_label.config(text="Please enter an answer.", fg=COLOR_PALETTE["ACCENT_FAIL"])
        return
    if isCorrect(user_input,CURRENT_ANSWER):
        score_awarded = 10 if ATTEMPTS_LEFT==2 else 5
        SCORE += score_awarded
        feedback_label.config(text=f"✅ Correct! (+{score_awarded} points)", fg=COLOR_PALETTE["ACCENT_SUCCESS"])
        QUESTION_COUNT += 1
        answer_entry.delete(0,tk.END)
        window.after(500,nextQuestionOrEnd)
    else:
        ATTEMPTS_LEFT -= 1
        if ATTEMPTS_LEFT==1:
            message = f"Incorrect. One attempt left (5 points available)."
            show_feedback_window(message, hint=CURRENT_HINT)
            answer_entry.delete(0,tk.END)
            answer_entry.focus_set()
            return
        elif ATTEMPTS_LEFT==0:
            message = f"Incorrect. The correct answer was: {CURRENT_ANSWER}."
            show_feedback_window(message)
            QUESTION_COUNT += 1
            answer_entry.delete(0,tk.END)
            nextQuestionOrEnd()

def show_feedback_window(message, hint=None):
    feedback_window = Toplevel(window)
    feedback_window.title("Feedback")
    feedback_window.geometry("500x300")
    feedback_window.config(bg=COLOR_PALETTE["ACCENT_FAIL"])
    feedback_window.attributes('-topmost', True)
    tk.Label(feedback_window,text=message,font=('Inter',16),bg=COLOR_PALETTE["ACCENT_FAIL"],fg="white").pack(pady=20)
    if hint:
        tk.Label(feedback_window,text=hint,font=('Inter',14),bg=COLOR_PALETTE["ACCENT_FAIL"],fg="white",wraplength=450).pack(pady=10)
    def close_and_unwait():
        feedback_window.destroy()
        window.grab_release()
    tk.Button(feedback_window,text="Continue", command=close_and_unwait, bg="white", fg=COLOR_PALETTE["FG_PRIMARY"]).pack(pady=10)
    feedback_window.grab_set()
    window.wait_window(feedback_window)

def nextQuestionOrEnd():
    if QUESTION_COUNT < MAX_QUESTIONS:
        displayProblem()
    else:
        displayResults()

def displayResults():
    clear_frame(main_frame)
    window.title("Math Quiz | Results")
    main_frame.config(bg=COLOR_PALETTE["BG_PRIMARY"])
    set_background(main_frame)
    
    results_card = tk.Frame(main_frame, bg=COLOR_PALETTE["BG_SECONDARY"], padx=40,pady=40)
    results_card.pack(pady=70,padx=20)
    
    final_score_percentage = (SCORE/(MAX_QUESTIONS*10))*100
    rank = get_rank(final_score_percentage)
    
    tk.Label(results_card,text=f"Quiz Complete, {USER_NAME}!", font=('Inter',20,'bold'), fg=COLOR_PALETTE["FG_PRIMARY"], bg=COLOR_PALETTE["BG_SECONDARY"]).pack(pady=10)
    tk.Label(results_card,text=f"Total Score: {SCORE}/{MAX_QUESTIONS*10}", font=('Inter',16), fg=COLOR_PALETTE["ACCENT_PRIMARY"], bg=COLOR_PALETTE["BG_SECONDARY"]).pack(pady=5)
    tk.Label(results_card,text=f"Final Rank: {rank}", font=('Inter',18,'bold'), fg=COLOR_PALETTE["ACCENT_SUCCESS"], bg=COLOR_PALETTE["BG_SECONDARY"]).pack(pady=10)
    
    tk.Button(results_card,text="Replay", command=displayWelcomeScreen, font=('Inter',14), bg=COLOR_PALETTE["ACCENT_PRIMARY"], fg="white", relief='flat', padx=20,pady=10,width=15).pack(pady=15)
    tk.Button(results_card,text="Exit", command=quitQuizEarly, font=('Inter',14), bg=COLOR_PALETTE["ACCENT_FAIL"], fg="white", relief='flat', padx=20,pady=10,width=15).pack(pady=5)

# --- Main App ---
window = tk.Tk()
window.title("Math Quiz")
window.attributes('-fullscreen', True)
window.bind('<Escape>', lambda e: quitQuizEarly())

main_frame = tk.Frame(window, bg=COLOR_PALETTE["BG_PRIMARY"])
main_frame.pack(expand=True, fill='both')

displayWelcomeScreen()
window.mainloop()
