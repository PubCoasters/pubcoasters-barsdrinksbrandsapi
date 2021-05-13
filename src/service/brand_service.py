from flask import jsonify
from src.models.brand import Brand

class BrandService():

    def get_all_brands(self, all_brands, offset):
        try:
            brands = Brand.query.paginate(page=offset, per_page=5)
            for brand in brands.items:
                return_brand = {'uuid': brand.uuid, 'name': brand.name, 'type': ('' if brand.type is None else brand.type)}
                all_brands.append(return_brand)
            return jsonify(all_brands)
        except Exception as e:
            print(e)
            return jsonify({'message': 'unable to retrieve brands'}), 500
