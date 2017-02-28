# Patrick Bremehr
# Piece Class

class Chess_Piece:
	def __init__(self, file, rank, owner, type):
		self.file = file
		self.rank = rank
		self.type = type
		self.owner = owner 
		self.captured = False

	def move_piece(self, file, rank, promotion=""):
		self.file = file
		self.rank = rank
		if promotion != "":
			self.type = promotion

		# UNDO a promotion
		if promotion == "Undo":
			self.type = "Pawn"

	def check_equal(self, other):
		if self.file != other.file:
			return False
		if self.rank != other.rank:
			return False
		if self.type != other.type:
			return False
		return True