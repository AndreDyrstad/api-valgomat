from flask import Flask, request, Response
from flask_restful import reqparse, Api, Resource
from flask_cors import CORS
import json
from jaccard import use_scores
from database_folder import sql_queries as sql
import edit_config as config

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
        data = sql.get_questions_by_id("center")
        json_string = json.dumps(data,ensure_ascii = False)
        response = Response(json_string,content_type="application/json; charset=utf-8" )
        return data

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
        recommended_centers["patient_id"] = random_patient_id
        return recommended_centers

class Get_Response_Questions_By_ID(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        data = sql.get_all_questions_for_response_site_given_name(json_data['patient_id'])
        json_string = json.dumps(data,ensure_ascii = False)
        response = Response(json_string, content_type="application/json; charset=utf-8")
        return response

class Send_Patient_Response(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        sql.insert_patient_response(json_data)
        return {"message": "ok"}


class New_Question(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        sql.insert_question_from_api(json_data)

class All_Questions(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        print(json_data)
        all_questions = sql.get_all_questions()
        questions_from_config = sql.get_questions_by_id(json_data["entity"])

        all_questions["config"] = questions_from_config
        return all_questions

class Update_Question_Config(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        config.update_config_file(json_data, "patient")

class Get_Feedback(Resource):
    def get(self):
        response = sql.get_all_feedback()
        print(response)
        return response

class Add_Connection(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        return sql.insert_new_connection(json_data)

class Get_Connections(Resource):
    def get(self):
        return sql.get_all_connections_with_name()

api.add_resource(HelloWorld, '/')
api.add_resource(Patients, '/patients')
api.add_resource(Centers, '/centers')
api.add_resource(Submit_Center, '/train')
api.add_resource(Classify_Scores, '/scores')
api.add_resource(Get_Response_Questions_By_ID, '/feedbackQuestions')
api.add_resource(Send_Patient_Response, '/sendFeedback')
api.add_resource(New_Question, '/newQuestion')
api.add_resource(All_Questions, '/allQuestions')
api.add_resource(Update_Question_Config, '/updateQuestions')
api.add_resource(Get_Feedback, '/getFeedback')
api.add_resource(Add_Connection, '/makeConnection')
api.add_resource(Get_Connections, '/connections')

if __name__ == '__main__': 
    #app.run(host="0.0.0.0",port="8020" ,debug=True)
    app.run(debug=True)#, ssl_context='adhoc')


