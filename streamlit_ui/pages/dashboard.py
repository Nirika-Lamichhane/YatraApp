import streamlit as st
import requests
from utils.api import fetch_data

# --- 1. CONFIG & SESSION CHECK ---
st.set_page_config(page_title="Travel Dashboard", layout="wide")

if 'selected_dest_id' not in st.session_state:
    st.warning("⚠️ No destination selected. Please go back to the Home page.")
    st.stop()

dest_id = st.session_state.selected_dest_id
dest_name = st.session_state.selected_dest_name
access_token = st.session_state.get('access_token', '')

# --- 2. SIDEBAR NAVIGATION ---
st.sidebar.title(f"📍 {dest_name}")
st.sidebar.divider()

# Toggle between Standard CRUD and your ML Recommendation Logic
view_mode = st.sidebar.radio(
    "View Mode:",
    ["Standard Listings", "AI Recommendations (ML)"]
)

choice = st.sidebar.radio(
    "Explore Category:",
    ["Places to Visit", "Hotels", "Local Food", "Activities"]
)

# --- 3. DATA FETCHING LOGIC ---
st.title(f"{choice} in {dest_name}")

# Map UI labels to API endpoints and Model names
mapping = {
    "Places to Visit": {"url": "dashboard/places/", "model": "place", "type": "places"},
    "Hotels": {"url": "dashboard/hotels/", "model": "hotel", "type": "hotels"},
    "Local Food": {"url": "dashboard/food/", "model": "food", "type": "foods"},
    "Activities": {"url": "dashboard/activities/", "model": "activity", "type": "activities"}
}

current_map = mapping[choice]

with st.spinner(f"Fetching {choice}..."):
    if view_mode == "AI Recommendations (ML)":
        # Calls your @api_view recommend_view
        params = {
            "item_type": current_map["type"], 
            "dest_id": dest_id  # Matches our updated Django View
        }
        response = fetch_data("dashboard/recommend/", params=params)
        # Your ML view returns data inside a 'clustered_data' key
        items = response.get("clustered_data", []) if isinstance(response, dict) else []
    else:
        # Calls your standard ViewSets with filtering
        items = fetch_data(current_map["url"], params={"dest_id": dest_id})

# --- 4. DISPLAY & INTERACTION LOOP ---
if not items:
    st.info(f"No {choice.lower()} found for this destination.")
else:
    for item in items:
        with st.container(border=True):
            col1, col2 = st.columns([1, 3])
            
            with col1:
                if item.get('image'):
                    st.image(item['image'])
                else:
                    st.write("🖼️ No Image")
            
            with col2:
                st.subheader(item['name'])
                st.write(item.get('description', 'No description available.'))
                
                # Metadata (Specific to Hotels)
                if choice == "Hotels":
                    st.caption(f"⭐ Avg Rating: {item.get('rating', 'N/A')} | 💰 Price: {item.get('price', 'N/A')}")
                
                st.divider()
                
                # --- RATING SYSTEM ---
                st.write("Rate your experience:")
                # Unique key is vital for widgets in a loop
                rating_key = f"rate_{current_map['model']}_{item['id']}"
                user_rating = st.feedback("stars", key=rating_key)
                
                if user_rating is not None:
                    payload = {
                        "model": current_map["model"],
                        "object_id": item['id'],
                        "rating": user_rating + 1 # Convert 0-4 to 1-5
                    }
                    headers = {"Authorization": f"Bearer {access_token}"}
                    
                    try:
                        res = requests.post(
                            "http://127.0.0.1:8000/api/dashboard/submit-rating/", 
                            json=payload, 
                            headers=headers
                        )
                        if res.status_code == 200:
                            st.toast(f"✅ Rated {item['name']} {user_rating + 1} stars!")
                        else:
                            st.error("Could not save rating.")
                    except Exception as e:
                        st.error(f"Connection error: {e}")