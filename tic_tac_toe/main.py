from flask import *
import time
import queue

import tictactoe
import player

# local testing
#HOST = '127.0.0.1'
# hosted server
HOST = '0.0.0.0'
PORT = '5000'
USERS = []
KEY = str(input('enter secret key: '))


app = Flask(__name__)
ttt = tictactoe.TicTacToe()
q = queue.Queue()


def put_mp(q_item):
	for x in ttt.players:
		q.put(q_item)

def game_stream():
	while True:
		data = q.get(block=True, timeout=None)
		yield data

def validate_key(key_in):
	return (key_in != None) and (key_in == KEY)

def validate_name(name_in):
	return (name_in != None) and (name_in != "")

def register_user(ip, name):
	p = player.Player(ip, name)
	ttt.register_player(p)
	USERS.append(p.id)
	return p
	
def stream_template(template_name, **context):
	app.update_template_context(context)
	t = app.jinja_env.get_template(template_name)
	rv = t.stream(context)
	rv.disable_buffering()
	return rv


@app.route('/login', methods=['GET', 'POST'])
def login():

	ip = request.environ['REMOTE_ADDR']
	msg = ""
	
	if request.method == 'GET':
		# check if already logged in
		# if registered as a player redirect to game
		# otherwise GAME IS FULL
		if request.cookies.get('login'):
			return redirect(url_for('game'))
		
	if request.method == 'POST':
		# check username and key
		# check if user can join game
		# redirect to game if it can be joined
		key_in = request.form['key']
		name_in = request.form['username']
		if validate_key(key_in):
			if validate_name(name_in):
				p = register_user(ip, name_in)
				if ttt.can_player_play():	
					resp = redirect(url_for('game'))
					resp.set_cookie('login', p.id) 
					return resp
				else:
					msg = "game is full!"
			else:
				msg = "invalid username!"
		else:
			msg = "invalid key! are you sure you're supposed to be here?"

	return render_template('login.html', msg=msg)


# maybe do this later
@app.route('/lobby', methods=['GET'])
def lobby():

	if request.method == 'GET':
		# wait for players...
		# ...redirect to game
		pass

	return render_template('lobby.html')

	
@app.route('/game', methods=['GET', 'POST'])
def game():

	id = request.cookies.get('login')
	ttt.msg = ""
	
	if request.method == 'GET':
	
		# verify that user has logged in with cookies
		# if not redirect to login
		if not request.cookies.get('login'):
			return redirect(url_for('login'))
		
		if id not in USERS:
			resp = redirect(url_for('login'))
			resp.set_cookie('login', '', expires=0)
			return resp
			
	if request.method == 'POST':
		# check if a board button was clicked
		# check if its the right players turn
		# get the id of the clicked button
		# make_move()
		# check for game ending conditions
		# stream updated board (queue)
		# next turn
		
		if 'tile' in request.form:
			data = request.form['tile']
			idx = int(data)
			
			if not ttt.can_player_join():
			
				# is players turn?
				if ttt.is_players_turn(id):
					ttt.make_move(idx)
					
				ttt.msg = (list(ttt.players.values())[ttt.players_turn]).name + "'s turn!"
				
				# was game won?
				is_win = ttt.is_win()
				if is_win[0]:
					ttt.game_over = True
					ttt.winner(is_win[1])
					ttt.msg = ttt.players[is_win[1]].name + " wins!"
				
				# is game draw?
				if ttt.is_full():
					ttt.game_over = True
					ttt.msg = "draw! you're both losers!"
				
				put_mp(ttt)
				
			return ""
			
		# was game reset?
		if 'reset' in request.form:
			ttt.clear()
			ttt.game_over = False
			ttt.msg = (list(ttt.players.values())[ttt.players_turn]).name + "'s turn!"
			put_mp(ttt)
			return ""
	
	# TODO: move to lobby... not really necessary
	# handle waiting for players
	if ttt.can_player_join():
		ttt.msg = "Please wait for players..."
	else:
		ttt.msg = (list(ttt.players.values())[ttt.players_turn]).name + "'s turn!"
	put_mp(ttt)
		
	return Response(stream_with_context(stream_template('game.html', stream=game_stream())))
	


if __name__ == "__main__":
	try: app.run(host=HOST, port=PORT, threaded=True)
	except KeyboardInterrupt:
		pass