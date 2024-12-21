import streamlit as st
from PIL import Image
import requests
import io

# Iestatīt lapas virsrakstu un izskatu
st.set_page_config(page_title="🎨 Icon Generator", page_icon="🎨", layout="centered")

# Jūsu Hugging Face API atslēga (⚠️ Nav ieteicams publiski izmantot)
HUGGINGFACE_API_KEY = "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"

# Funkcija, lai ģenerētu ikonu, izmantojot Hugging Face Inference API
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
        # Sūta POST pieprasījumu uz Hugging Face Inference API
        response = requests.post(
            "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4",
            headers=headers,
            json=payload
        )
        if response.status_code == 200:
            # Pārbauda, vai atbildē ir attēla dati
            if 'image/' in response.headers.get('Content-Type', ''):
                image = Image.open(io.BytesIO(response.content))
                return image
            else:
                # Ja nav attēla, mēģina izvilkt kļūdas ziņojumu no JSON
                error_info = response.json()
                error_message = error_info.get("error", "Nezināma kļūda.")
                st.error(f"Kļūda ikonas ģenerēšanā: {error_message}")
                return None
        else:
            # Mēģina izvilkt kļūdas ziņojumu no JSON
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
st.title("🎨 Icon Generator")
st.write("Enter a text description to generate an icon. Examples: 'blue heart with white outline', 'gold smiley face'.")

with st.form(key='icon_form'):
    description = st.text_input("Text Description", "e.g., blue heart with white outline")
    submit_button = st.form_submit_button(label='Generate Icon')

if submit_button:
    if description.strip() == "":
        st.warning("Lūdzu, ievadi teksta aprakstu ikonas ģenerēšanai.")
    else:
        with st.spinner('Ģenerēju ikonu...'):
            icon_image = generate_icon(description)
            if icon_image:
                st.image(icon_image, caption="Generated Icon", use_container_width=True)
                
                # Lejupielādes poga
                buf = io.BytesIO()
                icon_image.save(buf, format="PNG")
                byte_im = buf.getvalue()
                st.download_button(
                    label="Download Icon",
                    data=byte_im,
                    file_name="icon.png",
                    mime="image/png",
                )
            else:
                st.error("Neizdevās ģenerēt ikonu.")
