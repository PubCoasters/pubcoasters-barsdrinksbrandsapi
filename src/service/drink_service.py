from flask import jsonify
from models.drink import Drink
from models.user_drink import UserDrink

class DrinkService():

    def get_all_drinks(self, all_drinks, user, offset):
        try:
            drinks = Drink.query.distinct().outerjoin(UserDrink, Drink.id == UserDrink.drink_id).paginate(page=offset, per_page=5)
            for drink in drinks.items:
                if len(drink.user_drink) == 0:
                    return_drink = {
                        'uuid': drink.uuid, 
                        'drinkName': drink.name,
                        'userLiked': False
                    }
                else:
                    user_found = user in (obj.user_name for obj in drink.user_drink)
                    return_drink = {
                        'uuid': drink.uuid, 
                        'drinkName': drink.name,
                        'userLiked': user_found
                    }
                all_drinks.append(return_drink)
            return jsonify(all_drinks)
        except Exception as e:
            print(e)
            if (e.__str__() == '404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'):
                return jsonify([])
            return jsonify({'message': 'unable to retrieve drinks'}), 500

    def get_single_drink(self, drink_name, user):
        try:
            return_drinks = []
            drink = Drink.query.distinct().filter_by(name=drink_name.lower()).outerjoin(UserDrink, Drink.id == UserDrink.drink_id).first()
            if drink is None:
                return jsonify([]), 200
            if len(drink.user_drink) == 0:
                return_drink = {
                    'uuid': drink.uuid, 
                    'drinkName': drink.name,
                    'userLiked': False
                }
            else:
                user_found = user in (obj.user_name for obj in drink.user_drink)
                return_drink = {
                    'uuid': drink.uuid, 
                    'drinkName': drink.name,
                    'userLiked': user_found
                }
            return_drinks.append(return_drink)
            return jsonify(return_drinks)
        except Exception as e:
            print(e)
            return jsonify({'message': 'unable to retrieve drink'}), 500