from flask import jsonify
from src.models.bar import Bar
from src.models.location import Location
from src.models.neighborhood import Neighborhood
from src.app import db

class BarService():

    def get_all_bars(self, all_bars, offset):
        try:
            bars = db.session.query(Bar, Location).filter(Location.id == Bar.location_id).paginate(page=offset, per_page=5)
            for bar, location in bars.items:
                return_bar = None
                if bar.neighborhood_id is not None:
                    nbhood = Neighborhood.query.filter_by(id=bar.neighborhood_id).first()
                    return_bar = {'uuid': bar.uuid, 'bar': bar.name, 'location': location.location, 'address': ('' if bar.address is None else bar.address), 'type': ('' if bar.type is None else bar.type), 'neighborhood': nbhood.neighborhood}
                else:
                    return_bar = {'uuid': bar.uuid, 'bar': bar.name, 'location': location.location, 'address': ('' if bar.address is None else bar.address), 'type': ('' if bar.type is None else bar.type), 'neighborhood': ''}
                all_bars.append(return_bar)
            return jsonify(all_bars)
        except Exception as e:
            print(e)
            return jsonify({'message': 'unable to retrieve bars'}), 500

