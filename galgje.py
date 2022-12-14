import fnmatch                                      #gebruikt op regexp op de achtergrond om lijsten te filteren obv pattern
from termcolor import colored                       #kleurtjes voor de leesbaarheid in console
from random import choice                           #af en toe moeten we een woord uit de locale woordenlijst kiezen om tegen de webapp aan te gooien
import woordenlijstClass                            #de klasse voor de locale woordenlijst
import webapp                                       #webapp houdt alle requestverianten (pin, letter, woord) en geeft webresults terug.
from woordenfilter import schoon_letters_kandidaatwoorden , schoon_gooiwoord_kandidaatwoorden
from art import tprint  
import webgalg
from time import perf_counter
import datetime

letterfrequentie = 'erinaotsldgkupmchbvfwjzyxq'     #dynamisch maken volgens de collectie van de woordendatabase
hit = 0
miss = 0

wl = woordenlijstClass.Woordenlijst()               #nieuwe woordenlijstklasse instantieren en vervolgens de woordenlijst daar uit ophalen.
wl = wl.get_woordenlijst()

def hit_miss(hit,miss):
    total = hit+miss
    hit = round(hit/total*100)
    miss = round(miss/total*100)
    result = 'Totaal aantal pogingen: ' + str(total) + '.\n'
    result = result + "Hit/Miss-ratio(%):" +str(hit) + '/' + str(miss) + '.'
    return result

def sessie():
    web = webapp.Webapp()
    pin = web.get_nieuwe_pin()
    kanditaat_woorden = wl
    aantal_pogingen = 1
    letterNietInWoord = []
    luckyShotsMissed = []

    for character in letterfrequentie:
        if character == 'e':            #start met tellen van de doorlooptijd
            start_time = perf_counter()
        global miss
        global hit
        resultaat = web.post_letter(pin,character)

        woord = resultaat["geraden letters"]
        aantal_pogingen = resultaat["resterend pogingen"]
        spelstatus = resultaat["spel status"]
        patroon = str.replace(woord,"_","?")

        print('Trying met pincode ' + str(pin) + ' ' + character + ': ' + spelstatus  + ' ' + str(aantal_pogingen))
        #print(webgalg.tekengalg(10 - aantal_pogingen))

        #pas de lijst met kandidaatwoorden aan door ze te matchen met het patroon wat je terugkrijgt van galgje
        kanditaat_woorden = fnmatch.filter(kanditaat_woorden,patroon)
        kanditaat_woorden.sort()
        
        #als letter niet in woord, voeg dan de letter toe aan een lijstje
        #zodat je daarna de woorden met die die letters bevatten uit de kandidaatwoorden kunt gooien
        if spelstatus == "Deze letter zit niet in het woord":
            letterNietInWoord.append(character)

        kanditaat_woorden =  schoon_letters_kandidaatwoorden(kanditaat_woorden,letterNietInWoord)

        if aantal_pogingen != 0:
            #pik een woord uit de overgebleven mogelijke woorden en gooi deze richting de webapplicatie
            luckyShot = choice(kanditaat_woorden)
            resultaat = web.post_woord(pin,luckyShot)
            aantal_pogingen = resultaat["resterend pogingen"]
            spelstatus = resultaat["spel status"]

            #als het luckyshot niet matcht, dan ook uit de db wegpoetsen anders kan ie nog weer gebruikt worden
            if spelstatus == 'Dat is niet het woord':
                luckyShotsMissed.append(luckyShot)

            kanditaat_woorden = schoon_gooiwoord_kandidaatwoorden(kanditaat_woorden,luckyShotsMissed)
            print('Trying met pincode ' + str(pin) + ' ' + luckyShot + ': ' + spelstatus + ', aantal pogingen over: ' + str(aantal_pogingen) + ', aantal woorden in kandidaat_woorden: ' +  str(len(kanditaat_woorden)))

        if aantal_pogingen == 0 or spelstatus == "Je hebt dit spel gewonnen!":
            print(colored('Patroon met geraden letters: ' + patroon,'cyan'))
            print(colored('Kansloos geprobeerd met: ' + str(luckyShotsMissed),'magenta'))
            print(colored('Overgebleven kandidaten:' + str(kanditaat_woorden),'grey'))

            if aantal_pogingen == 0:
                miss += 1
                message = 'Helaas, woord niet geraden: "' + resultaat["woord dat geraden moest worden"] + '"'
                webmessage = '<img src="https://media.tenor.com/yDBioPEKjRAAAAAC/married-with-children-al-bundy.gif"><br><font color="red">' + message + '</font>'
                print(webgalg.tekengalg(9))
                print(colored(message,'white','on_red',['bold']))
                
            else:
                hit += 1
                message = '"' + resultaat["woord dat geraden moest worden"] + '" geraden in '+str(10 - aantal_pogingen) + ' pogingen!' 
                webmessage = message
                print(colored(message,'yellow','on_green',['bold']))
                tprint(resultaat["woord dat geraden moest worden"])
                
            print(colored(hit_miss(hit,miss),'blue','on_white',['bold']))
            print('-'*150)
            end_time = perf_counter()
            now = datetime.datetime.now()
            dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
            with open("logfile.log","a") as logfile:
                logfile.write(str(dt_string) + ':\t' + message + '\t\t' + " aantal sec: {:.3f}".format(end_time - start_time) +'\n'+ hit_miss(hit,miss) + '\n')

            return webmessage +  '<br><h5 align="center">' +  hit_miss(hit,miss) + " aantal sec: {:.3f}".format(end_time - start_time)

