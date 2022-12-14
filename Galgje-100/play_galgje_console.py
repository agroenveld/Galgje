import requests
import re
from termcolor import colored
from time import perf_counter

amount_of_wins = 0
amount_of_losses = 0

def get_pin():
    url = 'http://beprek.nl/galgje?pin=nieuw'
    response = requests.get(url).json()['resultaat']
    pin = response['galgje pin']
    return pin

def get_words():
    word_list = open('Galgje-100\woorden.txt', 'r').readlines()
    word_list = [word.rstrip().lower() for word in word_list]
    return word_list

def get_length_word(pin):
    url = f'http://beprek.nl/galgje?pin={pin}'
    response = requests.get(url).json()['resultaat']
    word_length = len(response['geraden letters'])
    return word_length

def clean_words_length(word_list, word_length):
    clean_word_list = []
    if word_length:
        for word in word_list:
                if len(word) <= word_length:
                    clean_word_list.append(word)
    return clean_word_list

def clean_words(clean_word_list, correct_letter_positions):  
    clean_word_list_orig = clean_word_list
    clean_word_list = []
    correct_letter_positions = correct_letter_positions.replace('_','.')
    for word in clean_word_list_orig:
        search_obj = re.search(rf'(^{correct_letter_positions})', word, re.M|re.I)
        if search_obj != None:
            clean_word_list.append(search_obj.group(1))  
    return clean_word_list
    
def pick_letter(clean_word_list, guessed_letters):
    letters = [chr(i) for i in range(ord("a"), ord("z") + 1)]
    remaining_letters = [letter for letter in letters if letter not in guessed_letters]
    letter_counts = {letter: sum(letter in word for word in clean_word_list) for letter in remaining_letters}
    letter = max(letter_counts, key=letter_counts.get)
    guessed_letters.append(letter)

    return letter, guessed_letters

def post_letter(pin, letter):
    url = f'http://beprek.nl/galgje?pin={pin}&letter={letter}'
    response = requests.get(url).json()['resultaat']

    return response

def post_word(pin, word):
    url = f'http://beprek.nl/galgje?pin={pin}&woord={word}'
    response = requests.get(url).json()['resultaat']

    return response

def start_session():
    start_time = perf_counter()
    global amount_of_wins
    global amount_of_losses
    pin = get_pin()
    word_length = get_length_word(pin)
    word_list = get_words()
    guessed_letters = []
    clean_word_list = clean_words_length(word_list, word_length)

    while True:
        print(len(clean_word_list))
        letter, guessed_letters = pick_letter(clean_word_list,guessed_letters)
        if len(clean_word_list) == 1:
            post_word_response = post_word(pin,clean_word_list[0])
            print(post_word_response)
            if post_word_response['spel status'] == 'Je hebt dit spel gewonnen!':
                amount_of_wins += 1
                break
        else:
            post_letter_response = post_letter(pin,letter)
            print(post_letter_response)
            if post_letter_response['spel status'] == 'Je hebt een letter geraden!':            
                clean_word_list = clean_words(clean_word_list, post_letter_response['geraden letters'])
            if post_letter_response['spel status'] == 'Je hebt dit spel gewonnen!':
                amount_of_wins += 1 
                break 
        if (post_letter_response['spel status'] or post_word_response['spel status']) == 'Je hebt dit spel verloren!':
            amount_of_losses += 1
            break
    end_time = perf_counter()
    print()
    print(colored(f'Statistics: W{amount_of_wins}/ L{amount_of_losses}','white','on_red',['bold']))
    print(colored(f'Time: {end_time - start_time}','white','on_blue',['bold']))
    print()


if __name__ == '__main__':
    while True:
        start_session()
