import streamlit as st
from PIL import Image
import requests
import io
import os
import time

# Iestatīt lapas virsrakstu un izskatu
st.set_page_config(page_title="📖 AI Storybook Creator", page_icon="📚", layout="centered")

# Jūsu Hugging Face API atslēga (⚠️ Nav ieteicams publiski izmantot)
HUGGINGFACE_API_KEY = "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"

if not HUGGINGFACE_API_KEY:
    st.error("HUGGINGFACE_API_KEY nav iestatīta. Lūdzu, iestatiet vides mainīgo `HUGGINGFACE_API_KEY`.")
    st.stop()

# Funkcija, lai ģenerētu attēlu, izmantojot Hugging Face Inference API
def generate_image(description, max_retries=5, delay=10):
    attempt = 0
    while attempt < max_retries:
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
                    st.error(f"Kļūda attēla ģenerēšanā: {error_message}")
                    return None
            elif response.status_code == 503:
                # Modelis vēl ielādējas, atkārto pieprasījumu pēc pauzes
                st.warning(f"Modelis vēl ielādējas. Atkārto pieprasījumu pēc {delay} sekundēm... (Mēģinājums {attempt + 1}/{max_retries})")
                attempt += 1
                time.sleep(delay)
            else:
                # Mēģina izvilkt kļūdas ziņojumu no JSON
                try:
                    error_info = response.json()
                    error_message = error_info.get("error", "Nezināma kļūda.")
                    st.error(f"Kļūda attēla ģenerēšanā: {error_message}")
                except ValueError:
                    st.error(f"Kļūda attēla ģenerēšanā: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            st.error(f"Kļūda attēla ģenerēšanā: {e}")
            return None
    st.error("Neizdevās ģenerēt attēlu pēc vairākiem mēģinājumiem.")
    return None

# Funkcija, lai ģenerētu attēlus katrai stāsta daļai
def generate_storybook(story_text):
    paragraphs = story_text.split('\n')
    images = []
    for idx, paragraph in enumerate(paragraphs, start=1):
        if paragraph.strip() == "":
            continue
        st.info(f"Ģenerēju attēlu iekšējam stāsta daļai {idx}...")
        image = generate_image(paragraph)
        if image:
            images.append((paragraph, image))
        else:
            st.error(f"Neizdevās ģenerēt attēlu iekšējam stāsta daļai {idx}.")
    return images

# Lietotāja interfeiss
st.title("📖 AI Storybook Creator")
st.write("Create your own illustrated storybook by entering your story below. Each paragraph will have a corresponding AI-generated image.")

with st.form(key='storybook_form'):
    story_input = st.text_area("Enter your story here:", height=300, placeholder="Write your story, separating paragraphs with a newline...")
    submit_button = st.form_submit_button(label='Create Storybook')

if submit_button:
    if story_input.strip() == "":
        st.warning("Lūdzu, ievadiet stāstu, lai veidotu stāsta grāmatu.")
    else:
        with st.spinner('Creating your storybook...'):
            story_images = generate_storybook(story_input)
            if story_images:
                for idx, (paragraph, image) in enumerate(story_images, start=1):
                    st.markdown(f"### Page {idx}")
                    st.write(paragraph)
                    st.image(image, caption=f"Illustration for Page {idx}", use_container_width=True)
                    
                    # Lejupielādes poga katram attēlam
                    buf = io.BytesIO()
                    image.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    st.download_button(
                        label=f"Download Illustration {idx}",
                        data=byte_im,
                        file_name=f"illustration_page_{idx}.png",
                        mime="image/png",
                    )
            else:
                st.error("Neizdevās veidot stāsta grāmatu.")
