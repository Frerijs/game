import streamlit as st
import openai
from PIL import Image
import io
import base64
import requests

# Iestatīt lapas virsrakstu un izskatu
st.set_page_config(page_title="🎨 Ikona Ģenerators", page_icon="🎨", layout="centered")

# Iegūst Hugging Face API atslēgu no Streamlit Secrets
HUGGINGFACE_API_KEY = st.secrets["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"]

# Funkcija, lai ģenerētu ikonu no teksta apraksta, izmantojot Hugging Face API
def generate_icon(description):
    try:
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
        }
        payload = {
            "inputs": description,
            "options": {
                "use_gpu": True  # Ja pieejams GPU
            }
        }
        response = requests.post(
            "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4",
            headers=headers,
            json=payload
        )
        if response.status_code == 200:
            image_bytes = response.content
            image = Image.open(io.BytesIO(image_bytes))
            return image
        else:
            st.error(f"Kļūda ikonas ģenerēšanā: {response.status_code} - {response.text}")
            return None
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
            icon_image = generate_icon(description)
            if icon_image:
                st.image(icon_image, caption="Ģenerētā Ikona", use_column_width=True)
                
                # Lejupielādes poga
                buffer = io.BytesIO()
                icon_image.save(buffer, format="PNG")
                byte_im = buffer.getvalue()
                st.download_button(
                    label="Lejupielādēt Ikonu",
                    data=byte_im,
                    file_name="icon.png",
                    mime="image/png",
                )
