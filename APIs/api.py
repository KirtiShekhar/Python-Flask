from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
app.secret_key = 'Kirti@02021997'
api = Api(app)

COUNTRIES = {
    '1': {'name': 'Maldives', 'capital': 'Male'},
    '2': {'name': 'India', 'capital': 'New Delhi'},
    '3': {'name': 'United States', 'capital': 'Washington D.C.'},
    '4': {'name': 'Japan', 'capital': 'Tokyo'},
}

countriesParser = reqparse.RequestParser()


class CountriesList(Resource):
    def get(self):
        return COUNTRIES

    def post(self):
        countriesParser.add_argument("name")
        countriesParser.add_argument("capital")
        countriesArgs = countriesParser.parse_args()
        countriesId = int(max(COUNTRIES.keys())) + 1
        countriesId = '%i' % countriesId
        COUNTRIES[countriesId] = {
            "name": countriesArgs["name"],
            "capital": countriesArgs["capital"],
        }
        return COUNTRIES[countriesId], 201


class Country(Resource):
    def get(self, countriesId):
        if countriesId not in COUNTRIES:
            return "Record not found", 404
        else:
            return COUNTRIES[countriesId]

    def put(self, countriesId):
        countriesParser.add_argument("name")
        countriesParser.add_argument("capital")
        countriesArgs = countriesParser.parse_args()
        if countriesId not in COUNTRIES:
            return "Record not found", 404
        else:
            country = COUNTRIES[countriesId]
            country["name"] = countriesArgs["name"] if countriesArgs["name"] is not None else country["name"]
            country["capital"] = countriesArgs["capital"] if countriesArgs["capital"] is not None else country[
                "capital"]

    def delete(self, countriesId):
        if countriesId not in COUNTRIES:
            return "Record not found", 404
        else:
            del COUNTRIES[countriesId]
            return 'deleted', 204


api.add_resource(CountriesList, '/countries')
api.add_resource(Country, '/country/<countriesId>')


@app.route('/apiRestful')
def api():
    return '<h1> Restful API </h1>'
