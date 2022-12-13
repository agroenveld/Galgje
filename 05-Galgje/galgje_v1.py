import requests
import fnmatch
from time import sleep
from termcolor import colored
from random import choice

#woordenlijst met woorden die tegen de galg aan kunnen worden gesmeten.
f = open("woorden.txt", "rt") # alleen-lezen van tekst
woordenDatabase = f.read().splitlines()
f.close()

base_url = 'http://beprek.nl/galgje'
pin = ''
letterfrequentie = 'enatirodslgvhkmubpwjzcfxyq'  #Uit een onderzoek uit 1985 blijkt dit de volgorde te zijn



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
  
            
def sessie():
    pin = haal_nieuwe_pin()
    db = woordenDatabase
    aantal_pogingen = 1


    for l in letterfrequentie:
        resultaat = post_letter(pin,l)
        woord = resultaat["geraden letters"]
        aantal_pogingen = resultaat["resterend pogingen"]
        spelstatus = resultaat["spel status"]

        #print(resultaat)
        woordlengte = len(woord)
        patroon = str.replace(woord,"_","?")
        

        #match de woorden in de db met het patroon
        db = fnmatch.filter(db,patroon)
        db.sort()

        # if spelstatus == "Deze letter zit niet in het woord":
        #     for w in db:
        #         if w.count(l) < 1:
        #             db.remove(w)
        
        #print(len(db))
        print(db)
        
        gooiwoord = choice(db)
        resultaat = post_woord(pin,gooiwoord)
        spelstatus = resultaat["spel status"]

        if aantal_pogingen == 0:
            print(colored('Max pogingen bereikt, het woord was: ' + resultaat["woord dat geraden moest worden"] ,'red'))
            sleep(1)
            return True   
        
        if spelstatus == "Je hebt dit spel gewonnen!":
            print(colored('Woord geraden in '+str(10 - aantal_pogingen)+ ' pogingen! Het woord was: ' + resultaat["woord dat geraden moest worden"],"green"))
            sleep(1)
            return True
        


for i in range(10000):
    sessie()


