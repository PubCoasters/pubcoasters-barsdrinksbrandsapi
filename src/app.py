from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_sslify import SSLify
from config import Config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{Config.credentials['username']}:{Config.credentials['password']}@/{Config.credentials['schema']}?unix_socket=/cloudsql/{Config.credentials['connectionname']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
cors = CORS(app)
sslify = SSLify(app)

from service.bar_service import BarService as bar_service
from service.drink_service import DrinkService as drink_service
from service.brand_service import BrandService as brand_service

@app.route('/test', methods=['GET'])
@cross_origin()
def test():
    return jsonify({'message': 'test works'})


@app.route('/bars', methods=['GET'])
@cross_origin()
def get_bars():
    all_bars = []
    user_arg = request.args.get('user')
    req_arg = request.args.get('offset')
    if (req_arg is None):
        page = 1
    else:
        page = int(req_arg)

    return bar_service().get_all_bars(all_bars, user_arg, page)


@app.route('/drinks', methods=['GET'])
@cross_origin()
def get_drinks():
    all_drinks = []
    user_arg = request.args.get('user')
    req_arg = request.args.get('offset')
    if (req_arg is None):
        page = 1
    else:
        page = int(req_arg)

    return drink_service().get_all_drinks(all_drinks, user_arg, page)


@app.route('/brands', methods=['GET'])
@cross_origin()
def get_brands():
    all_brands = []
    user_arg = request.args.get('user')
    req_arg = request.args.get('offset')
    if (req_arg is None):
        page = 1
    else:
        page = int(req_arg)

    return brand_service().get_all_brands(all_brands, user_arg, page)


@app.route('/brand/<string:brand_name>', methods=['GET'])
@cross_origin()
def get_single_brand(brand_name):
    user_arg = request.args.get('user')
    return brand_service().get_single_brand(brand_name, user_arg)



@app.route('/drink/<string:drink_name>', methods=['GET'])
@cross_origin()
def get_single_drink(drink_name):
    user_arg = request.args.get('user')
    return drink_service().get_single_drink(drink_name, user_arg)


@app.route('/bar/<string:bar_name>', methods=['GET'])
@cross_origin()
def get_single_bar(bar_name):
    user_arg = request.args.get('user')
    req_arg = request.args.get('offset')
    if (req_arg is None):
        page = 1
    else:
        page = int(req_arg)
    return bar_service().get_bar_by_name(bar_name, user_arg, page)
