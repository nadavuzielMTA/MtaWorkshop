import time
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from mongo.db_client import AtlasMongoClient
from apis.zoom_api.zoom_api import ZoomAPI
from apis.gmail_api.gmail import GmailAPI

mongo = AtlasMongoClient()
zoom = ZoomAPI()
gmail = GmailAPI()
parser = RequestParser()


class SomethingResource(Resource):
    def aget(self):
        return {'time': time.time()}

    def get(self):
        db = mongo.db
        return {'time': db.test.find_one()['time']}


class ComplaintResource(Resource):
    def get(self):
        complains = mongo.db.complaints
        return {'time': complains.find_one()['content']}


class ZoomResource(Resource):
    def get(self):
        join_url, meeting_password = zoom.createMeeting()
        info = f'here is your zoom meeting link {join_url} and your password: "{meeting_password}"'
        return {'time': info}


class GmailResource(Resource):
    def get(self):
        join_url, meeting_password = zoom.createMeeting()
        # gmail.send_mail(join_url, meeting_password)
        return {'time': f'{join_url}, {meeting_password}'}
