from flask import Flask, render_template, session, redirect, url_for, request, jsonify
import dataInterface
app = Flask(__name__, static_folder='static')

#TODO: CHANGE THIS
# Set the secret key to use sessions in Flask
app.secret_key = 'your_secret_key_here'  # Change this to a secure secret key


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
    
    return "<h1>Search Users</h1>"

@app.route("/view_profile/")
def account_verification():
    
    if not session.get("login"): # if they arent signed in send them to the home page
        return redirect(url_for("home"))
    
    return "<h1>Account verified"

@app.route("/profile/<string:username>")
def profile(username):
    return username
'''

APIs

'''

@app.route("/api/add_user", methods=["POST"])
def add_user():
    successful = False
    
    if successful:
        return 500
    return 200

@app.route("/api/login/", methods=["POST"])
def sign_in():
    successful = False
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    #TODO: change this to grab from database
    user_in_database = True
    password_matches = True
    
    if user_in_database and password_matches:
        return jsonify({"success": True, "url": url_for("profile", username=username)})
    
    return jsonify({'success': False})

@app.route("/api/get_user", methods=["GET"])
def get_user():
    user_profile = "profile"
    
    return user_profile

@app.route("/api/search_account")
def search_account():
    pass


if __name__ == "__main__":
    app.run(debug=True)