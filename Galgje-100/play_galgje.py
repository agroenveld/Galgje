from time import sleep
import beprek_galgje
import galgje_words
from time import perf_counter
from termcolor import colored

hit = 0
miss = 0


def hit_miss(hit,miss):
    total = hit+miss
    hit = round(hit/total*100)
    miss = round(miss/total*100)
    result = 'Totaal aantal pogingen: ' + str(total) + '.\n'
    result = result + "Hit/Miss-ratio(%):" +str(hit) + '/' + str(miss) + '.'
    return result

def session():
    global hit
    global miss

    tries = 0
    start_time = perf_counter()

    api = beprek_galgje.Api()
    words = galgje_words.Words()

    pin = api.get_pin()
    word_length = api.get_length_word(pin)
  
    word_list = words.get_words()
    clean_word_list = words.clean_words_length(word_list, word_length)

    guessed_letters = []

    while True:
        tries +=1
        print(len(clean_word_list))
        letter, guessed_letters = words.pick_letter(clean_word_list,guessed_letters)
        if len(clean_word_list) == 1:
            post_word_response = api.post_word(pin,clean_word_list[0])
            print(post_word_response)
            if post_word_response['spel status'] == 'Je hebt dit spel gewonnen!':
                hit += 1
                message = '"' + post_word_response["woord dat geraden moest worden"] + '" geraden in '+str(tries) + ' pogingen!' 
                webmessage = message 
                break
        else:
            post_letter_response = api.post_letter(pin,letter)
            
            if post_letter_response['spel status'] == 'Je hebt een letter geraden!':            
                clean_word_list = words.clean_words(clean_word_list, post_letter_response['geraden letters'])
            if post_letter_response['spel status'] == 'Je hebt dit spel gewonnen!':
                hit += 1
                message = '"' + post_letter_response["woord dat geraden moest worden"] + '" geraden in '+str(tries) + ' pogingen!' 
                webmessage = message 
                break 
        if (post_letter_response['spel status'] or post_word_response['spel status']) == 'Je hebt dit spel verloren!':
            miss += 1
            message = 'Helaas, woord niet geraden: "' + (post_letter_response["woord dat geraden moest worden"] or post_letter_response["woord dat geraden moest worden"])  + '"'
            webmessage = '<img src="https://media.tenor.com/yDBioPEKjRAAAAAC/married-with-children-al-bundy.gif"><br><font color="red">' + message + '</font>'
            break

    end_time = perf_counter()
    return webmessage +  '<br><h5 align="center">' +  hit_miss(hit,miss) + ' aantal sec: {:.4f}'.format(end_time - start_time)
