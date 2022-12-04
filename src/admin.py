from datetime import datetime
from flask import Blueprint, request, render_template, url_for, flash, redirect
from src.modules.mongedb import mongo

admin = Blueprint("admin", __name__, url_prefix="/v1/admin")

# dashboard view
@admin.route("/")
def home():
    # initialize variables
    tokens = []
    offline_tk =[]
    all_users = []

    db = mongo.Embraceher
    # fetch all uses from db
    for urs in db.users.find():
        all_users.append(urs)
    # fetch ann tokens from db
    for tk in db.tokens.find():
        tokens.append(tk)
        # get valid and invalid tokens
        if tk["valid"] == False:
            
            offline_tk.append(tk)

    # assigning values to all users 
    allurs = len(all_users)
    all_tokens = len(tokens)
    offline_tokens = len(offline_tk)
    online_tokens = all_tokens-offline_tokens
    
    return render_template("home.html", offline=offline_tokens, online=online_tokens, alltk=all_tokens, allusr=allurs)




# fetch all users and search users db
@admin.route("/fetch/users", methods=["POST", "GET"])
def users():
    db = mongo.Embraceher

    # filter search term or return all
    if request.method == 'POST':
        search_input = request.form['search'].strip()
        category_input = request.form['category'].strip()

        users = db.users.find({category_input:{"$regex":search_input, '$options':'i'}})
        
    else:
        # return all users
        users = db.users.find()

    return render_template("users.html", users=users)



# to be reviewed ========================================== 

# edit users view
@admin.route("/users/edit:<emailid>", methods=["POST", "GET"])
def edit_user(emailid):

    all_users = []
    db = mongo.Embraceher
    # get form datas
    if request.method == 'POST':
        # get form data
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        username = request.form['username'].strip()
        phone = request.form['phone'].strip()
        origin = request.form['origin'].strip()
        gender = request.form['gender'].strip()
        token = request.form['token'].strip()
        # post update 
        try:
            data = {"Full_Name":name,"Phone_Number":phone,"Email":email,"Gender":gender,"Nationality":origin,"Username":username,"Token":token}
            db.users.update_one({"Email":emailid},{"$set":data})

            user = db.users.find()

            flash("user updated successfully!!", category='success')
            return redirect(url_for('admin.users', users=user))
        # if post error return error
        except:
            # fetch all users
            user = db.users.find()

            flash("user update failed", category='error')
            return redirect(url_for('admin.users', users=user))

 
    else:
        # fetch user with email == emailid
        user = db.users.find_one({'Email':emailid})

    for urs in db.users.find():
        all_users.append(urs)
    
    return render_template("edituser.html", users=all_users, user= user)

# ==============================================================================



# delete a user
@admin.route("/delete/user:<token>")
def delete_user(token):
    db = mongo.Embraceher
    # try deleting user
    try:
        db.users.delete_one({"Token":token})

        user = db.users.find()

        db.tokens.update_one({"Token":token},{"$set":{"valid":True}})

        flash("user deleted successfully!!", category='success')
    # else return error
    except:
        user = db.users.find()
        flash("problem deleting user", category='error')
    
    return redirect(url_for('admin.users', users=user)) 




# token view
@admin.route("/fetch/token" , methods=["POST", "GET"])
def tokens():
    db = mongo.Embraceher

    # post request data
    if request.method == "POST":
        input_token = request.form["token"].strip()
        input_filter = request.form["filter"].strip()

        # get input token // 
        if input_token != "":
            # chwck token lenght
            if len(input_token)!= 6:
                token = db.tokens.find()
                flash("length of token should be equall 6")
               
                return render_template("token.html", token=token)

            # check if token already exitt
            chk_token = db.tokens.find_one({"Token":input_token})
            if chk_token is not None:

                token = db.tokens.find()
                flash( "token already exit")
                return render_template("token.html", token=token)
            
            # insert into db and set valid equall false for new token
            try:
    
                db.tokens.insert_one({"Token":input_token, "Created_at":datetime.now(), "valid": True})

                token = db.tokens.find()
                flash("token added successfully")
                return render_template("token.html", token=token)
            except:
                token = db.tokens.find()
                flash("error adding token")
                return render_template("token.html", token=token)

        token = db.tokens.find({"Token": {"$regex":input_filter,'$options':'i'}})
        return render_template("token.html", token=token)

    else:
        token = db.tokens.find()

    return render_template("token.html", token=token)




# delete token
@admin.route("/delete/token:<token>", methods=['GET', 'POST'] )
def delete_token(token):
    db = mongo.Embraceher

    if request.method  == "GET":
         # try deleting token
        try:
            # delete token from users db and token db
            db.tokens.delete_one({"Token":token})
            db.users.delete_one({"Token":token})
            # fetch all token
            token = db.tokens.find()

            flash("token deleted successfully")
            return render_template("token.html", token=token)
        # error deleting token
        except:
            token = db.tokens.find()

            flash("error deleting token")
            return render_template("token.html", token=token)
    # if not post request
    else:
        token = db.tokens.find()

        flash("Reload page and try operation again")
        return render_template("token.html", token=token)




# edit token
@admin.route("/edit/token:<token>", methods=['GET', 'POST'])
def edit_token(token):
    db = mongo.Embraceher
    
    if request.method == 'POST':
        # catct token from post
        input_token = request.form['token-data']

        if input_token != "":
            # chwck token lenght
            if len(input_token)!= 6:
                token = db.tokens.find()
                flash("length of token should be equall 6")
               
                return render_template("token.html", token=token)

            # check if token already exitt
            chk_token = db.tokens.find_one({"Token":input_token})
            if chk_token is not None:

                token = db.tokens.find()
                flash( "token already exit")
                return render_template("token.html", token=token)

            # update token 
            try:
                db.tokens.update_one({"Token":token},{"$set":{"Token":input_token}})
                db.users.update_one({"Token":token},{"$set":{"Token":input_token}})

                token = db.tokens.find()

                flash("token updated successfully")
                return render_template("token.html", token=token)
            except:
                token = db.tokens.find()

                flash("error updating token")
                return render_template("token.html", token=token)


    else:

        token = db.tokens.find()

        flash("Reload page and try operation again")
        return render_template("token.html", token=token)
   










# health tips view 
@admin.route("/fetch/healthtips")
def tips():


    return render_template("healthtips.html")











# health tips view 
@admin.route("/test")
def test():


    return render_template("test.html")