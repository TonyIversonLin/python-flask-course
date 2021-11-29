from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel


class Item(Resource):

    @jwt_required() 
    def get(self, name):
        target_item = ItemModel.find_by_name(name)

        if target_item:
            return target_item.json()
        else:
            return {'message': 'item no found'}, 404
    
    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float, required=True, help='this field can not be blank.')
        parser.add_argument('store_id', type=int, required=True, help='this field can not be blank.')
        request_data = parser.parse_args()

        check_item_exist = ItemModel.find_by_name(name)

        if check_item_exist:
            return {'message': 'Item already existed'}, 400  # something wrong with the request
        else:
            item = ItemModel(name, request_data['price'], request_data['store_id'])
            try:
                item.save_to_db()
                return 201
            except:
                return {'message': 'An error occurred inserting the item'}, 500 # Internal server error
            

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float, required=True, help='this field can not be blank.')
        parser.add_argument('store_id', type=int, required=True, help='this field can not be blank.')
        request_data = parser.parse_args()

        target_item = ItemModel.find_by_name(name)

        if target_item is None:
            new_item = ItemModel(name, request_data['price'], request_data['store_id'])
            new_item.save_to_db()
        else:
            target_item.price = request_data['price']
            target_item.store_id = request_data['store_id']
            target_item.save_to_db()
        

    def delete(self, name):
        target_item = ItemModel.find_by_name(name)
        if target_item:
            target_item.delete_to_db()
            return {'message': 'Item deleted'}
        else:
            return {'message': 'Item does not exist'}




class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}, 200
