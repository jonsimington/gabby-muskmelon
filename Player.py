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

			# Check diagonal spaces
			if self.check_space(chr(ord(piece.file) + 1), piece.rank + self.rank_direction)[1] == 1:
				if self.color == "White" and piece.rank == 7:
					pass
				elif self.color == "Black" and piece.rank == 2:
					pass
				else:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 1), piece.rank + self.rank_direction, ""))

			if self.check_space(chr(ord(piece.file) - 1), piece.rank + self.rank_direction)[1] == 1:
				if self.color == "White" and piece.rank == 7:
					pass
				elif self.color == "Black" and piece.rank == 2:
					pass
				else:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 1), piece.rank + self.rank_direction, ""))

			# En Passante

		elif piece.type == "Rook":
			# Extend in each direction until find piece or wall
			for rank in range(piece.rank + 1, 9):
				space = self.check_space(piece.file, rank)
				if space[0]:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, rank, ""))
				elif space[1] == 1:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, rank, ""))
					break
				else:
					break

			for rank in range(piece.rank - 1, 0, -1):
				space = self.check_space(piece.file, rank)
				if space[0]:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, rank, ""))
				elif space[1] == 1:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, rank, ""))
					break
				else:
					break

			for file in range(ord(piece.file) + 1, ord('h') + 1):
				space = self.check_space(chr(file), piece.rank)
				if space[0]:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(file), piece.rank, ""))
				elif space[1] == 1:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(file), piece.rank, ""))
					break
				else:
					break

			for file in range(ord(piece.file) - 1, ord('a') - 1, -1):
				space = self.check_space(chr(file), piece.rank)
				if space[0]:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(file), piece.rank, ""))
				elif space[1] == 1:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(file), piece.rank, ""))
					break
				else:
					break
		elif piece.type == "Knight":
			if ord(piece.file) - 1 > 96:
				if piece.rank - 2 > 0:
					space = self.check_space(chr(ord(piece.file) - 1), piece.rank - 2)
					if space[0] or space[1] == 1:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 1), piece.rank - 2, ""))
				if piece.rank + 2 < 9:
					space = self.check_space(chr(ord(piece.file) - 1), piece.rank + 2)
					if space[0] or space[1] == 1:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 1), piece.rank + 2, ""))
				if ord(piece.file) - 2 > 96:
					if piece.rank - 1 > 0:
						space = self.check_space(chr(ord(piece.file) - 2), piece.rank - 1)
						if space[0] or space[1] == 1:
							possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 2), piece.rank - 1, ""))
					if piece.rank + 1 < 9:
						space = self.check_space(chr(ord(piece.file) - 2), piece.rank + 1)
						if space[0] or space[1] == 1:
							possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 2), piece.rank + 1, ""))
			if ord(piece.file) + 1 < 105:
				if piece.rank - 2 > 0:
					space = self.check_space(chr(ord(piece.file) + 1), piece.rank - 2)
					if space[0] or space[1] == 1:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 1), piece.rank - 2, ""))
				if piece.rank + 2 < 9:
					space = self.check_space(chr(ord(piece.file) + 1), piece.rank + 2)
					if space[0] or space[1] == 1:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 1), piece.rank + 2, ""))
				if ord(piece.file) + 2 < 105:
					if piece.rank - 1 > 0:
						space = self.check_space(chr(ord(piece.file) + 2), piece.rank - 1)
						if space[0] or space[1] == 1:
							possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 2), piece.rank - 1, ""))
					if piece.rank + 1 < 9:
						space = self.check_space(chr(ord(piece.file) + 2), piece.rank + 1)
						if space[0] or space[1] == 1:
							possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 2), piece.rank + 1, ""))
		elif piece.type == "Bishop":
			# Extend in 4 diagonal directions
			# Positve positive
			for x in range(1,9):
				if x + piece.rank < 9 and x + ord(piece.file) < 105:
					space = self.check_space(chr(ord(piece.file) + x), piece.rank + x)
					if space[0]:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + x), piece.rank + x, ""))
					elif space[1] == 1:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + x), piece.rank + x, ""))
						break
					else:
						break
				else:
					break

			# Positive Rank, negative file
			for x in range(1,9):
				if x + piece.rank < 9 and ord(piece.file) - x > 96:
					space = self.check_space(chr(ord(piece.file) - x), piece.rank + x)
					if space[0]:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - x), piece.rank + x, ""))
					elif space[1] == 1:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - x), piece.rank + x, ""))
						break
					else:
						break
				else:
					break

			# Negative Rank, positive File
			for x in range(1,9):
				if piece.rank - x > 0 and ord(piece.file) + x < 105:
					space = self.check_space(chr(ord(piece.file) + x), piece.rank - x)
					if space[0]:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + x), piece.rank - x, ""))
					elif space[1] == 1:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + x), piece.rank - x, ""))
						break
					else:
						break
				else:
					break

			# Negative Negative
			for x in range(1,9):
				if piece.rank - x > 0 and ord(piece.file) - x > 96:
					space = self.check_space(chr(ord(piece.file) - x), piece.rank - x)
					if space[0]:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - x), piece.rank - x, ""))
					elif space[1] == 1:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - x), piece.rank - x, ""))
						break
					else:
						break
				else:
					break

		elif piece.type == "Queen":
			for x in range(1,9):
				if x + piece.rank < 9 and x + ord(piece.file) < 105:
					space = self.check_space(chr(ord(piece.file) + x), piece.rank + x)
					if space[0]:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + x), piece.rank + x, ""))
					elif space[1] == 1:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + x), piece.rank + x, ""))
						break
					else:
						break
				else:
					break

			# Positive Rank, negative file
			for x in range(1,9):
				if x + piece.rank < 9 and ord(piece.file) - x > 96:
					space = self.check_space(chr(ord(piece.file) - x), piece.rank + x)
					if space[0]:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - x), piece.rank + x, ""))
					elif space[1] == 1:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - x), piece.rank + x, ""))
						break
					else:
						break
				else:
					break

			# Negative Rank, positive File
			for x in range(1,9):
				if piece.rank - x > 0 and ord(piece.file) + x < 105:
					space = self.check_space(chr(ord(piece.file) + x), piece.rank - x)
					if space[0]:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + x), piece.rank - x, ""))
					elif space[1] == 1:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + x), piece.rank - x, ""))
						break
					else:
						break
				else:
					break

			# Negative Negative
			for x in range(1,9):
				if piece.rank - x > 0 and ord(piece.file) - x > 96:
					space = self.check_space(chr(ord(piece.file) - x), piece.rank - x)
					if space[0]:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - x), piece.rank - x, ""))
					elif space[1] == 1:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - x), piece.rank - x, ""))
						break
					else:
						break
				else:
					break

			for rank in range(piece.rank + 1, 9):
				space = self.check_space(piece.file, rank)
				if space[0]:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, rank, ""))
				elif space[1] == 1:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, rank, ""))
					break
				else:
					break

			for rank in range(piece.rank - 1, 0, -1):
				space = self.check_space(piece.file, rank)
				if space[0]:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, rank, ""))
				elif space[1] == 1:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, rank, ""))
					break
				else:
					break

			for file in range(ord(piece.file) + 1, ord('h') + 1):
				space = self.check_space(chr(file), piece.rank)
				if space[0]:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(file), piece.rank, ""))
				elif space[1] == 1:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(file), piece.rank, ""))
					break
				else:
					break

			for file in range(ord(piece.file) - 1, ord('a') - 1, -1):
				space = self.check_space(chr(file), piece.rank)
				if space[0]:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(file), piece.rank, ""))
				elif space[1] == 1:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(file), piece.rank, ""))
					break
				else:
					break
		elif piece.type == "King":
			# Can move to any one adjacent space
			for rank in range(piece.rank - 1, piece.rank + 2):
				for file in range(ord(piece.file) - 1, ord(piece.file) + 2):
					if rank > 0 and rank < 9 and file > 96 and file < 105:
						if rank != piece.rank or chr(file) != piece.file:
							space = self.check_space(chr(file), rank)
							if space[0] or space[1] == 1:
								possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(file), rank, ""))

		return possible_moves

	def check_space(self, file, rank):
		# print("Checking ", file, rank)
		for piece in self.pieces:
			if piece.rank == rank and piece.file == file:
				return (False, 0)
		for piece in self.opponent.pieces:
			if piece.rank == rank and piece.file == file:
				return (False, 1)
		return (True, 0)

	def move_piece(self, piece, file, rank, promotion):
		piece.move_piece(file, rank, promotion)
