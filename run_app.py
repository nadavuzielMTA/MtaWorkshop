from flask import Flask
from flask_restful import Api

from be.pipelines.rest_server.rest_server import ZoomMeetingResource, RegisterResource, AppointmentResource, \
    NewComplaintResource, lawyerComplaintResource

app = Flask(__name__)
api = Api(app)

api.add_resource(ZoomMeetingResource, '/api/meetings')
api.add_resource(AppointmentResource, '/api/appointment')
api.add_resource(RegisterResource, '/api/login')
api.add_resource(NewComplaintResource, '/api/complaint')
api.add_resource(lawyerComplaintResource, '/api/lawyer_complaint')


if __name__ == '__main__':
    try:
        app.run()
    except Exception as e:
        print(e)

