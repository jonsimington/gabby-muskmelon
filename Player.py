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

	def get_possible_moves(self):
		pass

	def get_moves_piece(self, piece, threat_search=False):
		#print("CALLING GET MOVES WITH threat_search=" + str(threat_search))
		possible_moves = []

		# If in_check == True, only possible moves are to take piece causing check if only one, or to block that piece from check
		# Either way, we need to identify what piece is causing check

		# Also need to be able to check if move will open King to check\

		# Function to get 'threatened' squares
		
		"""
		# Find Check causing piece(s)
		if self.in_check:
			# Loop through opponent pieces and check pieces in danger, relative to king?
			# Find King Piece
			for piece in self.pieces:
				if piece.type == "King":
					king_piece = piece
					break

			for piece in self.opponent.pieces:
				if piece.type == "Pawn":


					# Check diagonals in one space
				elif piece.type == "Knight":
					# Check 8 jumps
				elif piece.type == "Bishop":
					# Check diagonals
				elif piece.type == "Queen":
					# Check EVERYTHING
				elif piece.type == "Rook":
					# Check straight lines

		"""
		#checking_piece = None
		#if self.in_check:
		#	checking_piece = self.get_checking_piece()

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
			space = self.check_space(chr(ord(piece.file) + 1), piece.rank + self.rank_direction)
			if space[1] == 1:
				if self.color == "White" and piece.rank == 7:
					pass
				elif self.color == "Black" and piece.rank == 2:
					pass
				else:
					move = Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 1), piece.rank + self.rank_direction, "")
					move.set_piece_captured(space[2])
					possible_moves.append(move)
			elif space[1] == 0 and threat_search:
				possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 1), piece.rank + self.rank_direction, "", note="blocked"))

			space = self.check_space(chr(ord(piece.file) - 1), piece.rank + self.rank_direction)
			if space[1] == 1:
				if self.color == "White" and piece.rank == 7:
					pass
				elif self.color == "Black" and piece.rank == 2:
					pass
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
					move = Chess_Move(piece, piece.file, piece.rank, piece.file, rank, "")
					move.set_piece_captured(space[2])
					possible_moves.append(move)
					break
				elif space[1] == 0 and threat_search:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, rank, "", note="blocked"))
					break
				else:
					break

			for file in range(ord(piece.file) - 1, ord('a') - 1, -1):
				space = self.check_space(chr(file), piece.rank)
				if space[0]:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(file), piece.rank, ""))
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
					move = Chess_Move(piece, piece.file, piece.rank, piece.file, rank, "")
					move.set_piece_captured(space[2])
					possible_moves.append(move)
					break
				elif space[1] == 0 and threat_search:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, piece.file, rank, "", note="blocked"))
				else:
					break

			for file in range(ord(piece.file) - 1, ord('a') - 1, -1):
				space = self.check_space(chr(file), piece.rank)
				if space[0]:
					possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(file), piece.rank, ""))
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
			#print("BEFORE")
			#for move in possible_moves:
		#		move.output_string()
			for move in possible_moves:
				# Make move
				self.move_piece(move.piece, move.to_file, move.to_rank, "")
				check_caused = king_str in self.get_threat_squares()
				self.move_piece(move.piece, move.from_file, move.from_rank, "")
				# Check if threat spaces include king space
				if check_caused:
					# Remove move from possible moves
					possible_moves[:] = [m for m in possible_moves if not m.check_equal(move)]
			#print("AFTER")
			#for move in possible_moves:
			#	move.output_string()

		
		return possible_moves

	def check_space(self, file, rank):
		# print("Checking ", file, rank)
		for piece in self.pieces:
			if piece.rank == rank and piece.file == file:
				return (False, 0)
		for piece in self.opponent.pieces:
			if piece.rank == rank and piece.file == file:
				return (False, 1, piece)
		return (True, 0)

	def move_piece(self, piece, file, rank, promotion):
		piece.move_piece(file, rank, promotion)

	def get_threat_squares(self):
		threats = {}
		for piece in self.opponent.pieces:
			piece_moves = self.opponent.get_moves_piece(piece, threat_search=True)
			# capture_move = [move for move in piece_moves if move.captured != None]
			for move in piece_moves:
				if piece.type != "Pawn":
					space_str = move.to_file + str(move.to_rank)
					if not space_str in threats:
						threats[space_str] = piece
				elif piece.type == "Pawn":
					if move.captured != None:
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
		#print(threats[space_str].type, threats[space_str].file, str(threats[space_str].rank))
		return threats[space_str]




