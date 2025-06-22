from pymongo import MongoClient
import bcrypt

MONGO_URI=st.secrets["mongo"]["uri"]
Client=MongoClient(MONGO_URI)
db=Client["Quickprep"]
users_collection=db["users"]

def create_user(username,password):
    if users_collection.find_one({"username":username}):
        return False
    hashed_pw=bcrypt.hashpw(password.encode(),bcrypt.gensalt())
    users_collection.insert_one({"username":username,"password":hashed_pw,"history":[]})
    return True

def authenticate_user(username,password):
    user=users_collection.find_one({"username":username})
    if not user:
        return False
    return bcrypt.checkpw(password.encode(),user["password"])

def get_user_history(username):
    user=users_collection.find_one({"username":username})
    return user.get("history",[]) if user else []

def save_user_history(username,file_entry):
    users_collection.update_one(
        {"username":username},
        {"$push":{"history":file_entry}}
    )