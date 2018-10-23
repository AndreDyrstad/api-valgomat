from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS, cross_origin
import json
from pprint import pprint
from classifier import classify_document

app = Flask(__name__)
api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

parser = reqparse.RequestParser()
parser.add_argument('task')

class HelloWorld(Resource):
    def get(self):
        with open('storage/patients.json') as f:
            data = json.load(f)
        print(type(data))
        pprint(data)
        return data


class Patients(Resource):
    def get(self):
        with open('storage/patients.json') as f:
            data = json.load(f)
        print(type(data))
        pprint(data)
        return data

class Centers(Resource):
    def get(self):
        with open('storage/centers.json') as f:
            data = json.load(f)
        print(type(data))
        pprint(data)
        return data

class Classify(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        a = classify_document(json_data)
        return {"center": "Her kommer navn på anbefalt senter"}

class SubmitCenter(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        return {"message": "Ditt svar er nå registrert"}

api.add_resource(HelloWorld, '/')
api.add_resource(Classify, '/classify')
api.add_resource(Patients, '/patients')
api.add_resource(Centers, '/centers')
api.add_resource(SubmitCenter, '/train')


if __name__ == '__main__':
    app.run(debug=True)


