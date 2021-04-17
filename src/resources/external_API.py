import requests
from flask_restful import Resource, reqparse
import json

from models.data import ExternalDataModel

class External_Data(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('url',
        type = str,
        required = True,
        help = "this field cannot be left blank"
    )


    def post(self):
        args = External_Data.parser.parse_args()

        try:
            response = requests.get(args['url'])
        except:
            return {'message':'An error occurred retrieving the data'}, 500
        if(response.status_code != 200):
            return {'message':'An error occurred retrieving the data'}, 500

        try:
            responseData = response.json()
        except:
            return {"message":"URL not compatible"}, 500
        models = []

        try:
            for r in responseData:
                if(ExternalDataModel.find_by_login(r['login'])) is None:
                    models.append(ExternalDataModel(r['login'], r['id'], r['node_id'], r['url'], r['avatar_url'], r['description']))
        except:
            return {"message":"URL not compatible"}, 500

        try:
            ExternalDataModel.save_list_to_db(models)
        except:
            return {'message':'An error occurred saving the data'}, 500


        return {'message':'Data saved successfully'}


    def get(self):
        models = ExternalDataModel.find_all()


        if models:
            return [m.json() for m in models]
        return {'message':'Data not found'}, 404
