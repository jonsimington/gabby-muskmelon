# Patrick Bremehr
# Player Class

from Move import Chess_Move
from Piece import copy_piece
import random, time

def IterDeepMiniMax(player, max_depth, max_q_depth, time_limit, alpha, beta):
	history_table = {}
	start_time = time.time()
	for depth in range(1, max_depth + 1):
		if time.time() - start_time < time_limit:
			next_move = DLMMiniMax(player, depth, max_q_depth, start_time, time_limit, alpha, beta, history_table)
	return next_move


def DLMMiniMax(player, depth, q_depth, start_time, time_limit, alpha, beta, history_table):
	moves = player.get_all_moves()
	best_move = []
	best_eval = -9999.0
	updated_alpha = alpha
	updated_beta = beta
	for move in moves:
		pos_move = apply_move(player, move)
		max_eval = MinMove(pos_move, depth - 1, q_depth, start_time, time_limit, updated_alpha, updated_beta)
		if max_eval > best_eval:
			best_move = [move]
			best_eval = max_eval
		elif max_eval == best_eval:
			if len(best_move) > 0:
				best_move.append(move)
			else:
				best_move = [move]
		if max_eval >= updated_beta:
			return random.choice(best_move)
		elif max_eval <= updated_alpha:
			continue
		else:
			updated_alpha = max_eval
	return random.choice(best_move)


def MaxMove(player, depth, q_depth, start_time, time_limit, alpha, beta):
	if depth == 0 and (player.get_quietness() or q_depth == 0):
		return player.get_eval(player.color)
	else:
		best_score = -9999.0
		updated_alpha = alpha
		updated_beta = beta
		moves = player.get_all_moves()

		if len(moves) == 0:
			return player.get_eval(player.color)

		for move in moves:
			if time.time() - start_time >= time_limit:
				return best_score
			result_state = apply_move(player, move)
			if depth == 0:
				result_move = MinMove(result_state, depth, q_depth - 1, start_time, time_limit, updated_alpha, updated_beta)
			else:
				result_move = MinMove(result_state, depth - 1, q_depth, start_time, time_limit, updated_alpha, updated_beta)
			if result_move > best_score:
				best_score = result_move
			if result_move >= updated_beta:
				return best_score
			elif result_move <= updated_alpha:
				continue
			else:
				updated_alpha = result_move
		return best_score

def MinMove(player, depth, q_depth, start_time, time_limit, alpha, beta):
	if depth == 0 and (player.opponent.get_quietness() or q_depth == 0):
		return player.get_eval(player.opponent.color)
	else:
		best_score = 9999.0
		updated_alpha = alpha
		updated_beta = beta
		moves = player.opponent.get_all_moves() 
		
		if len(moves) == 0:
			return player.get_eval(player.opponent.color)

		for move in moves:
			if time.time() - start_time >= time_limit:
				return best_score
			result_state = apply_move(player, move, on_opponent=True)
			if depth == 0:
				result_move = MaxMove(result_state, depth, q_depth - 1, start_time, time_limit, updated_alpha, updated_beta)
			else:
				result_move = MaxMove(result_state, depth - 1, q_depth, start_time, time_limit, updated_alpha, updated_beta)
			if result_move < best_score:
				best_score = result_move
			if result_move <= updated_alpha:
				return best_score
			elif result_move >= updated_beta:
				continue
			else:
				updated_beta = result_move
		return best_score


