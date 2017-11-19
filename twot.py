from bs4 import BeautifulSoup

import requests
import json
from flask import Flask, render_template
from flask import Response

app = Flask(__name__)

beer = [0 for i in range(100)]
abv = [0 for i in range(100)]
style = [0 for i in range(100)]
size = [0 for i in range(100)]
price = [0 for i in range(100)]
beercount = 0
allbeers = []



@app.route("/jinga")
def template_test():
    return render_template('template.html', my_string="Wheeeee!", my_list=[0,1,2,3,4,5])

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
    allbeers = []
    beercount = index
    for i in range(0 , beercount):
        l = [ beer[i],style[i],abv[i],size[i],price[i] ]
        beers.append(l)
        j = {'type': beer[i], 'style':style[i],'abv':abv[i],'size':size[i],'price':price[i]}
        allbeers.append(j)

   # web.header('Content-Type', 'application/json')
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
    table = "" \
            "<script type=\"text/javascript\" src=\"https://cdn.datatables.net/1.10.16/js/dataTables.bootstrap.min.js\"></script>\
            <script type=\"text/javascript\" src=\"https://cdn.datatables.net/responsive/2.2.0/js/dataTables.responsive.min.js\"></script>\
            <script type=\"text/javascript\" src=\"https://cdn.datatables.net/responsive/2.2.0/js/responsive.bootstrap.min.js\"></script>\
            <script type=\"text/javascript\" src=\"http://cdnjs.cloudflare.com/ajax/libs/jquery/1.9.1/jquery.min.js\"></script>\
<script type=\"text/javascript\" src=\"https://cdn.datatables.net/1.10.16/js/jquery.dataTables.min.js\"></script>\
    <link rel=\"stylesheet\" type=\"text/css\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\">\
    <link rel=\"stylesheet\" type=\"text/css\" href=\"https://cdn.datatables.net/1.10.16/css/dataTables.bootstrap.min.css\">\
    <link rel=\"stylesheet\" type=\"text/css\" href=\"https://cdn.datatables.net/fixedheader/3.1.3/css/fixedHeader.bootstrap.min.css\">\
    <link rel=\"stylesheet\" type=\"text/css\" href=\"https://cdn.datatables.net/responsive/2.2.0/css/responsive.bootstrap.min.css\">\
<script>\
$(document).ready(function() {\
    var table = $(\'#myDummyTable\').DataTable( {\
        responsive: true\
    } );\
} );\
</script>\
<table id=\"myDummyTable\" class=\"tablesorter table table-striped\">\
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

    return Response(table)

@app.route('/tablefile')
def beersFile():
    global beercount

    with open('beers.json') as json_data:
        d = json.load(json_data)

    table = "" \
            "<script type=\"text/javascript\" src=\"https://cdn.datatables.net/1.10.16/js/dataTables.bootstrap.min.js\"></script>\
            <script type=\"text/javascript\" src=\"https://cdn.datatables.net/responsive/2.2.0/js/dataTables.responsive.min.js\"></script>\
            <script type=\"text/javascript\" src=\"https://cdn.datatables.net/responsive/2.2.0/js/responsive.bootstrap.min.js\"></script>\
            <script type=\"text/javascript\" src=\"http://cdnjs.cloudflare.com/ajax/libs/jquery/1.9.1/jquery.min.js\"></script>\
<script type=\"text/javascript\" src=\"https://cdn.datatables.net/1.10.16/js/jquery.dataTables.min.js\"></script>\
    <link rel=\"stylesheet\" type=\"text/css\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\">\
    <link rel=\"stylesheet\" type=\"text/css\" href=\"https://cdn.datatables.net/1.10.16/css/dataTables.bootstrap.min.css\">\
    <link rel=\"stylesheet\" type=\"text/css\" href=\"https://cdn.datatables.net/fixedheader/3.1.3/css/fixedHeader.bootstrap.min.css\">\
    <link rel=\"stylesheet\" type=\"text/css\" href=\"https://cdn.datatables.net/responsive/2.2.0/css/responsive.bootstrap.min.css\">\
<script>\
$(document).ready(function() {\
    var table = $(\'#myDummyTable\').DataTable( {\
        responsive: true\
    } );\
} );\
</script>\
<table id=\"myDummyTable\" class=\"tablesorter table table-striped\">\
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

    for beer in d:
        table = table + "<tr>"
        table = table + "<td>" + beer['style'] +"</td>"
        table = table + "<td>" + beer['type'] +"</td>"
        table = table + "<td>" + str(beer['abv']) +"</td>"
        table = table + "<td>" + beer['size'] +"</td>"
        table = table + "<td>" + beer['price'] +"</td>"
        table = table + "</tr>"

    table = table +   "</tbody></table>"

    return Response(table)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
