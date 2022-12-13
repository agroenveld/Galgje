import requests
import fnmatch
from time import sleep
from termcolor import colored
from random import choice
import winsound


#woordenlijst met woorden die tegen de galg aan kunnen worden gesmeten.
f = open("woorden.txt", "rt") # alleen-lezen van tekst
woordenDatabase = f.read().splitlines()
f.close()
#de woorden in de db nog even lowercase maken.
woordenDatabaseLower = [item.lower() for item in woordenDatabase]

base_url = 'http://beprek.nl/galgje'
pin = ''
#letterfrequentie = 'enatirodslgvhkmubpwjzcfxyq'  #Uit een onderzoek uit 1985 blijkt dit de volgorde te zijn
letterfrequentie = 'eaiountrdslgvhkmbpwjzcfxyq'


def haal_nieuwe_pin():
    response = requests.request("GET", base_url + '?pin=nieuw')
    resultaat = response.json()["resultaat"]
    pin = resultaat["galgje pin"]
    return pin

def post_letter(pin,letter):
    pin = str(pin) #string van maken ander kan ie niet in de url opbouw hieronder
    response = requests.request("GET" , base_url + "?pin=" + pin + "&letter=" + letter)
    resultaat = response.json()["resultaat"]
    return resultaat

def post_woord(pin,woord):
    pin = str(pin) 
    response = requests.request("GET" , base_url + "?pin=" + pin + "&woord=" + woord)
    resultaat = response.json()["resultaat"]
    return resultaat

#haal de woorden uit de db die de tekens bevatten in de reeks (die ztten niet in het woord) en geef een valide db terug.
def clean_letters_db(db,reeks):
    cleaned = []
    flag = 1
    for woord in db:
        for letter in reeks:
            if letter not in woord:
                flag = 1
            else:
                flag = 0
                break
        if (flag == 1):
            cleaned.append(woord)
    return cleaned

#haal gefaalde gooiwoorden uit de database, anders kunnen ze nog een keer ingezet worden 
def clean_gooiwoord_db(db,reeks):
    cleaned = []
    flag = 1
    for woord in db:
        for gw in reeks:
            if gw != woord:
                flag = 1
            else:
                flag = 0
                break
        if (flag == 1):
            cleaned.append(woord)
    return cleaned
        
            
def sessie():
    pin = haal_nieuwe_pin()
    db = woordenDatabaseLower
    aantal_pogingen = 1
    niet_in_woord = []
    gooiwoordenlijst = []
    
    for l in letterfrequentie:
        resultaat = post_letter(pin,l)
        woord = resultaat["geraden letters"]
        aantal_pogingen = resultaat["resterend pogingen"]
        spelstatus = resultaat["spel status"]
        patroon = str.replace(woord,"_","?")
        
        print('Trying met pincode ' + str(pin) + ' ' + l + ': ' + spelstatus)

        #match de woorden in de db met het patroon en sorteer de db nog even
        db = fnmatch.filter(db,patroon)
        db.sort()

        #als letter niet in woord dan bouw een lijstje op met die letter
        #zodat je daarna de woorden met die die letters bevatten uit de database kunt gooien
        if spelstatus == "Deze letter zit niet in het woord":
            niet_in_woord.append(l)
                
        db =  clean_letters_db(db,niet_in_woord) 

        #pik een woord uit de overgebleven mogelijke woorden en gooi deze richting de webapplicatie        
        gooiwoord = choice(db)
        resultaat = post_woord(pin,gooiwoord)
        aantal_pogingen = resultaat["resterend pogingen"]
        spelstatus = resultaat["spel status"]

        #als het gooiwoord niet matcht, dan ook uit de db wegpoetsen anders kan ie nog weer gebruikt worden
        if spelstatus == 'Dat is niet het woord':
            gooiwoordenlijst.append(gooiwoord)

        db = clean_gooiwoord_db(db,gooiwoordenlijst)    
        
        print('Trying met pincode ' + str(pin) + ' ' + gooiwoord + ': ' + spelstatus)

        if aantal_pogingen == 0:
            print(db)
            print(patroon)
            print(gooiwoordenlijst)
            print(colored('Max pogingen bereikt, het woord was: ' + resultaat["woord dat geraden moest worden"] ,'red'))
            print('############################################################################')
            winsound.Beep(500, 30)
            return True   
        
        if spelstatus == "Je hebt dit spel gewonnen!":
            print(db)
            print(patroon)
            print(gooiwoordenlijst)
            print(colored('Woord geraden in '+str(10 - aantal_pogingen)+ ' pogingen! Het woord was: ' + resultaat["woord dat geraden moest worden"],"green"))
            print('############################################################################')
            winsound.Beep(2000, 30)
            return True
 
for i in range(5):
    sessie()
