from flask import Flask, request, Response, json, abort
from http import HTTPStatus

from src.utils.suffixTree import SuffixTree
from src.utils.stringFormat import normalize_input
from src.api.suggestions.cityQuery import CityQuery
import os

Q_PARAMETER = "q"
LATITUDE_PARAMETER = "latitude"
LONGITUDE_PARAMETER = "longitude"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILEPATH = os.path.join(ROOT_DIR, "../../data/cities_canada-usa.tsv")


def create_app():
    app = Flask(__name__)
    suffix_tree = SuffixTree(DATA_FILEPATH)

    @app.route("/suggestions", methods=["GET"])
    def suggestions():
        q = request.args.get(Q_PARAMETER) if request.args.get(Q_PARAMETER) else ""
        response = Response(mimetype='application/json')

        try:
            latitude = float(request.args.get(LATITUDE_PARAMETER)) if request.args.get(LATITUDE_PARAMETER) else None
            longitude = float(request.args.get(LONGITUDE_PARAMETER)) if request.args.get(LONGITUDE_PARAMETER) else None
            city_query = CityQuery(normalize_input(q), latitude, longitude, suffix_tree)
            response.data = json.dumps(city_query.get(), sort_keys=False, indent=2)
            response.status_code = HTTPStatus.OK
        except ValueError:
            return abort(HTTPStatus.BAD_REQUEST)
        return response

    return app
