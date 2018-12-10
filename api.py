from flask import Flask, jsonify, request, make_response, Response
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS, cross_origin
import json
from jaccard import predict_center, use_scores
from sql_queries import get_all_questions, insert_patient_answers, insert_new_center

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

        file = get_all_questions()

        print(file)

        json_string = json.dumps(file,ensure_ascii=False)
        response = Response(json_string,content_type="application/json; charset=utf-8" )

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
        print(insert_patient_answers(json_data))
        print(a)
        return a

class SubmitCenter(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        insert_new_center(json_data)
        #post_id = collection.insert_one(json_data).inserted_id
        #print(post_id)
        return {"message": "Ditt svar er nå registrert"}

class Classify_Scores(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        print(json_data)
        return use_scores(json_data)


api.add_resource(HelloWorld, '/')
api.add_resource(Classify, '/classify')
api.add_resource(Patients, '/patients')
api.add_resource(Centers, '/centers')
api.add_resource(SubmitCenter, '/train')
api.add_resource(Classify_Scores, '/scores')


if __name__ == '__main__': 
    #app.run(host="0.0.0.0",port="8020" ,debug=True)
    app.run(debug=True)


