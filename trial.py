import streamlit as st
import base62 as bs
import pymongo

client = pymongo.MongoClient(**st.secrets["mongo"])

def longtoshort(m_long):
        
    m_short= bs.encode(m_long)

    return m_short

def shorttolong(m_short):
        
    m_long= bs.decode(m_short)

    return m_long

url = st.number_input('Enter/ Paste the URL', min_value=1, max_value=1000000, value=5, step=1)
# url = st.text_input("Enter/ Paste the URL")
# s_url=shorttolong(url)
l_url = longtoshort(url)

st.write(l_url)