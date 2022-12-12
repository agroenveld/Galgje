import requests
class Webapp:
    def __init__(self):
        self.base_url = 'http://beprek.nl/galgje'

    def get_nieuwe_pin(self):
        self.response = requests.request("GET", self.base_url + '?pin=nieuw') 
        self.resultaat = self.response.json()["resultaat"]
        self.pin = self.resultaat["galgje pin"]
        return self.pin

    #functie om binnen een sessie een letter tegen galgje aan te houden. 
    def post_letter(self,pin,letter):
        self.pin = str(self.pin) #string van maken ander kan ie niet in de url opbouw hieronder
        self.response = requests.request("GET" , self.base_url + "?pin=" + self.pin + "&letter=" + letter)
        self.resultaat = self.response.json()["resultaat"]
        return self.resultaat

    #functie om binnen een sessie een woord tegen galgje aan te houden
    def post_woord(self,pin,woord):
        self.pin = str(self.pin) 
        self.response = requests.request("GET" , self.base_url + "?pin=" + self.pin + "&woord=" + woord)
        self.resultaat = self.response.json()["resultaat"]
        return self.resultaat