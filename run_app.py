from flask import Flask
from flask_restful import Api

from be.pipelines.rest_server.rest_server import ZoomMeetingResource, PsycologistResource, RegisterResource

app = Flask(__name__)
api = Api(app)

api.add_resource(ZoomMeetingResource, '/api/zoom_meeting')
api.add_resource(PsycologistResource, '/api/create_meeting')
api.add_resource(RegisterResource, '/api/login')

if __name__ == '__main__':
    try:
        app.run()
    except Exception as e:
        print(e)

