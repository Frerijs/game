import streamlit as st

# Spēles sākuma stāvoklis
if 'board' not in st.session_state:
    st.session_state.board = [''] * 9
    st.session_state.current_player = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None

def check_winner(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontālie
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertikālie
        [0, 4, 8], [2, 4, 6]              # Diagonāles
    ]
    for combo in winning_combinations:
        a, b, c = combo
        if board[a] == board[b] == board[c] and board[a] != '':
            return board[a]
    if '' not in board:
        return 'Draw'
    return None

def make_move(index):
    if st.session_state.game_over:
        st.warning("Spēle ir beigusies! Spēlējiet vēlreiz.")
        return
    if st.session_state.board[index] == '':
        st.session_state.board[index] = st.session_state.current_player
        winner = check_winner(st.session_state.board)
        if winner:
            st.session_state.game_over = True
            st.session_state.winner = winner
        else:
            st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'

def reset_game():
    st.session_state.board = [''] * 9
    st.session_state.current_player = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None

# Lietotāja interfeiss
st.title("🎮 Tic-Tac-Toe ar Streamlit")

if st.session_state.game_over:
    if st.session_state.winner == 'Draw':
        st.success("Spēle beigusies ar neizšķirumu!")
    else:
        st.success(f"Spēlētājs {st.session_state.winner} ir uzvarējis!")
    if st.button("Restartēt Spēli"):
        reset_game()

st.write(f"Pašreizējais spēlētājs: {st.session_state.current_player}")

# Spēles lauciņa izveide
cols = st.columns(3)
for i in range(9):
    with cols[i % 3]:
        if st.session_state.board[i] == '':
            if st.button('', key=i, on_click=make_move, args=(i,)):
                pass
        else:
            st.button(st.session_state.board[i], key=i, disabled=True)

if not st.session_state.game_over:
    winner = check_winner(st.session_state.board)
    if winner:
        st.session_state.game_over = True
        st.session_state.winner = winner
