from pymongo import MongoClient

try:
    print("Connecting to Database...")
    client = MongoClient()
    db = client.HackBU
    print("Connected to db :)")
except:
    print("Could not connect to db :(")

users = db.users

def create():
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
    

def login():
    username = input("What is your username? Enter: ")
    
    user = users.find_one({'username' : username})
    
    if user is not None:
        print("Hello " + str(user['name']) + "!")
    else:
        print("Could not find")


def delete():
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


def clear():
    try:
        users.drop()
        print("cleared users collection.")
    except:
        print("Could not clear users collection.")


def show_all():
    try:
        cursor = users.find({})
        for doc in cursor:
            print(doc)
    except:
        print("Could not show users collection.")


accessing = True

while(accessing):
    choice = input("\
1 - create, \
2 - login, \
3 - delete, \
4 - clear, \
5 - Show all, \
else to exit. Enter: \
")
    if choice == '1':
        create()
    elif choice == '2':
        login()
    elif choice == '3':
        delete()
    elif choice == '4':
        clear()
    elif choice == '5':
        show_all()
    else:
        accessing = False
