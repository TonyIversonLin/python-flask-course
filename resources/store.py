from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.store import StoreModel

class Store(Resource):

    def get(self, name):
        target_store = StoreModel.find_by_name(name)

        if target_store:
            return target_store.json(), 200
        else:
            return {'message': 'store not found'}, 404
    
    def post(self, name):

        print('i am here')
        if StoreModel.find_by_name(name):
            return {'message': 'A store is already exist'}
        else:
            new_store = StoreModel(name)

            try:
                new_store.save_to_db()
                return 201
            except:
                return {'message': 'Fail to save'}, 500


    def delete(self, name):
        target_store = StoreModel.find_by_name(name)
        if target_store:
            target_store.delete_to_db()
            return {'message': 'Store deleted'}
        else:
            return {'message': 'Store not exist'}


class StoreList(Resource):
    
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}, 200