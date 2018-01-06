from bs4 import BeautifulSoup
import requests
import json
from flask import Flask, Response, render_template, send_from_directory, request

app = Flask(__name__, static_url_path='')

#
#global list of all the beers
#
allBeers = []

#
# lazy set up of statics for dev env, in prod these would be served by nginx
@app.route('/twot.png', methods=['GET'])
def servePNG():
    print("servepng")
    return send_from_directory('', 'twot.png')


@app.route('/styles.css', methods=['GET'])
def serveCSS():
    print("servecss")
    return send_from_directory('', 'styles.css')

#
# real routes
#
@app.route('/table', methods=['POST'])
def my_form_post():
    print(request.form)
    return "button"


@app.route('/get')
def getBeers():
    global allBeers

    allBeers.clear() #start over

    req = requests.get("http://thewhiteoaktavern.com/whats-on-tap")
    #soup = BeautifulSoup(req.text, "html.parser")

    # save the last request
    f = open("request.txt", "w")
    f.write(req.text)
    f.close()

    extract(req.text)

    text = json.dumps(allBeers, sort_keys=True, indent=4, separators=(',', ': '))
    return Response(text, mimetype='application/json')

#
# really here just for test, picts up the last request file
#
@app.route('/')
def fromFile():
    global allBeers

    allBeers.clear() #start over

    f = open('request.txt', "r")
    reqText = f.read()
    f.close()

    extract(reqText)

    text = json.dumps(allBeers, sort_keys=True, indent=4, separators=(',', ': '))

    print(text)

    return Response(text, mimetype='application/json')


#
# take the existing beer data and present it
#
@app.route('/table')
def beersTable():
    return render_template('simple.html', title="Beers", description='Beers at the Tavern', beers=allBeers)

#
# utilities
#  : extract takes an html string and populates the global beer list
#
def extract(htmlText): #ths has the side effect of populating the global beer list
    soup = BeautifulSoup(htmlText, "html.parser")

    for beer in soup.find_all(attrs={'class': "beer-column"}):
         name = (beer.find("a", "beername")).text.strip()  # strip laft and right

         abv = "0"
         abvs = beer.find_all("span", "abv")
         if len(abvs) > 0:  # apparently root beer gets put on tap with empty abv
             txt = beer.find("span", "abv")
             abv = txt.text.split("%")[0]  # pull the number out

         style = beer.find("span", "style").text

         sizePrice = beer.find("span", "sizeprice")  # split and pull the two numbers out
         things = sizePrice.text.split()
         size = things[0]
         price = things[2]

         j = {'type': name, 'style': style, 'abv': abv, 'size': size, 'price': price}
         allBeers.append(j)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
