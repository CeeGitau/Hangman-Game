import tkinter as tk
from tkinter import messagebox
import random

# Categorized words based on topics
word_categories = {
    "Music": ["music", "melody", "harmony", "rhythm", "symphony"],
    "Technology": ["programming", "algorithm", "computer", "software", "hardware"],
    "Nature": ["forest", "ocean", "mountain", "river", "desert"],
    "Random": ["wrought", "candid", "zombie", "puzzle", "mystery"]
}

# Initialize variables
guessed_letters = []
attempts = 6

# Create a window
window = tk.Tk()
window.title("Hangman Game")

selected_category = tk.StringVar(value="Random")  # Default category
guess_word = random.choice(word_categories[selected_category.get()])

# Function to update the word list when a new category is selected
def update_word_list(*args):
    global guess_word, guessed_letters, attempts
    guessed_letters = []
    attempts = 6
    guess_word = random.choice(word_categories[selected_category.get()])
    update_word_display()
    update_attempts_display()
    draw_hangman()
    reset_letter_buttons()

# Function to check if the player has won
def check_win():
    return all(letter in guessed_letters for letter in guess_word)

# Function to check if the player has lost
def check_loss():
    return attempts == 0

# Function to handle a letter guess from both input and button clicks
def guess_letter(letter=None):
    global attempts
    if letter is None:  # Input from text entry box
        letter = letter_entry.get().lower()
    
    if letter.isalpha() and len(letter) == 1:
        if letter in guessed_letters:
            messagebox.showinfo("Hangman", f"You've already guessed '{letter}'")
        elif letter in guess_word:
            guessed_letters.append(letter)
            update_word_display()
            if check_win():
                messagebox.showinfo("Hangman", "Congratulations! You win!")
                reset_game()
        else:
            guessed_letters.append(letter)
            attempts -= 1
            update_attempts_display()
            draw_hangman()
            if check_loss():
                messagebox.showinfo("Hangman", "Better luck next time. The word was: " + guess_word)
                reset_game()

        # Disable and cross out letter button
        if letter in letter_buttons:
            letter_buttons[letter].config(state="disabled", fg="red", text=letter + "̶")  # Crossed out
        letter_entry.delete(0, tk.END)  # Clear the input field
    else:
        messagebox.showinfo("Hangman", "Please enter a single letter")

# Function to reset the game
def reset_game():
    update_word_list()

# Function to update the word display
def update_word_display():
    display_word = ""
    for letter in guess_word:
        if letter in guessed_letters:
            display_word += letter
        else:
            display_word += "_"
        display_word += " "
    word_label.config(text=display_word)

# Function to update the attempts display
def update_attempts_display():
    attempts_label.config(text=f"Attempts left: {attempts}")

# Function to draw the hangman figure
def draw_hangman():
    canvas.delete("hangman")
    if attempts < 6:
        canvas.create_oval(125, 125, 175, 175, width=4, tags="hangman")  # Head
    if attempts < 5:
        canvas.create_line(150, 175, 150, 225, width=4, tags="hangman")  # Body
    if attempts < 4:
        canvas.create_line(150, 200, 125, 175, width=4, tags="hangman")  # Left Arm
    if attempts < 3:
        canvas.create_line(150, 200, 175, 175, width=4, tags="hangman")  # Right Arm
    if attempts < 2:
        canvas.create_line(150, 225, 125, 250, width=4, tags="hangman")  # Left Leg
    if attempts < 1:
        canvas.create_line(150, 225, 175, 250, width=4, tags="hangman")  # Right Leg

# Function to reset letter buttons
def reset_letter_buttons():
    for letter, button in letter_buttons.items():
        # Reset button text and appearance
        button.config(state="normal", fg="black", text=letter)   

# Create GUI elements
category_label = tk.Label(window, text="Select Topic:", font=("Arial", 16))
category_menu = tk.OptionMenu(window, selected_category, *word_categories.keys())
category_menu.config(width=10, font=("Arial", 14))

word_label = tk.Label(window, text="", font=("Arial", 24))
attempts_label = tk.Label(window, text="", font=("Arial", 16))
letter_entry = tk.Entry(window, width=5, font=("Arial", 16))

# Frame to hold buttons side by side
button_frame = tk.Frame(window)
guess_button = tk.Button(button_frame, text="Guess", command=lambda: guess_letter())
reset_button = tk.Button(button_frame, text="Reset", command=reset_game)
guess_button.pack(side="left", padx=5)  # Add some padding between the buttons
reset_button.pack(side="left", padx=5)

# Create the hangman canvas
canvas = tk.Canvas(window, width=300, height=300)
canvas.create_line(50, 250, 250, 250, width=4)  # Base line
canvas.create_line(200, 250, 200, 100, width=4)  # Post
canvas.create_line(100, 100, 200, 100, width=4)  # Beam
canvas.create_line(150, 100, 150, 120, width=4)  # Rope
canvas.pack()

# Create a frame to hold the letter buttons
letters_frame = tk.Frame(window)
letter_buttons = {}

# Create letter buttons (A-Z)
for letter in "abcdefghijklmnopqrstuvwxyz":
    btn = tk.Button(letters_frame, text=letter, font=("Arial", 16), width=2, command=lambda l=letter: guess_letter(l))
    btn.pack(side="left", padx=2, pady=5)
    letter_buttons[letter] = btn

# Pack GUI elements
category_label.pack()
category_menu.pack(pady=5)
word_label.pack()
attempts_label.pack()
letter_entry.pack()
button_frame.pack(pady=10)
letters_frame.pack(pady=10)  # Pack the frame containing the letter buttons

# Update initial displays
update_word_display()
update_attempts_display()
draw_hangman()

# Set up a trace to call the function when a new category is selected
selected_category.trace("w", update_word_list)

# Run the application
window.mainloop()
