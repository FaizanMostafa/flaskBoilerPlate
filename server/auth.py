from flask_login import login_user, logout_user
from flask import request, jsonify
from flask_restful import Resource, reqparse
import bcrypt
from config import login_manager
from db import db
from datetime import datetime

Users = db["Users"]

parser = reqparse.RequestParser()

class User():
    def __init__(self, email):
        self.email = email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email

def verifyPassword(email, password):
    hashed_pwd = Users.find_one({
        "email": email
    })["password"]

    if bcrypt.checkpw(password.encode("utf8"), hashed_pwd):
        return True
    else:
        return False

@login_manager.unauthorized_handler
def unauthorized():
    retJson = {
        "user": None,
        "status": 401
    }
    return jsonify(retJson)

@login_manager.user_loader
def load_user(email):
    user = Users.find_one({
        "email": email
    })
    if not user:
        return None
    return User(user['email'])

def userExists(email):
    user = Users.find_one({
        "email": email
    })
    if user is not None:
        return True
    else:
        return False

def getUser(email):
    user = Users.find_one({
        "email": email
    })
    return user

def register(data):
    Users.insert_one(data)

def login(email):
    obj = User(getUser(email)["email"])
    login_user(obj)

class Register(Resource):
    def post(self):
        try:
            data = request.get_json()
            firstname = data["firstName"]
            lastname = data["lastName"]
            email = data["email"]
            password = data["password"]
            if userExists(email):
                return jsonify({
                    "emailExists": True,
                    "message": 'User with email "{}" already exist!'.format(email)
                })

            hashed_pw = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())

            register({
                "firstName": firstname,
                "lastName": lastname,
                "email": email,
                "password": hashed_pw,
                "gender": "",
                "phone": "",
                "birthDate": "",
                "country": "",
                "city": "",
                "education": "",
                "type": "",
                "registeredAt": datetime.now()
            })

            user = getUser(email)
            retJson = {
                "type": "success",
                "user": {
                    "firstName": user["firstName"],
                    "lastName": user["lastName"],
                    "email": user["email"],
                    "gender": user["gender"],
                    "phone": user["phone"],
                    "birthDate": user["birthDate"],
                    "country": user["country"],
                    "city": user["city"],
                    "education": user["education"],
                    "type": user["type"],
                    "registeredAt": user["registeredAt"]
                },
                "message": "User registered successfully!"
            }

            return jsonify(retJson)
        except Exception as err:
            print("Error: ", err)
            retJson = {
                "type": "error"
            }
            return jsonify(retJson)

class Login(Resource):
    def post(self):
        try:
            data = request.get_json()
            email = data["email"]
            password = data["password"]
            if not userExists(email):
                return jsonify({
                    "type": "error",
                    "message": 'User with email "{}" doesn\'t exist'.format(email)
                })
            correct_pswd = verifyPassword(email, password)
            if correct_pswd:
                login(email)
                user = getUser(email)
                retJson = {
                    "type": "success",
                    "user": {
                        "firstName": user["firstName"],
                        "lastName": user["lastName"],
                        "email": user["email"],
                        "gender": user["gender"],
                        "phone": user["phone"],
                        "birthDate": user["birthDate"],
                        "country": user["country"],
                        "city": user["city"],
                        "education": user["education"],
                        "type": user["type"],
                        "registeredAt": user["registeredAt"]
                    },
                    "message": "Successfully logged in!"
                }
                return jsonify(retJson)
            else:
                return jsonify({
                    "type": "error",
                    "message": "Wrong credentials"
                })
        except Exception as err:
            print("Error: ", err)
            retJson = {
                "type": "error"
            }
            return jsonify(retJson)

class Logout(Resource):
    def get(self):
        try:
            logout_user()
            retJson = {
                "message": "User logged out successfully",
                "type": "success"
            }
            return jsonify(retJson)
        except Exception as err:
            print("Error: ", err)
            retJson = {
                "type": "error"
            }
            return jsonify(retJson)