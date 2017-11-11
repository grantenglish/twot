from bs4 import BeautifulSoup

import requests
import web
import json
from flask import Flask
from flask import Response

app = Flask(__name__)

beer = [0 for i in range(100)]
abv = [0 for i in range(100)]
style = [0 for i in range(100)]
size = [0 for i in range(100)]
price = [0 for i in range(100)]
beercount = 0


@app.route('/')
def getBeers():
    global beercount
    r  = requests.get("http://thewhiteoaktavern.com/whats-on-tap")

    data = r.text

    soup = BeautifulSoup(data, "html.parser")

    index = 0
#        beer = [0 for i in range(100)]
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

    beers = []
    beercount = index
    for i in range(0 , beercount):
        l = [ beer[i],style[i],abv[i],size[i],price[i] ]
        beers.append(l)

   # web.header('Content-Type', 'application/json')
    text = json.dumps(beers,sort_keys=True,indent=4, separators=(',', ': '))
    return Response(text,  mimetype='application/json')

@app.route('/table')
def beersTable():
    global beercount
    table = "" \
           "     <script type=\"text/javascript\" src=\"http://cdnjs.cloudflare.com/ajax/libs/jquery/1.9.1/jquery.min.js\"></script>\
<script type=\"text/javascript\" src=\"https://cdn.datatables.net/1.10.16/js/jquery.dataTables.min.js\"></script>\
<script>\
$(function(){\
$(\"#myDummyTable\").DataTable();\
});\
</script>\
<table id=\"myDummyTable\" class=\"tablesorter\">\
<thead>\
<tr>\
  <th>Name</th>\
  <th>Style</th>\
  <th>ABV</th>\
  <th>Size</th>\
  <th>Price</th>\
</tr>\
</thead>\
<tbody>"

    for i in range(0, beercount):
        table = table + "<tr>"
        table = table + "<td>" + beer[i] +"</td>"
        table = table + "<td>" + style[i] +"</td>"
        table = table + "<td>" + str(abv[i]) +"</td>"
        table = table + "<td>" + size[i] +"</td>"
        table = table + "<td>" + price[i] +"</td>"
        table = table + "</tr>"

    table = table +   "</tbody></table>"

    return table

if __name__ == "__main__":
    app.run()
