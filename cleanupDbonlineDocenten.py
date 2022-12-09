# test-prep-woordenlijst.py
# lees het bestand woorden.txt in en maak puzzelwoorden.txt

from random import choice

def maak_lijst_van_bestand(bestandsnaam):
    with open(bestandsnaam, 'r') as file:
        woordenlijst = file.readlines()
    return woordenlijst

def schrijf_lijst_naar_bestand(woordenlijst, bestandsnaam):
    with open(bestandsnaam, 'w') as file:
        file.writelines(woordenlijst)

def is_romeins_getal(woord):
    roman = {'i':1,'v':5,'x':10,'l':50,'c':100,'d':500,'m':1000,'iv':4,'ix':9,'xl':40,'xc':90,'cd':400,'cm':900}
    i = 0
    num = 0
    try:
        while i < len(woord):
            if i + 1 < len(woord) and woord[i:i + 2] in roman:
                num += roman[woord[i:i + 2]] 
                i += 2 
            else:
                #print(i)
                num += roman[woord[i]]
                i += 1
        if num > 0:
            return True
        else:
            return False
    except:
        return False

def voldoet_aan_alle_criteria(woord = ''):
    voldoet = True
    if len(woord) < 4:
        voldoet = False
    elif len(woord) > 13:
        voldoet = False
    elif not woord.isascii():
        voldoet = False
    elif not woord.isalpha():
        voldoet = False
    elif is_romeins_getal(woord):
        voldoet = False
    return voldoet


# stappen
# Lees de woorden uit woorden.txt
# Voor ieder woord in de lijst
#   Als woord voldoet aan alle criteria
#      Kopieer woord naar puzzelwoordenlijst
# Kopieer 1000 toevalswoorden uit de puzzelwoordenlijst naar een restlijst
# Schrijf restlijst naar puzzelwoorden.txt

woorden = maak_lijst_van_bestand('woorden.txt')
print(len(woorden), "woorden ingelezen van bestand woorden.txt")
puzzelwoorden = []
for woord in woorden:
    woord = woord.strip().lower()
    if voldoet_aan_alle_criteria(woord):
        puzzelwoorden.append(woord)
        # print(woord)

print(len(puzzelwoorden), "woorden uitgefilterd")

restlijst = []
for aantal in range(1000):
    woord = choice(puzzelwoorden)
    while woord in restlijst:
        woord = choice(puzzelwoorden)
    #print(woord)
    restlijst.append(woord)

print(len(restlijst), "woorden geselecteerd voor de puzzelwoorden")
schrijf_lijst_naar_bestand(restlijst, 'puzzelwoorden.txt')
print("Nieuw bestand puzzelwoorden.txt aangemaakt.")