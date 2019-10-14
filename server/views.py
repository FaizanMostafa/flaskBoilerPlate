from flask_restful import Resource, reqparse
from flask_login import login_required, current_user
from flask import jsonify
from werkzeug.utils import secure_filename
from auth import getUser
from db import db
import json
from helper import JSONEncoder
from datetime import datetime

Users = db["Users"]

parser = reqparse.RequestParser()


class GetUserDetails(Resource):
    @login_required
    def get(self):
        try:
            user = getUser(current_user.email)
            retJson = {
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
                    "registeredAt": user["registeredAt"],
                    "preferences": {
                        "jobRadius": user["preferences"]["jobRadius"],
                        "jobType": user["preferences"]["jobType"],
                        "country": user["preferences"]["country"],
                        "city": user["preferences"]["city"],
                        "excludedSkills": user["preferences"]["excludedSkills"],
                        "sameAddress": user["preferences"]["sameAddress"],
                        "emailNotifications": user["preferences"]["emailNotifications"]
                    }
                }
            }
            return jsonify(retJson)
        except Exception as err:
            print("Error: ", err)
            retJson = {
                "status": 500,
                "message": "err"
            }
            return jsonify(retJson)