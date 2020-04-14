from flask import Flask, request, jsonify, g
from simplexml  import dumps
from flask import Flask, request, jsonify, g
#from flask_restful import Resource, Api, reqparse
from .estimator import estimator
import time

app = Flask(__name__)
app.config['DEBUG'] = True
# api = Api(app)

# Data = {
#     region: {
#         name: "Africa",
#         avgAge: 19.7,
#         avgDailyIncomeInUSD: 5,
#         avgDailyIncomePopulation: 0.71
#     },
#     periodType: "days",
#     timeToElapse: 58,
#     reportedCases: 674,
#     population: 66622705,
#        totalHospitalBeds: 1380614
# }

@app.before_request
def before_req():
    g.start = time.time() * 1000


@app.after_request
def after_req(response):
    f = open('logs.txt', 'a+')
    request_method = request.method
    request_path = request.path
    response_time = round(time.time() * 1000 - g.start)
    response_status_code = response.status_code

    f.write("{} \t\t {} \t\t {} \t\t {} ms \n".format(request_method, request_path, response_status_code, response_time))
    f.close()
    return response


@app.route('/')
def home():
    return "Building for SDG Andela with Facebook by Denis Mbey Akola"


@app.route('/api/v1/on-covid-19', methods=['POST'])
def get_estimation_default():
    req_data = request.get_json()
    res = estimator(req_data)
    return jsonify(res)


@app.route('/api/v1/on-covid-19/json', methods=['POST'])
def get_estimation_json():
    return get_estimation_default()


@app.route('/api/v1/on-covid-19/xml', methods=['POST'])
def get_estimation_xml():
    req_data = request.get_json()
    res = dumps({'response': estimator(req_data)})
    return res


@app.route('/api/v1/on-covid-19/logs', methods=['GET'])
def get_logs():
    f = open('logs.txt', 'r')
    contents = f.read()
    f.close()
    return contents


app.run()
 