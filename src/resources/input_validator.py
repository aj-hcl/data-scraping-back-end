import requests
from flask_restful import Resource, reqparse
import json
from bs4 import BeautifulSoup


class Validator(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('url',
        type = str,
        required = True,
        help = "Invalid input"
    )
    post_parser.add_argument('tags',
        type = dict,
        action = "append",
        required = True,
        help = "Invalid input"
    )


    def post(self):
        args = Validator.post_parser.parse_args()

        checks = args["tags"]
        
        #check input length
        length = len(checks)
        if(length < 1):
            return {"message":"Input must have at least some data"}, 400

        #get tags from url
        url = args["url"]


        tags = []
        try:
            for t in checks:
                
                tag = {}
                for key in t:
                    
                    if(key == "tag_key"):
                        
                        tag[key] = t[key]
                    else:
                        tag["tag_name"] = key
                        tag["tag_data"] = t[key]
                
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
    def get(self):
        args = Validator.get_parser.parse_args()
        try:
            response = requests.get("http://127.0.0.1:4000/tag_saver", json = {"url":args['url']})
            responseData = response.json()
        except:
            return {'message':'An error retrieving the data'}, 500

        #return what the saving service returned
        return responseData, response.status_code

