"""
Flask app module
"""

from http import HTTPStatus
from flask import Flask, request, Response, json, abort, url_for, redirect
from dataclasses_serialization.json import JSONSerializer

from src.utils.suffix_tree import SuffixTree
from src.utils.format_helper import normalize_input
from src.api.suggestions.city_query import CityQuery

Q_PARAMETER = "q"
LATITUDE_PARAMETER = "latitude"
LONGITUDE_PARAMETER = "longitude"


def create_app():
    """Returns flask app router"""
    app = Flask(__name__)
    suffix_tree = SuffixTree()

    @app.route("/")
    # Redirects basic path to suggestions route
    def hello():
        return redirect(url_for('suggestions'), code=HTTPStatus.TEMPORARY_REDIRECT)

    @app.route("/suggestions", methods=["GET"])
    # Returns suggested cities according to query, latitude and longitude parameters
    def suggestions():
        q = request.args.get(Q_PARAMETER) if request.args.get(Q_PARAMETER) else ""

        try:
            latitude = float(request.args.get(LATITUDE_PARAMETER)) if request.args.get(LATITUDE_PARAMETER) else None
            longitude = float(request.args.get(LONGITUDE_PARAMETER)) if request.args.get(LONGITUDE_PARAMETER) else None
            city_query = CityQuery(suffix_tree)

        except ValueError:
            return abort(HTTPStatus.BAD_REQUEST)

        response = Response(
            json.dumps(JSONSerializer.serialize(city_query.get(normalize_input(q), latitude, longitude)),
                       ensure_ascii=False,
                       sort_keys=False,
                       indent=2),
            mimetype='application/json',
            content_type="application/json; charset=utf-8"
        )
        response.status_code = HTTPStatus.OK
        return response

    return app
