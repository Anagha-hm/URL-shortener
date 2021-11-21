import streamlit as st
import base62 as bs
import pymongo
from bson.objectid import ObjectId
import random as rd
import requests as rq
import pandas as pd
import hashlib
from urllib.parse import urlparse
import funs as fn  
import wmi

client = pymongo.MongoClient(**st.secrets["mongo"])
db=client.tally_db
map_url= db.url_map


st.title("URL Shortener")


menu = ["Home","Login","SignUp"]
choice = st.sidebar.selectbox("Menu",menu)

if choice == "Home":
    st.subheader("Home")

    #add image and para

elif choice == "Login":

    st.subheader("Hello User!")

    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password",type='password')

    if st.sidebar.checkbox("Login"):

        hashed_pswd = fn.make_hashes(password)

        result = fn.login_user(username,fn.check_hashes(password,hashed_pswd))

        if result:

            st.success("Logged In as {}".format(username))

            task = st.selectbox("Task",["shorten url","Analytics","Profiles"])

            url = st.text_input('Enter/ Paste the URL')

            if task == "shorten url":

                st.subheader("Shorten URL")

                fn.core_logic(url)

            elif task == "Analytics":
                st.subheader("Analytics")

                fn.analytic_fun(url)

            elif task == "Profiles":
                st.subheader("User Profiles")
                user_result = fn.view_all_users()
                st.write(user_result)
                #st.dataframe(clean_db)
        else:
            st.warning("Incorrect Username/Password")

        



elif choice == "SignUp":
    st.subheader("Create New Account")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password",type='password')

    if st.button("Signup"):
        #create_usertable()
        fn.add_userdata(new_user,fn.make_hashes(new_password))
        st.success("You have successfully created a valid Account")
        st.info("Go to Login Menu to login")



# store long url in a new record
# get the objectId of that record
# do longtoshort
# rest api

items= map_url.find()
items= list(items)

