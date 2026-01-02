import streamlit as st
from utils.api import fetch_data

# 1. Check if user actually selected a destination
if 'selected_dest_id' not in st.session_state:
    st.warning("⚠️ No destination selected. Please go back to the Home page.")
    st.stop()

dest_id = st.session_state.selected_dest_id
dest_name = st.session_state.selected_dest_name

# --- SIDEBAR NAVIGATION ---
st.sidebar.title(f"📍 {dest_name}")
st.sidebar.divider()
choice = st.sidebar.radio(
    "Explore Category:",
    ["Places to Visit", "Hotels", "Local Food", "Activities"]
)

# --- MAIN CONTENT AREA ---
st.title(f"{choice} in {dest_name}")

# Map choices to your Django API endpoints
endpoint_map = {
    "Places to Visit": "dashboard/places/",
    "Hotels": "dashboard/hotels/",
    "Local Food": "dashboard/food/",
    "Activities": "dashboard/activities/"
}

endpoint = endpoint_map[choice]

# Fetch filtered data from Django
# This calls: http://127.0.0.1:8000/api/dashboard/hotels/?dest_id=5
with st.spinner(f"Loading {choice}..."):
    data = fetch_data(endpoint, params={"dest_id": dest_id})

if not data:
    st.info(f"No {choice.lower()} found for this destination yet.")
else:
    # Display the data efficiently
    for item in data:
        with st.container(border=True):
            # Use columns to show an image (if you have media) next to text
            col1, col2 = st.columns([1, 3])
            
            with col1:
                if item.get('image'): # If your model has an image field
                    st.image(item['image'])
                else:
                    st.write("🖼️ No Image")
            
            with col2:
                st.subheader(item['name'])
                st.write(item.get('description', 'No description available.'))
                
                # If it's a hotel, maybe show price/rating
                if choice == "Hotels":
                    st.caption(f"⭐ Rating: {item.get('rating', 'N/A')} | 💰 Price: {item.get('price', 'N/A')}")