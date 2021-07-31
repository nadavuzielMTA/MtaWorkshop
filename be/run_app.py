from flask import Flask
from flask_restful import Api

from be.pipelines.rest_server.rest_server import ZoomResource, ComplaintResource, GmailResource

app = Flask(__name__)
api = Api(app)

api.add_resource(ZoomResource, '/time')
api.add_resource(ComplaintResource, '/complaint')
api.add_resource(GmailResource, '/send_mail')

if __name__ == '__main__':
    app.run()

