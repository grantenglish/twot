from bs4 import BeautifulSoup
import json

allBeers = []

def getBeers():
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

    print(json.dumps(allBeers, sort_keys=True, indent=4, separators=(',', ': ')))

    return


if __name__ == "__main__":
    getBeers()

