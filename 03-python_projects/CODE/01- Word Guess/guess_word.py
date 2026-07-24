import random

def choose_word():
    # List of words to choose from
    words = ["python", "programming", "computer", "algorithm", "data", "science", "machine", "learning"]
    # Randomly choose a word from the list
    return random.choice(words)

def display_word(word, guessed_letters):
    display = ""
    # Loop through each letter in the word
    for letter in word:
        # If the letter has been guessed, add it to the display
        if letter in guessed_letters:
            display += letter
        # If the letter hasn't been guessed, display a dash
        else:
            display += "-"
    return display

def guess_word(word):
    guessed_letters = set() # Set to store guessed letters
    attempts = 0 # Counter for the number of attempts

    print("Welcome to the Word Guessing Game! Try to guess the word.")

    while True:
        # Display the word with guessed letters revealed and dashes for unguessed letters
        print(f"\nWord: {display_word(word, guessed_letters)}")
        user_guess = input("Enter a letter: ").lower() # Ask user for input
        attempts += 1 # Increment attempt count
        
        # Check for invalid input
        if len(user_guess) != 1 or not user_guess.isalpha():
            print("Invalid input! Please enter a single letter.")
            continue

        # Check if the letter has already been guessed
        elif user_guess in guessed_letters:
            print("You already guessed that letter. Try another one.")

        # Check if the letter is in the word
        elif user_guess in word:
            print("Correct guess!")
            guessed_letters.add(user_guess) # Add guessed letter to set
            
        else:
            print("Incorrect guess. Try again.")

        # Check if all letters in the word have been guessed
        if all(letter in guessed_letters for letter in word):
            print(f"Congratulations! You guessed the word '{word}' in {attempts} attempts.")
            break


def main():
    word = choose_word() # Choose a word
    guess_word(word) # Start the guessing game

if __name__ == "__main__":
    main()
