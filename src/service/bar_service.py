from flask import jsonify
from models.bar import Bar
from models.location import Location
from models.neighborhood import Neighborhood
from models.user_bar import UserBar
from app import db

class BarService():

    def get_all_bars(self, all_bars, user, offset):
        try:
            bars_info = Bar.query.distinct().outerjoin(UserBar, Bar.id == UserBar.bar_id).join(Location, Location.id == Bar.location_id).outerjoin(Neighborhood, Neighborhood.id == Bar.neighborhood_id).paginate(page=offset, per_page=5)
            for data in bars_info.items:
                return_bar = None
                if len(data.user_bar) == 0:
                    return_bar = {
                        'uuid': data.uuid,
                        'barName': data.name,
                        'location': data.location.location,
                        'address': ('' if data.address is None else data.address),
                        'type': ('' if data.type is None else data.type),
                        'neighborhood': ('' if data.neighborhood is None else data.neighborhood.neighborhood),
                        'userLiked': False
                    }
                else:
                   user_found = user in (obj.user_name for obj in data.user_bar)
                   return_bar = {
                        'uuid': data.uuid,
                        'barName': data.name,
                        'location': data.location.location,
                        'address': ('' if data.address is None else data.address),
                        'type': ('' if data.type is None else data.type),
                        'neighborhood': ('' if data.neighborhood is None else data.neighborhood.neighborhood),
                        'userLiked': user_found
                    } 
                all_bars.append(return_bar)
            return jsonify(all_bars)
        except Exception as e:
            print(e)
            if (e.__str__() == '404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'):
                return jsonify([])
            return jsonify({'message': 'unable to retrieve bars'}), 500

    
    def get_bar_by_name(self, bar_name, user, page):
        try:
            bar_info = Bar.query.distinct().filter_by(name=bar_name.lower()).outerjoin(UserBar, Bar.id == UserBar.bar_id).join(Location, Location.id == Bar.location_id).outerjoin(Neighborhood, Neighborhood.id == Bar.neighborhood_id).paginate(page=page, per_page=5)
            return_bars = []
            for data in bar_info.items:
                return_bar = None
                if len(data.user_bar) == 0:
                    return_bar = {
                        'uuid': data.uuid,
                        'barName': data.name,
                        'location': data.location.location,
                        'address': ('' if data.address is None else data.address),
                        'type': ('' if data.type is None else data.type),
                        'neighborhood': ('' if data.neighborhood is None else data.neighborhood.neighborhood),
                        'userLiked': False
                    }
                else:
                   user_found = user in (obj.user_name for obj in data.user_bar)
                   return_bar = {
                        'uuid': data.uuid,
                        'barName': data.name,
                        'location': data.location.location,
                        'address': ('' if data.address is None else data.address),
                        'type': ('' if data.type is None else data.type),
                        'neighborhood': ('' if data.neighborhood is None else data.neighborhood.neighborhood),
                        'userLiked': user_found
                    } 
                return_bars.append(return_bar)
            return jsonify(return_bars)
        except Exception as e:
            print(e)
            if (e.__str__() == '404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'):
                return jsonify([])
            return jsonify({'message': 'unable to retrieve bars'}), 500

