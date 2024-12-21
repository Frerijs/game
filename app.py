from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Spēles datubāze
games = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('create_game')
def handle_create_game():
    game_id = str(uuid.uuid4())[:8]  # Ģenerē unikālu spēles ID
    games[game_id] = {
        'players': [],
        'board': [''] * 9,
        'current_turn': 'X',
        'winner': None
    }
    join_room(game_id)
    games[game_id]['players'].append(request.sid)
    emit('game_created', {'game_id': game_id})

@socketio.on('join_game')
def handle_join_game(data):
    game_id = data['game_id']
    if game_id in games and len(games[game_id]['players']) < 2:
        join_room(game_id)
        games[game_id]['players'].append(request.sid)
        emit('game_joined', {'game_id': game_id, 'board': games[game_id]['board'], 'current_turn': games[game_id]['current_turn']}, room=game_id)
        emit('player_joined', {'msg': 'Another player has joined the game.'}, room=game_id)
    else:
        emit('error', {'msg': 'Game not found or already full.'})

@socketio.on('make_move')
def handle_make_move(data):
    game_id = data['game_id']
    position = data['position']
    player = request.sid

    if game_id not in games:
        emit('error', {'msg': 'Game not found.'})
        return

    game = games[game_id]

    if game['winner']:
        emit('error', {'msg': 'Game has already been won.'})
        return

    if game['players'][game['current_turn_index(game_id, player)']] != player:
        emit('error', {'msg': 'Not your turn.'})
        return

    if game['board'][position] == '':
        game['board'][position] = game['current_turn']
        emit('update_board', {'board': game['board'], 'current_turn': game['current_turn']}, room=game_id)
        winner = check_winner(game['board'])
        if winner:
            game['winner'] = winner
            emit('game_over', {'winner': winner}, room=game_id)
        elif '' not in game['board']:
            game['winner'] = 'Draw'
            emit('game_over', {'winner': 'Draw'}, room=game_id)
        else:
            game['current_turn'] = 'O' if game['current_turn'] == 'X' else 'X'
            emit('update_turn', {'current_turn': game['current_turn']}, room=game_id)
    else:
        emit('error', {'msg': 'Position already taken.'})

def check_winner(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rindiņi
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Kolonnas
        [0, 4, 8], [2, 4, 6]              # Diagonāles
    ]

    for combo in winning_combinations:
        a, b, c = combo
        if board[a] == board[b] == board[c] != '':
            return board[a]
    return None

def handle_disconnect():
    # Implementēt, ja nepieciešams
    pass

@socketio.on('disconnect')
def handle_disconnect_event():
    handle_disconnect()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
