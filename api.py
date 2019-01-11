from flask import Flask, jsonify, request, make_response, Response
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS, cross_origin
import json
from jaccard import predict_center, use_scores
import sql_queries as sql

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

        file = sql.get_all_questions()

        print(file)

        json_string = json.dumps(file,ensure_ascii=False)
        response = Response(json_string,content_type="application/json; charset=utf-8" )

        return response


class Patients(Resource):
    def get(self):

        data = sql.get_questions_by_id("patient")
        json_string = json.dumps(data,ensure_ascii = False)
        response = Response(json_string,content_type="application/json; charset=utf-8" )
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
        print(sql.insert_patient_answers(json_data))
        print(a)
        return a

class Submit_Center(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        sql.insert_new_center(json_data)
        #post_id = collection.insert_one(json_data).inserted_id
        #print(post_id)
        return {"message": "Ditt svar er nå registrert"}

class Classify_Scores(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        random_patient_id = sql.insert_patient_answers(json_data)
        recommended_centers = use_scores(json_data)
        return recommended_centers

class Get_Response_Questions_By_ID(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        print(json_data['patient_id'])
        data = sql.get_all_questions_for_response_site_given_name(json_data['patient_id'])
        print(data)
        json_string = json.dumps(data,ensure_ascii = False)
        response = Response(json_string, content_type="application/json; charset=utf-8")
        return response

class Send_Patient_Response(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        print(json_data)
        sql.insert_patient_response(json_data)
        return {"message": "ok"}


class New_Question(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        sql.insert_question_from_api(json_data)


api.add_resource(HelloWorld, '/')
api.add_resource(Classify, '/classify')
api.add_resource(Patients, '/patients')
api.add_resource(Centers, '/centers')
api.add_resource(Submit_Center, '/train')
api.add_resource(Classify_Scores, '/scores')
api.add_resource(Get_Response_Questions_By_ID, '/feedbackQuestions')
api.add_resource(Send_Patient_Response, '/sendFeedback')
api.add_resource(New_Question, '/newQuestion')


if __name__ == '__main__': 
    #app.run(host="0.0.0.0",port="8020" ,debug=True)
    app.run(debug=True)


