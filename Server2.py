from flask import Flask, request, render_template
import xml.etree.ElementTree as ET
import random, math, threading
from threading import Timer

#Boilerplate code for a threaded, repeating timer which executes a method
#On a different thread
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

#Picks out a function to execure based on server's config
def apply_strategy(Conf, Budget):
    #List of strategies with map (I wish python had switch statements)
    strategies = {
        'random' : rand_strategy,
        'half' : half_strategy,
        'always_five' : always_five_strategy,
        'always_ten' : always_ten_strategy,
        'careful_random' : rand_within_budget_strategy
    }
    chosenstrat = ''
    #Read the strategy from config file
    for child in Conf:
        if child.tag == 'Strategy':
            chosenstrat = child.text
    #Execute the function which matches the key we read from config
    offer = strategies[chosenstrat](Budget)
    return offer

#Bids a random number between 1 and 10
def rand_strategy(Budget):
    offer = random.randint(1,10)
    return offer

#Always bids half the remaining funds, rounded up
def half_strategy(Budget):
    baseOffer = Budget/2
    offer = math.ceil(baseOffer)
    return offer

#Always bids 5p
def always_five_strategy(Budget):
    return 5

#Always bids 10p
def always_ten_strategy(Budget):
    return 10

#Pick a random number between 1 and remaining funds, rounding up
def rand_within_budget_strategy(Budget):
    offer = random.randint(1,Budget)
    return offer

#Create the server as a method so that different config files can be sent & it is
#easier to open multiple server instances
def create_server(Config):
    #Add on 50p to server budget, declared within create_server as a Nonlocal
    #variable is needed
    def topup_budget():
        nonlocal budget
        budget = 50
    #Initialize flask
    app = Flask(__name__)
    app.debug = True
    #Load the config file for this server
    configdata = ET.parse(Config + '.config')
    root = configdata.getroot()
    #Initializing variables
    budget = 50
    wins = 0
    interval = 0
    offers = []
    #Check the interval of payment listed in the configuration file
    for child in root:
        if child.tag == 'interval':
            interval = child.text
    #Initialize a timer to execute the topup function
    # after a number of seconds equal to the interval
    topuptimer = RepeatedTimer(int(interval), topup_budget)

    @app.route('/', methods=['POST'])
    def make_bid():
        nonlocal offers
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
        if (offer > -1):
            offers.append(str(offer))
            offers.append("False")
        return res

    @app.route('/winner', methods=['POST'])
    def after_auction():
        #Nonlocal used so that budget will be retained on this instance of the server
        nonlocal budget
        nonlocal wins
        nonlocal offers
        #Recieve the overall cost of our bid from the request
        cost = request.get_json(force=True)
        #Subtract the cost of this bid from the budget
        budget -= int(cost)
        wins += 1
        offers[-1] = "True"
        print(str(offers))
        #Quality of life server info, allows accurate knowledge of server budget
        print('Winner is Server' + Config[-1:] + ', remaining budget is ' + str(budget) + 'p')
        #Return null as Flask does not like return on it's own
        return ''

    @app.route('/bankrupt', methods=['POST'])
    def all_bankrupt():
        return str(wins)

    @app.route('/view', methods=['POST','GET'])
    def get_page():
        #Load a page for this server and tell it what server it is attached to
        #It only needs the server letter so that's all we send
        nonlocal Config
        return render_template('GraphicalView.html', server = Config[-1:])

    @app.route('/update', methods=['POST'])
    def update_view():
        #Get the name of the chosen strategy from the config file
        consenstrat = ''
        for child in root:
            if child.tag == 'Strategy':
                chosenstrat = child.text
        #requests is very particular about return type, so I bodged allow
        #the return data into a string that we can split on the other end
        res = (str(wins) + ',' + chosenstrat + ',' + str(budget) + ',' +interval)
        #Add each offer onto the end of the return string
        for offer in offers:
            res += (','+ offer)

        return res

    return app
