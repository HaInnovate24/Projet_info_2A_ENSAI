"""
Streamlit page for the main player menu.

Provides navigation to available actions such as listing players or playing games for logged-in users.
"""

import streamlit as st

from utils.api_client import api_client
from utils.log_init import get_page_logger

st.title("Player stats")
logger = get_page_logger("player_menu")

# 1. Get player_id from query params
player_id = st.query_params.get("id_player")

# If no ID is provided, stop immediately
if not player_id:
    st.warning("No player ID provided in the URL.")
    st.stop()

# 2. Fetch the data
response = api_client.get(f"/player/{player_id}")

# 3. Check if the request was successful
if response.get("status_code") == 200:
    player = response.get("data")
    # Store it in session state so other pages can use it
    st.session_state["player"] = player
else:
    st.error("Could not retrieve player information.")
    logger.error(f"Failed to fetch player {player_id}: {response.get('status_code')}")
    st.stop()  # <--- CRITICAL: This stops the script so it doesn't try to display info for a non-existent player

# --- NOW THE REST OF THE CODE RUNS ONLY IF PLAYER WAS FOUND ---

# --- PLAYER INFORMATION DISPLAY ---
st.subheader(f"{player['username']}")

# Create two columns
col1, col2 = st.columns(2)

with col1:
    # Display Elo using a metric
    elo_rating = player.get("elo", 0)
    st.metric(label="Elo Rating", value=elo_rating)

with col2:
    # Display email
    st.write(f" **Email:** {player.get('email', 'N/A')}")

    # Display Pokemon fan status
    is_fan = player.get("is_pokemon_fan", False)
    st.checkbox("Is a Pokémon fan?", value=is_fan, disabled=True)

st.divider()

# --- Rest of your menu logic ---
# (e.g., if st.button("Play a Dice game"): ...)
