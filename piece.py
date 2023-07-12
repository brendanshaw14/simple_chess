from PIL import Image, ImageTk
import tkinter as tk

class piece: 
    def __init__(self, name, color, position, image_path): 
        #initialize name, color, and position
        self.name = name
        self.color = color
        self.position = position
        #convert image to tk object and initialize
        image = Image.open(image_path)
        resized_image = image.resize((55, 55))
        self.image = ImageTk.PhotoImage(resized_image)



    def getTranslation(self, current_pos, move_x, move_y):
        new_x = ord(current_pos[0]) - ord('a') + move_x + 1
        new_y = int(current_pos[1]) + move_y
        if (new_x) < 1 or (new_x) > 8:
            return None
        elif (new_y) < 1 or (new_y) > 8:
            return None 
        else: 
            return chr(ord('a') + new_x - 1) + str(new_y)

    #retreives the possible moves of a piece
    def getMoves(self, piece, board_dict): 
        possibleMoves = None
        #get moves if it's a pawn
        if piece.name == "new_pawn" or piece.name == "pawn":
            possibleMoves = self.pawnMoves(piece, board_dict)
        #get moves if it's a knight
        if piece.name == "knight":
            possibleMoves = self.knightMoves(piece, board_dict) 
        #get moves if it's a bishop
        if piece.name == "bishop":
            possibleMoves = self.bishopMoves(piece, board_dict) 
        #get moves if it's a bishop
        if piece.name == "rook":
            possibleMoves = self.rookMoves(piece, board_dict) 
        #get moves if it's a queen
        if piece.name == "queen":
            possibleMoves = self.queenMoves(piece, board_dict)
        #get moves if it's a king
        if piece.name == "king":
            possibleMoves = self.kingMoves(piece, board_dict)
        return possibleMoves 

    #returns the set of possible moves for the given pawn        
    def pawnMoves(self, piece, board_dict):
        possibleMoves = set()
        if piece.color == "white":
            #get the translations
            forward = self.getTranslation(piece.position, 0, -1)
            forward_2 = self.getTranslation(piece.position, 0, -2)
            diag_right = self.getTranslation(piece.position, 1, -1) 
            diag_left = self.getTranslation(piece.position, -1, -1) 
        else:
            #get the translations
            forward = self.getTranslation(piece.position, 0, 1)
            forward_2 = self.getTranslation(piece.position, 0, 2)
            diag_right = self.getTranslation(piece.position, 1, 1) 
            diag_left = self.getTranslation(piece.position, -1, 1) 
        #check forward1 
        if forward in board_dict and board_dict[forward] is None:
            possibleMoves.add(forward)
        if piece.name == "new_pawn":
            #check forward_2 
            if forward_2 in board_dict and board_dict[forward_2] is None:
                possibleMoves.add(forward_2)
        #check diag_right
        if diag_right in board_dict and board_dict[diag_right] is not None: 
            if board_dict[diag_right].color != piece.color:
                possibleMoves.add(diag_right)
        #check diag_left
        if diag_left in board_dict and board_dict[diag_left] is not None:  
            if board_dict[diag_left].color != piece.color:
                possibleMoves.add(diag_left)
        return possibleMoves

    #returns the set of possible moves for the given knight 
    def knightMoves(self, piece, board_dict): 
        possible_moves = set()
        translations = set()
        #loop through the translations
        for i in range(-2, 3):
            if i == 2 or i == -2: 
                translations.add(self.getTranslation(piece.position, i, 1))
                translations.add(self.getTranslation(piece.position, i, -1))
            if i == 1 or i == -1: 
                translations.add(self.getTranslation(piece.position, i, 2))
                translations.add(self.getTranslation(piece.position, i, -2))
        for move in translations:
            if move in board_dict:
                if board_dict[move] is None:
                    possible_moves.add(move)
                if board_dict[move] is not None and board_dict[move].color != piece.color:
                    possible_moves.add(move)
        return possible_moves

    #returns the set of possible moves for the given bishop
    def bishopMoves(self, piece, board_dict):
        possible_moves = set()
        #up right moves
        for i in range(1, 9):
            translation = self.getTranslation(piece.position, i, i)
            #don't add if not a valid square
            if translation not in board_dict:
                break
            #if a piece is there already
            elif board_dict[translation] is not None: 
                #if the color is the same, break.
                if board_dict[translation].color == piece.color:
                    break
                #if the color is different, allow move but break
                else: 
                    possible_moves.add(translation)
                    break
            #if the squre is empty
            else: 
                possible_moves.add(translation)
        #down right moves
        for i in range(1, 9):
            translation = self.getTranslation(piece.position, i, -i)
            #don't add if not a valid square
            if translation not in board_dict:
                break
            #if a piece is there already
            elif board_dict[translation] is not None: 
                #if the color is the same, break.
                if board_dict[translation].color == piece.color:
                    break
                #if the color is different, allow move but break
                else: 
                    possible_moves.add(translation)
                    break
            #if the squre is empty
            else: 
                possible_moves.add(translation)
        #down left moves
        for i in range(1, 9):
            translation = self.getTranslation(piece.position, -i, i)
            #don't add if not a valid square
            if translation not in board_dict:
                break
            #if a piece is there already
            elif board_dict[translation] is not None: 
                #if the color is the same, break.
                if board_dict[translation].color == piece.color:
                    break
                #if the color is different, allow move but break
                else: 
                    possible_moves.add(translation)
                    break
            #if the squre is empty
            else:
                possible_moves.add(translation)
        #up left moves
        for i in range(1, 9):
            translation = self.getTranslation(piece.position, -i, -i)
            #don't add if not a valid square
            if translation not in board_dict:
                break
            #if a piece is there already
            elif board_dict[translation] is not None: 
                #if the color is the same, break.
                if board_dict[translation].color == piece.color:
                    break
                #if the color is different, allow move but break
                else: 
                    possible_moves.add(translation)
                    break
            #if the squre is empty
            else: 
                possible_moves.add(translation)
        return possible_moves
    
    #returns the set of possible moves for the given rook                            
    def rookMoves(self, piece, board_dict):
        possible_moves = set()
        #down moves
        for i in range(1, 9):
            translation = self.getTranslation(piece.position, 0, -i)
            #don't add if not a valid square
            if translation not in board_dict:
                break
            #if a piece is there already
            elif board_dict[translation] is not None: 
                #if the color is the same, break.
                if board_dict[translation].color == piece.color:
                    break
                #if the color is different, allow move but break
                else: 
                    possible_moves.add(translation)
                    break
            #if the squre is empty
            else: 
                possible_moves.add(translation)
        #down moves
        for i in range(1, 9):
            translation = self.getTranslation(piece.position, 0, i)
            #don't add if not a valid square
            if translation not in board_dict:
                break
            #if a piece is there already
            elif board_dict[translation] is not None: 
                #if the color is the same, break.
                if board_dict[translation].color == piece.color:
                    break
                #if the color is different, allow move but break
                else: 
                    possible_moves.add(translation)
                    break
            #if the squre is empty
            else: 
                possible_moves.add(translation)
        #left moves
        for i in range(1, 9):
            translation = self.getTranslation(piece.position, -i, 0)
            #don't add if not a valid square
            if translation not in board_dict:
                break
            #if a piece is there already
            elif board_dict[translation] is not None: 
                #if the color is the same, break.
                if board_dict[translation].color == piece.color:
                    break
                #if the color is different, allow move but break
                else: 
                    possible_moves.add(translation)
                    break
            #if the squre is empty
            else:
                possible_moves.add(translation)
        #right moves
        for i in range(1, 9):
            translation = self.getTranslation(piece.position, i, 0)
            #don't add if not a valid square
            if translation not in board_dict:
                break
            #if a piece is there already
            elif board_dict[translation] is not None: 
                #if the color is the same, break.
                if board_dict[translation].color == piece.color:
                    break
                #if the color is different, allow move but break
                else: 
                    possible_moves.add(translation)
                    break
            #if the squre is empty
            else: 
                possible_moves.add(translation)
        return possible_moves 

    #returns the set of possible moves for the given queen 
    def queenMoves(self, piece, board_dict):
        return self.bishopMoves(piece, board_dict) | self.rookMoves(piece, board_dict)

    #returns the set of possible moves for the given king
    def kingMoves(self, piece, board_dict): 
        translations = set()
        possible_moves = set()
        #get all the one square moves
        translations.add(self.getTranslation(piece.position, -1, -1))
        translations.add(self.getTranslation(piece.position, -1, 0))
        translations.add(self.getTranslation(piece.position, -1, 1))
        translations.add(self.getTranslation(piece.position, 1, -1))
        translations.add(self.getTranslation(piece.position, 1, 0))
        translations.add(self.getTranslation(piece.position, 1, 1))
        translations.add(self.getTranslation(piece.position, 0, -1))
        translations.add(self.getTranslation(piece.position, 0, 1))
        #validate the moves
        for move in translations:
            if move in board_dict:
                if board_dict[move] is None:
                    possible_moves.add(move)
                if board_dict[move] is not None and board_dict[move].color != piece.color:
                    possible_moves.add(move)
        return possible_moves

