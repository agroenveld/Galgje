import re

class Words:
    def get_words(self):
        try:
            word_list = open('Galgje-100\woorden.txt', 'r').readlines()
            word_list = [word.rstrip().lower() for word in word_list]
            return word_list
        except:
            print('ERROR: woorden.txt cannot be opened.')
            print('Program will be aborted...')
            exit() 

    def clean_words_length(self, word_list, word_length):
        clean_word_list = []
        if word_length:
            for word in word_list:
                    if len(word) <= word_length:
                        clean_word_list.append(word)
        return clean_word_list

    def clean_words(self, clean_word_list, correct_letter_positions):  
        clean_word_list_orig = clean_word_list
        clean_word_list = []
        correct_letter_positions = correct_letter_positions.replace('_','.')
        for word in clean_word_list_orig:
            search_obj = re.search(rf'(^{correct_letter_positions})', word, re.M|re.I)
            if search_obj != None:
                clean_word_list.append(search_obj.group(1))  
        return clean_word_list
    
    def pick_letter(self, clean_word_list, guessed_letters):
        letters = [chr(i) for i in range(ord("a"), ord("z") + 1)]
        remaining_letters = [letter for letter in letters if letter not in guessed_letters]
        letter_counts = {letter: sum(letter in word for word in clean_word_list) for letter in remaining_letters}
        letter = max(letter_counts, key=letter_counts.get)
        guessed_letters.append(letter)

        return letter, guessed_letters