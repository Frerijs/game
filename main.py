import streamlit as st
from PIL import Image, ImageDraw
import random

# Izmanto sesijas stāvokli spēles stāvokļa uzturēšanai
if 'ball_position' not in st.session_state:
    st.session_state.ball_position = [50, 50]  # Sākuma pozīcija [x, y]
    st.session_state.level = 1
    st.session_state.score = 0
    st.session_state.obstacles = []
    st.session_state.generate_obstacles = True

# Funkcija, lai ģenerētu šķēršļus
def generate_obstacles(level):
    obstacles = []
    for _ in range(level + 5):  # Palielina šķēršļu skaitu ar līmeni
        x = random.randint(50, 450)
        y = random.randint(50, 450)
        width = random.randint(20, 50)
        height = random.randint(20, 50)
        obstacles.append((x, y, width, height))
    return obstacles

# Izlabotā funkcija, lai zīmētu spēles laukumu
def draw_game(ball_pos, obstacles):
    img = Image.new('RGB', (500, 500), color='white')
    draw = ImageDraw.Draw(img)
    
    # Zīmē bumbiņu
    ball_radius = 15
    draw.ellipse((ball_pos[0]-ball_radius, ball_pos[1]-ball_radius,
                  ball_pos[0]+ball_radius, ball_pos[1]+ball_radius), fill='blue')
    
    # Zīmē šķēršļus
    for obs in obstacles:
        x, y, w, h = obs
        draw.rectangle([x, y, x + w, y + h], fill='red')
    
    return img

# Funkcija, lai pārbaudītu sadursmi
def check_collision(ball_pos, obstacles):
    ball_x, ball_y = ball_pos
    ball_radius = 15
    for obs in obstacles:
        obs_x, obs_y, obs_w, obs_h = obs
        # Vienkārša sadursmes pārbaude
        if (obs_x < ball_x < obs_x + obs_w) and (obs_y < ball_y < obs_y + obs_h):
            return True
    return False

# Funkcija, lai pārietu uz nākamo līmeni
def next_level():
    st.session_state.level += 1
    st.session_state.ball_position = [50, 50]
    st.session_state.score += 10
    st.session_state.generate_obstacles = True

# Poga kustībai
col1, col2, col3 = st.columns(3)
with col1:
    if st.button('⬆️'):
        st.session_state.ball_position[1] -= 10
with col2:
    if st.button('⬅️'):
        st.session_state.ball_position[0] -= 10
    if st.button('➡️'):
        st.session_state.ball_position[0] += 10
with col3:
    if st.button('⬇️'):
        st.session_state.ball_position[1] += 10

# Ģenerē šķēršļus ja nepieciešams
if st.session_state.generate_obstacles:
    st.session_state.obstacles = generate_obstacles(st.session_state.level)
    st.session_state.generate_obstacles = False

# Pārbauda sadursmi
collision = check_collision(st.session_state.ball_position, st.session_state.obstacles)

# Ja nav sadursmes, zīmē spēli
if not collision:
    game_image = draw_game(st.session_state.ball_position, st.session_state.obstacles)
    st.image(game_image, caption=f"Līmenis: {st.session_state.level}  |  Punkti: {st.session_state.score}")
    
    # Pārbauda, vai bumbiņa sasniedz beigām (piemēram, x > 450)
    if st.session_state.ball_position[0] > 450:
        next_level()
        st.success(f"Tu pārgāji uz līmeni {st.session_state.level}!")
else:
    st.error("Sadevies ar šķēršļi! Spēle beigusies.")
    if st.button("Spēlēt no jauna"):
        st.session_state.ball_position = [50, 50]
        st.session_state.level = 1
        st.session_state.score = 0
        st.session_state.obstacles = []
        st.session_state.generate_obstacles = True
