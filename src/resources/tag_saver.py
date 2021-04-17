import requests
from flask_restful import Resource, reqparse
import json

from models.tag import TagModel, URL_Model

class TagSaver(Resource):
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
        args = TagSaver.post_parser.parse_args()

        url = URL_Model.find_by_url(args['url'])
        if(url is None):
            URL_Model(args['url']).save_to_db()
            url = URL_Model.find_by_url(args['url'])

        models = []
        for t in args['tags']:
            if(TagModel.find_tag(url.uid, t['tag_name'], t['tag_key']) is None):
                models.append(TagModel(url.uid, t['tag_name'], t['tag_data'], t['tag_key']))
            else:
                return {"message":"tag already in database"}, 500


        try:
            TagModel.save_list_to_db(models)
        except Exception as e:
            return {'message':str(e)}, 500


        return {'message':'Data saved successfully'}


    get_parser = reqparse.RequestParser()
    get_parser.add_argument('url',
        type = str,
        required = True,
        help = "Invalid input"
    )
    def get(self):
        args = TagSaver.get_parser.parse_args()

        url = URL_Model.find_by_url(args['url'])
        if(url is None):
            return {"message":"URL is not stored in database"}
        
        tags = TagModel.find_all_by_url_id(url.uid)

        return {"tags": [t.json() for t in tags]}
