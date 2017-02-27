# Patrick Bremehr
# Move Class

class Chess_Move:
	def __init__(self, piece, from_file, from_rank, to_file, to_rank, promotion):
		self.captured = None
		self.from_file = from_file
		self.from_rank = from_rank
		self.to_file = to_file
		self.to_rank = to_rank
		self.piece = piece
		self.promotion = promotion