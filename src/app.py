from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
# from flask_sslify import SSLify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Sahil23!@localhost/app_localdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
cors = CORS(app)
# sslify = SSLify(app)

from src.service.bar_service import BarService as bar_service
from src.service.drink_service import DrinkService as drink_service
from src.service.brand_service import BrandService as brand_service

@app.route('/test', methods=['GET'])
@cross_origin()
def test():
    return jsonify({'message': 'test works'})


@app.route('/bars', methods=['GET'])
@cross_origin()
def get_bars():
    all_bars = []

    req_arg = request.args.get('offset')
    if (req_arg is None):
        page = 1
    else:
        page = int(req_arg)

    return bar_service().get_all_bars(all_bars, page)


@app.route('/drinks', methods=['GET'])
@cross_origin()
def get_drinks():
    all_drinks = []

    req_arg = request.args.get('offset')
    if (req_arg is None):
        page = 1
    else:
        page = int(req_arg)

    return drink_service().get_all_drinks(all_drinks, page)


@app.route('/brands', methods=['GET'])
@cross_origin()
def get_brands():
    all_brands = []

    req_arg = request.args.get('offset')
    if (req_arg is None):
        page = 1
    else:
        page = int(req_arg)

    return brand_service().get_all_brands(all_brands, page)


@app.route('/brands/<string:brand_name>', methods=['GET'])
@cross_origin()
def get_single_brand(brand_name):
    return brand_service().get_single_brand(brand_name)



@app.route('/drinks/<string:drink_name>', methods=['GET'])
@cross_origin()
def get_single_drink(drink_name):
    return drink_service().get_single_drink(drink_name)


@app.route('/bars/<string:bar_name>', methods=['GET'])
@cross_origin()
def get_single_bar(bar_name):
    return bar_service().get_single_bar(bar_name)
