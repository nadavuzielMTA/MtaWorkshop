import jwt
import requests
import json
from time import time
from datetime import datetime

API_KEY = 'hZM0-vF-TBuPLXKb6tStQw'
API_SEC = '9dV8iXmt8LWrhglgEsY5thmWvEKkXiFrJOfI'


class ZoomAPI:
    def createMeeting(self, date_and_time):
        meeting_details = self.generate_meeting_details(date_and_time)
        headers = {'authorization': 'Bearer %s' % self.generateToken(),
                   'content-type': 'application/json'}
        r = requests.post(
            f'https://api.zoom.us/v2/users/me/meetings',
            headers=headers, data=json.dumps(meeting_details))

        print("\n creating zoom meeting ... \n")
        # print(r.text)
        # converting the output into json and extracting the details
        y = json.loads(r.text)
        join_url = y["join_url"]

        return join_url

    # create a function to generate a token
    # using the pyjwt library
    @staticmethod
    def generateToken():
        token = jwt.encode(

            # Create a payload of the token containing
            # API Key & expiration time
            {'iss': API_KEY, 'exp': time() + 5000},

            # Secret used to generate token signature
            API_SEC,

            # Specify the hashing alg
            algorithm='HS256'
        )
        return token

    @staticmethod
    def generate_meeting_details(date_and_time) :
        return {"topic": "The title of your zoom meeting",
                "type": 2,
                "start_time": f'{date_and_time}',
                "duration": "30",
                "timezone": "Europe/Madrid",
                "agenda": "test",

                "recurrence": {"type": 1,
                             "repeat_interval": 1},
                "password": "1234",
                "settings": {"host_video": "true",
                            "participant_video": "False",
                            "join_before_host": "False",
                            "mute_upon_entry": "False",
                            "watermark": "true",
                            "audio": "voip",
                            "auto_recording": "cloud"}}
