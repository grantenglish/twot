from bs4 import BeautifulSoup

import requests
import json
from flask import Flask, render_template
from flask import Response

app = Flask(__name__)

beercount = 0
allbeers = []



@app.route('/template')
def template_test():
    global allbeers
    print(allbeers)
    return render_template('simple.html', title="Wheeeee!", description='description', beers=allbeers)

@app.route('/')
def getBeers():
    global beercount
    global allbeers

    r  = requests.get("http://thewhiteoaktavern.com/whats-on-tap")

    data = r.text

    soup = BeautifulSoup(data, "html.parser")

    beer = [0 for i in range(100)]
    abv = [0 for i in range(100)]
    style = [0 for i in range(100)]
    size = [0 for i in range(100)]
    price = [0 for i in range(100)]

    index = 0
    for link in soup.find_all("a", "beername"):
        beer[index] = link.text.strip()
        index = index + 1

    index= 0
    for abvelement in soup.find_all("span", "abv"):
        abv[index] = abvelement.text
        index = index + 1

    index = 0
    for styleelement in soup.find_all("span", "style"):
        style[index] = styleelement.text
        index = index + 1

    index = 0
    for sizeprice in soup.find_all("span", "sizeprice"):
        things = sizeprice.text.split()
        size[index] = things[0]
        price[index] = things[2]
        index = index + 1

    beercount = index
    for i in range(0 , beercount):
        j = {'type': beer[i], 'style':style[i],'abv':abv[i],'size':size[i],'price':price[i]}
        allbeers.append(j)

    text = json.dumps(allbeers,sort_keys=True,indent=4, separators=(',', ': '))
    return Response(text,  mimetype='application/json')

@app.route('/file')
def fromFile():
    with open('beers.json') as json_data:
        d = json.load(json_data)
        print(d)

    text = json.dumps(d, sort_keys=True, indent=4, separators=(',', ': '))
    return Response(text, mimetype='application/json')


@app.route('/table')
def beersTable():
    global beercount
    return render_template('simple.html', title="Wheeeee!", description='description', beers=allbeers)

@app.route('/tablefile')
def beersFile():
    global beercount

    with open('beers.json') as json_data:
        d = json.load(json_data)

    return render_template('simple.html', title="Wheeeee!", description='description', beers=d)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
