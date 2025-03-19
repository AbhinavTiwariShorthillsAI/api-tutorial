from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User: {self.name}, Email: {self.email}>'
    
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help='Name cannot be blank')
user_args.add_argument('email', type=str, required=True, help='Email cannot be blank')

userfields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}

class Users(Resource):
    @marshal_with(userfields)
    def get(self):
        users = UserModel.query.all()
        return users
    
    @marshal_with(userfields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args['name'], email=args['email'])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201
    
class User(Resource):
    @marshal_with(userfields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message='User not found')
        return user
    
    @marshal_with(userfields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message='User not found')
        user.name = args['name']
        user.email = args['email']
        db.session.commit()
        return
    
    @marshal_with(userfields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message='User not found')
        db.session.delete(user)
        db.session.commit()
        return user, 204

api.add_resource(Users, '/users')
api.add_resource(User, '/users/<int:id>')

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)  

