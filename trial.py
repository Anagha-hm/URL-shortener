import streamlit as st
import base62 as bs
import psycopg2

url = st.number_input('Enter/ Paste the URL', min_value=1, max_value=1000000, value=5, step=1)
# Initialize connection.
# Uses st.cache to only run once.
@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()
st.write(url)
