from bs4 import BeautifulSoup
import requests
import json
from flask import Flask, Response, render_template, send_from_directory

app = Flask(__name__, static_url_path='')

allBeers = []


@app.route('/twot.png', methods=['GET'])
def servePNG():
    print("servepng")
    return send_from_directory('', 'twot.png')


@app.route('/styles.css', methods=['GET'])
def serveCSS():
    print("servecss")
    return send_from_directory('', 'styles.css')


@app.route('/get')
def getBeers():
    global allBeers

    req = requests.get("http://thewhiteoaktavern.com/whats-on-tap")
    soup = BeautifulSoup(req.text, "html.parser")

    # save the last request
    f = open("request.txt", "w")
    f.write(req.text)
    f.close()

    #pull the data out of the response
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

    text = json.dumps(allBeers, sort_keys=True, indent=4, separators=(',', ': '))
    return Response(text, mimetype='application/json')


@app.route('/')
def fromFile():
    global allBeers
    f = open('request.txt', "r")
    reqText = f.read()
    f.close()

    soup = BeautifulSoup(reqText, "html.parser")

    for beer in soup.find_all(attrs={'class': "beer-column"}):
        name=(beer.find("a", "beername")).text.strip()

        abv = "0"
        abvs = beer.find_all("span", "abv")
        if len(abvs) > 0:
            abv = beer.find("span", "abv")
            abv = abv.text

        style = beer.find("span", "style").text

        sizePrice = beer.find("span", "sizeprice")
        things = sizePrice.text.split()
        size = things[0]
        price = things[2]
        j = {'type': name, 'style': style, 'abv': abv, 'size': size, 'price': price}
        allBeers.append(j)

        text = json.dumps(allBeers, sort_keys=True, indent=4, separators=(',', ': '))

    print(text)

    return Response(text, mimetype='application/json')


@app.route('/table')
def beersTable():
    return render_template('simple.html', title="Beers", description='Beers at the Tavern', beers=allBeers)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
