# Patrick Bremehr
# Piece Class

class Chess_Piece:
	def __init__(self, file, rank, owner, type):
		self.file = file
		self.rank = rank
		self.type = type
		self.owner = owner 
		self.captured = False

	def move_piece(self, file, rank, promotion):
		self.file = file
		self.rank = rank
		# print("MOVING", self.type, "to " file, rank)