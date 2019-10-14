from config import app, api
from auth import Register, Login, Logout
from views import (
    GetUserDetails
)
from flask import send_from_directory

api.add_resource(Register, "/register")
api.add_resource(Login, "/login")
api.add_resource(GetUserDetails, "/get-user-details")
api.add_resource(Logout, "/logout")

@app.route('/assets/<path:path>')
def serve_files(path):
    return send_from_directory('templates/assets/', path)

@app.route("/")
def index():
    return {"status": "server is up and running"}
