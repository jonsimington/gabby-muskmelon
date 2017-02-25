# Patrick Bremehr
# Player Class

class Chess_Player:
	def __init__(self, color, name):
		self.color = color
		self.in_check = False
		self.lost = False
		self.made_move = False
		self.name = name
		self.pieces = []
		self.opponent = opponent
		if color == "white":
			self.rank_direction = 1
		elif color == "black":
			self.rank_direction = -1 

	def set_opponent(self, opponent):
		self.opponent = opponent

	


