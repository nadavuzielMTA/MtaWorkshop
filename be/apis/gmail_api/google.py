import datetime
import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


def Create_Service(api_name, api_version, *scopes):
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    pickle_file = 'be/apis/gmail_api/token.json'

    if os.path.exists(pickle_file):
        cred = Credentials.from_authorized_user_file(pickle_file, SCOPES)
    else:
        cred = None
    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None


def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt