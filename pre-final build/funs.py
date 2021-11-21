import streamlit as st
import base62 as bs
import pymongo
from bson.objectid import ObjectId
import random as rd
import requests as rq
import pandas as pd
import hashlib
from urllib.parse import urlparse
import wmi

client = pymongo.MongoClient(**st.secrets["mongo"])
db=client.tally_db
map_url= db.url_map


def longtoshort(m_long):
        
    m_short= bs.encode(m_long)

    return m_short

def shorttolong(m_short):
        
    m_long= bs.decode(m_short)

    return m_long

def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
def create_usertable():
	
	db.createCollection("usertable")

def add_userdata(username,password):
	db.usertable.insert_one({"user_id":username,"password":password})

def login_user(username,password):
	data = db.usertable.find({"user_id":username,"password":password})
	return list(data)

def view_all_users():
	data = db.usertable.find()
	return list(data)

def core_logic(url):

    s_link=""
    if url != "":

        
        if len(list(map_url.find({"long":url})))==0:

            
            r= rd.getrandbits(56)

            res= map_url.insert_one({

                'long':url,
                'rand': r,
                'short': longtoshort(r),
                'count': 1
            })

            s_link= "https://ak.ly/"+longtoshort(r)
            
            link = f'[{s_link}]({url})'
            st.markdown(link, unsafe_allow_html=True)


        else:
            q1={"long":url}
            q2={"$inc":{"count":1}}
            map_url.update(q1,q2)
            
            temp=list(map_url.find({"long":url}))[0]
            s_link="https://ak.ly/"+temp.get('short')
            
            link = f'[{s_link}]({url})'
            st.markdown(link, unsafe_allow_html=True)

            st.write("This link has been clicked",temp["count"],"times")

def analytic_fun(url):

    o = urlparse(url)
    st.write("Protocol :",o.scheme)
    st.write("Port :",o.port)
    st.write("Net Location :",o.netloc)
    #st.write("Path :",o.path)
    #st.write("query :",o.query)

    
    
    c = wmi.WMI()   
    my_system = c.Win32_ComputerSystem()[0]
    st.write(f"Manufacturer: {my_system.Manufacturer}")
    #st.write(f"Model: {my_system. Model}")
    #st.write(f"Name: {my_system.Name}")
    st.write(f"NumberOfProcessors: {my_system.NumberOfProcessors}")
    st.write(f"SystemType: {my_system.SystemType}")
    #st.write(f"SystemFamily: {my_system.SystemFamily}")