def apply_move(player, move, on_opponent=False):
	new_player = copy_player_state(player)
	
	if on_opponent:
		piece_set = new_player.opponent.pieces
		opp_set = new_player.pieces
	else:
		piece_set = new_player.pieces
		opp_set = new_player.opponent.pieces
	
	# Find move.piece for new state
	for piece in piece_set:
		if piece.type == move.piece.type and piece.rank == move.piece.rank and piece.file == move.piece.file:
			move.piece = piece
			break

	if move.captured != None:
		for piece in opp_set:
			if piece.type == move.captured.type and piece.rank == move.captured.rank and piece.file == move.captured.file:
				move.captured = piece
				break

	# Check for castling
	if move.piece.type == "King":
		if ord(move.from_file) - ord(move.to_file) == 2:
			for r_piece in piece_set:
				if r_piece.type == "Rook":
					if r_piece.file == 'a':
						if on_opponent:
							new_player.opponent.move_piece(r_piece, 'd', r_piece.rank, "")
							del new_player.opponent.prev_moves[-1]
						else:
							new_player.move_piece(r_piece, 'd', r_piece.rank, "")
							del new_player.prev_moves[-1]
						break
		elif ord(move.to_file) - ord(move.from_file) == 2:
			for r_piece in piece_set:
				if r_piece.type == "Rook":
					if r_piece.file == 'h':
						if on_opponent:
							new_player.opponent.move_piece(r_piece, 'f', r_piece.rank, "")
							del new_player.opponent.prev_moves[-1]
						else:
							new_player.move_piece(r_piece, 'f', r_piece.rank, "")
							del new_player.prev_moves[-1]
						break
	# Actual Move
	if on_opponent:
		new_player.opponent.move_piece(move.piece, move.to_file, move.to_rank, move.promotion)
		while len(new_player.opponent.prev_moves) > 4:
			del new_player.opponent.prev_moves[0]
	else:
		new_player.move_piece(move.piece, move.to_file, move.to_rank, move.promotion)
		while len(new_player.prev_moves) > 4:
			del new_player.prev_moves[0]

	# Update turns to draw
	if move.captured != None or move.piece.type == "Pawn":
		new_player.turns_to_draw = 100
	else:
		new_player.turns_to_draw -= 1

	# Remove captured opponent piece
	if move.captured != None:
		captured_piece = move.captured
		for x in range(len(opp_set)):
			piece = opp_set[x]
			if piece.type == captured_piece.type and piece.rank == captured_piece.rank and piece.file == captured_piece.file:
				del opp_set[x]
				break

	# Update threat squares and if in check
	if on_opponent:
		new_player.update_threat_squares()
		new_player.in_check = new_player.get_check_status()
	else:
		new_player.opponent.update_threat_squares()
		new_player.opponent.in_check = new_player.opponent.get_check_status()

	# Update en passant target (for opponent)
	if move.piece.type == "Pawn":
		if abs(move.to_rank - move.from_rank) == 2:
			tar_file = move.to_file
			if on_opponent:
				tar_rank = move.to_rank - new_player.opponent.rank_direction
				new_player.en_passant_target = tar_file + str(tar_rank)
			else:
				tar_rank = move.to_rank - new_player.rank_direction
				new_player.opponent.en_passant_target = tar_file + str(tar_rank)

	# Update last move
	if on_opponent:
		new_player.opponent.last_move = move
	else:
		new_player.last_move = move

	return new_player


