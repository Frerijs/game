import streamlit as st
import openai
from PIL import Image
import io
import os
from dotenv import load_dotenv

# Ielādē vides mainīgos no .env faila
load_dotenv()

# Iestatīt lapas virsrakstu un izskatu
st.set_page_config(page_title="Ikona Ģenerators", page_icon="🎨", layout="centered")

# Iegūst OpenAI API atslēgu no vides mainīgajiem
openai.api_key = os.getenv("OPENAI_API_KEY")

# Funkcija, lai ģenerētu ikonu no teksta apraksta
def generate_icon(description):
    try:
        response = openai.Image.create(
            prompt=description,
            n=1,
            size="256x256",  # Ikonas izmērs
            response_format="url"  # Saite uz ģenerēto attēlu
        )
        image_url = response['data'][0]['url']
        return image_url
    except Exception as e:
        st.error(f"Kļūda ikonas ģenerēšanā: {e}")
        return None

# Lietotāja interfeiss
st.title("🎨 Ikona Ģenerators")
st.write("Ievadi teksta aprakstu, lai ģenerētu ikonu.")

with st.form(key='icon_form'):
    description = st.text_input("Teksta apraksts", "Piemērs: Zila sirds ar baltu kontūru")
    submit_button = st.form_submit_button(label='Ģenerēt Ikonu')

if submit_button:
    if description.strip() == "":
        st.warning("Lūdzu, ievadi teksta aprakstu ikonas ģenerēšanai.")
    else:
        with st.spinner('Ģenerēju ikonu...'):
            icon_url = generate_icon(description)
            if icon_url:
                st.image(icon_url, caption="Ģenerētā Ikona", use_column_width=True)
                st.markdown(f"[Lejupielādēt Ikonu]({icon_url})")
