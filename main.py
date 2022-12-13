from flask import Flask
import galgje

app = Flask(__name__)

@app.route("/")

def index():
    mysessie = galgje.sessie()
    output = '<head><meta http-equiv="refresh" content="0"></head><body bgcolor="black" text="white"><font face="verdana"><h6 align="center" valign="center">http://beprek.nl/galgje</h1>'
    output = output + '<h2 align="center" valign="center">' + mysessie + '</h2>'
    output = output + '<p>&nbsp;</p>'
    output = output + '<center><font color="red">de groeten van google2</font></center>'   
    return output

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
    #app.run(host="10.52.56.91", port=8080, debug=True)