def copy_player_state(player):
	new_player = Chess_Player(player.color, player.name)
	opp_state = Chess_Player(player.opponent.color, player.opponent.name)
	new_player.in_check = player.in_check
	new_player.lost = player.lost
	new_player.turns_to_draw = player.turns_to_draw
	new_player.made_move = player.made_move
	new_player.rank_direction = player.rank_direction
	new_player.en_passant_target = player.en_passant_target
	new_player.pieces = [copy_piece(p, new_player) for p in player.pieces]
	new_player.threat_squares = {d:player.threat_squares[d] for d in player.threat_squares}
	new_player.prev_moves = [d.copy() for d in player.prev_moves]
	new_player.last_move = player.last_move
	
	opp_state.in_check = player.opponent.in_check
	opp_state.lost = player.opponent.lost
	opp_state.made_move = player.opponent.made_move
	opp_state.rank_direction = player.opponent.rank_direction
	opp_state.turns_to_draw = player.opponent.turns_to_draw
	opp_state.en_passant_target = player.en_passant_target
	opp_state.pieces = [copy_piece(p, opp_state) for p in player.opponent.pieces]
	opp_state.threat_squares = {d:player.opponent.threat_squares[d] for d in player.opponent.threat_squares}
	opp_state.prev_moves = [d.copy() for d in player.opponent.prev_moves]
	opp_state.last_move = player.opponent.last_move
	
	new_player.opponent = opp_state
	opp_state.opponent = new_player
	return new_player

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
		self.en_passant_target = ""
		self.threat_squares = {}
		self.turns_to_draw = 100
		self.prev_moves = []
		self.last_move = None

	def set_opponent(self, opponent):
		self.opponent = opponent

	def get_all_moves(self):
		all_moves = []
		for piece in self.pieces:
			possible_moves = self.get_moves_piece(piece)
			for move in possible_moves:
				all_moves.append(move)
		return all_moves

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

			# Check en passant target square
			if self.en_passant_target != "":
				if piece.rank + self.rank_direction == int(self.en_passant_target[1]) and abs(ord(piece.file) - ord(self.en_passant_target[0])) == 1:
					move = Chess_Move(piece, piece.file, piece.rank, self.en_passant_target[0], int(self.en_passant_target[1]), "")
					# Find opponent piece that was captured
					for opp_piece in self.opponent.pieces:
						if opp_piece.type == "Pawn":
							if opp_piece.file == self.en_passant_target[0] and opp_piece.rank - self.opponent.rank_direction == int(self.en_passant_target[1]):
								move.set_piece_captured(opp_piece)
								break
					possible_moves.append(move)
		elif piece.type == "Rook":
			self.find_verhor_moves(possible_moves, threat_search, piece)
		elif piece.type == "Knight":
			if ord(piece.file) - 1 > 96:
				if piece.rank - 2 > 0:
					can_move = self.analyze_move(possible_moves, threat_search, piece, chr(ord(piece.file) - 1), piece.rank - 2)
				if piece.rank + 2 < 9:
					can_move = self.analyze_move(possible_moves, threat_search, piece, chr(ord(piece.file) - 1), piece.rank + 2)
				if ord(piece.file) - 2 > 96:
					if piece.rank - 1 > 0:
						can_move = self.analyze_move(possible_moves, threat_search, piece, chr(ord(piece.file) - 2), piece.rank - 1)
					if piece.rank + 1 < 9:
						can_move = self.analyze_move(possible_moves, threat_search, piece, chr(ord(piece.file) - 2), piece.rank + 1)
			if ord(piece.file) + 1 < 105:
				if piece.rank - 2 > 0:
					can_move = self.analyze_move(possible_moves, threat_search, piece, chr(ord(piece.file) + 1), piece.rank - 2)
				if piece.rank + 2 < 9:
					can_move = self.analyze_move(possible_moves, threat_search, piece, chr(ord(piece.file) + 1), piece.rank + 2)
				if ord(piece.file) + 2 < 105:
					if piece.rank - 1 > 0:
						can_move = self.analyze_move(possible_moves, threat_search, piece, chr(ord(piece.file) + 2), piece.rank - 1)
					if piece.rank + 1 < 9:
						can_move = self.analyze_move(possible_moves, threat_search, piece, chr(ord(piece.file) + 2), piece.rank + 1)
		elif piece.type == "Bishop":
			self.find_diag_moves(possible_moves, threat_search, piece)
		elif piece.type == "Queen":
			self.find_diag_moves(possible_moves, threat_search, piece)
			self.find_verhor_moves(possible_moves, threat_search, piece)
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
			# Castling
			if not self.in_check:
				if not piece.has_moved:
					if self.color == "White":
						for rook_piece in self.pieces:
							if rook_piece.type == "Rook":
								if rook_piece.file == 'a' and rook_piece.rank == 1 and rook_piece.has_moved == False:
									if self.check_space('d', 1)[0] and self.check_space('c', 1)[0] and self.check_space('b', 1)[0]:
										if 'e1' not in self.threat_squares and 'd1' not in self.threat_squares and 'c1' not in self.threat_squares:
											# Castle on the left
											possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 2), piece.rank, ""))
								elif rook_piece.file == 'h' and rook_piece.rank == 1 and rook_piece.has_moved == False:
									if self.check_space('f', 1)[0] and self.check_space('g', 1)[0]:
										if 'e1' not in self.threat_squares and 'f1' not in self.threat_squares and 'g1' not in self.threat_squares:
											# Can castle on the right (e1, f1, g1)
											possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 2), piece.rank, ""))
					elif self.color == "Black":
						for rook_piece in self.pieces:
							if rook_piece.type == "Rook":
								if rook_piece.file == 'a' and rook_piece.rank == 8 and rook_piece.has_moved == False:
									if self.check_space('d', 8)[0] and self.check_space('c', 8)[0] and self.check_space('b', 8)[0]:
										if 'e8' not in self.threat_squares and 'd8' not in self.threat_squares and 'c8' not in self.threat_squares:
											# Castle on the left (e8, d8, c8)
											possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) - 2), piece.rank, ""))
								elif rook_piece.file == 'h' and rook_piece.rank == 8 and rook_piece.has_moved == False:
									if self.check_space('f', 8)[0] and self.check_space('g', 8)[0]:
										if 'e8' not in self.threat_squares and 'f8' not in self.threat_squares and 'g8' not in self.threat_squares:
											# Castle on the right (e8, f8, g8)
											possible_moves.append(Chess_Move(piece, piece.file, piece.rank, chr(ord(piece.file) + 2), piece.rank, ""))
		
		for piece in self.pieces:
			if piece.type == "King":
				king_piece = piece
				king_str = piece.file + str(piece.rank)
				break

		# Look through moves, if one puts King in check, it's not valid
		if not threat_search:
			for x in range(len(possible_moves) - 1, -1, -1):
				# Make move
				move = possible_moves[x]
				init_pos = move.piece.has_moved
				en_passant_save = self.en_passant_target
				self.move_piece(move.piece, move.to_file, move.to_rank, move.promotion)
				del self.prev_moves[-1]
				castling_origin = {}

				# If castling, move Rook piece as well
				if move.piece.type == "King":
					if ord(move.from_file) - ord(move.to_file) == 2:
						# Left-side castling, find rook to move as well
						for r_piece in self.pieces:
							if r_piece.type == "Rook":
								if r_piece.file == 'a':
									castling_origin["piece"] = r_piece
									castling_origin["file"] = r_piece.file
									castling_origin["rank"] = r_piece.rank
									self.move_piece(r_piece, 'd', r_piece.rank, "")
									del self.prev_moves[-1]
					elif ord(move.to_file) - ord(move.from_file) == 2:
						# Right side castling, find rook to move as well
						for r_piece in self.pieces:
							if r_piece.type == "Rook":
								if r_piece.file == 'h':
									castling_origin["piece"] = r_piece
									castling_origin["file"] = r_piece.file
									castling_origin["rank"] = r_piece.rank
									self.move_piece(r_piece, 'f', r_piece.rank, "")
									del self.prev_moves[-1]  

				# Remove captured piece
				captured_piece = None
				if move.captured != None:
					for i in range(len(self.opponent.pieces)):
						opp_piece = self.opponent.pieces[i]

						# Check if en passant
						if en_passant_save != "":
							if opp_piece.file == en_passant_save[0] and opp_piece.rank == int(en_passant_save[1]):
								captured_piece = move.captured
								del self.opponent.pieces[i]
								break

						# Regular capture
						if opp_piece.file == move.captured.file and opp_piece.rank == move.captured.rank:
							captured_piece = move.captured
							del self.opponent.pieces[i]
							break
				
				# Determine threatened squares
				king_str = king_piece.file + str(king_piece.rank)
				threats = self.get_opp_attacks()
				check_caused = king_str in threats

				# Undo move
				if move.promotion != "":
					if not init_pos:
						self.move_piece(move.piece, move.from_file, move.from_rank, "Undo", undo_has_moved=True)
					else:
						self.move_piece(move.piece, move.from_file, move.from_rank, "Undo")
				else:
					if not init_pos:
						self.move_piece(move.piece, move.from_file, move.from_rank, "", undo_has_moved=True)
					else:
						self.move_piece(move.piece, move.from_file, move.from_rank, "")
				
				del self.prev_moves[-1]
				# Undo Rook part of castling
				if len(castling_origin) != 0:
					self.move_piece(castling_origin["piece"], castling_origin["file"], castling_origin["rank"], "", undo_has_moved=True)
					del self.prev_moves[-1]

				# Replace any captured pieces
				if captured_piece != None:
					self.opponent.pieces.append(captured_piece)

				# Replace en_passant_target variable
				self.en_passant_target = en_passant_save

				# Fix prev_move array
				
				# Check if threat spaces include king space
				if check_caused:
					# Remove move from possible moves
					del possible_moves[x]
		
		return possible_moves

	def find_diag_moves(self, possible_moves, threat_search, piece):
		for x in range(1,9):
			if x + piece.rank < 9 and x + ord(piece.file) < 105:
				if not self.analyze_move(possible_moves, threat_search, piece, chr(ord(piece.file) + x), piece.rank + x):
					break
			else:
				break
		for x in range(1,9):
			if x + piece.rank < 9 and ord(piece.file) - x > 96:
				if not self.analyze_move(possible_moves, threat_search, piece, chr(ord(piece.file) - x), piece.rank + x):
					break
			else:
				break
		for x in range(1,9):
			if piece.rank - x > 0 and ord(piece.file) + x < 105:
				if not self.analyze_move(possible_moves, threat_search, piece, chr(ord(piece.file) + x), piece.rank - x):
					break
			else:
				break
		for x in range(1,9):
			if piece.rank - x > 0 and ord(piece.file) - x > 96:
				if not self.analyze_move(possible_moves, threat_search, piece, chr(ord(piece.file) - x), piece.rank - x):
					break
			else:
				break

	def find_verhor_moves(self, possible_moves, threat_search, piece):
		for rank in range(piece.rank + 1, 9):
			if not self.analyze_move(possible_moves, threat_search, piece, piece.file, rank):
				break
		for rank in range(piece.rank - 1, 0, -1):
			if not self.analyze_move(possible_moves, threat_search, piece, piece.file, rank):
				break
		for file in range(ord(piece.file) + 1, ord('h') + 1):
			if not self.analyze_move(possible_moves, threat_search, piece, chr(file), piece.rank):
				break
		for file in range(ord(piece.file) - 1, ord('a') - 1, -1):
			if not self.analyze_move(possible_moves, threat_search, piece, chr(file), piece.rank):
				break
			
	def analyze_move(self, possible_moves, threat_search, piece, file, rank):
		space = self.check_space(file, rank)
		if space[0]:
			possible_moves.append(Chess_Move(piece, piece.file, piece.rank, file, rank, ""))
			return True
		elif space[1] == 1:
			move = Chess_Move(piece, piece.file, piece.rank, file, rank, "")
			move.set_piece_captured(space[2])
			possible_moves.append(move)
			return False
		elif space[1] == 0 and threat_search:
			possible_moves.append(Chess_Move(piece, piece.file, piece.rank, file, rank, "", note="blocked"))
			return False
		else:
			return False

	def check_space(self, file, rank):
		for piece in self.pieces:
			if piece.rank == rank and piece.file == file:
				return (False, 0)
		for piece in self.opponent.pieces:
			if piece.rank == rank and piece.file == file:
				return (False, 1, piece)
		return (True, 0)

	def move_piece(self, piece, file, rank, promotion, undo_has_moved=False):
		self.prev_moves.append({"to_file": file, "to_rank": rank, "from_file": piece.file, "from_rank":piece.rank})
		if self.en_passant_target != "":
			self.en_passant_target = ""
		piece.move_piece(file, rank, promotion, undo_has_moved)

	def get_eval(self, player_color):
		points = 0

		# Return 0 for stalemate causing states
		if len(self.prev_moves) == len(self.opponent.prev_moves) and len(self.prev_moves) == 4:
			if self.prev_moves[0] == self.prev_moves[1] and self.prev_moves[2] == self.prev_moves[3]:
				if self.opponent.prev_moves[0] == self.opponent.prev_moves[1] and self.opponent.prev_moves[2] == self.opponent.prev_moves[3]:
					return 0

		if self.turns_to_draw == 0:
			return 0

		for p in self.pieces:
			if p.type == "Queen":
				if player_color == "White":
					if p.rank > 2:
						points += 13.5
					else:
						points += 9
				else:
					if p.rank < 7:
						points += 13.5
					else:
						points += 9
			elif p.type == "Rook":
				if player_color == "White":
					if p.rank > 2:
						points += 7.5
					else:
						points += 5
				else:
					if p.rank < 7:
						points += 7.5
					else:
						points += 5
			elif p.type == "Bishop" or p.type == "Knight":
				if player_color == "White":
					if p.rank > 2:
						points += 4.5
					else:
						points += 3
				else:
					if p.rank < 7:
						points += 4.5
					else:
						points += 3
			elif p.type == "Pawn":
				if player_color == "White":
					if p.rank > 2:
						points += 1.5
					else:
						points += 1
				else:
					if p.rank < 7:
						points += 1.5
					else:
						points += 1
		for p in self.opponent.pieces:
			if p.type == "Queen":
				if player_color == "White":
					if p.rank < 7:
						points -= 13.5
					else:
						points -= 9
				else:
					if p.rank > 2:
						points -= 13.5
					else:
						points -= 9
			elif p.type == "Rook":
				if player_color == "White":
					if p.rank < 7:
						points -= 7.5
					else:
						points -= 5
				else:
					if p.rank > 2:
						points -= 7.5
					else:
						points -= 5
			elif p.type == "Bishop" or p.type == "Knight":
				if player_color == "White":
					if p.rank < 7:
						points -= 4.5
					else:
						points -= 3
				else:
					if p.rank > 2:
						points -= 4.5
					else:
						points -= 3

			elif p.type == "Pawn":
				if player_color == "White":
					if p.rank < 7:
						points -= 1.5
					else:
						points -= 1
				else:
					if p.rank > 2:
						points -= 1.5
					else:
						points -= 1

		# Points for threatened squares
		points -= 0.25 * len(self.threat_squares)
		points += 0.25 * len(self.opponent.threat_squares)

		# Points for pieces being threatened and pieces threatened
		for piece in self.opponent.pieces:
			p_str = piece.file + str(piece.rank)
			if p_str in self.opponent.threat_squares:
				if piece.type == "King":
					threat_king = len(self.opponent.threat_squares[p_str])
					if threat_king < 2:
						points += 4
					elif threat_king >= 2:
						points += 50
				elif piece.type == "Queen":
					points += 4.5 * len(self.opponent.threat_squares[p_str])
				elif piece.type == "Rook":
					points += 2.5 * len(self.opponent.threat_squares[p_str])
				elif piece.type == "Bishop" or piece.type == "Rook":
					points += 1.5 * len(self.opponent.threat_squares[p_str])
				elif piece.type == "Pawn":
					points += 0.5 * len(self.opponent.threat_squares[p_str])
		for piece in self.pieces:
			p_str = piece.file + str(piece.rank)
			if p_str in self.threat_squares:
				if piece.type == "King":
					threat_king = len(self.threat_sqaures[p_str])
					if threat_king < 2:
						points -= 4
					elif threat_king >= 2:
						points -= 50
				elif piece.type == "Queen":
					points -= 4.5 * len(self.threat_squares[p_str])
				elif piece.type == "Rook":
					points -= 2.5 * len(self.threat_squares[p_str])
				elif piece.type == "Bishop" or piece.type == "Rook":
					points -= 1.5 * len(self.threat_squares[p_str])
				elif piece.type == "Pawn":
					points -= 0.5 * len(self.threat_squares[p_str])

		return points	

	def get_quietness(self):
		if self.opponent.last_move != None:
			if self.opponent.last_move.captured != None:
				return False
		return True

	def get_threat_squares(self):
		
		threats = {}
		for piece in self.opponent.pieces:
			piece_moves = self.opponent.get_moves_piece(piece, threat_search=True)
			for move in piece_moves:
				if piece.type != "Pawn":
					space_str = move.to_file + str(move.to_rank)
					if not space_str in threats:
						threats[space_str] = [piece]
					elif space_str in threats:
						threats[space_str].append(piece)
				elif piece.type == "Pawn":
					# IF move was diagonal
					if move.to_file != move.from_file and move.to_rank != move.from_rank:
						space_str = move.to_file + str(move.to_rank)
						if not space_str in threats:
							threats[space_str] = [piece]
						elif space_str in threats:
							threats[space_str].append(piece)

		return threats

	def get_opp_attacks(self):
		can_attack = {}
		for piece in self.opponent.pieces:
			if piece.type == "Pawn":
				# Just check diagonals
				if piece.file != 'h':
					space = self.check_space(chr(ord(piece.file) + 1), piece.rank + self.opponent.rank_direction)
					if space[1] == 1 or space[1] == 0:
						s_str = chr(ord(piece.file) + 1) + str(piece.rank + self.opponent.rank_direction)
						if not s_str in can_attack:
							can_attack[s_str] = [piece]
						elif s_str in can_attack:
							can_attack[s_str].append(piece)
				if piece.file != 'a':
					space = self.check_space(chr(ord(piece.file) - 1), piece.rank + self.opponent.rank_direction)
					if space[1] == 1 or space[1] == 0:
						s_str = chr(ord(piece.file) - 1) + str(piece.rank + self.opponent.rank_direction)
						if not s_str in can_attack:
							can_attack[s_str] = [piece]
						elif s_str in can_attack:
							can_attack[s_str].append(piece)

				# Check en passante maybe?
			elif piece.type == "Rook":
				for rank in range(piece.rank + 1, 9):
					if not self.analyze_threat(piece.file, rank, can_attack, piece):
						break
				for rank in range(piece.rank - 1, 0, -1):
					if not self.analyze_threat(piece.file, rank, can_attack, piece):
						break
				for file in range(ord(piece.file) + 1, ord('h') + 1):
					if not self.analyze_threat(chr(file), piece.rank, can_attack, piece):
						break
				for file in range(ord(piece.file) - 1, ord('a') - 1, -1):
					if not self.analyze_threat(chr(file), piece.rank, can_attack, piece):
						break
			elif piece.type == "Bishop":
				for x in range(1,9):
					if x + piece.rank < 9 and x + ord(piece.file) < 105:
						if not self.analyze_threat(chr(ord(piece.file) + x), piece.rank + x, can_attack, piece):
							break
					else:
						break
				for x in range(1,9):
					if x + piece.rank < 9 and ord(piece.file) - x > 96:
						if not self.analyze_threat(chr(ord(piece.file) - x), piece.rank + x, can_attack, piece):
							break
					else:
						break
				for x in range(1,9):
					if piece.rank - x > 0 and ord(piece.file) + x < 105:
						if not self.analyze_threat(chr(ord(piece.file) + x), piece.rank - x, can_attack, piece):
							break
					else:
						break
				for x in range(1,9):
					if piece.rank - x > 0 and ord(piece.file) - x > 96:
						if not self.analyze_threat(chr(ord(piece.file) - x), piece.rank - x, can_attack, piece):
							break
					else:
						break
			elif piece.type == "Queen":
				for x in range(1,9):
					if x + piece.rank < 9 and x + ord(piece.file) < 105:
						if not self.analyze_threat(chr(ord(piece.file) + x), piece.rank + x, can_attack, piece):
							break
					else:
						break
				for x in range(1,9):
					if x + piece.rank < 9 and ord(piece.file) - x > 96:
						if not self.analyze_threat(chr(ord(piece.file) - x), piece.rank + x, can_attack, piece):
							break
					else:
						break
				for x in range(1,9):
					if piece.rank - x > 0 and ord(piece.file) + x < 105:
						if not self.analyze_threat(chr(ord(piece.file) + x), piece.rank - x, can_attack, piece):
							break
					else:
						break
				for x in range(1,9):
					if piece.rank - x > 0 and ord(piece.file) - x > 96:
						if not self.analyze_threat(chr(ord(piece.file) - x), piece.rank - x, can_attack, piece):
							break
					else:
						break
				for rank in range(piece.rank + 1, 9):
					if not self.analyze_threat(piece.file, rank, can_attack, piece):
						break
				for rank in range(piece.rank - 1, 0, -1):
					if not self.analyze_threat(piece.file, rank, can_attack, piece):
						break
				for file in range(ord(piece.file) + 1, ord('h') + 1):
					if not self.analyze_threat(chr(file), piece.rank, can_attack, piece):
						break
				for file in range(ord(piece.file) - 1, ord('a') - 1, -1):
					if not self.analyze_threat(chr(file), piece.rank, can_attack, piece):
						break
			elif piece.type == "Knight":
				if ord(piece.file) - 1 > 96:
					if piece.rank - 2 > 0:
						s_str = chr(ord(piece.file) - 1) + str(piece.rank - 2)
						if s_str not in can_attack:
							can_attack[s_str] = [piece]
						elif s_str in can_attack:
							can_attack[s_str].append(piece)
					if piece.rank + 2 < 9:
						s_str = chr(ord(piece.file) - 1) + str(piece.rank + 2)
						if s_str not in can_attack:
							can_attack[s_str] = [piece]
						elif s_str in can_attack:
							can_attack[s_str].append(piece)
					if ord(piece.file) - 2 > 96:
						if piece.rank - 1 > 0:
							s_str = chr(ord(piece.file) - 2) + str(piece.rank - 1)
							if s_str not in can_attack:
								can_attack[s_str] = [piece]
							elif s_str in can_attack:
								can_attack[s_str].append(piece)
						if piece.rank + 1 < 9:
							s_str = chr(ord(piece.file) - 2) + str(piece.rank + 1)
							if s_str not in can_attack:
								can_attack[s_str] = [piece]
							elif s_str in can_attack:
								can_attack[s_str].append(piece)
				if ord(piece.file) + 1 < 105:
					if piece.rank - 2 > 0:
						s_str = chr(ord(piece.file) + 1) + str(piece.rank - 2)
						if s_str not in can_attack:
							can_attack[s_str] = [piece]
						elif s_str in can_attack:
							can_attack[s_str].append(piece)
					if piece.rank + 2 < 9:
						s_str = chr(ord(piece.file) + 1) + str(piece.rank + 2)
						if s_str not in can_attack:
							can_attack[s_str] = [piece]
						elif s_str in can_attack:
							can_attack[s_str].append(piece)
					if ord(piece.file) + 2 < 105:
						if piece.rank - 1 > 0:
							s_str = chr(ord(piece.file) + 2) + str(piece.rank - 1)
							if s_str not in can_attack:
								can_attack[s_str] = [piece]
							elif s_str in can_attack:
								can_attack[s_str].append(piece)
						if piece.rank + 1 < 9:
							s_str = chr(ord(piece.file) + 2) + str(piece.rank + 1)
							if s_str not in can_attack:
								can_attack[s_str] = [piece]
							elif s_str in can_attack:
								can_attack[s_str].append(piece)
			elif piece.type == "King":
				for rank in range(piece.rank - 1, piece.rank + 2):
					for file in range(ord(piece.file) - 1, ord(piece.file) + 2):
						if rank > 0 and rank < 9 and file > 96 and file < 105:
							if rank != piece.rank or chr(file) != piece.file:
								space_str = chr(file) + str(rank)
								if not space_str in self.threat_squares:
									if space_str not in can_attack:
										can_attack[space_str] = [piece]
									elif space_str in can_attack:
										can_attack[space_str].append(piece)
		return can_attack	

	def analyze_threat(self, file, rank, can_attack, piece):
		space = self.check_space(file, rank)
		s_str = file + str(rank)
		if not s_str in can_attack:
			can_attack[s_str] = [piece]
		elif s_str in can_attack:
			can_attack[s_str].append(piece)
		if space[0]:
			return True
		else:
			return False

	def update_threat_squares(self):
		self.threat_sqaures = self.get_opp_attacks()

	def get_check_status(self):
		king_str = ""
		for piece in self.pieces:
			if piece.type == "King":
				king_str = piece.file + str(piece.rank)
				return king_str in self.threat_squares

		# Should never get here
		return False