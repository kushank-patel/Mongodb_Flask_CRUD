from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)

app.secret_key = "secretkey"

app.config['MONGO_URI'] = "mongodb://127.0.0.1:27017/Users"

mongo = PyMongo(app)

# To add user in Mongodb 
@app.route('/add',methods=['POST'])
def add_user():
    json = request.json
    name = json['name']
    email = json['email']
    password = json['pwd']

    if name and email and password and request.method =='POST':
        hashed_password = generate_password_hash(password)
        id = mongo.db.Users.insert({'name':name,'email':email,'pwd':hashed_password})
        resp = jsonify("user added successfully")
        resp.status_code = 200
        return resp

    else:
        return not_found()

# Retrive users from Mongodb
@app.route('/users')
def users():
    users = mongo.db.Users.find()
    resp = dumps(users)
    return resp

# Search for perticular user
@app.route('/user/<id>')
def user(id):
    user = mongo.db.Users.find_one({'_id':ObjectId(id)})
    resp = dumps(user)
    return resp

# Delete perticular user
@app.route('/delete/<id>',methods=['DELETE'])
def delete_user(id):
    mongo.db.Users.delete_one({'_id':ObjectId(id)})
    resp = jsonify("User deleted successfully")
    resp.status_code = 200
    return resp

# Update user informations
@app.route('/update/<id>',methods=['PUT'])
def update_user(id):
    _id = id
    json = request.json
    name = json['name']
    email = json['email']
    password = json['pwd']

    if name and email and password and _id and request.method =='PUT':
        hashed_password = generate_password_hash(password)
        mongo.db.Users.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'name':name, 'email':email, 'pwd': hashed_password}})
        resp = jsonify("User updated successfully")
        resp.status_code = 200
        return resp

    else:
        return not_found()      

# Error handling
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

if __name__ == "__main__":
    app.run(debug=True)