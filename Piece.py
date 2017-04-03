# Patrick Bremehr
# Piece Class

def copy_piece(piece, player_owner):
	new_piece = Chess_Piece(piece.file, piece.rank, player_owner, piece.type)
	new_piece.has_moved = piece.has_moved
	return new_piece

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

	def __repr__(self):
		return self.type + " " + self.file + str(self.rank)