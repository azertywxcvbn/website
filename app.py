from flask import Flask, render_template
import requests
import json
import urllib3
import os
from bs4 import BeautifulSoup
directory = os.path.dirname(__file__)
app = Flask(__name__)


@app.route('/buy')
def buy():
    file = os.path.join(directory, 'data.json')
    with open(file, "r") as jsonFile:
        data = json.load(jsonFile)
    data["amount"] += 1
    with open(file, "w") as jsonFile:
        json.dump(data, jsonFile)
    return return_winst()


def getDate():
    url = "https://www.morningstar.be/be/funds/snapshot/snapshot.aspx?id=F00000VA3Q"
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    div = soup.find('div', class_='clearfix TopRelPos')
    table = soup.find(
        'table', class_='snapshotTextColor snapshotTextFontStyle snapshotTable overviewKeyStatsTable')

    date = table.find('span', class_='heading').text
    return date


def getCurrentPrice():
    url = "https://www.morningstar.be/be/funds/snapshot/snapshot.aspx?id=F00000VA3Q"
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    div = soup.find('div', class_='clearfix TopRelPos')
    table = soup.find(
        'table', class_='snapshotTextColor snapshotTextFontStyle snapshotTable overviewKeyStatsTable')

    current = table.find('td', class_='line text').text
    current = current[4:]
    current = current.replace(",", ".")
    return current


def calculate_winst():

    url = "https://www.morningstar.be/be/funds/snapshot/snapshot.aspx?id=F00000VA3Q"
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    div = soup.find('div', class_='clearfix TopRelPos')
    table = soup.find(
        'table', class_='snapshotTextColor snapshotTextFontStyle snapshotTable overviewKeyStatsTable')

    current = table.find('td', class_='line text').text
    current = current[4:]
    current = current.replace(",", ".")

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


def getRotation():
    if calculate_winst() > 0:
        return "rotateup"
    else:
        return "rotatedown"


@ app.route('/')
def return_winst():
    amount = get_amountBought()
    currentprice = getCurrentPrice()
    price = calculate_winst()
    date = getDate()
    arrowrotation = getRotation()
    return render_template('index.html', current=price, date=date, arrowrotation=arrowrotation, currentprice=currentprice, amount=amount)
