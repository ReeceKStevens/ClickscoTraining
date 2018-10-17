from flask import Flask
from werkzeug.wsgi import DispatcherMiddleware
from Server1 import app as Server1
from Server2 import create_server

application = Flask(__name__)

application.wsgi_app = DispatcherMiddleware(Server1,{
    '/ServerA': create_server('a'),
    '/ServerB': create_server('a'),
    '/ServerC': create_server('a'),
    '/ServerD': create_server('a'),
    '/ServerE': create_server('a')
})

Server1.run()
