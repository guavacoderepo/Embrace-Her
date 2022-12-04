from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from src.modules.mongedb import mongo
from datetime import datetime
import validators

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

# sign up route
@auth.route("create/user", methods=["POST"])
def create_user():
    # initialize all respose variables
    db = mongo.Embraceher

    data = {}
    status = False
    message = "invalid request"
    # check request type
    if request.method=="POST":
        full_name = request.json.get("Full_Name","").strip()
        phone_number = request.json.get("Phone_Number","").strip()
        email = request.json.get("Email","").strip()
        gender = request.json.get("Gender","").strip()
        Nationality = request.json.get("Nationality","").strip()
        username = request.json.get("Username","").strip()
        token = request.json.get("Token","").strip()
        pwd1 = request.json.get("Password","").strip()
        pwd2 = request.json.get("Confirm_Password","").strip()

        # check name lenght
        if len(full_name)<4:
            message = "full name too short or null"
            return jsonify({"status": status, "data": data, "message":message})
        
        # check if name contains at least two words
        if " " not in full_name:
            message = "please enter at least two names"
            return jsonify({"status": status, "data": data, "message":message})

        # check if valid email
        if not validators.email(email):
            message = "invalid email format"
            return jsonify({"status": status, "data": data, "message":message})

# not every user will like their details disposed
# no auth on gender, phone number and nationality

        # check password lenght
        if len(pwd1)<6:
            message = "password too short!!! length should be greater then 6"
            return jsonify({"status": status, "data": data, "message":message})
        
        # check token lenght
        if len(token)!= 6:
            message = "length of token should be equall 6"
            return jsonify({"status": status, "data": data, "message":message})

        # check if valid token
        tokens = db.tokens.find_one({"Token":token})
        if tokens is None:
            message = "invalid token"
            return jsonify({"status": status, "data": data, "message":message})

        # check if email already exist
        chk_email = db.users.find_one({"Emial":email})
        if chk_email is not None:
            message = "email already exit"
            return jsonify({"status": status, "data": data, "message":message})

        # check if username already exist
        chk_user = db.users.find_one({"Username":username})
        if chk_user is not None:
            message = "username already exit"
            return jsonify({"status": status, "data": data, "message":message})

        # check if token token already taken
        if tokens["valid"] != True:
            message = "hardware already connected to a device!!! login using your details"
            return jsonify({"status": status, "data": data, "message":message})
        
        # check username lenght
        if len(username)<3:
            message = "username too short or null"
            return jsonify({"status": status, "data": data, "message":message})
        
        # check pwd1 and pwd2
        if pwd1 != pwd2:
            message = "password mismatch!!! incorrect password"
            return jsonify({"status": status, "data": data, "message":message})

        # hash pwd
        pwd_hash = generate_password_hash(pwd1)

        # update token to validity to false
        db.tokens.update_one({"Token":token},{"$set":{"valid":False}})

        # post user details
        db.users.insert_one({"Full_Name":full_name,"Phone_Number":phone_number,"Email":email,"Gender":gender,"Nationality":Nationality,"Username":username,"Token":token,"Password":pwd_hash,"Created_at":datetime.now()})
        status = True
        data = {"Full_Name":full_name,"Phone_Number":phone_number,"Email":email,"Gender":gender,"Nationality":Nationality,"Username":username,"Token":token,"Created_at":datetime.now()}
        return jsonify({"status": status, "data": data, "message":message})


    return jsonify({"status": status, "data": data, "message":message})


# sign in route
@auth.route("/login", methods=["POST"])
def login():
     # initialize all respose variables
    db = mongo.Embraceher

    data = {}
    status = False
    message = "invalid request"
    # check request type
    if request.method=="POST":
        userid = request.json.get("Userid","").strip()
        pwd = request.json.get("Password","").strip()

        # check if userid exit in email or username
        if validators.email(userid):
            chk_userid = db.users.find_one({"Email":userid})
        else:
            chk_userid = db.users.find_one({"Username":userid})

        # check if user exist
        if chk_userid is None:
            message = "incorrect userid!!! user does not exist"
            return jsonify({"status": status, "data": data, "message":message})

        # check password
        if not check_password_hash(pwhash=chk_userid["Password"], password=pwd):
            message = "incorrect password"
            return jsonify({"status": status, "data": data, "message":message})
        

        # if successful
        status = True
        data = {"Full_Name":chk_userid["Full_Name"],"Phone_Number":chk_userid["Phone_Number"],"Email":chk_userid["Email"],"Gender":chk_userid["Gender"],"Nationality":chk_userid["Nationality"],"Username":chk_userid["Username"],"Token":chk_userid["Token"]}
        return jsonify({"status": status, "data": data, "message":message})
        

    return jsonify({"status": status, "data": data, "message":message})
