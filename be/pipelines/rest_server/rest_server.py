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

psychologist_name_to_hebrew = {'ליאת הר-טוב': 'leat har-tov',
                               'רינה אאלוף': 'rina aaluf',
                               'קלרה מולדן': 'clara moldan',
                               'אדי גרין': 'adi grin'}


class AppointmentResource(Resource):
    def get(self):
        action = request.args.get('action')
        if action == 'list_of_dates':
            return self.get_available_dates_from_psychologist()

        elif action == 'available_time':
            psychologist_name = request.args.get('psychologist_name')
            psychologist_name = psychologist_name_to_hebrew.get(psychologist_name, '')
            date = request.args.get('date')
            psychologist_zoom_meetings = db.meeting.find({"psychologist_name": psychologist_name, 'date': date})
            return self.get_available_time_for_psychologist(psychologist_zoom_meetings)

    def post(self):
        username = request.form.get('username')
        date = request.form.get('date')
        start_time = request.form.get('time')
        psychologist_name = request.form.get('psychologist_name')
        email = request.form.get('email')

        psychologist_name = psychologist_name_to_hebrew.get(psychologist_name, '')
        user = db.user.find_one({"username": username})
        if not user:
            return 'אנא התחבר לאתר על מהת לקבוע פגישה.\n הרישום לאתר אינו מחייב מסירת פרטים אישיים!'

        user_zoom_meeting = user.get('zoom_meetings', {})
        if user_zoom_meeting:
            zoom_link = user_zoom_meeting.get('zoom_link')
            db.meeting.find_one_and_delete({'zoom_link': zoom_link})

        date_and_time = date + 'T10: ' + start_time[:3] + ' ' + start_time[3:] # format '2021-10-04T10: 09: 00'
        zoom_link = zoom.createMeeting(date_and_time)
        zoom_obj = {"zoom_link": zoom_link, "date": date, "start_time": start_time,
                    "psychologist_name": psychologist_name, 'user': username}

        db.meeting.insert(zoom_obj)
        db.user.find_one_and_update({"username": username},
                                    {"$set": {'zoom_meetings': zoom_obj}}, upsert=True)

        contnet = 'נרשמת בהצלחה'
        if email:
            gmail.send_mail(zoom_link, email, date, start_time)
            contnet = 'נשרמת בהצלחה, נשלח אליך מייל עם הפרטים'

        return contnet

    @staticmethod
    def get_available_dates_from_psychologist():
        sdate = datetime.datetime.now().date()
        available_dates = [str(sdate + datetime.timedelta(days=i)) for i in range(30)]
        return available_dates

    @staticmethod
    def get_available_time_for_psychologist(zoom_meetings):
        stime = datetime.time(9, 00)

        available_appointments = [str((datetime.datetime.combine(datetime.date(1, 1, 1), stime) +
                                       datetime.timedelta(minutes=30*i)).time())[:-3] for i in range(19)]

        if zoom_meetings.count == 0:
            return available_appointments

        for zoom_meeting in zoom_meetings:
            if zoom_meeting['start_time'] in available_appointments:
                available_appointments.remove(zoom_meeting['start_time'])
        return available_appointments


class lawyerComplaintResource(Resource):
    def get(self):
        complaints = db.complaint.find()
        return [{'name': complaint.get('name'), 'user_id': complaint.get('user_id'),
                 'description': complaint.get('description'), 'last_update': str(complaint.get('last_update')),
                 'sent': complaint.get('sent'), 'sent_to_police': complaint.get('sent_to_police'),
                 'in_treatment': complaint.get('in_treatment'), 'done': complaint.get('done'),
                 'created': complaint.get('created')} for complaint in complaints]

    def post(self):
        user_id = request.form.get('user_id')
        sent = request.form.get('sent')
        sent_to_police = request.form.get('sent_to_police')
        in_treatment = request.form.get('in_treatment')
        done = request.form.get('done')

        db.complaint.find_one_and_update({"user_id": user_id},
                                         {"$set": {'sent_to_police': sent_to_police == 'true', 'sent': sent == 'true',
                                                   'in_treatment': in_treatment == 'true', 'done': done == 'true'}},
                                         upsert=True)


class ComplaintResource(Resource):
    def get(self):
        username = request.args.get('username')
        complaint = db.complaint.find_one({'username': username})
        if not complaint:
            return {'sent_to_police': 'false', 'sent': 'false',
                    'in_treatment': 'false', 'done': 'false'}
        return {'sent_to_police': complaint['sent_to_police'], 'sent': complaint['sent'],
                'in_treatment': complaint['in_treatment'], 'done': complaint['done']}

    def post(self):
        name = request.form.get('name')
        user_id = request.form.get('user_id')
        email = request.form.get('email')
        city = request.form.get('city')
        phone_number = request.form.get('phone_number')
        date = request.form.get('date')
        place = request.form.get('place')
        time = request.form.get('time')
        description = request.form.get('description')
        username = request.form.get('username')

        user_complaint = db.complaint.find_one({'user_id': user_id})
        if user_complaint:
            db.complaint.remove({'user_id': user_id})
        try:
            db.complaint.insert({'name': name, 'user_id': user_id, 'email': email, 'city': city,
                                 'phone_number': phone_number, 'date': date, 'place': place, 'time': time,
                                 'description': description, 'username': username, 'sent': True,
                                 'sent_to_police': False, 'in_treatment': False, 'done': False,
                                 'last_update': str(datetime.datetime.now().date()),
                                 'created': str(datetime.datetime.now().date())})
        except Exception as e:
            return e

        return "התלונה נרשמה במערכת וטטופל בהקדם. אנא עקוב אחר האיזור האישי."


class ZoomMeetingResource(Resource):
    def get(self):
        username = request.args.get('username')

        if not username:
            return {}

        if username in psychologist_name_to_hebrew.values():
            zoom_meetings = db.meeting.find({'psychologist_name': username})
        else:
            zoom_meetings = db.meeting.find({'user': username})

        return [{'title': zoom_meeting['start_time'],
                 'url': zoom_meeting['zoom_link'],
                 'start': zoom_meeting['date']} for zoom_meeting in zoom_meetings]


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


