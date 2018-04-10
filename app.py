from flask import Flask
from flask import render_template
from flask import request
from pymongo import MongoClient

app = Flask(__name__)

try:
    print("Connecting to Database...")
    client = MongoClient()
    db = client.HackBU
    print("Connected to db :)")
except:
    print("Could not connect to db :(")

users = db.users

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET'])
def create():
    username = request.args.get('username', '')
    name = request.args.get('name', '')
    new_user = {
        'username' : username,
        'name' : name
    }
    user = users.find_one({'username' : username})

    if user is not None:
        return render_template('error.html', error="User already exists!")

    try:    
        users.insert_one(new_user)
        print("Account created.")
        return render_template('login.html', user=new_user)
    except:
        return render_template('error.html', error="Could not insert user.")

@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username', '')
    user = users.find_one({'username' : username})
    if user is None:
        return render_template('error.html', error="User does not exist.")
    print("User: " + str(user))
    return render_template('login.html', user=user)
