from flask import Flask, request
import xml.etree.ElementTree as ET
import random, math, threading
from threading import Timer
#Create the server as a method so that different config files can be sent & it is
#easier to open multiple server instances

def apply_strategy(Conf, Budget):
    strategies = {
        'random' : rand_strategy,
        'half' : half_strategy,
        'always five' : always_five_strategy,
        'always ten' : always_ten_strategy,
        'careful random' : rand_within_budget_strategy
    }
    chosenstrat = ''

    for child in Conf:
        if child.tag == 'Strategy':
            chosenstrat = child.text

    offer = strategies[chosenstrat](Budget)
    return offer

def rand_strategy(Budget):
    offer = random.randint(1,10)
    return offer

def half_strategy(Budget):
    baseOffer = Budget/2
    offer = math.ceil(baseOffer)
    return offer

def always_five_strategy(Budget):
    return 5

def always_ten_strategy(Budget):
    return 10

def rand_within_budget_strategy(Budget):
    offer = random.randint(1,Budget)
    return offer

def create_server(Config):

    def topup_budget():
        nonlocal budget
        pay = 50
        budget += pay

    app = Flask(__name__)
    app.debug = True
    #Load the config file for this server
    configdata = ET.parse(Config + '.config')
    root = configdata.getroot()

    budget = 50
    wins = 0
    interval = 0

    for child in root:
        if child.tag == 'interval':
            interval = child.text

    topupTimer = threading.Timer (int(interval), topup_budget, args = ())
    topupTimer.start()

    @app.route('/', methods=['POST'])
    def make_bid():
        #Technically we don't do anything with this but will need it in later versions
        keywords = request.get_json(force=True)
        #Generate a random bid (Different bidding styles will be added in later versions)
        if (budget <= 0):
            offer = -1
        else:
            offer = apply_strategy(root, budget)
        url = ''
        #Required to read the url due to nature of ElementTree
        for child in root:
            if (child.tag == 'adURL'):
                url = child.text
        #Format the offer into a string as requests only allows a few data types
        res = (str(offer) + ' ' + url + ' ' + request.base_url)
        return res

    @app.route('/winner', methods=['POST'])
    def after_auction():
        #Nonlocal used so that budget will be retained on this instance of the server
        nonlocal budget
        nonlocal wins
        #Recieve the overall cost of our bid from the request
        cost = request.get_json(force=True)
        #Subtract the cost of this bid from the budget
        budget -= int(cost)
        wins += 1
        #Quality of life server info, allows accurate knowledge of server budget
        print('Winner is Server' + Config[-1:] + ', remaining budget is ' + str(budget) + 'p')
        #Return null as Flask does not like return on it's own
        return ''

    @app.route('/bankrupt', methods=['POST'])
    def all_bankrupt():
        return str(wins)

    return app
