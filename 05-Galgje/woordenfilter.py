
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

