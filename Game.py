# Patrick Bremehr
# Game class

import copy
import re
from Player import Chess_Player
from Piece import Chess_Piece

class Chess_Game:
	def __init__(self):
		self.moves = []
		self.pieces = []
		self.current_turn = 0
		self.fen = ""
		self.player = None

	def read_fen(self, fen_str, color):
		self.fen = fen_str
		fen_data = re.split(' |/', fen_str)
		player_1 = Chess_Player("White", "Player 1")
		player_2 = Chess_Player("Black", "Player 2")
		player_1.set_opponent(player_2)
		player_2.set_opponent(player_1)
		if color == "White":
			self.player = player_1
			if fen_data[8] == 'w':
				if fen_data[10] != '-':
					self.player.en_passant_target = fen_data[10]
		elif color == "Black":
			self.player = player_2
			if fen_data[8] == 'b':
				if fen_data[10] != '-':
					self.player.en_passant_target = fen_data[10]

		files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
		for i in range(8):
			file_offset = 0
			for j in range(len(fen_data[i])):
				if not fen_data[i][j].isdigit():
					piece_type = fen_data[i][j].upper()
					if piece_type == 'Q':
						p_type = "Queen"
					elif piece_type == 'K':
						p_type = "King"
					elif piece_type == 'N':
						p_type = "Knight"
					elif piece_type == 'R':
						p_type = "Rook"
					elif piece_type == 'B':
						p_type = "Bishop"
					elif piece_type == 'P':
						p_type = "Pawn"

					if fen_data[i][j].isupper():
						piece = Chess_Piece(files[j+file_offset], 8 - i, player_1, p_type)
						player_1.pieces.append(piece)
					else:
						piece = Chess_Piece(files[j+file_offset], 8 - i, player_2, p_type)
						player_2.pieces.append(piece)

					self.pieces.append(piece)
				else:
					file_offset += int(fen_data[i][j]) - 1

		if color == 'White':
			relevant = [letter for letter in fen_data[9] if letter.isupper()]
			foundQ = 'Q' in relevant
			foundK = 'K' in relevant
		elif color == 'Black':
			relevant = [letter for letter in fen_data[9] if letter.islower()]
			foundQ = 'q' in relevant
			foundK = 'k' in relevant
		if not foundQ and not foundK:
			# Find King piece and mark it has moved
			for piece in self.player.pieces:
				if piece.type == "King":
					piece.has_moved = True
					break
		elif foundK and not foundQ:
			# King and kingside rook hasn't moved, find rook that isn't kingside
			for piece in [p for p in self.player.pieces if piece.type == "Rook"]:
				if not (piece.file == 'h' and piece.rank == 1):
					piece.has_moved = True
		elif foundQ and not foundK:
			# King and queenside rook hasn't moved, find rook that isn't queenside
			for piece in [p for p in self.player.pieces if piece.type == "Rook"]:
				if not (piece.file == 'a' and piece.rank == 1):
					piece.has_moved = True	