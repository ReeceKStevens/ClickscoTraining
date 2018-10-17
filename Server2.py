from flask import Flask, request
import xml.etree.ElementTree as ET
from werkzeug.serving import run_simple

def create_server(Config):
    app = Flask(__name__)
    app.debug = True

    #configdata = ET.parse(Config + '.config')
    #root = configdata.getroot()

    @app.route('/', methods=['POST', 'GET'])
    def handle_data():
        keywords = (request.get_json(force=True))
        print (keywords)
        return 'Something'

    return app
