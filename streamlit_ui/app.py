import requests
import streamlit as st

BASE_URL = "http://127.0.0.1:8000/api"

def login_user(username, password):
    """Calls /api/token/ to get JWT tokens"""
    url = f"{BASE_URL}/token/"
    response = requests.post(url, json={"username": username, "password": password})
    if response.status_code == 200:
        return response.json() # Returns 'access' and 'refresh'
    return None

def fetch_data(endpoint, params=None):
    """Generic fetcher for your dashboard and accounts APIs"""
    headers = {}
    if "access_token" in st.session_state:
        headers["Authorization"] = f"Bearer {st.session_state.access_token}"
    
    response = requests.get(f"{BASE_URL}/{endpoint}", headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    return []