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
        
    def get_woordenlijst(self):
        return self.woordenLijst

    

  