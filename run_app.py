from flask import Flask
from flask_restful import Api

from pipelines.rest_server import ComplaintResource, GmailResource, ZoomResource

app = Flask(__name__)
api = Api(app)

api.add_resource(ZoomResource, '/time')
api.add_resource(ComplaintResource, '/complaint')
api.add_resource(GmailResource, '/send_mail')

if __name__ == '__main__':
    while True:
        try:
            app.run()
        except Exception as e:
            print(e)
