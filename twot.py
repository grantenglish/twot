from bs4 import BeautifulSoup

import requests
import web
import json

urls = (
    '/', 'beers',
    '/table', 'table'
)
app = web.application(urls, globals())

class beers:
    def GET(self):
        r  = requests.get("http://thewhiteoaktavern.com/whats-on-tap")

        data = r.text

        soup = BeautifulSoup(data, "html.parser")

        index = 0
        beer = [0 for i in range(100)]
        for link in soup.find_all("a", "beername"):
            print(link.text)
            beer[index] = link.text.strip()
            index = index + 1

        index= 0
        abv = [0 for i in range(100)]
        for abvelement in soup.find_all("span", "abv"):
            print(abvelement.text)
            abv[index] = abvelement.text
            index = index + 1

        index = 0
        style = [0 for i in range(100)]
        for styleelement in soup.find_all("span", "style"):
            print(styleelement.text)
            style[index] = styleelement.text
            index = index + 1

        index = 0
        size = [0 for i in range(100)]
        price = [0 for i in range(100)]
        for sizeprice in soup.find_all("span", "sizeprice"):
            print("Start 0")
            print(sizeprice.text)
            things = sizeprice.text.split()
            print("Start 1")
            print(things[0])
            size[index] = things[0]
            print(things[2])
            price[index] = things[2]
            print("End")
            index = index + 1

        beers = []
        for i in range(0 , 30):
            print(beer[i],style[i],abv[i],size[i],price[i])
            l = [ beer[i],style[i],abv[i],size[i],price[i] ]
            beers.append(l)

        web.header('Content-Type', 'application/json')
        return json.dumps(beers,sort_keys=True,indent=4, separators=(',', ': '))

class table:
    def GET(self):
        return "" \
               "     <script type=\"text/javascript\" src=\"http://cdnjs.cloudflare.com/ajax/libs/jquery/1.9.1/jquery.min.js\"></script>\
    <script type=\"text/javascript\" src=\"http://cdnjs.cloudflare.com/ajax/libs/jquery.tablesorter/2.9.1/jquery.tablesorter.min.js\"></script>\
    <script>\
    $(function(){\
    $(\"#myDummyTable\").tablesorter();\
    });\
    </script>\
    <table id=\"myDummyTable\" class=\"tablesorter\">\
  <thead>\
    <tr>\
      <th>Name</th>\
      <th>ID</th>\
      <th>Favorite Color</th>\
    </tr>\
  </thead>\
  <tfoot>\
    <tr>\
      <th>Name</th>\
      <th>ID</th>\
      <th>Favorite Color</th>\
    </tr>\
  </tfoot>\
  <tbody>\
    <tr>\
      <td>Jim</td>\
      <td>00001</td>\
      <td>Blue</td>\
    </tr>\
    <tr>\
      <td>Sue</td>\
      <td>00002</td>\
      <td>Red</td>\
    </tr>\
    <tr>\
      <td>Barb</td>\
      <td>00003</td>\
      <td>Green</td>\
    </tr>\
  </tbody>\
</table>"

if __name__ == "__main__":
    app.run()
