import requests
import random
import re

def get_pin():
    url = 'http://beprek.nl/galgje?pin=nieuw'
    response = requests.get(url).json()['resultaat']
    pin = response['galgje pin']
    return pin

def get_words():
    word_list = open('woorden.txt', 'r').readlines()
    return word_list

def get_length_word(pin):
    url = f'http://beprek.nl/galgje?pin={pin}'
    response = requests.get(url).json()['resultaat']
    word_length = len(response['geraden letters'])
    return word_length

def clean_words_length(word_list, word_length):
    clean_word_length_list = []
    if word_length:
        for word in word_list:
                if len(word) <= word_length:
                    clean_word_length_list.append(word)
    return clean_word_length_list

def clean_words(clean_word_length_list, correct_letter = None, correct_letter_positions = None):  
    if correct_letter:
        correct_letter_positions = correct_letter_positions.replace('_','.')
        for word in clean_word_length_list:
            search_obj = re.search(rf'(^{correct_letter_positions})', word, re.M|re.I)
            if search_obj != None:
                clean_word_list.append(search_obj.group(1))
           
    return clean_word_list
    
def pick_letter(clean_word_list, guessed_letters):
    
    # Create a list of all possible letters
    letters = [chr(i) for i in range(ord("a"), ord("z") + 1)]
        
    # Remove letters that have already been guessed
    remaining_letters = [letter for letter in letters if letter not in guessed_letters]

    # Count the number of times each remaining letter occurs in the remaining words
    letter_counts = {letter: sum(letter in word for word in clean_word_list) for letter in remaining_letters}

    # Choose the letter with the highest count
    letter = max(letter_counts, key=letter_counts.get)
    guessed_letters.append(letter)
    return letter, guessed_letters

def post_letter(pin, letter):
    url = f'http://beprek.nl/galgje?pin={pin}&letter={letter}'
    response = requests.get(url).json()['resultaat']
    guesses_left = response['resterend pogingen']
    if response['spel status'] == 'Je hebt een letter geraden!':
        correct_letter = letter
        correct_letter_positions = response['geraden letters']
        return response, guesses_left, correct_letter, correct_letter_positions
    else:
        return response, guesses_left

#def post_word(pin, word):

if __name__ == '__main__':
    pin = get_pin()
    word_length = get_length_word(pin)
    word_list = get_words()
    guessed_letters = []
    clean_word_length_list = clean_words_length(word_list, word_length)
    clean_word_list = []
    for i in range(10):
    # while True:
        clean_word_list = clean_words(clean_word_length_list, #### Hier moet nog parameters komen voor het de correct_letter en de correct_letter position)
        letter, guessed_letters = pick_letter(clean_word_list,guessed_letters)
        print(post_letter(pin,letter))
        print(len(clean_word_list))
