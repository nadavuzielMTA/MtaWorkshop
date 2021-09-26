import datetime
from flask import request
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from be.mongo.db_client import AtlasMongoClient
from be.apis.zoom_api.zoom_api import ZoomAPI
from be.apis.gmail_api.gmail import GmailAPI

import logging

mongo = AtlasMongoClient()
db = mongo.db
zoom = ZoomAPI()
gmail = GmailAPI()
parser = RequestParser()


class PsycologistResource(Resource):
    def get(self):
        list_psycologists_names = []
        psycologists = db.psycologist.find()

        for psycologist in psycologists:
            list_psycologists_names.append(psycologist.get('name'))

        return list_psycologists_names


class AppointmentResource(Resource):
    def get(self):
        psychologist_name = request.args.get('psychologist_name')
        action = request.args.get('action')
        if action == 'list_of_dates':
            return self.get_available_dates_from_psycologist()

        elif action == 'available_time':
            date = request.args.get('date')
            psychologist_zoom_meetings = db.zoom.fine_one({"psychologist_name": psychologist_name},
                                                          {'date': date})
            if not psychologist_zoom_meetings:
                return ['אין שעות פנויות ביום זה.\n נסה בתאריך אחר :)']

            return self.get_available_time_for_psycologist(psychologist_zoom_meetings)

    def post(self):
        username = request.form.get('username')
        date = request.form.get('date')
        start_time = request.form.get('start_time')
        psycologist_name = request.form.get('psycologist_name')
        email = request.form.get('email')

        user = db.user.find_one({"username": username})
        if not user:
            return 'אנא התחבר לאתר על מהת לקבוע פגישה.\n הרישום לאתר אינו מחייב מסירת פרטים אישיים!'

        date_and_time = date + 'T10:' + start_time
        zoom_link = zoom.createMeeting(date_and_time)
        zoom_obj = {"zoom_link": zoom_link, "date": date, "start_time": start_time,
                    "psycologist_name": psycologist_name, 'user': username}

        db.zoom.insert(zoom_obj)
        db.user.find_one_and_update({"username": username},
                                    {"$set": {'zoom_meetings': zoom_obj}}, upsert=True)
        db.psycologist.find_one_and_update({"name": psycologist_name},
                                           {"$push": {'zoom_meetings': zoom_obj}}, upsert=True)

        contnet = 'נרשמת בהצלחה'
        if email:
            gmail.send_mail(zoom_link, email, date, start_time)
            contnet = 'נשרמת בהצלחה, נשלח אליך מייל עם הפרטים'

        return contnet

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
        username = request.args.get('username')
        user_details = db.user.find({'username': username})
        zoom_meeting_details = user_details.get('zoom_meeting_details')
        return zoom_meeting_details.get('id'), zoom_meeting_details.get('zoom_link')


class RegisterResource(Resource):

    #login
    def get(self):
        username = request.args.get('username')
        password = request.args.get('password')
        user = db.user.find_one({"username": username})
        if user and user.get('password') == password:
            return True
        return False

    #register
    def post(self):
        args = parser.parse_args()
        username = request.form.get('username')
        password = request.form.get('password')
        user = db.user.find({"username": username})
        if user.count() != 0:
            return False

        try:
            user = db.user.insert_one({"username": username, "password": password})
        except Exception as e:
            logging.warning(f'failed to add user : {username} {password} ')
            user = None

        if user:
            return True

        return False