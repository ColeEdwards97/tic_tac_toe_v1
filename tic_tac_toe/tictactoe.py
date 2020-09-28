class TicTacToe(object):
	""" Tic Tac Toe Game! """ 
	
	def __init__(self):
		self.board = [None for x in range(9)]
		self.players = {}
		self.players_turn = 0	
		self.game_over = False
		self.msg = ""
		
	
	def register_player(self, player):
		if self.can_player_join():
			if 'X' not in self.players:
				self.players['X'] = player
			else:
				self.players['O'] = player
		
	def can_player_join(self):
		return len(self.players) < 2
		
	def can_player_play(self):
		return len(self.players) <= 2
	
	def is_players_turn(self, id):
		# prevents players from playing without enough players
		if self.can_player_join():
			return False
		else:
			return id == list(self.players.values())[self.players_turn].id
	
	def get_current_player(self):
		return list(self.players.values())[self.players_turn]
	
	def get_player_by_id(self, id):
		for p in list(self.players.values()):
			if p.id == id: 
				return p
		return None
				
	def next_turn(self):
		self.players_turn = 1 - self.players_turn
		
	def make_move(self, idx):
		self.set_at(idx, list(self.players.keys())[self.players_turn])
		self.next_turn()
	
	def set_at(self, idx, val):
		self.board[idx] = val
		
	def get_at(self, idx):
		return self.board[idx]
		
	def is_full(self):
		return all([x != None for x in self.board])
		
	def clear(self):
		self.board = [None for x in range(9)]
	
	def is_win(self):
	
		# rows
		for i in range(3):
			row = self.board[i*3:i*3+3]
			if all((x != None) and (x == row[0]) for x in row):
				return (True, row[0])
		
		# columns
		for i in range(3):
			col = self.board[i::3]
			if all((x != None) and (x == col[0]) for x in col):
				return (True, col[0])
		
		# diagonal 1
		diag_1 = self.board[::4]
		if all((x != None) and (x == diag_1[0]) for x in diag_1):
			return (True, diag_1[0])
		
		# diagonal 2
		diag_2 = self.board[2:7:2]
		if all((x != None) and (x == diag_2[0]) for x in diag_2):
			return (True, diag_2[0])
		
		return (False, None)

	def winner(self, side):
		self.players[side].win()
		if side == 'X':
			self.players['O'].loss()
		elif side == 'O':
			self.players['X'].loss()