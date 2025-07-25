import streamlit as st
from auth import authenticate_user
from auth import get_user_history
from auth import create_user
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import pymongo

load_dotenv()
def login_page():
    st.title("Login")

    username=st.text_input("Username")
    password=st.text_input("Password",type="password")

    if(st.button("Login")):
        if authenticate_user(username,password):
            st.success("Login Successful")
            st.session_state["authenticated"]=True
            st.session_state["username"]=username

            MONGO_URI=os.getenv("MONGO_URI") or st.secrets["MONGO_URI"]
            Client=pymongo.MongoClient(MONGO_URI)
            db=Client["Quickprep"]
            users=db["users"]
            user=users.find_one({"username":username})
            st.session_state["history"]=user.get("history",[]) if user else []
            st.rerun()
        else:
            st.error("Invalid username or password")

    if st.button("Signup"):
        if create_user(username,password):
            st.success("User created successfully! Please Login")
        else:
            st.error("Username already exists. Please try a different one")