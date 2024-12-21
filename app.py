import streamlit as st
import streamlit.components.v1 as components

# Iestatīt lapas virsrakstu un izskatu
st.set_page_config(page_title="🦖 Dino Runner", layout="wide")

st.title("🦖 Dino Runner")
st.write("Spēlē Dino Runner spēli zemāk, izmantojot internetu!")

# GitHub Pages URL
game_url = "https://yourusername.github.io/dino_runner/dino_game.html"  # Aizvietojiet ar savu URL

# Iebūvēt spēli ar iframe
components.iframe(game_url, width=800, height=450, scrolling=True)
