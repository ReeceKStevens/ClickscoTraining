from flask import Flask, request
import xml.etree.ElementTree as ET
import random
#Create the server as a method so that different config files can be sent
def create_server(Config):
    app = Flask(__name__)
    app.debug = True
    #Load the config file for this server
    configdata = ET.parse(Config + '.config')
    root = configdata.getroot()
    @app.route('/', methods=['POST', 'GET'])
    def handle_data():
        #Technically we don't do anything with this but will need it in later versions
        keywords = (request.get_json(force=True))
        #Generate a random bid (Different bidding styles will be added in later versions)
        offer = random.randint(5,20)
        url = ''
        #Required to read the url due to nature of ElementTree
        for child in root:
            url = child.text
        #Format the offer into a string as requests only allows a few data types
        res = (str(offer) + ' ' + url)
        return res

    return app
