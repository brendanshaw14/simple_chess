from PIL import Image, ImageTk
import tkinter as tk
from piece import * 
# Move class for the simple chess game
# Author: Brendan Shaw, April 2023
#   The move class is functionally stores the minimax search tree with each of the game states stored as a board_dict
#   at each node. the node also holds a piece and a position, and an evaluation rating, which represents the value of
#   the board for that team's player given the pieces in board_dict

#CHOOSE DEPTH FOR MINIMAX HERE:
MAX_DEPTH = 3

class move_node: 

    def __init__(self, piece, position, piece_set, board_dict, team_color, depth): 
        #intialize the position and the piece of the current move
        self.piece = piece
        self.position = position
        #initialize the value of the move to 0 and declare the set of all possible moves from that point
        self.value = 0
        self.next_moves = set()
        self.depth = depth
        self.team_color = team_color
        self.piece_set = piece_set.copy()
        self.board_dict = board_dict.copy()
        self.worst_outcome = 1000

        #update the boarddict
        #if the node isn't the head node
        if self.piece is not None: 
            #empty that spot on the board_dict
            self.board_dict[self.piece.position] = None
            #put the piece in its new position in the board dict and handle capture
            if self.board_dict[self.position] is not None: 
                print("capture encountered")
                self.piece_set.remove(self.board_dict[self.position])
                self.board_dict[self.position] = None
            self.board_dict[self.position] = self.piece
        #set the value of the game state after the move
        self.value = self.getValue()          
        #initialize the next moves set
        #self.next_moves = self.piece.getMoves(self.piece, self.board_dict)
        #for each piece
        if depth <= MAX_DEPTH:
            for piece in self.piece_set:
                #if we are only getting black moves
                if depth % 2 == 0: 
                    if piece.color == "black":
                        for move in piece.getMoves(piece, self.board_dict):
                                indent = depth * "  "
                                new_node = move_node(piece, move, self.piece_set, self.board_dict, self.team_color, depth + 1)
                                self.next_moves.add(new_node)
                                print(indent + "node created: "+ piece.color + " " + piece.name + " to " + move + "; score: " + str(new_node.value))
                else:
                    if piece.color == "white":
                        for move in piece.getMoves(piece, self.board_dict):
                            if piece.color == "white":
                                indent = depth * "  "
                                new_node = move_node(piece, move, self.piece_set, self.board_dict, self.team_color, depth + 1)
                                self.next_moves.add(new_node)
                                print(indent + "node created: "+ piece.color + " " + piece.name + " to " + move + "; score: " + str(new_node.value))
 

    def getValue(self):
        value = 0
        #define piece values
        PAWN_VALUE = 10
        KNIGHT_VALUE = 30
        BISHOP_VALUE = 30
        ROOK_VALUE = 50
        QUEEN_VALUE = 90 
        KING_VALUE = 900
        for piece in self.piece_set: 
            #get moves if it's a pawn
            if piece.name == "new_pawn" or piece.name == "pawn":
                if piece.color == self.team_color: 
                    value += PAWN_VALUE
                else: 
                    value -= PAWN_VALUE
            #get moves if it's a knight
            if piece.name == "knight":
                if piece.color == self.team_color: 
                    value += KNIGHT_VALUE
                else: 
                    value -= KNIGHT_VALUE
            #get moves if it's a bishop
            if piece.name == "bishop":
                if piece.color == self.team_color: 
                    value += BISHOP_VALUE
                else: 
                    value -= BISHOP_VALUE
            #get moves if it's a bishop
            if piece.name == "rook":
                if piece.color == self.team_color: 
                    value += ROOK_VALUE
                else: 
                    value -= ROOK_VALUE
            #get moves if it's a queen
            if piece.name == "queen":
                if piece.color == self.team_color: 
                    value += QUEEN_VALUE
                else: 
                    value -= QUEEN_VALUE
            #get moves if it's a king
            if piece.name == "king":
                if piece.color == self.team_color: 
                    value += KING_VALUE
                else: 
                    value -= KING_VALUE
        return value

    def print(self):
        print("printing move:")
        print("name:" + self.piece.name)
        print("position: " + self.position)
        print("board value: " + str(self.value))

    def getWorstOutcome(self):
        current_worst = 1000
        for move in self.next_moves: 
            if move.getValue() < current_worst:
                current_worst = move.getValue()
        return current_worst

    def minimax(self):
        #base case- return the current node if it has no children
        if self.next_moves == set():
            return self
        #if nodes team is different or the head node: return the child with max value
        elif self.piece == None or self.piece.color != self.team_color:
            max_value = -1290
            for move in self.next_moves: 
                next_minimax = move.minimax()
                if next_minimax.value >= max_value: 
                    max_value = next_minimax.value
                    best_move = move
            print("best value returned: " + str(best_move.value))
            return best_move
        #if nodes team is the opponent, return the child with min value
        else:
            min_value = 1290
            for move in self.next_moves: 
                next_minimax = move.minimax()
                if next_minimax.value <= min_value: 
                    min_value = next_minimax.value
                    worst_move = move
            print("worst value returned: "+ str(worst_move.value))
            return worst_move
            
                
        
