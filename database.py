import mysql.connector
import streamlit as st
import pandas as pd
import random
import string

def get_db_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
    )

def run_query(query, params=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # UPDATE/INSERT işlemleri için commit gerekir
        if query.strip().upper().startswith(("UPDATE", "INSERT", "DELETE")):
            conn.commit()
            return cursor.rowcount
        else:
            return cursor.fetchall()
    finally:
        conn.close()

def generate_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))