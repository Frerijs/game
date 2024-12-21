import streamlit as st
from PIL import Image
import requests
import io

# Iestatīt lapas virsrakstu un izskatu
st.set_page_config(page_title="🎨 Ikona Ģenerators", page_icon="🎨", layout="centered")

# API Atslēga (Nav ieteicams)
HUGGINGFACE_API_KEY = "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"

# Funkcija, lai ģenerētu ikonu no teksta apraksta, izmantojot Hugging Face Inference API
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
        # Izsauc Inference API modeli
        response = requests.post(
            "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4",
            headers=headers,
            json=payload
        )
        if response.status_code == 200:
            # Hugging Face Inference API parasti atgriež attēla bināro datus
            image = Image.open(io.BytesIO(response.content))
            return image
        else:
            # Ja tiek atgriezts JSON ar kļūdu, parādīt kļūdas ziņojumu
            try:
                error_info = response.json()
                error_message = error_info.get("error", "Nezināma kļūda.")
                st.error(f"Kļūda ikonas ģenerēšanā: {error_message}")
            except ValueError:
                st.error(f"Kļūda ikonas ģenerēšanā: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Kļūda ikonas ģenerēšanā: {e}")
        return None

# Lietotāja interfeiss
st.title("🎨 Ikona Ģenerators")
st.write("Ievadi teksta aprakstu, lai ģenerētu ikonu. Piemēri: 'zila sirds ar baltu kontūru', 'zelts smaidiņš'.")

with st.form(key='icon_form'):
    description = st.text_input("Teksta apraksts", "Piemērs: zila sirds ar baltu kontūru")
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
                buf = io.BytesIO()
                icon_image.save(buf, format="PNG")
                byte_im = buf.getvalue()
                st.download_button(
                    label="Lejupielādēt Ikonu",
                    data=byte_im,
                    file_name="icon.png",
                    mime="image/png",
                )
