from flask import Flask, render_template
import requests
import json
import urllib3
import requests
import os
from bs4 import BeautifulSoup
directory = os.path.dirname(__file__)
app = Flask(__name__)


@app.route('/buy')
def buy():
    print("zz")
    file = os.path.join(directory, 'data.json')
    with open(file, "r") as jsonFile:
        data = json.load(jsonFile)
    data["amount"] += 1
    with open(file, "w") as jsonFile:
        json.dump(data, jsonFile)
    print("zz")
    return return_winst()


def calculate_winst():
    url = "https://markets.ft.com/data/funds/tearsheet/charts?s=BE6264508548:EUR"
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    section = soup.find('section')
    div = section.find(
        'div', class_='mod-tearsheet-overview__quote').ul.li

    current = div.find('span', class_='mod-ui-data-list__value').text
    print(current)
    current = float(current) * float(get_amountBought())
    paid = get_price()

    winst = current - paid
    return round(winst, 2)


def get_amountBought():
    file = os.path.join(directory, 'data.json')
    with open(file, 'r') as myfile:
        data = myfile.read()
    obj = json.loads(data)
    amountBought = obj["amount"]
    return amountBought


def get_price():

    file = os.path.join(directory, 'data.json')
    with open(file, 'r') as myfile:
        data = myfile.read()
    obj = json.loads(data)

    totalPrice = obj["bought"]
    total = 0
    for i in totalPrice:
        total += obj["bought"][i]

    return total


@app.route('/')
def return_winst():
    price = calculate_winst()

    return render_template('index.html', current=price)
