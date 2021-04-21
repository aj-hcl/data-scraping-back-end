import requests
from flask_restful import Resource, reqparse
import json
from bs4 import BeautifulSoup


class Validator(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('checkboxesChecked',
        type = str,
        action = "append",
        required = True,
        help = "Invalid input"
    )


    def post(self):
        args = Validator.post_parser.parse_args()

        checks = args["checkboxesChecked"]
        url = checks[0]

        #check input length
        length = len(checks)
        if(length < 2):
            return {"message":"Input must have at least some data"}, 400

        dicts = []
        for i in range(1,length):
            checks[i] = checks[i].replace("'",'"')
            try:
                dicts.append(json.loads(checks[i]))
            except:
                return {"message":"Invalid input"}, 400


        tags = []
        try:
            for d in dicts:
                
                tag = {}
                for key in d:
                    
                    if(key == "tag_key"):
                        
                        tag[key] = d[key]
                    else:
                        tag["tag_name"] = key
                        tag["tag_data"] = d[key]
                
                tags.append(tag)

        except:
            return {"message": "Invalid input"}, 400


        #send to saving service
        try:
            response = requests.post("http://127.0.0.1:4000/tag_saver", json = {"url":url, "tags": tags})
            responseData = response.json()
        except:
            return {'message':'An error occurred saving the data'}, 500

        #return what the saving service returned
        return responseData, response.status_code


    get_parser = reqparse.RequestParser()
    get_parser.add_argument('url',
        type = str,
        required = True,
        help = "Invalid input"
    )
    def put(self):
        args = Validator.get_parser.parse_args()
        try:
            response = requests.get("http://127.0.0.1:4000/tag_saver", json = {"url":args['url']})
            responseData = response.json()
        except:
            return {'message':'An error retrieving the data'}, 500

        #return what the saving service returned
        return responseData, response.status_code

