import requests
import json

USER_ID = "E6-WY3ocSrSfq_YMqVeh7w"
TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6ImhaTTAtdkYtVEJ1UExYS2I2dFN0UXciLCJleHAiOjE2NDYyOTQ0MDAsImlhdCI6MTYzMjc1NzYwMH0.DXVWsnKccaLAhaDFbJibaCR7GqjkuytK9Q-NtVlMKvY"


class ZoomAPI:
    def createMeeting(self, date_and_time):
        meeting_details = self.generate_meeting_details(date_and_time)
        headers = {'authorization': 'Bearer %s' % TOKEN,
                   'content-type': 'application/json'}
        r = requests.post(f'https://api.zoom.us/v2/users/{USER_ID}/meetings', headers=headers,
                          data=json.dumps(meeting_details))

        print("\n creating zoom meeting ... \n")
        # print(r.text)
        # converting the output into json and extracting the details
        y = json.loads(r.text)
        join_url = y.get("join_url", 'failed creating zoom url')

        return join_url

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

