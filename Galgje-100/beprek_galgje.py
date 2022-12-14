import requests

class Api:
    def __init__(self):
        self.base_url = 'http://beprek.nl/galgje'

    def get_pin(self):
        url = f'{self.base_url}?pin=nieuw'
        response = requests.get(url).json()['resultaat']
        pin = response['galgje pin']
        return pin

    def get_length_word(self, pin):
        url = f'{self.base_url}?pin={pin}'
        response = requests.get(url).json()['resultaat']
        word_length = len(response['geraden letters'])
        return word_length

    def post_letter(self, pin, letter):
        url = f'{self.base_url}?pin={pin}&letter={letter}'
        response = requests.get(url).json()['resultaat']
        return response

    def post_word(self, pin, word):
        url = f'{self.base_url}?pin={pin}&woord={word}'
        response = requests.get(url).json()['resultaat']
        return response