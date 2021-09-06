import datetime
import time
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from be.mongo.db_client import AtlasMongoClient
from be.apis.zoom_api.zoom_api import ZoomAPI
from be.apis.gmail_api.gmail import GmailAPI

mongo = AtlasMongoClient()
db = mongo.db
zoom = ZoomAPI()
gmail = GmailAPI()
parser = RequestParser()


class PsycologistResource(Resource):
    def get(self):
        args = parser.parse_args()
        psychologist_name = args.get('psychologist_name')
        action = args.get('action')
        if action == 'available_dates':
            return self.get_available_dates_from_psycologist()

        elif action == 'available_time':
            psychologist_details = db.psycologist.fine_one({"name": psychologist_name})
            zoom_meetings = psychologist_details.get('zoom_meetings')
            return self.get_available_time_for_psycologist(zoom_meetings)

        print(db.test.find_one()['time'])
        return {'time': db.test.find_one()['time']}

    @staticmethod
    def get_available_dates_from_psycologist():
        sdate = datetime.datetime.now().date()
        available_dates = [sdate + datetime.timedelta(days=i) for i in range(30)]
        return available_dates

    @staticmethod
    def get_available_time_for_psycologist(zoom_meetings):
        stime = datetime.time(9, 00)

        available_appointments = [(datetime.datetime.combine(datetime.date(1, 1, 1), stime) +
                                   datetime.timedelta(minutes=30*i)).time() for i in range(18)]
        for zoom_meeting in zoom_meetings:
            if zoom_meeting['start_time'] in available_appointments:
                available_appointments.pop(zoom_meeting['start_time'])
        return available_appointments


class ComplaintResource(Resource):
    def get(self):
        complains = mongo.db.complaints
        return {'time': complains.find_one()['content']}


class ZoomMeetingResource(Resource):
    def get(self):
        args = parser.parse_args()
        username = args.get('username')
        user_details = db.user.find({'username': username})
        zoom_meeting_details = user_details.get('zoom_meeting_details')
        return zoom_meeting_details.get('id'), zoom_meeting_details.get('zoom_link')

    def post(self):
        args = parser.parse_args()
        username = args.get('username')
        date = args.get('date')
        start_time = args.get('start_time')
        psycologist_name = args.get('psycologist_name')

        date_and_time = date + 'T10:' + start_time
        zoom_link = zoom.createMeeting(date_and_time)
        zoom_meeting_details = {"zoom_meeting_details": {"zoom_link"},
                                                         "date": date,
                                                         "start_time": start_time}
        db.user.find_one_and_update({"username": username},
                                    {"$set": zoom_meeting_details}, upsert=True)

        db.psycologist.fine_one_and_update({"name": psycologist_name},
                                           {"$push": {'zoom_meetings': zoom_meeting_details}}, upsert=True)

        return zoom_link
