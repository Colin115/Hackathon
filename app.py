from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from dataInterface import *
from barcodeReader import *
import os
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
UPLOAD_FOLDER = "./uploads"
###
###   MOCK FUNCS TILL THEY DONE
###

def verify_identity(path_to_driver_license_front: str, path_to_driver_license_back:str, path_to_selfie:str):
    dirty_data = get_id_data(path_to_driver_license_back)
    data = parse_id_data(dirty_data)
    
    user_data = read_all_user_select_data_from_csv(FILE, session.get("username"))
    print(data['fname'].upper(), user_data['fname'].upper(), data['lname'].upper() , data['lname'].upper())
    if (data['fname'].upper() != user_data['fname'].upper() or data['lname'].upper() != user_data['lname'].upper()):
        return False
    
    return True


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
        return redirect(url_for("login"))
    user_data = read_all_user_select_data_from_csv(FILE, username) #TODO: get user data from database
    
    social_media_data = user_data['social_media']
    parsed_data = {}
    for account in social_media_data:
        count = 0
        while len(social_media_data[account]) > 0:
            if count == 0:
                parsed_data[account] = social_media_data[account].pop(0)
            else:
                parsed_data[f'{account} #{count}'] = social_media_data[account].pop(0)
            count += 1
            
    
    return render_template("profile.html",
                           username=user_data["username"],
                           fname=user_data['fname'],
                           lname=user_data['lname'],
                           verified=user_data['verified'],
                           social_media=parsed_data,
                           ALLOWED_SOCIALS=ALLOWED_SOCIALS)
    
@app.route("/verify_user_id/")
def verify_user_id_page():
    if not session.get("login"): # if they arent signed in send them to the home page
        return redirect(url_for("login"))
    elif not session.get("username"):
        return redirect(url_for("login"))
    
    
    
    return render_template("verify_user_id.html")
    
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
    actual_username = find_username_from_social_account(username, platform)
    
    if actual_username is None:
        return jsonify({"success": False, "error": "user not found"}), 404
    
    session["last_searched_user"] = actual_username
    
    #return success code
    return jsonify({"success": True, "message": "successfully added the account", "url": url_for("view_profile_verified", username=username, platform=platform)}), 200
    
     


@app.route("/api/add_social/<string:username>/<string:platform>/", methods=["POST"])
def add_social_account(username, platform):
    ### make sure they are logged in, have a valid user name, and the platform is one we support
    if not session.get("login"):
        return jsonify({"error": "you must be logged in"}), 400
    elif not session.get("username"):
        return jsonify({"error": "no user name"}), 400
    elif platform not in ALLOWED_SOCIALS:
        return jsonify({"error": "not an allowed social media"}), 400
    
    ### check if they already have the account registered
    user_data = read_all_user_select_data_from_csv(FILE, session.get("username"))
    accounts = user_data.get("social_media")
    if accounts is not None:
        if accounts.get(platform) is not None and username in accounts.get(platform):
            return jsonify({"success": False, "message": "account already verified"}), 400
    
    ### add user account to database
    add_social_media_account(session.get("username"), username, platform, FILE)
    
    return jsonify({"success": True, "message": "Successfully added the account"})

@app.route("/api/delete_social/<string:username>/<string:platform>/", methods=["POST"])
def delete_social_account(username, platform):
    ### make sure they are logged in, have a valid user name, and the platform is one we support
    print(2)
    if not session.get("login"):
        return jsonify({"error": "you must be logged in"}), 401
    elif not session.get("username"):
        return jsonify({"error": "no user name"}), 400
    elif platform not in ALLOWED_SOCIALS:
        return jsonify({"error": "not an allowed social media"}), 400
    
    ### verify account exists
    user_data = read_all_user_select_data_from_csv(FILE, session.get("username"))
    accounts = user_data.get("social_media")
    if accounts is None:
        return jsonify({"success": False, "error": "account not registered"}), 404
    if accounts.get(platform) is None or username not in accounts.get(platform):
        return jsonify({"success": False, "error": "account not registered"}), 404
    
    remove_social_media_account(session.get("username"), username, platform, FILE)
    
    return jsonify({"success": True})


@app.route("/api/verify_user_id/", methods=["POST"])
def verify_user_id():
        # Check if the request contains files
    if 'front' not in request.files or 'back' not in request.files or 'selfie' not in request.files:
        return jsonify({"error": "Missing files"}), 400

    ### Process files and Save them    
    front_file = request.files['front']
    back_file = request.files['back']
    selfie_file = request.files['selfie']

    # Save the files to the uploads directory
    front_path = os.path.join(UPLOAD_FOLDER, front_file.filename)
    back_path = os.path.join(UPLOAD_FOLDER, back_file.filename)
    selfie_path = os.path.join(UPLOAD_FOLDER, selfie_file.filename)

    front_file.save(front_path)
    back_file.save(back_path)
    selfie_file.save(selfie_path)

    ### Call function to verify identify
    success = verify_identity(front_path, back_path, selfie_path)
    
    ### Delete images
    os.remove(front_path)
    os.remove(back_path)
    os.remove(selfie_path)
    
    if success:
        ### Update database to show verified
        updated_verified(session.get("username"), FILE)
        return jsonify({
            "success": True,
        }), 200
    
    return jsonify({"success": False, "message": "verification failed"}), 400

if __name__ == "__main__":
    app.run(debug=True)