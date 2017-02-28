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
		self.threat_squares = {}

	def set_opponent(self, opponent):
		self.opponent = opponent

	def get_moves_piece(self, piece, threat_search=False):
		possible_moves = []
		if piece.type == "Pawn":
			# Normal
			if self.check_space(piece.file, piece.rank + self.rank_direction)[0]:
				# Promotions
				if self.color == "White" and piece.rank == 7:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, piece.rank + self.rank_direction, "Rook"))
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, piece.rank + self.rank_direction, "Bishop"))
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, piece.rank + self.rank_direction, "Queen"))
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, piece.rank + self.rank_direction, "Knight"))
				elif self.color == "Black" and piece.rank == 2:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, piece.rank + self.rank_direction, "Rook"))
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, piece.rank + self.rank_direction, "Bishop"))
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, piece.rank + self.rank_direction, "Queen"))
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, piece.rank + self.rank_direction, "Knight"))
				else:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, piece.rank + self.rank_direction, ""))

				# Move two spaces
				if (self.color == "White" and piece.rank == 2) or (self.color == "Black" and piece.rank == 7):
					if self.check_space(piece.file, piece.rank + 2 * self.rank_direction)[0]:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, piece.rank + 2 * self.rank_direction, ""))

			# Check diagonal spaces
			if piece.file != 'h': 
				space = self.check_space(chr(ord(piece.file) + 1), piece.rank + self.rank_direction)
				if space[1] == 1:
					if self.color == "White" and piece.rank == 7:
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 1), piece.rank + self.rank_direction, "Queen")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 1), piece.rank + self.rank_direction, "Rook")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 1), piece.rank + self.rank_direction, "Bishop")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 1), piece.rank + self.rank_direction, "Knight")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
					elif self.color == "Black" and piece.rank == 2:
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 1), piece.rank + self.rank_direction, "Queen")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 1), piece.rank + self.rank_direction, "Rook")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 1), piece.rank + self.rank_direction, "Bishop")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 1), piece.rank + self.rank_direction, "Knight")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
					else:
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 1), piece.rank + self.rank_direction, "")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
				elif space[1] == 0 and threat_search:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 1), piece.rank + self.rank_direction, "", note="blocked"))

			if piece.file != 'a':
				space = self.check_space(chr(ord(piece.file) - 1), piece.rank + self.rank_direction)
				if space[1] == 1:
					if self.color == "White" and piece.rank == 7:
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 1), piece.rank + self.rank_direction, "Queen")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 1), piece.rank + self.rank_direction, "Rook")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 1), piece.rank + self.rank_direction, "Bishop")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 1), piece.rank + self.rank_direction, "Knight")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
					elif self.color == "Black" and piece.rank == 2:
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 1), piece.rank + self.rank_direction, "Queen")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 1), piece.rank + self.rank_direction, "Rook")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 1), piece.rank + self.rank_direction, "Bishop")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 1), piece.rank + self.rank_direction, "Knight")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
					else:
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 1), piece.rank + self.rank_direction, "")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
				elif space[1] == 0 and threat_search:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 1), piece.rank + self.rank_direction, "", note="blocked"))

			# En Passante--------------------

		elif piece.type == "Rook":
			# Extend in each direction until find piece or wall
			for rank in range(piece.rank + 1, 9):
				space = self.check_space(piece.file, rank)
				if space[0]:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, rank, ""))
				elif space[1] == 1:
					move = Chess_Move(piece, piece.file, piece.rank, piece.file, rank, "")
					move.set_piece_captured(space[2])
					possible_moves.append(move)
					break
				elif space[1] == 0 and threat_search:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, rank, "", note="blocked"))
					break
				else:
					break

			for rank in range(piece.rank - 1, 0, -1):
				space = self.check_space(piece.file, rank)
				if space[0]:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, rank, ""))
				elif space[1] == 1:
					move = Chess_Move(piece, piece.file, piece.rank, piece.file, rank, "")
					move.set_piece_captured(space[2])
					possible_moves.append(move)
					break
				elif space[1] == 0 and threat_search:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, rank, "", note="blocked"))
					break
				else:
					break

			for file in range(ord(piece.file) + 1, ord('h') + 1):
				space = self.check_space(chr(file), piece.rank)
				if space[0]:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(file), piece.rank, ""))
				elif space[1] == 1:
					move = Chess_Move(piece, piece.file, piece.rank, chr(file), piece.rank, "")
					move.set_piece_captured(space[2])
					possible_moves.append(move)
					break
				elif space[1] == 0 and threat_search:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(file), piece.rank, "", note="blocked"))
					break
				else:
					break

			for file in range(ord(piece.file) - 1, ord('a') - 1, -1):
				space = self.check_space(chr(file), piece.rank)
				if space[0]:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(file), piece.rank, ""))
				elif space[1] == 1:
					move = Chess_Move(piece, piece.file, piece.rank, chr(file), piece.rank, "")
					move.set_piece_captured(space[2])
					possible_moves.append(move)
					break
				elif space[1] == 0 and threat_search:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(file), piece.rank, "", note="blocked"))
					break
				else:
					break
		elif piece.type == "Knight":
			if ord(piece.file) - 1 > 96:
				if piece.rank - 2 > 0:
					space = self.check_space(chr(ord(piece.file) - 1), piece.rank - 2)
					if space[0]:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 1), piece.rank - 2, ""))
					elif space[1] == 1:
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 1), piece.rank - 2, "")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
					elif space[1] == 0 and threat_search:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 1), piece.rank - 2, "", note="blocked"))
				if piece.rank + 2 < 9:
					space = self.check_space(chr(ord(piece.file) - 1), piece.rank + 2)
					if space[0]:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 1), piece.rank + 2, ""))
					elif space[1] == 1:
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 1), piece.rank + 2, "")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
					elif space[1] == 0 and threat_search:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 1), piece.rank + 2, "", note="blocked"))
				if ord(piece.file) - 2 > 96:
					if piece.rank - 1 > 0:
						space = self.check_space(chr(ord(piece.file) - 2), piece.rank - 1)
						if space[0]:
							possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 2), piece.rank - 1, ""))
						elif space[1] == 1:
							move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 2), piece.rank - 1, "")
							move.set_piece_captured(space[2])
							possible_moves.append(move)
						elif space[1] == 0 and threat_search:
							possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 2), piece.rank - 1, "", note="blocked"))
					if piece.rank + 1 < 9:
						space = self.check_space(chr(ord(piece.file) - 2), piece.rank + 1)
						if space[0]:
							possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 2), piece.rank + 1, ""))
						elif space[1] == 1:
							move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 2), piece.rank + 1, "")
							move.set_piece_captured(space[2])
							possible_moves.append(move)
						elif space[1] == 0 and threat_search:
							possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 2), piece.rank + 1, "", note="blocked"))
			if ord(piece.file) + 1 < 105:
				if piece.rank - 2 > 0:
					space = self.check_space(chr(ord(piece.file) + 1), piece.rank - 2)
					if space[0]:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 1), piece.rank - 2, ""))
					elif space[1] == 1:
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 1), piece.rank - 2, "")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
					elif space[1] == 0 and threat_search:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 1), piece.rank - 2, "", note="blocked"))
				if piece.rank + 2 < 9:
					space = self.check_space(chr(ord(piece.file) + 1), piece.rank + 2)
					if space[0]:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 1), piece.rank + 2, ""))
					elif space[1] == 1:
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 1), piece.rank + 2, "")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
					elif space[1] == 0 and threat_search:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 1), piece.rank + 2, "", note="blocked"))
				if ord(piece.file) + 2 < 105:
					if piece.rank - 1 > 0:
						space = self.check_space(chr(ord(piece.file) + 2), piece.rank - 1)
						if space[0]:
							possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 2), piece.rank - 1, ""))
						elif space[1] == 1:
							move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 2), piece.rank - 1, "")
							move.set_piece_captured(space[2])
							possible_moves.append(move)
						elif space[1] == 0 and threat_search:
							possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 2), piece.rank - 1, "", note="blocked"))
					if piece.rank + 1 < 9:
						space = self.check_space(chr(ord(piece.file) + 2), piece.rank + 1)
						if space[0]:
							possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 2), piece.rank + 1, ""))
						elif space[1] == 1:
							move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 2), piece.rank + 1, "")
							move.set_piece_captured(space[2])
							possible_moves.append(move)
						elif space[1] == 0 and threat_search:
							possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 2), piece.rank + 1, "", note="blocked"))

		elif piece.type == "Bishop":
			# Extend in 4 diagonal directions
			# Positve positive
			for x in range(1,9):
				if x + piece.rank < 9 and x + ord(piece.file) < 105:
					space = self.check_space(chr(ord(piece.file) + x), piece.rank + x)
					if space[0]:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + x), piece.rank + x, ""))
					elif space[1] == 1:
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + x), piece.rank + x, "")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
						break
					elif space[1] == 0 and threat_search:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + x), piece.rank + x, "", note="blocked"))
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
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - x), piece.rank + x, "")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
						break
					elif space[1] == 0 and threat_search:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - x), piece.rank + x, "", note="blocked"))
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
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + x), piece.rank - x, "")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
						break
					elif space[1] == 0 and threat_search:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + x), piece.rank - x, "", note="blocked"))
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
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - x), piece.rank - x, "")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
						break
					elif space[1] == 0 and threat_search:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - x), piece.rank - x, "", note="blocked"))
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
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + x), piece.rank + x, "")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
						break
					elif space[1] == 0 and threat_search:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + x), piece.rank + x, "", note="blocked"))
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
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - x), piece.rank + x, "")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
						break
					elif space[1] == 0 and threat_search:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - x), piece.rank + x, "", note="blocked"))
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
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + x), piece.rank - x, "")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
						break
					elif space[1] == 0 and threat_search:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + x), piece.rank - x, "", note="blocked"))
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
						move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - x), piece.rank - x, "")
						move.set_piece_captured(space[2])
						possible_moves.append(move)
						break
					elif space[1] == 0 and threat_search:
						possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - x), piece.rank - x, "", note="blocked"))
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
					move = Chess_Move(piece, piece.file, piece.rank, piece.file, rank, "")
					move.set_piece_captured(space[2])
					possible_moves.append(move)
					break
				elif space[1] == 0 and threat_search:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, rank, "", note="blocked"))
					break
				else:
					break

			for rank in range(piece.rank - 1, 0, -1):
				space = self.check_space(piece.file, rank)
				if space[0]:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, rank, ""))
				elif space[1] == 1:
					move = Chess_Move(piece, piece.file, piece.rank, piece.file, rank, "")
					move.set_piece_captured(space[2])
					possible_moves.append(move)
					break
				elif space[1] == 0 and threat_search:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, rank, "", note="blocked"))
					break
				else:
					break

			for file in range(ord(piece.file) + 1, ord('h') + 1):
				space = self.check_space(chr(file), piece.rank)
				if space[0]:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(file), piece.rank, ""))
				elif space[1] == 1:
					move = Chess_Move(piece, piece.file, piece.rank, chr(file), piece.rank, "")
					move.set_piece_captured(space[2])
					possible_moves.append(move)
					break
				elif space[1] == 0 and threat_search:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(file), piece.rank, "", note="blocked"))
				else:
					break

			for file in range(ord(piece.file) - 1, ord('a') - 1, -1):
				space = self.check_space(chr(file), piece.rank)
				if space[0]:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(file), piece.rank, ""))
				elif space[1] == 1:
					move = Chess_Move(piece, piece.file, piece.rank, chr(file), piece.rank, "")
					move.set_piece_captured(space[2])
					possible_moves.append(move)
					break
				elif space[1] == 0 and threat_search:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(file), piece.rank, "", note="blocked"))
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
							if space[0]:
								space_str = chr(file) + str(rank)
								if not space_str in self.threat_squares:
									possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(file), rank, ""))
							elif space[1] == 1:
								move = Chess_Move(piece, piece.file, piece.rank, chr(file), rank, "")
								move.set_piece_captured(space[2])
								possible_moves.append(move)
							elif space[1] == 0 and threat_search:
								possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(file), rank, "", note="blocked"))
		
		#if checking_piece != None:
		#	possible_moves = [move for move in possible_moves if move.captured == checking_piece]
		# Find King Piece
		for piece in self.pieces:
			if piece.type == "King":
				king_piece = piece
				king_str = piece.file + str(piece.rank)
				break
		# Look through moves, if one puts King in check, it's not valid
		# Use game state, but make sure to change back
		if not threat_search:
			for x in range(len(possible_moves) - 1, -1, -1):
				# Make move
				move = possible_moves[x]
				self.move_piece(move.piece, move.to_file, move.to_rank, move.promotion)
				king_str = king_piece.file + str(king_piece.rank)
				threats = self.get_threat_squares()
				
				check_caused = king_str in threats
				if move.promotion != "":
					self.move_piece(move.piece, move.from_file, move.from_rank, "Undo")
				else:
					self.move_piece(move.piece, move.from_file, move.from_rank, "")
				# Check if threat spaces include king space
				if check_caused:
					# Remove move from possible moves
					del possible_moves[x]
		
		return possible_moves

	def check_space(self, file, rank):
		for piece in self.pieces:
			if piece.rank == rank and piece.file == file:
				#print("BLOCKED")
				return (False, 0)
		for piece in self.opponent.pieces:
			if piece.rank == rank and piece.file == file:
				#print("BLOCKED")
				return (False, 1, piece)
		#print("OPEN")
		return (True, 0)

	def move_piece(self, piece, file, rank, promotion):
		piece.move_piece(file, rank, promotion)

	def get_threat_squares(self):
		threats = {}
		for piece in self.opponent.pieces:
			piece_moves = self.opponent.get_moves_piece(piece, threat_search=True)
			for move in piece_moves:
				#move.output_string()
				if piece.type != "Pawn":
					space_str = move.to_file + str(move.to_rank)
					if not space_str in threats:
						threats[space_str] = piece
				elif piece.type == "Pawn":
					# IF move was diagonal
					if move.to_file != move.from_file and move.to_rank != move.from_rank:
						space_str = move.to_file + str(move.to_rank)
						if not space_str in threats:
							threats[space_str] = piece

		# Need a way to include capturing turns that still keep you in threat
		return threats

	def update_threat_squares(self):
		self.threat_squares = self.get_threat_squares()

	def get_checking_piece(self):
		# Find king piece
		for piece in self.pieces:
			if piece.type == "King":
				space_str = piece.file + str(piece.rank)
				break
		threats = self.get_threat_squares()
		return threats[space_str]




