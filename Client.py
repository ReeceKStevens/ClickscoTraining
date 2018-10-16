from flask import Flask, render_template
from flask_socketio import SocketIO
import xml.etree.ElementTree as ET

app = Flask(__name__)
app.config[ 'SECRET_KEY' ] = 'abmmceccdadd123#'
socketio = SocketIO(app)
configdata = ET.parse('Adverts.config')
root = configdata.getroot()

def chooseAd(keywords):
    keywordList = str(keywords['keywords']).split()
    matches = [ ]
    print (keywordList)
    for child in root:
        print(child.attrib['name'])
        if child.attrib['name'] in keywordList:
            matches.append(child.attrib['name'])

    print(matches)

@app.route('/')
def client():
  return render_template('Requests.html')

def messageRecieved(methods=['GET', 'POST']):
    print('Message was recieved')

@socketio.on('connection established')
def handle_connection(methods=['GET']):
    print('Connection Established')

@socketio.on('keywords recieved')
def handle_custom_event(json, methods=['GET', 'POST']):
    print('recieved keywords: ' + str(json))
    response = chooseAd(json)
    socketio.emit('my response', json, callback=messageRecieved)

if __name__ == '__main__':
  socketio.run(app, debug=True)
