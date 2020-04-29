from data.db_session import create_session
from data.users import User

from api.parsers.parser_user import parser

from flask_restful import abort, Resource
from flask import jsonify


def abort_if_user_not_found(user_id):
    session = create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f'User {user_id} not found')


class UserResourse(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = create_session()
        user = session.query(User).get(user_id)
        return jsonify(
            {
                'users': [user.to_dict(only=['id', 'surname', 'name', 'age', 'hometown', 'position', 'speciality', 'address', 'email'])]
            }
        )

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResourse(Resource):
    def get(self):
        session = create_session()
        users = session.query(User).all()
        return jsonify(
            {
                'users': [item.to_dict(only=['id', 'surname', 'name', 'age', 'hometown', 'position', 'speciality', 'address', 'email']) for item in users]
            }
        )

    def post(self):
        args = parser.parse_args()
        session = create_session()
        if session.query(User.email).filter(User.email == args['email']).first():
            return jsonify({'error': 'Email is already exists'})
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            hometown=args['hometown'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'])
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
