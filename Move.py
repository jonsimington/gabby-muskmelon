# Patrick Bremehr
# Move Class

class Chess_Move:
	def __init__(self, piece, from_file, from_rank, to_file, to_rank, promotion, note=""):
		self.captured = None
		self.from_file = from_file
		self.from_rank = from_rank
		self.to_file = to_file
		self.to_rank = to_rank
		self.piece = piece
		self.promotion = promotion
		self.note = note

	def set_piece_captured(self, captured):
		self.captured = captured

	def check_equal(self, other_move):
		if self.from_file != other_move.from_file:
			return False
		if self.from_rank != other_move.from_rank:
			return False
		if self.piece.type != other_move.piece.type:
			return False
		if self.to_file != other_move.to_file:
			return False
		if self.to_rank != other_move.to_rank:
			return False
		if self.promotion != other_move.promotion:
			return False
		return True

	def output_string(self):
		if self.promotion != "":
			print(self.piece.type + " at " + self.from_file + str(self.from_rank) + " to " + self.to_file + str(self.to_rank) + ", Promoted to " + self.promotion)
		else:
			print(self.piece.type + " at " + self.from_file + str(self.from_rank) + " to " + self.to_file + str(self.to_rank))

	def __repr__(self):
		tempStr = self.piece.type + " at " + self.from_file + str(self.from_rank) + " to " + self.to_file + str(self.to_rank)
		if self.captured != None:
			tempStr += ", capturing + " + self.captured.type
		return tempStr
