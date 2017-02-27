# Patrick Bremehr
# Player Class

from Move import Chess_Move

class Chess_Player:
	def __init__(self, color, name):
		self.color = color
		self.in_check = False
		self.lost = False
		self.made_move = False
		self.name = name
		self.pieces = []
		self.opponent = None
		if color == "White":
			self.rank_direction = 1
		elif color == "Black":
			self.rank_direction = -1 

	def set_opponent(self, opponent):
		self.opponent = opponent

	def get_possible_moves(self):
		pass

	def get_moves_piece(self, piece):
		possible_moves = []
		if piece.type == "Pawn":
			# Normal
			if self.check_space(piece.file, piece.rank + self.rank_direction)[0]:
				# Promotions
				print("DEBUG!!!!!!!! ", self.color)
				if self.color == "White" and piece.rank == 7:
					pass
				elif self.color == "Black" and piece.rank == 2:
					pass
				else:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, piece.rank + self.rank_direction, ""))

				# Move two spaces
				if (self.color == "White" and piece.rank == 2) or (self.color == "Black" and piece.rank == 7):
					if self.check_space(piece.file, piece.rank + 2 * self.rank_direction)[0]:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, piece.rank + 2 * self.rank_direction, ""))

			
			# Capture
			# En Passante

			return possible_moves
		elif piece.type == "Rook":
			# Horizantal and Vertical
			pass
		elif piece.type == "Knight":
			pass
		elif piece.type == "Bishop":
			pass
		elif piece.type == "Queen":
			pass
		elif piece.type == "King":
			pass

	def check_space(self, file, rank):
		print("Checking ", file, rank)
		for piece in self.pieces:
			if piece.rank == rank and piece.file == file:
				return (False, 0)
		for piece in self.opponent.pieces:
			if piece.rank == rank and piece.file == file:
				return (False, 1)
		return (True, 0)



	


