from random import randint

class Player(object):
	
	def __init__(self, ip, name):
		self.ip = ip
		self.name = name
		self.id = self.ip + '_' + ''.join(["{}".format(randint(0, 9)) for x in range(0, 4)])
		self.wins = 0
		self.losses = 0
		
	def win(self):
		self.wins += 1
	
	def loss(self):
		self.losses += 1