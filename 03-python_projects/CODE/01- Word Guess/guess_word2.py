# Generate a random word
import random, time, os
allowed_attempts = 10

def choose_word():
    words = ["apple", "banana", "orange", "grape", "strawberry", 'carrot', 'tomato']
    return random.choice(words)

def rules():
    print(f'''
          Welcome to Guess the Word!
          You have {allowed_attempts} attempts to guess the correct word.
          ''')

def display_word(word, guessed_letters):
    for letter in word:
        if letter in guessed_letters :
            print(letter, end="")       
        else:
            print("-", end="") 
            
def clear_screen():
    time.sleep(0.8)
    os.system('cls')

# Main game loop
def guess_word():
    rules()
    word = choose_word()
    guessed_letters = set()
    attempts = 0
    while True:
        guess = input("\nEnter a letter: ")
        attempts += 1
        if guess in word:
            print("\nCorrect guess!")
            guessed_letters.add(guess)
            
        else:
            print("\nWrong guess!")

        clear_screen()
        display_word(word, guessed_letters)

        if len(guessed_letters) == len(set(word)):
            print(f"\nYou guessed the word {word} correctly!")
            break

        elif attempts == allowed_attempts:
            print(f"\nYou have exhausted all {allowed_attempts} attempts. Game over!")
            print(f"The correct word was {word}.")
            break

if __name__ == "__main__":
    guess_word()
