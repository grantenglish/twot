from bs4 import BeautifulSoup

import requests

# url = raw_input("Enter a website to extract the URL's from: ")

r  = requests.get("http://thewhiteoaktavern.com/whats-on-tap")

data = r.text

soup = BeautifulSoup(data, "html.parser")

for link in soup.find_all("a", "beername"):
    print(link.text)

for abv in soup.find_all("span", "abv"):
    print(abv.text)

for style in soup.find_all("span", "style"):
    print(style.text)

for sizeprice in soup.find_all("span", "sizeprice"):
    print(sizeprice.text)


