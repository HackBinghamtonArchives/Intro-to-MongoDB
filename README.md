# Intro-to-MongoDB
Repository for HackBU Demo on MongoDB (with Python & Flask)

__________________________________

### About


MongoDB is Object-Oriented, simple, dynamic and scalable NoSQL database. It is 
based on the NoSQL document store model, in which data objects are stored as 
separate documents inside a collection instead of storing the data into columns 
and rows of a traditional relational database.


### Setting Up


For this tutorial we will need to setup MongoDB locally on your machine. [Click here to find an installation for your OS.](https://docs.mongodb.com/manual/administration/install-community/)

Familarity with [Flask](http://flask.pocoo.org/) is helpful, but not essential.


### Layout


+ MongoDB Installation
+ MongoDB Basics
+ Using MongoDB with Python3
+ Using MongoDB with Flask


## Basics


### Features


+ Persistent storage
+ Documents stored in BSON (binary JSON)
	+ Mongo essentially uses JSON
+ JSON objects can be stored directly into a Mongo Database
+ Libraries with many popular languages _(Python, Go, Javascript, etc.)_


### Concepts


| Term | Meaning |
|------|---------|
|document|database record, BSON object|
|Collections|A Collection of documents or BSON objects|
|Queries|Look up Cursors|
|Cursors|Basically an index of a collection (Makes MongoDB really fast since it doesn't load the entire collection)|


## Using MongoDB with Python


There are many libraries for working with MongoDB in python. For our use, we will use `pymongo`.


#### Accessing a database


```python
from pymongo import MongoClient

try:
    print("Connecting to Database...")
    client = MongoClient()
    db = client.HackBU
    print("Connected to db :)")
 except:
    print("Could not connect to db :(")
```

If you installed MongoDB properly and have a Mongo server running, this should print out `Connected to db :)`.


#### Accessing a collection


```python
try:
    users = db.users
    print("Connected to collection :)")
except:
    print("Could not connect to collection :(")
```

#### Finding a document
```python
username = input("What is your username? Enter: ")

user = users.find_one({'username' : username})

if user is not None:
    print("Hello " + str(user['name']) + "!")
else:
    print("Could not find " + username + ".")
```

#### Inserting a document


```python
username = input("Username: ")
name = input("Name: ")

new_user = {
    'username' : username,
    'name' : name
}

user = users.find_one({'username' : username})

if user is not None:
    print("User already exists!")
    return 
try:    
    users.insert_one(new_user).inserted_id
    print("Account created.")
except:
    print("Could not insert user.")
```


#### Deleting a document


```python
username = input("What is your username? Enter: ")

user = users.find_one({'username' : username})

if user is None:
    print("User does not exist")
else:
    users.delete_one(user)
    user = users.find_one({'username' : username})
    if user is None:
        print("User deleted.")
    else:
        print("Could not delete user.")
```


#### Deleting a collection


```python
try:
    users.drop()
    print("cleared users collection.")
except:
    print("Could not clear users collection.")
```


#### Iterating a collection


```python
try:
    cursor = users.find({})
    for doc in cursor:
        print(doc)
except:
    print("Could not show users collection.")
```


## Using MongoDB with Flask


Now we can take our previous code and use it with a flask app!

First import some libraries and create our Flask app

```python
from flask import Flask
from flask import render_template
from flask import request
from pymongo import MongoClient

app = Flask(__name__)
```

Then setup our database:

```python
try:
    print("Connecting to Database...")
    client = MongoClient()
    db = client.HackBU
    print("Connected to db :)")
except:
    print("Could not connect to db :(")

users = db.users
```

Next let's create our index route

```python
@app.route("/")
def index():
    return render_template('index.html')
```

With index.html containing

```html
<!doctype html>
Create account:<br>
<form action="/create">
  User Name:<br><input type="text" name="username">
  <br>
  Name:<br><input type="text" name="name">
  <br>
  <button>Create</button>
</form>

<br><br>

Login account:
<br>
<form action="/login">
  User Name:<br><input type="text" name="username">
  <br>
  <button>Login</button>
</form>
```

Next we can create our login route and create route

```python
@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username', '')
    user = users.find_one({'username' : username})
    if user is None:
        return render_template('error.html', error="User does not exist.")
    print("User: " + str(user))
    return render_template('login.html', user=user)


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
```

Inside of login and create routes we use `login.html` and `error.html`

```html
<!--login.html-->
<!doctype html>
{% if user %}
  <h1>Hello {{ user.name }}!</h1>
{% else %}
  <h1>User does not exist.</h1>
{% endif %}
```

```html
<!--error.html-->
<!doctype html>
{% if error %}
  <h1>Error: {{ error }}</h1>
{% else %}
  <h1>404.</h1>
{% endif %}
```

The directory layout of our files is

```
/app.py
/templates
	/index.html
	/login.html
	/error.html
```

And then to run `FLASK_APP=app.py flask run` from the project directory.

And that's it! We now have a working flask app that can be used to create and login to accounts. Using Flask you can also setup sessions to keep a user logged in, along with some hashing libraries such as bcrypt to safely store users passwords. 


## Conclusion


MongoDB is a very powerful document database that may be used with a variety of languages. Python is one such language, and as shown above it is very easy to get a simple app up and running. By using Flask with pymongo, one can setup a simple app to create accounts and login.


## Documentation


+ [PyMongo](https://api.mongodb.com/python/current/)
+ [Flask](http://flask.pocoo.org/docs/0.12)
