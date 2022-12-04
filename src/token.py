from flask import Blueprint, request, jsonify
from datetime import datetime
from src.modules.mongedb import mongo


token = Blueprint("token",__name__, url_prefix="/api/v1/token")


@token.route("/create/token", methods = ["POST"])
def create_token():
    # initialize mongo db
    db = mongo.Embraceher.tokens
    # initialize all respose variables
    data = {}
    status = False
    message = "invalid request"
    # check request type
    if request.method=="POST":
        token = request.json.get("Token","").strip()
        # print(len(token))
        # check token lenght
        if len(token)!= 6:
            message = "length of token should be equall 6"
            return jsonify({"status": status, "data": data, "message":message})

        # check if token already exitt
        chk_token = db.find_one({"Token":token})
        if chk_token is not None:
            message = "token already exit"
            return jsonify({"status": status, "data": data, "message":message})
        
        # insert into db and set valid equall false for new token
        db.insert_one({"Token":token, "Created_at":datetime.now(), "valid": True})

        status = True
        data = {"Token":token, "Created_at":datetime.now(), "valid": True}

    return jsonify({"status": status, "data": data, "message":message})
        

