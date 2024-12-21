import streamlit as st
import pandas as pd

# Piemēra datu struktūra līmeņiem
levels = {
    1: {"question": "1. Kā sauc Latviju valsts galvaspilsētu?", "answer": "Rīga"},
    2: {"question": "2. Kāds ir 2 + 2?", "answer": "4"},
    # Pievieno līdz 100. līmenim
}

# Iegūst lietotāja pašreizējo līmeni
if 'current_level' not in st.session_state:
    st.session_state.current_level = 1

def check_answer(user_answer):
    correct = levels[st.session_state.current_level]['answer'].strip().lower()
    if user_answer.strip().lower() == correct:
        st.session_state.current_level += 1
        st.success("Pareizi! Nākamais līmenis.")
    else:
        st.error("Nepareizi. Mēģini vēlreiz.")

st.title("Populāra Spēle ar 100 Līmeņiem")

if st.session_state.current_level > 100:
    st.balloons()
    st.success("Apsveicam! Tu ieguvi visus 100 līmeņus!")
else:
    current = st.session_state.current_level
    st.header(f"Līmenis {current}")
    st.write(levels[current]['question'])
    user_input = st.text_input("Tavs atbildes variants:")
    if st.button("Iesniegt"):
        check_answer(user_input)
