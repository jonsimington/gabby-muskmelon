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
		# self.current_player = None
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
		elif color == "Black":
			self.player = player_2
		
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
					file_offset += int(fen_data[i][j])

		if fen_data[8] == 'w':
			self.current_player = player_1
		else:
			self.current_player = player_2