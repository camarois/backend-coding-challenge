from flask import Flask

def create_app():
    app = Flask(__name__)

    #@app.route('/suggestions', methods=['GET'])

    return app