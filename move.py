from PIL import Image, ImageTk
import tkinter as tk
from piece import * 
# Move class for the simple chess game
# Author: Brendan Shaw, April 2023
#   The move class is functionally stores the minimax search tree with each of the game states stored as a board_dict
#   at each node. the node also holds a piece and a position, and an evaluation rating, which represents the value of
#   the board for that team's player given the pieces in board_dict

class move: 
    def __init__(self, piece, position, piece_set, board_dict, depth): 
        #intialize the position and the piece of the current move
        self.piece = piece
        self.position = position
        #initialize the value of the move to 0 and declare the set of all possible moves from that point
        self.value = 0
        self.nextmoves = set()
        self.depth = depth
        #initialize the next moves set
        #for piece in piece_set: 
   
    def getValue(self, piece_set, team_color):
        value = 0
        #define piece values
        PAWN_VALUE = 10
        KNIGHT_VALUE = 30
        BISHOP_VALUE = 30
        ROOK_VALUE = 50
        QUEEN_VALUE = 90 
        KING_VALUE = 900
        for piece in piece_set: 
            #get moves if it's a pawn
            if piece.name == "new_pawn" or piece.name == "pawn":
                if piece.color == team_color: 
                    value += PAWN_VALUE
                else: 
                    value -= PAWN_VALUE
            #get moves if it's a knight
            if piece.name == "knight":
                if piece.color == team_color: 
                    value += KNIGHT_VALUE
                else: 
                    value -= KNIGHT_VALUE
            #get moves if it's a bishop
            if piece.name == "bishop":
                if piece.color == team_color: 
                    value += BISHOP_VALUE
                else: 
                    value -= BISHOP_VALUE
            #get moves if it's a bishop
            if piece.name == "rook":
                if piece.color == team_color: 
                    value += ROOK_VALUE
                else: 
                    value -= ROOK_VALUE
            #get moves if it's a queen
            if piece.name == "queen":
                if piece.color == team_color: 
                    value += QUEEN_VALUE
                else: 
                    value -= QUEEN_VALUE
            #get moves if it's a king
            if piece.name == "king":
                if piece.color == team_color: 
                    value += KING_VALUE
                else: 
                    value -= KING_VALUE
            return value