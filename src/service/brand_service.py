from flask import jsonify
from models.brand import Brand
from models.user_brand import UserBrand

class BrandService():

    def get_all_brands(self, all_brands, user, offset):
        try:
            brands = Brand.query.distinct().outerjoin(UserBrand, UserBrand.brand_id == Brand.id).paginate(page=offset, per_page=5)
            for brand in brands.items:
                return_brand = None
                if len(brand.user_brand) == 0:
                    return_brand = {
                        'uuid': brand.uuid, 
                        'brandName': brand.name, 
                        'type': ('' if brand.type is None else brand.type),
                        'userLiked': False
                    }
                else:
                   user_found = user in (obj.user_name for obj in brand.user_brand)
                   return_brand = {
                        'uuid': brand.uuid, 
                        'brandName': brand.name, 
                        'type': ('' if brand.type is None else brand.type),
                        'userLiked': user_found
                    } 
                all_brands.append(return_brand)
            return jsonify(all_brands)
        except Exception as e:
            print(e)
            if (e.__str__() == '404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'):
                return jsonify([])
            return jsonify({'message': 'unable to retrieve brands'}), 500

    def get_single_brand(self, brand_name, user):
        try:
            return_brands = []
            brand = Brand.query.distinct().filter_by(name=brand_name.lower()).outerjoin(UserBrand, UserBrand.brand_id == Brand.id).first()
            if brand is None:
                return jsonify([]), 200
            if len(brand.user_brand) == 0:
                return_brand = {
                    'uuid': brand.uuid, 
                    'brandName': brand.name,
                    'type': ('' if brand.type is None else brand.type),
                    'userLiked': False
                }
            else:
                user_found = user in (obj.user_name for obj in brand.user_brand)
                return_brand = {
                    'uuid': brand.uuid, 
                    'brandName': brand.name, 
                    'type': ('' if brand.type is None else brand.type),
                    'userLiked': user_found
                } 
            return_brands.append(return_brand)
            return jsonify(return_brands)
        except Exception as e:
            print(e)
            return jsonify({'message': 'unable to retrieve brand'}), 500
