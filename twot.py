from bs4 import BeautifulSoup
import requests
import json
from flask import Flask, Response, render_template, send_from_directory

app = Flask(__name__, static_url_path='')

allBeers = []


@app.route('/twot.png', methods=['GET'])
def servefile():
    print( "servefile")
    return send_from_directory( '', 'twot.png')


@app.route('/get')
def getBeers():
    global allBeers

    req  = requests.get("http://thewhiteoaktavern.com/whats-on-tap")
    soup = BeautifulSoup(req.text, "html.parser")

    beer = []
    for link in soup.find_all("a", "beername"):
        beer.append(link.text.strip())

    abv = []
    for abvelement in soup.find_all("span", "abv"):
        abv.append(abvelement.text)

    style = []
    for styleelement in soup.find_all("span", "style"):
        style.append(styleelement.text)

    size = []
    price = []
    for sizeprice in soup.find_all("span", "sizeprice"):
        things = sizeprice.text.split()
        size.append(things[0])
        price.append(things[2])

    allBeers = []
    beercount = len(beer)
    for i in range(0 , beercount-1):
        j = {'type': beer[i], 'style':style[i],'abv':abv[i],'size':size[i],'price':price[i]}
        allBeers.append(j)

    text = json.dumps(allBeers, sort_keys=True, indent=4, separators=(',', ': '))
    return Response(text,  mimetype='application/json')

@app.route('/')
def fromFile():
    global allBeers
    with open('beers.json') as json_data:
        allBeers = json.load(json_data)

    print(allBeers)
    text = json.dumps(allBeers, sort_keys=True, indent=4, separators=(',', ': '))
    return Response(text, mimetype='application/json')


@app.route('/table')
def beersTable():
    return render_template('simple.html', title="Beers", description='Beers at the Tavern', beers=allBeers)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
