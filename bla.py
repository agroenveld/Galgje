import requests

url = 'https://onzetaal.nl/taalloket/zoek-spelling?in=spelling&zoek=liquidatie'

x = requests.get(url)

print(x.content)
