from http import HTTPStatus
import os
from flask import Flask, request, Response, json, abort, url_for, redirect

from src.utils.suffix_tree import SuffixTree
from src.utils.string_format import normalize_input
from src.api.suggestions.city_query import CityQuery

Q_PARAMETER = "q"
LATITUDE_PARAMETER = "latitude"
LONGITUDE_PARAMETER = "longitude"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILEPATH = os.path.join(ROOT_DIR, "../../data/cities_canada-usa.tsv")


def create_app():
    app = Flask(__name__)
    suffix_tree = SuffixTree(DATA_FILEPATH)

    @app.route("/")
    def hello():
        return redirect(url_for('suggestions'), code=HTTPStatus.TEMPORARY_REDIRECT)

    @app.route("/suggestions", methods=["GET"])
    def suggestions():
        q = request.args.get(Q_PARAMETER) if request.args.get(Q_PARAMETER) else ""

        try:
            latitude = float(request.args.get(LATITUDE_PARAMETER)) if request.args.get(LATITUDE_PARAMETER) else None
            longitude = float(request.args.get(LONGITUDE_PARAMETER)) if request.args.get(LONGITUDE_PARAMETER) else None

            city_query = CityQuery(normalize_input(q), latitude, longitude, suffix_tree)

        except ValueError:
            return abort(HTTPStatus.BAD_REQUEST)

        response = Response(
            json.dumps(city_query.get(), sort_keys=False, indent=2),
            mimetype='application/json'
        )
        response.status_code = HTTPStatus.OK
        return response

    return app
