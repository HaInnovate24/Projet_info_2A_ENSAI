import pandas as pd
import streamlit as st

from utils.api_client import api_client
from utils.log_init import get_page_logger

st.title("Player Stats")

logger = get_page_logger("player_stats")

# Récupération de l'identifiant dans l'URL
player_id = st.query_params.get("id_player")

if player_id is None:
    st.error("Aucun identifiant de joueur fourni.")
    st.stop()

# Appel de l'API
response = api_client.get(
    f"/player/{player_id}",
)

# Vérification de la réponse
if not response:
    st.error("Impossible de récupérer les informations du joueur.")
    st.stop()

player = response["data"]

# Affichage du nom d'utilisateur
st.subheader(player["username"])

# Crétaion de deux colonnes
col1, col2 = st.columns(2)

with col1:
    st.metric("Elo", player["elo"])

with col2:
    st.write(f"Email : {player['email']}")
    st.checkbox("Fan de Pokémon", value=player["pokemon_fan"])


# Récupération des parties du joueur
games_response = api_client.get("/game", params={"id_player": player_id})

games = games_response["data"]

if len(games) == 0:
    st.info("Pas de jeu pour ce joueur.")
else:
    rows = []

    for game in games:
        # Déterminer l'adversaire
        if str(game["player1"]["id_player"]) == str(player_id):
            opponent = game["player2"]
        else:
            opponent = game["player1"]

        # Déterminer le résultat
        winner = game["winner"]

        if winner is None:
            result = "Match nul"
        elif str(winner["id_player"]) == str(player_id):
            result = "Victoire"
        else:
            result = "Défaite"

        # Nom du mode
        if game["game_mode"] == "dice":
            mode = "Dés"
        elif game["game_mode"] == "coinflip":
            mode = "Pile ou face"
        else:
            mode = game["game_mode"]

        rows.append({
            "Mode": mode,
            "Adversaire": f"{opponent['username']} ({opponent['elo']})",
            "Résultat": result,
        })

    df = pd.DataFrame(rows)

    st.subheader("Historique des parties")
    st.dataframe(df, hide_index=True)
