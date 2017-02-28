# This is where you build your AI for the Chess game.

from joueur.base_ai import BaseAI
import random

from Piece import Chess_Piece
from Player import Chess_Player
from Game import Chess_Game


class AI(BaseAI):
    """ The basic AI functions that are the same between games. """

    def get_name(self):
        """ This is the name you send to the server so your AI will control the
        player named this string.

        Returns
            str: The name of your Player.
        """

        return "pawnsftw-patrick_bremehr"  # REPLACE THIS WITH YOUR TEAM NAME

    def start(self):
        """ This is called once the game starts and your AI knows its playerID
        and game. You can initialize your AI here.
        """
        self.game_obj = Chess_Game()
        self.game_obj.read_fen(self.game.fen, self.player.color)


        # replace with your start logic

    def game_updated(self):
        """ This is called every time the game's state updates, so if you are
        tracking anything you can update it here.
        """
        self.game_obj.player.opponent.pieces = self.player.opponent.pieces
        #self.game_obj.player.pieces = self.player.pieces
        self.game_obj.player.in_check = self.player.in_check

        # Check if a piece was captured
        if len(self.game.moves) > 0 and self.game.current_player == self.player:
            capture_move = self.game.moves[-1]
            captured_piece = capture_move.captured
            if captured_piece != None:
                # Find and Remove piece from our list
                for piece in self.game_obj.player.pieces:
                    if piece.type == captured_piece.type and piece.file == capture_move.to_file and piece.rank == capture_move.to_rank:
                        self.game_obj.player.pieces[:] = [p for p in self.game_obj.player.pieces if not (p.file == capture_move.to_file and p.rank == capture_move.to_rank)]
        



        self.game_obj.player.update_threat_squares()


    def end(self, won, reason):
        """ This is called when the game ends, you can clean up your data and
        dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why you won or
                          lost.
        """

        # replace with your end logic

    def run_turn(self):
        """ This is called every time it is this AI.player's turn.

        Returns:
            bool: Represents if you want to end your turn. True means end your
                  turn, False means to keep your turn going and re-call this
                  function.
        """

        # Here is where you'll want to code your AI.

        # 1)print the board to the console
        self.print_current_board()
        
        #print("Threat Squares")
        #for k in self.game_obj.player.get_threat_squares():
        #    print(k)

        # 2) print the opponent's last move to the console
        last_move = None
        if len(self.game.moves) > 0:
            print("Opponent's Last Move: '" + self.game.moves[-1].san + "'")
            last_move = self.game.moves[-1]

        # 3) print how much time remaining this AI has to calculate moves
        print("Time Remaining: " + str(self.player.time_remaining) + " ns")

        # 4) make a random valid move.
        moves = []
        pieces_checked = []
        index = 0

        while len(moves) == 0:
            random_piece = random.choice(self.game_obj.player.pieces)
            while random_piece in pieces_checked and index < len(self.game_obj.player.pieces):
                random_piece = random.choice(self.game_obj.player.pieces)
            pieces_checked.append(random_piece)
            index += 1
            moves = self.game_obj.player.get_moves_piece(random_piece, last_move)
        
        random_move = random.choice(moves)

        # Find Framework Game Piece to Move
        for piece in self.player.pieces:
            #print(piece.type, piece.file, str(piece.rank))
            if piece.type != random_piece.type:
                continue
            if piece.rank != random_piece.rank:
                continue
            if piece.file != random_piece.file:
                continue
            if random_move.promotion != "":
                piece.move(random_move.to_file, random_move.to_rank, random_move.promotion)
            else:
                piece.move(random_move.to_file, random_move.to_rank)
            break

        # Check for castling
        if random_move.piece.type == "King":
            if ord(random_move.from_file) - ord(random_move.to_file) == 2:
                # Left-side castling, find rook to move as well
                for r_piece in self.game_obj.player.pieces:
                    if r_piece.type == "Rook":
                        if r_piece.file == 'a':
                            self.game_obj.player.move_piece(r_piece, 'd', r_piece.rank, "")
            elif ord(random_move.to_file) - ord(random_move.from_file) == 2:
                # Right side castling, find rook to move as well
                for r_piece in self.game_obj.player.pieces:
                    if r_piece.type == "Rook":
                        if r_piece.file == 'h':
                            self.game_obj.player.move_piece(r_piece, 'f', r_piece.rank, "")
        self.game_obj.player.move_piece(random_piece, random_move.to_file, random_move.to_rank, random_move.promotion)

        return True  # to signify we are done with our turn.

    def print_current_board(self):
        """Prints the current board using pretty ASCII art
        Note: you can delete this function if you wish
        """

        # iterate through the range in reverse order
        for r in range(9, -2, -1):
            output = ""
            if r == 9 or r == 0:
                # then the top or bottom of the board
                output = "   +------------------------+"
            elif r == -1:
                # then show the ranks
                output = "     a  b  c  d  e  f  g  h"
            else:  # board
                output = " " + str(r) + " |"
                # fill in all the files with pieces at the current rank
                for file_offset in range(0, 8):
                    # start at a, with with file offset increasing the char
                    f = chr(ord("a") + file_offset)
                    current_piece = None
                    for piece in self.game.pieces:
                        if piece.file == f and piece.rank == r:
                            # then we found the piece at (file, rank)
                            current_piece = piece
                            break

                    code = "."  # default "no piece"
                    if current_piece:
                        # the code will be the first character of their type
                        # e.g. 'Q' for "Queen"
                        code = current_piece.type[0]

                        if current_piece.type == "Knight":
                            # 'K' is for "King", we use 'N' for "Knights"
                            code = "N"

                        if current_piece.owner.id == "1":
                            # the second player (black) is lower case.
                            # Otherwise it's uppercase already
                            code = code.lower()

                    output += " " + code + " "

                output += "|"
            print(output)
