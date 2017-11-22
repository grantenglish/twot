from bs4 import BeautifulSoup
import requests
import json
from flask import Flask, Response, render_template

app = Flask(__name__)

allbeers = []

@app.route('/get')
def getBeers():
    global allbeers

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

    allbeers = []
    beercount = len(beer)
    for i in range(0 , beercount-1):
        j = {'type': beer[i], 'style':style[i],'abv':abv[i],'size':size[i],'price':price[i]}
        allbeers.append(j)

    text = json.dumps(allbeers,sort_keys=True,indent=4, separators=(',', ': '))
    return Response(text,  mimetype='application/json')

@app.route('/')
def fromFile():
    global allbeers
    with open('beers.json') as json_data:
        allbeers = json.load(json_data)

    print(allbeers)
    text = json.dumps(allbeers, sort_keys=True, indent=4, separators=(',', ': '))
    return Response(text, mimetype='application/json')


@app.route('/table')
def beersTable():
    return render_template('simple.html', title="Beers", description='Beers at the Tavern', beers=allbeers)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
