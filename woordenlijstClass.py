class Woordenlijst:
    def __init__(self):
        #woordenlijst met woorden die tegen de galg aan kunnen worden gesmeten.
        try: 
            with open("woorden.txt", "rt") as f:# alleen-lezen van tekst
                self.woordenLijst = f.read().splitlines()    
        except:
            print('Error: woorden.txt kan niet gevonden worden.')
            print('programma wordt afgebroken....')
            exit()
        
        #de woorden in de db nog even lowercase maken en dedupliceren
        self.woordenLijst = [item.lower() for item in self.woordenLijst]
        self.woordenLijst = list(dict.fromkeys(self.woordenLijst))

        #zet alle woorden die voldoen in tijdelijke lijst, zet ze uiteindelijk in oorspronkelijke lijst
        self.puzzelwoorden = []
        for woord in self.woordenLijst:
            if self.voldoet_aan_alle_criteria(woord):
                self.puzzelwoorden.append(woord)
        self.woordenLijst = self.puzzelwoorden

    def is_romeins_getal(self, woord):
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

    def voldoet_aan_alle_criteria(self, woord = ''):
        voldoet = True
        if len(woord) < 4:
            voldoet = False
        elif len(woord) > 13:
            voldoet = False
        elif not woord.isascii():
            voldoet = False
        elif not woord.isalpha():
            voldoet = False
        elif self.is_romeins_getal(woord):
            voldoet = False
        return voldoet

    def get_woordenlijst(self):
        return self.woordenLijst