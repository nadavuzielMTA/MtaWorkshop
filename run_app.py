from flask import Flask
from flask_restful import Api

from be.pipelines.rest_server.rest_server import ZoomResource, ComplaintResource, GmailResource, SomethingResource

app = Flask(__name__)
api = Api(app)

api.add_resource(ZoomResource, '/zoom')
api.add_resource(ComplaintResource, '/complain')
api.add_resource(SomethingResource, '/api/time')
api.add_resource(GmailResource, '/send_mail')

if __name__ == '__main__':
    try:
        app.run()
    except Exception as e:
        print(e)

