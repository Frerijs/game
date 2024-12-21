import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# Iestatīt lapas virsrakstu un izskatu
st.set_page_config(page_title="🎨 Ikona Ģenerators", page_icon="🎨", layout="centered")

# Funkcija, lai izveidotu ikonu no apraksta
def generate_icon(description):
    # Vienkārša ikonu ģenerēšana balstoties uz atslēgvārdiem
    description = description.lower()

    # Izveido baltu fonu ar caurspīdīgumu
    img_size = (256, 256)
    image = Image.new("RGBA", img_size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # Definē krāsas
    colors = {
        "sirds": "red",
        "zvaigzne": "gold",
        "aplis": "blue",
        "smaidiņš": "yellow",
        "zelts": "goldenrod",
        "sarkans": "red",
        "zils": "blue",
        "zeltains": "goldenrod",
        "balts": "white",
        "melns": "black",
    }

    # Definē formas
    if "sirds" in description:
        # Sirds
        draw.polygon([(128, 40), (160, 120), (240, 120), (176, 180),
                      (208, 260), (128, 220), (48, 260), (80, 180),
                      (16, 120), (96, 120)], fill=colors.get("sirds", "red"))
    elif "zvaigzne" in description:
        # Zvaigzne
        draw.polygon([(128, 20), (150, 100), (240, 100), (170, 150),
                      (190, 230), (128, 180), (66, 230), (86, 150),
                      (16, 100), (106, 100)], fill=colors.get("zvaigzne", "gold"))
    elif "aplis" in description:
        # Aplis
        color = "blue"
        if "zils" in description:
            color = colors.get("zils", "blue")
        elif "sarkans" in description:
            color = colors.get("sarkans", "red")
        draw.ellipse([(32, 32), (224, 224)], outline=color, width=5)
    elif "smaidiņš" in description:
        # Smaidiņš
        draw.arc([(64, 64), (192, 192)], start=200, end=340, fill=colors.get("smaidiņš", "yellow"), width=5)
        draw.ellipse([(100, 100), (120, 120)], fill=colors.get("smaidiņš", "yellow"))
        draw.ellipse([(160, 100), (180, 120)], fill=colors.get("smaidiņš", "yellow"))
    else:
        # Ja nav atbilstoša atslēgvārda, zīmē vienkāršu aplis ar tekstu
        draw.ellipse([(32, 32), (224, 224)], outline="gray", width=5)
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except IOError:
            font = ImageFont.load_default()
        text = "Icon"
        text_width, text_height = draw.textsize(text, font=font)
        draw.text(((256 - text_width) / 2, (256 - text_height) / 2), text, fill="gray", font=font)

    return image

# Lietotāja interfeiss
st.title("🎨 Ikona Ģenerators")
st.write("Ievadi teksta aprakstu, lai ģenerētu ikonu. Piemēram, 'sirds', 'zvaigzne', 'aplis', 'smaidiņš'.")

with st.form(key='icon_form'):
    description = st.text_input("Teksta apraksts", "Piemērs: sirds")
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
            else:
                st.error("Neizdevās ģenerēt ikonu.")
