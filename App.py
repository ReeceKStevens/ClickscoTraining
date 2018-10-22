from flask import Flask
from werkzeug.wsgi import DispatcherMiddleware
from Server1 import app as Server1
from Server2 import create_server

application = Flask(__name__)

#Launch all of these programmes simeltaniously, also informs the server 2 instances
#which config file they should use, which savas a lot of code later
#Also assigns a unique endpoint to different server instances
application.wsgi_app = DispatcherMiddleware(Server1,{
    '/ServerA': create_server('data/ServerA'),
    '/ServerB': create_server('data/ServerB'),
    '/ServerC': create_server('data/ServerC'),
    '/ServerD': create_server('data/ServerD'),
    '/ServerE': create_server('data/ServerE'),
})
#Starts up all the servers, set to threaded to noticeably increase performance
#As each server runs on different threads
if __name__ == '__main__':
    Server1.run(threaded=True)
