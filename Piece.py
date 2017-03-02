# Patrick Bremehr
# Piece Class

class Chess_Piece:
	def __init__(self, file, rank, owner, type):
		self.file = file
		self.rank = rank
		self.type = type
		self.owner = owner 
		self.captured = False
		self.has_moved = False

	def move_piece(self, file, rank, promotion="", undo_has_moved=False):
		self.file = file
		self.rank = rank
		if promotion != "":
			self.type = promotion

		# UNDO a promotion
		if promotion == "Undo":
			self.type = "Pawn"
		if not self.has_moved:
			self.has_moved = True
		elif undo_has_moved:
			self.has_moved = False

	def check_equal(self, other):
		if self.file != other.file:
			return False
		if self.rank != other.rank:
			return False
		if self.type != other.type:
			return False
		return True