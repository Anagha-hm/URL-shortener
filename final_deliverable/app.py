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
from PIL import Image
import altair as alt
import numpy as np 
import matplotlib.pyplot as plt




client = pymongo.MongoClient(**st.secrets["mongo"])
db=client.tally_db
map_url= db.url_map

st.set_page_config(page_title='URL Shortener', page_icon='✂️')


st.title("URL Shortener")
st.write("An effort towards simulating a URL Shortener, presented at Tally Code Brewers hackathon")



menu = ["Home","Sign Up","Login"]
choice = st.sidebar.selectbox("Menu",menu)

if choice == "Home":
    st.subheader("Home")

    image = Image.open('img1.jpeg')
    st.image(image, caption='URL Shortening',width=400)

    st.write("Authors:")
    st.write(" Anagha HM and Karthik Sairam") 

elif choice == "Login":

    st.subheader("Hello User!")

    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password",type='password')
    

    if st.sidebar.checkbox("Login"):

        hashed_pswd = fn.make_hashes(password)

        result = fn.login_user(username,fn.check_hashes(password,hashed_pswd))

        if result:

            st.success("Logged In as {}".format(username))

            task = st.selectbox("Task",["Shorten My URL","Analytics"])

            url = st.text_input('Enter/ Paste the URL')

            if task == "Shorten My URL":

                st.subheader("Shorten My URL")

                fn.core_logic(url)

            elif task == "Analytics":
                st.subheader("Analytics")

                fn.analytic_fun(url)

                loo=list(map_url.find({},{"count":1,"long":1}))

                my_count=[int(i["count"]) for i in loo]
                my_long=[urlparse(i["long"]).netloc for i in loo]

            
                fig = plt.figure()
                
                plt.bar(my_long, my_count)
                plt.xlabel("URLs")
                plt.ylabel("Number of times shortened")
                plt.xticks(wrap=True)
                st.pyplot(fig)

        else:
            st.warning("Incorrect Username/Password")

        

elif choice == "Sign Up":
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

