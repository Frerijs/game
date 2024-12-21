import streamlit as st
import openai
from PIL import Image
import io
import os

# Iestatīt lapas virsrakstu un izskatu
st.set_page_config(page_title="Ikona Ģenerators", page_icon="🎨", layout="centered")

# Saglabā savu OpenAI API atslēgu drošā vietā
# Ieteicams izmantot .env failu vai vides mainīgos
# Šeit piemērs ar tiešo ievietošanu (NAV IETEICAMS)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Iestati savu vides mainīgo

# Funkcija, lai ģenerētu ikonu no teksta apraksta
def generate_icon(description):
    try:
        response = openai.Image.create(
            prompt=description,
            n=1,
            size="256x256",  # Ikonas izmērs
            response_format="b64_json"
        )
        image_data = response['data'][0]['b64_json']
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))
        return image
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
            icon = generate_icon(description)
            if icon:
                st.image(icon, caption="Ģenerētā Ikona", use_column_width=True)
                # Saglabā ikonu laika grāmatā (optional)
                buffer = io.BytesIO()
                icon.save(buffer, format="PNG")
                byte_im = buffer.getvalue()
                st.download_button(
                    label="Lejupielādēt Ikonu",
                    data=byte_im,
                    file_name="icon.png",
                    mime="image/png",
                )
