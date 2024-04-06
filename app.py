from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from dataInterface import *
app = Flask(__name__, static_folder='static')

#TODO: CHANGE THIS
# Set the secret key to use sessions in Flask
app.secret_key = 'your_secret_key_here'  # Change this to a secure secret key


'''
Session info
last_searched_user - last username on our platform that the user searched for
login - boolean of if the user is logged in
username - username of the person logged in

'''


#! ALLOWED SOCIALS
ALLOWED_SOCIALS = {"tinder", "facebook", "instagram"}
FILE = "./data.csv"
###
###   MOCK FUNCS TILL THEY DONE
###


def get_username_from_social(username, platform):
    actual_username = "john"
    return actual_username
'''

PAGES FOR FRONT


'''
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login/")
def login():
    return render_template("login.html")


@app.route("/sign_up/")
def sign_up():
    return render_template("sign_up.html")

@app.route("/check_username/")
def search_users():
    
    if not session.get("login"): # if they arent signed in send them to the home page
        return redirect(url_for("home"))
    
    return render_template("account_search.html", ALLOWED_SOCIALS=ALLOWED_SOCIALS)

@app.route("/view_profile/<string:username>/<string:platform>") 
def view_profile_verified(username, platform):
    
    if not session.get("login"): # if they arent signed in send them to the home page
        return redirect(url_for("home"))
    if not session.get("last_searched_user"): # if they havent searched for the user yet
        return redirect(url_for("search_users"))
    
    user_data = read_all_user_select_data_from_csv(session.get("last_searched_user"))
    
       
    return render_template("view_verified_account.html", fname=user_data['fname'], lname=user_data['lname'], username=username, platform=platform) 


@app.route("/profile/<string:username>") #TODO: db stuff
def profile(username):
    if not session.get("login"): # if they arent signed in send them to the home page
        return redirect(url_for("home"))
    user_data = read_all_user_select_data_from_csv(FILE, username) #TODO: get user data from database
    
    
    return render_template("profile.html",
                           username=user_data["username"],
                           fname=user_data['fname'],
                           lname=user_data['lname'],
                           verified=user_data['verified'],
                           social_media=user_data['social_media'])
    
    
'''

APIs

'''

@app.route("/api/add_user/", methods=["POST"])
def add_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    fname = data.get("fname")
    lname = data.get("lname")
    email = data.get("email")
    
    if None in (username, password, fname, lname, email):
        return jsonify({"error": "some forms were not filled out"}), 400
    
    ## Check if username is already taken
    if check_username_exists(username, read_usernames_from_csv(FILE)):
        return jsonify({"success": False,"error": "username already exists"}), 409
    
    # verify email optional
    
    ## add user to database
    write_usernames_and_passwords_to_csv(FILE, [username, password, fname, lname, email])
    session['login'] = True
    session["username"] = username
    return jsonify({"success": True, "url": url_for("profile", username=username) })

@app.route("/api/login/", methods=["POST"])
def sign_in():
    data = request.json
    username = data.get("username")
    password = data.get("password")
                
    if check_username_and_password(username, password, FILE):
        session["username"] = username
        session["login"] = True
        return jsonify({"success": True, "url": url_for("profile", username=session.get("username"))})
    
    return jsonify({'success': False})


@app.route("/api/get_user", methods=["GET"]) #TODO: all
def get_user():                             #? needed?
    user_profile = "profile"
    
    return user_profile


@app.route("/api/search_account_verified/<string:username>/<string:platform>/")
def search_account(username, platform):
    session["last_searched_user"] = None # default the last user to none
    
    ### make sure they are logged in, have a valid user name, and the platform is one we support
    if not session.get("login"):
        return jsonify({"error": "you must be logged in"}), 400
    elif not session.get("username"):
        return jsonify({"error": "no user name"}), 400
    elif platform not in ALLOWED_SOCIALS:
        return jsonify({"error": "not an allowed social media"}), 400
    
    ### check validity of username
    #TODO: from database function
    actual_username = get_username_from_social(username, platform)
    session["last_searched_user"] = actual_username
    
    #return success code
    return jsonify({"success": True, "message": "successfully added the account", "url": url_for("view_profile_verified", username=username, platform=platform)}), 200
    
     


@app.route("/api/add_social/<string:username>/<string:platform>")
def add_social_account(username, platform):
    ### make sure they are logged in, have a valid user name, and the platform is one we support
    if not session.get("login"):
        return jsonify({"error": "you must be logged in"}), 400
    elif not session.get("username"):
        return jsonify({"error": "no user name"}), 400
    elif platform not in ALLOWED_SOCIALS:
        return jsonify({"error": "not an allowed social media"}), 400
    
    ### check if they already have the account registered
    user_data = read_all_user_select_data_from_csv(FILE, username)
    accounts = user_data.get("social_media")
    if accounts is not None:
        if username in accounts["platform"]:
            return jsonify({"success": False, "message": "account already verified"}), 400
    
    ### add user account to database
    #TODO implement db
    return jsonify({"success": True, "message": "Successfully added the account"})


if __name__ == "__main__":
    app.run(debug=True)