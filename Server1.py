#Importing flask, as well as some additional libraries for enhanced functionality,
#also import ElementTree so we can parse the config file
from flask import Flask, render_template, request, redirect
import requests
import xml.etree.ElementTree as ET
from werkzeug.serving import run_simple
#Create the app value to allow flask to function
app = Flask(__name__)
app.debug = True
#Store the config file for refference later
configdata = ET.parse('data/Adverts.config')
root = configdata.getroot()

def chooseAd(keywords):
    #Split the input at space characters, this is so multiple words can be
    #evaluated seperately
    keywordList = keywords.split()
    #Initialize blank list and populate it with lower case version of the input
    #This is so input can be compared regardless of case
    keywordLower = []
    for word in keywordList:
        keywordLower.append(word.lower())
    #Create initial dictionary to store return value
    match = {"Ad": "", "Value": 0}
    #Iterate through each keyword in the config file
    for child in root:
        #Trigger if we find a keyword which exists in our inputs
        if child.attrib['name'] in keywordLower:
            value = ""
            ad = ""
            #Check each attribute in the keyword to collect it's value and ad
            for attribute in child:
                if attribute.tag == 'value':
                    value = attribute.text
                if attribute.tag == "ad":
                    ad = attribute.text
            #If the value of the match is higher than previous matches,
            #store it as the new best match (Value starts at 0)
            if int(value) > int(match["Value"]):
                match["Ad"] = ad
                match["Value"] = value
    #Return the ad url of the best match
    return match["Ad"]

#Top-level index for this application
@app.route('/', methods=['POST', 'GET'])
def handle_data():
    error = None
    response1 = ""
    keywords = ""
    #Code block only triggers if page was loaded via form submission
    if request.method == 'POST':
        try:
            #Extract the keywords from the form
            keywords = request.form['keyinput']
        except:
            keyjson = request.get_json(force=True)
            keywords = keyjson['keyinput']
        #Run function to determine best match for keywords provided
        response1 = chooseAd(keywords)
    #Load the frontend, either with or without an ad
    return render_template('Requests.html', ad1 = response1, words = keywords)

#Secondary route called on page load, does not redirect
@app.route('/secondAD', methods=['POST', 'GET'])
def serve_ad():
    #Initializing variables used in the loop, server names are in a list to save space
    winner = {'Offer': 0, 'URL': '', 'Server': ''}
    Servers = ['ServerA', 'ServerB', 'ServerC', 'ServerD', 'ServerE']
    #Make a request to each server
    for ServerName in Servers:
        #Post the keyword to the external server & recieve a response
        Res = requests.post('http://127.0.0.1:5000/'+ ServerName +'/', json = request.form)
        #Format the response into something we can use
        ResponseTuple = (Res.text).split()
        #Compare if this offer is better than the current best offer, both converted to integers for compatibility
        if int(ResponseTuple[0]) > int(winner['Offer']):
            #Record the details of our new highest bidder
            winner['Offer'] = ResponseTuple[0]
            winner['URL'] = ResponseTuple[1]
            winner['Server'] = ResponseTuple[2]

    if (winner['Server'] != ''):
        requests.post (winner['Server'] + '/winner', json = winner['Offer'])

    return winner['URL']

#Run the app using werkzeug, this lets us run multiple Flask services simeltaniously
if __name__ == '__main__':
    run_simple('localhost', 5000, app,
               use_reloader=True, use_debugger=True, use_evalex=True)
