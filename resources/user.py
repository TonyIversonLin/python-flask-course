import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='this field can not be blank.')
        parser.add_argument('password', type=str, required=True, help='this field can not be blank.')
        data = parser.parse_args()

        existed_user = UserModel.find_by_username(data['username'])

        if existed_user:
            return {'message': 'User already existed'}, 400
        else:
            new_user = UserModel(data['username'], data['password'])
            new_user.save_to_db()

            return {'message': 'User created successfully'}, 201


