import streamlit as st
from PIL import Image
import requests
import io
import time

# Set page title and layout
st.set_page_config(page_title="🎨 Icon Generator", page_icon="🎨", layout="centered")

# Your Hugging Face API key (⚠️ Not recommended for public use)
HUGGINGFACE_API_KEY = "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"

# Function to generate icons using Hugging Face Inference API with retry mechanism
def generate_icons(description, num_images=4, max_retries=5, delay=10):
    images = []
    for i in range(num_images):
        attempt = 0
        while attempt < max_retries:
            try:
                headers = {
                    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
                }
                payload = {
                    "inputs": description,
                    "options": {
                        "use_gpu": True  # Use GPU if available
                    }
                }
                
                # Send POST request to Hugging Face Inference API
                response = requests.post(
                    "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4",
                    headers=headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    # Check if response contains image data
                    if 'image/' in response.headers.get('Content-Type', ''):
                        image = Image.open(io.BytesIO(response.content))
                        images.append(image)
                        break  # Exit retry loop on success
                    else:
                        # If not image, try to parse JSON for error message
                        error_info = response.json()
                        error_message = error_info.get("error", "Unknown error.")
                        st.error(f"Icon generation failed: {error_message}")
                        break  # Exit retry loop on error
                elif response.status_code == 503:
                    # Service unavailable, possibly model loading
                    st.warning(f"Model is currently loading. Retrying in {delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                    attempt += 1
                    time.sleep(delay)
                else:
                    # Attempt to parse error message from JSON
                    try:
                        error_info = response.json()
                        error_message = error_info.get("error", "Unknown error.")
                        st.error(f"Icon generation failed: {error_message}")
                    except ValueError:
                        st.error(f"Icon generation failed: {response.status_code} - {response.text}")
                    break  # Exit retry loop on error
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
                break  # Exit retry loop on exception
        else:
            st.error(f"Failed to generate icon {i + 1} after {max_retries} attempts.")
    
    return images if images else None

# User Interface
st.title("🎨 Icon Generator")
st.write("Enter a text description to generate icons. Examples: 'blue heart with white outline', 'gold smiley face'.")

with st.form(key='icon_form'):
    description = st.text_input("Text Description", "e.g., blue heart with white outline")
    submit_button = st.form_submit_button(label='Generate Icons')

if submit_button:
    if description.strip() == "":
        st.warning("Please enter a text description to generate an icon.")
    else:
        with st.spinner('Generating icons...'):
            icon_images = generate_icons(description, num_images=4)
            if icon_images:
                for idx, icon_image in enumerate(icon_images, start=1):
                    st.image(icon_image, caption=f"Generated Icon {idx}", use_container_width=True)
                    
                    # Download button for each image
                    buf = io.BytesIO()
                    icon_image.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    st.download_button(
                        label=f"Download Icon {idx}",
                        data=byte_im,
                        file_name=f"icon_{idx}.png",
                        mime="image/png",
                    )
            else:
                st.error("Failed to generate icons.")
