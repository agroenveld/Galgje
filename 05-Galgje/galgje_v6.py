import requests
import fnmatch
from termcolor import colored
from random import choice
import winsound
from collections import Counter

#woordenlijst met woorden die tegen de galg aan kunnen worden gesmeten.
try: 
    with open("woorden.txt", "rt") as f:# alleen-lezen van tekst
        woordenDatabase = f.read().splitlines()    
except:
    print('Error: woorden.txt kan niet gevonden worden.')
    print('programma wordt afgebroken....')
    exit()
    
#de woorden in de db nog even lowercase maken en dedupliceren
woordenDatabase = [item.lower() for item in woordenDatabase]
woordenDatabase = list(dict.fromkeys(woordenDatabase))

# letterlijst = [] #gooi hier alle letters van alle woorden in
# for woord in woordenDatabase:
#     for letter in woord:
#         letterlijst.append(letter)

# #laat de occurrences even zien hier:
# aantal_per_letter = Counter(letterlijst)
# print(aantal_per_letter)

base_url = 'http://beprek.nl/galgje'
pin = ''
#letterfrequentie = 'enatirodslgvhkmubpwjzcfxyq'  #Uit een onderzoek uit 1985 blijkt dit de volgorde te zijn
letterfrequentie = 'erinaotsldgkupmchbvfwjzyxq'  #volgens de collectie van de woordendatabase is dit echter de volgorde
#letterfrequentie = 'eiaourntsldgkpmchbvfwjzyxq' #u en o nog wat naar voren gebracht
hit = 0
miss = 0

def haal_nieuwe_pin():
    response = requests.request("GET", base_url + '?pin=nieuw') 
    resultaat = response.json()["resultaat"]
    pin = resultaat["galgje pin"]
    return pin

#functie om binnen een sessie een letter tegen galgje aan te houden. 
def post_letter(pin,letter):
    pin = str(pin) #string van maken ander kan ie niet in de url opbouw hieronder
    response = requests.request("GET" , base_url + "?pin=" + pin + "&letter=" + letter)
    resultaat = response.json()["resultaat"]
    return resultaat

#functie om binnen een sessie een woord tegen galgje aan te houden
def post_woord(pin,woord):
    pin = str(pin) 
    response = requests.request("GET" , base_url + "?pin=" + pin + "&woord=" + woord)
    resultaat = response.json()["resultaat"]
    return resultaat

#haal de woorden uit de db die de tekens bevatten in de reeks (die ztten niet in het woord) en geef een valide db terug.
def schoon_letters_kandidaatwoorden(db,letterreeks):
    geschoondeLijst = []
    flag = 1
    for woord in db:
        for letter in letterreeks:
            if letter not in woord:
                flag = 1
            else:
                flag = 0
                break
        if (flag == 1):
            geschoondeLijst.append(woord)
    return geschoondeLijst

#haal gefaalde gooiwoorden uit de database, anders kunnen ze nog een keer ingezet worden 
def schoon_gooiwoord_kandidaatwoorden(db,woordenreeks):
    geschoondeLijst = []
    flag = 1
    for woord in db:
        for gooiwoord in woordenreeks:
            if gooiwoord != woord:
                flag = 1
            else:
                flag = 0
                break
        if (flag == 1):
            geschoondeLijst.append(woord)
    return geschoondeLijst

def hit_miss(hit,miss):
    total = hit+miss
    hit = hit/total*100
    miss = miss/total*100
    return('Totaal aantal pogingen: ' + str(total) + ". Hit/Miss-ratio: {:.2f}".format(hit) + '/' + "{:.2f}".format(miss))
    
            
def sessie():
    pin = haal_nieuwe_pin()
    kanditaat_woorden = woordenDatabase
    aantal_pogingen = 1
    niet_in_woord = []
    gooiwoordenlijst = []
    
    for l in letterfrequentie:
        global miss
        global hit
        resultaat = post_letter(pin,l)
        woord = resultaat["geraden letters"]
        aantal_pogingen = resultaat["resterend pogingen"]
        spelstatus = resultaat["spel status"]
        patroon = str.replace(woord,"_","?") 

        
        print('Trying met pincode ' + str(pin) + ' ' + l + ': ' + spelstatus  + ' ' + str(aantal_pogingen))

        #pas de lijst met kandidaatwoorden aan door ze te matchen met het patroon wat je terugkrijgt van galgje
        kanditaat_woorden = fnmatch.filter(kanditaat_woorden,patroon)
        kanditaat_woorden.sort()

        #als letter niet in woord dan bouw een lijstje op met die letter
        #zodat je daarna de woorden met die die letters bevatten uit de database kunt gooien
        if spelstatus == "Deze letter zit niet in het woord":
            niet_in_woord.append(l)
                
        kanditaat_woorden =  schoon_letters_kandidaatwoorden(kanditaat_woorden,niet_in_woord) 

        #pik een woord uit de overgebleven mogelijke woorden en gooi deze richting de webapplicatie        
        gooiwoord = choice(kanditaat_woorden)
        resultaat = post_woord(pin,gooiwoord)
        aantal_pogingen = resultaat["resterend pogingen"]
        spelstatus = resultaat["spel status"]

        #als het gooiwoord niet matcht, dan ook uit de db wegpoetsen anders kan ie nog weer gebruikt worden
        if spelstatus == 'Dat is niet het woord':
            gooiwoordenlijst.append(gooiwoord)
        if aantal_pogingen < 5:
            kanditaat_woorden = schoon_gooiwoord_kandidaatwoorden(kanditaat_woorden,gooiwoordenlijst)    
        
            print('Trying met pincode ' + str(pin) + ' ' + gooiwoord + ': ' + spelstatus + ', aantal pogingen over: ' + str(aantal_pogingen) + ', aantal woorden in kandidaat_woorden: ' +  str(len(kanditaat_woorden)))

        if aantal_pogingen == 0 or spelstatus == "Je hebt dit spel gewonnen!":
            print(colored('Patroon met geraden letters: ' + patroon,'cyan'))
            print(colored('Kansloos geprobeerd met: ' + str(gooiwoordenlijst),'magenta'))
            print(colored('Overgebleven kandidaten:' + str(kanditaat_woorden),'yellow'))
            
            
            if aantal_pogingen == 0:
                miss += 1
                message = 'Max pogingen bereikt, het woord was: ' + resultaat["woord dat geraden moest worden"] 
                print(colored(message,'white','on_red',['bold']))
                #winsound.Beep(500, 100)
            else:
                hit += 1
                message = 'Woord geraden in '+str(10 - aantal_pogingen)+ ' pogingen! Het woord was: ' + resultaat["woord dat geraden moest worden"]
                print(colored(message,'yellow','on_green',['bold']))
                #winsound.Beep(2000, 30)
            print(colored(hit_miss(hit,miss),'blue','on_white',['bold']))
            print('-'*150)
            return True   

for i in range(100):
    sessie()