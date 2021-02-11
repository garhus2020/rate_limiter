from flask import Flask, Request ,Response , abort
from flask_restful import Resource, Api, reqparse
from time import time
from configparser import ConfigParser
import datetime
from flask.json import jsonify

parser = ConfigParser()
parser.read('conf.ini')
c_rate = int(parser.get("rate_limiter", "rate"))
c_period=int(parser.get("rate_limiter", "period"))

app = Flask(__name__)
api = Api(app)


class Middleware:
    cont=[] # Container to hold the api requests with timestamp
    def __init__(self, app):
        self.app = app
    def __call__(self, env, start_response):
        def new_start_response(status, headers, exc_info=None):
            max_rate= c_rate
            begin_time = time()-c_period  # in this case 1 hour ago
            req_remain = sum(i>begin_time for i in Middleware.cont) +1 # number of requests in the last 1 hour
            if (req_remain <= max_rate) :
                Middleware.cont.append(time())
                headers.append(('X-RateLimit-Limit', c_rate))
                headers.append(('X-RateLimit-Remaining', c_rate-req_remain))
            else :
                abort(403 , "Rate limit exceeded")

            return start_response(status, headers, exc_info)

        return self.app(env, new_start_response)



class DateHandler(Resource):
    def get(self):
        date = datetime.datetime.now()
        return jsonify({'Now the date is': date})

api.add_resource(DateHandler, '/date/')
app.wsgi_app = Middleware(app.wsgi_app)

if __name__ == "__main__":
  app.run(host='0.0.0.0',debug=True)
