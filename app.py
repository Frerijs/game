import streamlit as st
from PIL import Image
import requests
import io
import os

# Iestatīt lapas virsrakstu un izskatu
st.set_page_config(page_title="🎨 AI Avatar Generator", page_icon="🖼️", layout="centered")

# Iegūst Hugging Face API atslēgu no vides mainīgajiem
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not HUGGINGFACE_API_KEY:
    st.error("HUGGINGFACE_API_KEY nav iestatīta. Lūdzu, iestatiet vides mainīgo `HUGGINGFACE_API_KEY`.")
    st.stop()

# Funkcija, lai ģenerētu avataru, izmantojot Hugging Face Inference API
def generate_avatar(description):
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
                st.error(f"Kļūda avatara ģenerēšanā: {error_message}")
                return None
        else:
            # Mēģina izvilkt kļūdas ziņojumu no JSON
            try:
                error_info = response.json()
                error_message = error_info.get("error", "Nezināma kļūda.")
                st.error(f"Kļūda avatara ģenerēšanā: {error_message}")
            except ValueError:
                st.error(f"Kļūda avatara ģenerēšanā: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Kļūda avatara ģenerēšanā: {e}")
        return None

# Lietotāja interfeiss
st.title("🎨 AI Avatar Generator")
st.write("Customize your avatar by selecting various attributes and styles. Click 'Generate Avatar' to create your unique avatar.")

with st.form(key='avatar_form'):
    # Avataru atribūtu izvēle
    hair_style = st.selectbox("Hair Style", ["Short", "Long", "Curly", "Straight", "Bald"])
    outfit = st.selectbox("Outfit", ["Casual", "Formal", "Sporty", "Fantasy", "Sci-Fi"])
    background = st.selectbox("Background", ["Plain", "Nature", "Cityscape", "Abstract", "Space"])
    style = st.selectbox("Art Style", ["Cartoon", "Realistic", "Futuristic", "Minimalist", "Vintage"])
    
    submit_button = st.form_submit_button(label='Generate Avatar')

if submit_button:
    # Sagatavot teksta aprakstu, balstoties uz lietotāja izvēlēm
    description = f"A {style} style avatar with {hair_style.lower()} hair, wearing {outfit.lower()} attire, set against a {background.lower()} background."
    
    with st.spinner('Generating your avatar...'):
        avatar_image = generate_avatar(description)
        if avatar_image:
            st.image(avatar_image, caption="Your Generated Avatar", use_container_width=True)
            
            # Lejupielādes poga
            buf = io.BytesIO()
            avatar_image.save(buf, format="PNG")
            byte_im = buf.getvalue()
            st.download_button(
                label="Download Avatar",
                data=byte_im,
                file_name="avatar.png",
                mime="image/png",
            )
        else:
            st.error("Neizdevās ģenerēt avataru.")
