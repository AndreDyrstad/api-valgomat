import json

from flask import Flask, request, Response
from flask_cors import CORS
from flask_restful import reqparse, Api, Resource

from utilities import update_config_file
import sql_queries as sql
from rbs import use_scores

app = Flask(__name__)
api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

parser = reqparse.RequestParser()
parser.add_argument('task')

class Status(Resource):
    def get(self):
        return{"status":"Server is up and running"}


class Patients(Resource):
    def get(self):
        return sql.get_questions_by_id("patient")

    def post(self):
        json_data = request.get_json(force=True)
        random_patient_id = sql.add_patient_answers(json_data)
        recommended_centers = use_scores(json_data)
        recommended_centers["patient_id"] = random_patient_id
        return recommended_centers

class Centers(Resource):
    def get(self):
        return sql.get_questions_by_id("center")

    def post(self):
        json_data = request.get_json(force=True)
        sql.add_new_center(json_data)
        return {"status": "success"}

class Get_Feedback_Questions_By_ID(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        data = sql.get_all_questions_for_response_site_given_name(json_data['patient_id'])
        json_string = json.dumps(data,ensure_ascii = False)
        response = Response(json_string, content_type="application/json; charset=utf-8")
        return response

class Patient_Feedback(Resource):
    def get(self):
        return sql.get_all_feedback()

    def post(self):
        json_data = request.get_json(force=True)
        sql.add_patient_response(json_data)
        return {"status": "success"}


class New_Question(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        sql.add_question_from_api(json_data)

class All_Questions(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        all_questions = sql.get_all_questions()
        questions_from_config = sql.get_questions_by_id(json_data["entity"])

        all_questions["config"] = questions_from_config
        return all_questions

class Update_Question_Config(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        update_config_file(json_data["response"], json_data["entity"])
        return {"status":"success"}

class Connections(Resource):
    def get(self):
        return sql.get_all_connections_with_name()

    def post(self):
        json_data = request.get_json(force=True)
        return sql.add_new_connection(json_data)

class Get_Centers_And_Answers(Resource):
    def get(self):
        return sql.get_all_questions_answered_by_center()

api.add_resource(Status, '/')
api.add_resource(Patients, '/patients')
api.add_resource(Centers, '/centers')
api.add_resource(Get_Feedback_Questions_By_ID, '/question/feedback')
api.add_resource(Patient_Feedback, '/feedback')
api.add_resource(New_Question, '/question/new')
api.add_resource(All_Questions, '/question/all')
api.add_resource(Update_Question_Config, '/question/update')
api.add_resource(Connections, '/connections')
api.add_resource(Get_Centers_And_Answers, '/centerData')

if __name__ == '__main__': 
    #app.run(host="0.0.0.0",port="8020" ,debug=True)
    app.run(debug=True)#, ssl_context='adhoc')
