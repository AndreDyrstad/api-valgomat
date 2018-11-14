from flask import Flask, jsonify, request, make_response, Response
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS, cross_origin
import json
from jaccard import predict_center
from sql_add import init, get_all_questions

#db = client['valgomat']
#collection = db['centers']


app = Flask(__name__)
api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

parser = reqparse.RequestParser()
parser.add_argument('task')

class HelloWorld(Resource):
    def get(self):
        with open('storage/patients.json',encoding='utf-8') as f:
            data = json.load(f)
        json_string = json.dumps(data,ensure_ascii = False)
        response = Response(json_string,content_type="application/json; charset=utf-8" )
        print(response)

        session = init()
        file = get_all_questions(session)
        print(file)

        response = json.dumps(file,ensure_ascii=False)

        return response


class Patients(Resource):
    def get(self):
        with open('storage/patients.json',encoding='utf-8') as f:
            data = json.load(f)
        print(type(data))
        json_string = json.dumps(data,ensure_ascii = False)
        response = Response(json_string,content_type="application/json; charset=utf-8" )
        print(response)
        return data

class Centers(Resource):
    def get(self):
        with open('storage/centers.json',encoding='utf-8') as f:
            data = json.load(f)
        json_string = json.dumps(data,ensure_ascii = False)
        response = Response(json_string,content_type="application/json; charset=utf-8" )
        print(response)
        return data

class Classify(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        a = predict_center(json_data)
        print(a)
        return a

class SubmitCenter(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        #post_id = collection.insert_one(json_data).inserted_id
        #print(post_id)
        return {"message": "Ditt svar er nå registrert"}

class Reload(Resource):
    def get(self):
        data = []
        #for item in collection.find():
            #data.append(item)
        #make_classifier(data)
        return{"message": "Ferdig"}

api.add_resource(HelloWorld, '/')
api.add_resource(Classify, '/classify')
api.add_resource(Patients, '/patients')
api.add_resource(Centers, '/centers')
api.add_resource(SubmitCenter, '/train')
api.add_resource(Reload, '/reload')


if __name__ == '__main__': 
    #app.run(host="0.0.0.0",port="8020" ,debug=True)
    app.run(debug=True)


