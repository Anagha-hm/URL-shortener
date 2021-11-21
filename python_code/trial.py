import streamlit as st
import base62 as bs
import pymongo
from bson.objectid import ObjectId
import random as rd
import requests as rq
import pandas as pd

client = pymongo.MongoClient(**st.secrets["mongo"])
db=client.tally_db
map_url= db.url_map

def longtoshort(m_long):
        
    m_short= bs.encode(m_long)

    return m_short

def shorttolong(m_short):
        
    m_long= bs.decode(m_short)

    return m_long

import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
def create_usertable():
	# c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')
	db.createCollection("usertable")

def add_userdata(username,password):
	# c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	# conn.commit()
	db.usertable.insert_one({"user_id":username,"password":password})

def login_user(username,password):
	# c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	# data = c.fetchall()
	data = db.usertable.find({"user_id":username,"password":password})
	return list(data)

def view_all_users():
	# c.execute('SELECT * FROM userstable')
	# data = c.fetchall()
	data = db.usertable.find()
	return list(data)


"""Simple Login App"""

st.title("Simple Login App")

menu = ["Home","Login","SignUp"]
choice = st.sidebar.selectbox("Menu",menu)

if choice == "Home":
    st.subheader("Home")

elif choice == "Login":
    st.subheader("Login Section")

    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password",type='password')
    if st.sidebar.checkbox("Login"):
        # if password == '12345':
        #create_usertable()
        hashed_pswd = make_hashes(password)

        result = login_user(username,check_hashes(password,hashed_pswd))
        if result:

            st.success("Logged In as {}".format(username))

            task = st.selectbox("Task",["shorten url","Analytics","Profiles"])
            if task == "shorten url":
                st.subheader("Shorten URL")

                url = st.text_input('Enter/ Paste the URL')

                s_link=""
                if url != "":

                    # also address the issue for conflicting random numbers (same)
                    if len(list(map_url.find({"long":url})))==0:

                        #st.write('loop entered')
                        r= rd.getrandbits(56)

                        res= map_url.insert_one({

                            'long':url,
                            'rand': r,
                            'short': longtoshort(r)
                        })

                        s_link= "https://ak.ly/"+longtoshort(r)
                        st.write(s_link)

                        response=rq.get(s_link, allow_redirects=False)
                        st.write(response.history)

                    else:

                        temp=list(map_url.find({"long":url}))[0]
                        s_link="https://ak.ly/"+temp.get('short')
                        st.write(s_link)

                        response=rq.get(s_link)
                        st.write(response.url)

                        #s_link= "https://ak.ly/"+longtoshort(r)
                        #st.write(s_link)


            elif task == "Analytics":
                st.subheader("Analytics")
            elif task == "Profiles":
                st.subheader("User Profiles")
                user_result = view_all_users()
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
        add_userdata(new_user,make_hashes(new_password))
        st.success("You have successfully created a valid Account")
        st.info("Go to Login Menu to login")



# store long url in a new record
# get the objectId of that record
# do longtoshort
# rest api

'''
url = st.text_input('Enter/ Paste the URL')

s_link=""
if url != "":

    # also address the issue for conflicting random numbers (same)
    if len(list(map_url.find({"long":url})))==0:

        #st.write('loop entered')
        r= rd.getrandbits(56)

        res= map_url.insert_one({

            'long':url,
            'rand': r,
            'short': longtoshort(r)
        })

        s_link= "https://ak.ly/"+longtoshort(r)
        st.write(s_link)

        response=rq.get(s_link, allow_redirects=False)
        st.write(response.history)

    else:

        temp=list(map_url.find({"long":url}))[0]
        s_link="https://ak.ly/"+temp.get('short')
        st.write(s_link)

        response=rq.get(s_link)
        st.write(response.url)

        #s_link= "https://ak.ly/"+longtoshort(r)
        #st.write(s_link)


'''
items= map_url.find()
items= list(items)

#st.write(items)



# Pull data from the collection.
# Uses st.cache to only rerun when the query changes or after 10 min.


'''

{
    _id: 'admin.superuser',
    userId: UUID("e731d4e7-bb8e-4e28-b256-3fc62c0e27ff"),
    user: 'superuser',
    db: 'admin',
    roles: [ { role: 'root', db: 'admin' } ],
    mechanisms: [ 'SCRAM-SHA-1', 'SCRAM-SHA-256' ]
  }
'''