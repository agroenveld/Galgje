import requests
from time import sleep
url = "http://beprek.nl/wartaal"
from termcolor import colored

while True:
    response = requests.request("GET", url)
    print(response.json()['bericht'])
    
    response = requests.request("GET" , url + "?destructief")
    print(response.json()['bericht'])

    response = requests.request("GET" , url + "?destructief&bondig")
    print(response.json()['bericht'])

    response = requests.request("GET" , url + "?bondig&ultrakort")
    print(colored(response.json()['bericht'],"red",None))

    sleep(1)
