from flask import Flask, request, Response, json
from http import HTTPStatus

from src.cities.utils import normalize_input
from src.web.cityQuery import CityQuery

Q_PARAMETER = "q"
LATITUDE_PARAMETER = "latitude"
LONGITUDE_PARAMETER = "longitude"


def create_app():
    app = Flask(__name__)
    #app.debug = True
    @app.route("/suggestions", methods=["GET"])
    def suggestions():
        q = request.args.get(Q_PARAMETER)
        latitude = request.args.get(LATITUDE_PARAMETER)
        longitude = request.args.get(LONGITUDE_PARAMETER)

        city_query = CityQuery(normalize_input(q), latitude, longitude)
        response = Response(json.dumps(city_query.get(), indent=2), mimetype='application/json')
        response.status_code = HTTPStatus.OK
        return response

    return app
