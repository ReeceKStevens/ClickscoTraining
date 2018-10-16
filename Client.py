from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config[ 'SECRET_KEY' ] = 'abmmceccdadd123#'
socketio = SocketIO(app)

@app.route('/')
def client():
  return render_template('Requests.html')

def messageRecieved(methods=['GET', 'POST']):
    print('Message was recieved')

@socketio.on('keywords recieved')
def handle_custom_event(json, methods=['GET', 'POST']):
    print('recieved my event: ' + str(json))
    socketio.emit('my response', json, callback=messageRecieved)

if __name__ == '__main__':
  socketio.run(app, debug=True)
