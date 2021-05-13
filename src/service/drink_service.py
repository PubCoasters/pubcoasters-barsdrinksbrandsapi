from flask import jsonify
from src.models.drink import Drink

class DrinkService():

    def get_all_drinks(self, all_drinks, offset):
        try:
            drinks = Drink.query.paginate(page=offset, per_page=5)
            for drink in drinks.items:
                return_drink = {'uuid': drink.uuid, 'name': drink.name}
                all_drinks.append(return_drink)
            return jsonify(all_drinks)
        except Exception as e:
            print(e)
            return jsonify({'message': 'unable to retrieve drinks'}), 500

    def get_single_drink(self, drink_name):
        try:
            drink = Drink.query.filter_by(name=drink_name.lower()).first()
            if drink is None:
                return jsonify({}), 200
            return_drink = {'uuid': drink.uuid, 'name': drink.name}
            return jsonify(return_drink)
        except Exception as e:
            print(e)
            return jsonify({'message': 'unable to retrieve drink'}), 500