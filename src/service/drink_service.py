from flask import jsonify
from src.models.drink import Drink
from src.models.user_drink import UserDrink

class DrinkService():

    def get_all_drinks(self, all_drinks, user, offset):
        try:
            drinks = Drink.query.outerjoin(UserDrink, Drink.id == UserDrink.drink_id).paginate(page=offset, per_page=5)
            for drink in drinks.items:
                if len(drink.user_drink) == 0:
                    return_drink = {
                        'uuid': drink.uuid, 
                        'name': drink.name,
                        'userLiked': False
                    }
                else:
                    user_found = user in (obj.user_name for obj in drink.user_drink)
                    return_drink = {
                        'uuid': drink.uuid, 
                        'name': drink.name,
                        'userLiked': user_found
                    }
                all_drinks.append(return_drink)
            return jsonify(all_drinks)
        except Exception as e:
            print(e)
            return jsonify({'message': 'unable to retrieve drinks'}), 500

    def get_single_drink(self, drink_name, user):
        try:
            drink = Drink.query.filter_by(name=drink_name.lower()).outerjoin(UserDrink, Drink.id == UserDrink.drink_id).first()
            if drink is None:
                return jsonify({}), 200
            if len(drink.user_drink) == 0:
                return_drink = {
                    'uuid': drink.uuid, 
                    'name': drink.name,
                    'userLiked': False
                }
            else:
                user_found = user in (obj.user_name for obj in drink.user_drink)
                return_drink = {
                    'uuid': drink.uuid, 
                    'name': drink.name,
                    'userLiked': user_found
                }
            return jsonify(return_drink)
        except Exception as e:
            print(e)
            return jsonify({'message': 'unable to retrieve drink'}), 500