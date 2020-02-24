from flask import Flask, request, Response, json, redirect, url_for
from http import HTTPStatus

from src.cities.trie import SuffixTree
from src.cities.utils import normalize_input
from src.web.queries.cityQuery import CityQuery
import os

Q_PARAMETER = "q"
LATITUDE_PARAMETER = "latitude"
LONGITUDE_PARAMETER = "longitude"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILEPATH = os.path.join(ROOT_DIR, "../../data/cities_canada-usa.tsv")


def create_app():
    app = Flask(__name__)

    #maybe put elsewhere
    suffix_tree = SuffixTree(DATA_FILEPATH)

    #@app.route("/")
    #def hello():
    #    return redirect(url_for('suggestions'))

    @app.route("/suggestions", methods=["GET"])
    def suggestions():
        q = request.args.get(Q_PARAMETER) if request.args.get(Q_PARAMETER) else ""
        latitude = float(request.args.get(LATITUDE_PARAMETER)) if request.args.get(LATITUDE_PARAMETER) else None
        longitude = float(request.args.get(LONGITUDE_PARAMETER)) if request.args.get(LONGITUDE_PARAMETER) else None

        city_query = CityQuery(normalize_input(q), latitude, longitude, suffix_tree)
        response = Response(json.dumps(city_query.get(), sort_keys=False, indent=2), mimetype='application/json')
        response.status_code = HTTPStatus.OK
        return response

    return app
