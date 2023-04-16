import tkinter as tk
from PIL import Image, ImageTk
from piece import piece
#from move import move



class board:
    # Create a dictionary of color codes for the board board squares
    COLORS = {
        'dark': '#164675', 
        'light': '#e9f0f7'
    }
    # Define constants
    BOARD_WIDTH = 480
    BOARD_HEIGHT = 480
    SQUARE_SIZE = BOARD_WIDTH // 8
    #define piece values
    PAWN_VALUE = 10
    KNIGHT_VALUE = 30
    BISHOP_VALUE = 30
    ROOK_VALUE = 50
    QUEEN_VALUE = 90 
    KING_VALUE = 900
   
    def __init__(self):
        # Create the main window
        root = tk.Tk()
        root.title('Chess Board')
        #declare the piece sets and starting side
        self.player_white = True 
        self.piece_set = set()
        self.board_dict = {}
        #important info
        self.piece_selected = None
        self.turn = "white"
        # Create the canvas to draw the board on
        self.canvas = tk.Canvas(root, width=self.BOARD_WIDTH, height=self.BOARD_HEIGHT)
        self.canvas.pack()
        #initialize button
        self.canvas.bind("<Button-1>", self.handleLeftClick)
        #print and initialize
        self.initializePieces()
        self.initializeBoardDict()
        self.drawBoard()
        # Start the main event loop
        root.mainloop()
    
    # Draw the board
    def drawBoard(self): 
        for row in range(8):
            for col in range(8):
                x1 = col * board.SQUARE_SIZE
                y1 = row * board.SQUARE_SIZE
                x2 = x1 + board.SQUARE_SIZE
                y2 = y1 + board.SQUARE_SIZE
                if (row + col) % 2 == 0:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=board.COLORS['light'])
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=board.COLORS['dark'])
        self.drawPieces()

    ##initialize pieces (side will always be white until code revised)
    def initializePieces(self):
        #add the top pawns
            for i in range(ord('a'), ord('h')+1):
                letter = chr(i) 
                position = letter + "2"
                self.piece_set.add(piece("new_pawn", "black", position, "piece images/bP.png"))
        #add the rooks
            self.piece_set.add(piece("rook", "black", "a1", "piece images/bR.png"))
            self.piece_set.add(piece("rook", "black", "h1", "piece images/bR.png"))
        #add the knights
            self.piece_set.add(piece("knight", "black", "b1", "piece images/bN.png"))
            self.piece_set.add(piece("knight", "black", "g1", "piece images/bN.png"))
        #add the bishops
            self.piece_set.add(piece("bishop", "black", "c1", "piece images/bB.png"))
            self.piece_set.add(piece("bishop", "black", "f1", "piece images/bB.png"))
        #add the queen
            self.piece_set.add(piece("queen", "black", "d1", "piece images/bQ.png"))
        #add the king
            self.piece_set.add(piece("king", "black", "e1", "piece images/bK.png"))

        #add the bottom pawns
            for i in range(ord('a'), ord('h')+1):
                letter = chr(i) 
                position = letter + "7"
                self.piece_set.add(piece("new_pawn", "white", position, "piece images/wP.png"))
        #add the rooks
            self.piece_set.add(piece("rook", "white", "a8", "piece images/wR.png"))
            self.piece_set.add(piece("rook", "white", "h8", "piece images/wR.png"))
        #add the knights
            self.piece_set.add(piece("knight", "white", "b8", "piece images/wN.png"))
            self.piece_set.add(piece("knight", "white", "g8", "piece images/wN.png"))
        #add the bishops
            self.piece_set.add(piece("bishop", "white", "c8", "piece images/wB.png"))
            self.piece_set.add(piece("bishop", "white", "f8", "piece images/wB.png"))
        #add the queen
            self.piece_set.add(piece("queen", "white", "d8", "piece images/wQ.png"))
        #add the king
            self.piece_set.add(piece("king", "white", "e8", "piece images/wK.png"))

    #initializes a dictionary representing each square on the board and if there is a piece in it        
    def initializeBoardDict(self):
        for i in range(ord('a'), ord('h')+1):
            for j in range(8):
                position = chr(i) + str(j+1)
                self.board_dict[position] = None
        for piece in self.piece_set:
            self.board_dict[piece.position] = piece

    #draws the piece to the board at its stored position
    def drawPieces(self):
        for piece in self.piece_set:
            piece_x = board.SQUARE_SIZE * (8 - (ord('h') - ord(piece.position[0]))) - 30
            piece_y = int(piece.position[1]) * board.SQUARE_SIZE - 30 
            self.canvas.create_image(piece_x, piece_y, image = piece.image)

    #converts the x coordinate to an int
    def convertX(self, old_x):
        return ord(old_x) - ord('a') + 1 

    #handles the left click 
    def handleLeftClick(self, event):
        #find the position that was clicked
        mouse_x = event.x
        mouse_y = event.y
        click_position = chr(ord('a') + int(mouse_x/board.SQUARE_SIZE)) + str(int(mouse_y/board.SQUARE_SIZE)+1)
        #if there was no piece selected, select the current piece
        if self.piece_selected is None and self.board_dict[click_position] is not None:
            #check if the right color is being selected
            print(self.turn)
            if self.turn == self.board_dict[click_position].color: 
                #set piece_selected to the piece at the position clicked on the board
                self.piece_selected = self.board_dict[click_position]
            
                print("piece was selected: position " + click_position)
        else: 
            #if the same piece was clicked twice, unselect the piece
            if self.piece_selected == self.board_dict[click_position]:
                self.piece_selected = None
                print("piece was unselected")
            else: 
                print("move to " + click_position + " attempted")
                #if a new spot was selected
                #verify that move was valid
                possibleMoves = self.getMoves(self.piece_selected)
                print("possible moves received by the handle function:")
                print(possibleMoves)
                if possibleMoves is not None:  
                    print(possibleMoves)
                    for move in possibleMoves:
                        if move == click_position:
                            self.handleMove(self.piece_selected, click_position)
                            self.piece_selected = None
                            break
                    self.piece_selected = None
                else: 
                    print("here")
                    self.piece_selected = None

    #move helper function 
    def handleMove(self, piece_selected, click_position):
        #check if it is a new pawn and change
        if piece_selected.name == "new_pawn":
            piece_selected.name = "pawn"
        #check for capture
        if self.board_dict[click_position] is not None: 
            self.handleCapture(self.board_dict[click_position])
        #set the pieces position to the clicked spot, empty the old spot, then update the board dict
        self.board_dict[piece_selected.position] = None
        piece_selected.position = click_position
        self.board_dict[click_position] = piece_selected
        #redraw the board
        if self.turn == "white":
            print("turn changed to black")
            self.turn = "black"
        else: 
            print("turn changed to white")
            self.turn = "white"
        #update board
        self.drawBoard()
        self.drawPieces()

    #captures the given piece, removing it from the board and from the piece array
    def handleCapture(self, piece):
        self.board_dict[piece.position] = None
        self.piece_set.remove(piece)

    #returns the translated square relative to the input position and the movement parameters, None if invalid move. 
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
    def getMoves(self, piece): 
        possibleMoves = None
        print(piece.name)
        #get moves if it's a pawn
        if piece.name == "new_pawn" or piece.name == "pawn":
            possibleMoves = self.pawnMoves(piece)
        #get moves if it's a knight
        if piece.name == "knight":
            possibleMoves = self.knightMoves(piece) 
        #get moves if it's a bishop
        if piece.name == "bishop":
            possibleMoves = self.bishopMoves(piece) 
        #get moves if it's a bishop
        if piece.name == "rook":
            possibleMoves = self.rookMoves(piece) 
        #get moves if it's a queen
        if piece.name == "queen":
            possibleMoves = self.queenMoves(piece)
        #get moves if it's a king
        if piece.name == "king":
            possibleMoves = self.kingMoves(piece)
        return possibleMoves 

    #returns the set of possible moves for the given pawn        
    def pawnMoves(self, piece):
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
        if forward in self.board_dict and self.board_dict[forward] is None:
            possibleMoves.add(forward)
        if piece.name == "new_pawn":
            #check forward_2 
            if forward_2 in self.board_dict and self.board_dict[forward_2] is None:
                possibleMoves.add(forward_2)
        #check diag_right
        if diag_right in self.board_dict and self.board_dict[diag_right] is not None: 
            if self.board_dict[diag_right].color != piece.color:
                possibleMoves.add(diag_right)
        #check diag_left
        if diag_left in self.board_dict and self.board_dict[diag_left] is not None:  
            if self.board_dict[diag_left].color != piece.color:
                possibleMoves.add(diag_left)
        return possibleMoves

    #returns the set of possible moves for the given knight 
    def knightMoves(self, piece): 
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
        print(translations)
        for move in translations:
            if move in self.board_dict:
                if self.board_dict[move] is None:
                    possible_moves.add(move)
                if self.board_dict[move] is not None and self.board_dict[move].color != piece.color:
                    possible_moves.add(move)
        return possible_moves

    #returns the set of possible moves for the given bishop
    def bishopMoves(self, piece):
        possible_moves = set()
        #up right moves
        for i in range(1, 9):
            translation = self.getTranslation(piece.position, i, i)
            print("testing translation: " + str(translation))
            #don't add if not a valid square
            if translation not in self.board_dict:
                break
            #if a piece is there already
            elif self.board_dict[translation] is not None: 
                #if the color is the same, break.
                if self.board_dict[translation].color == piece.color:
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
            print("testing translation: " + str(translation))
            #don't add if not a valid square
            if translation not in self.board_dict:
                break
            #if a piece is there already
            elif self.board_dict[translation] is not None: 
                #if the color is the same, break.
                if self.board_dict[translation].color == piece.color:
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
            print("testing translation: " + str(translation))
            #don't add if not a valid square
            if translation not in self.board_dict:
                break
            #if a piece is there already
            elif self.board_dict[translation] is not None: 
                #if the color is the same, break.
                if self.board_dict[translation].color == piece.color:
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
            print("testing translation: " + str(translation))
            #don't add if not a valid square
            if translation not in self.board_dict:
                print("not in the board dict")
                break
            #if a piece is there already
            elif self.board_dict[translation] is not None: 
                print("found somethingin the square")
                #if the color is the same, break.
                if self.board_dict[translation].color == piece.color:
                    break
                #if the color is different, allow move but break
                else: 
                    possible_moves.add(translation)
                    break
            #if the squre is empty
            else: 
                print("adding up left move")
                possible_moves.add(translation)
        print("printing possible moves from bishop function")
        print(possible_moves)
        return possible_moves
    
    #returns the set of possible moves for the given rook                            
    def rookMoves(self, piece):
        possible_moves = set()
        print(self.board_dict)
        #down moves
        for i in range(1, 9):
            translation = self.getTranslation(piece.position, 0, -i)
            print("testing translation: " + str(translation))
            #don't add if not a valid square
            if translation not in self.board_dict:
                break
            #if a piece is there already
            elif self.board_dict[translation] is not None: 
                #if the color is the same, break.
                if self.board_dict[translation].color == piece.color:
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
            print("testing translation: " + str(translation))
            #don't add if not a valid square
            if translation not in self.board_dict:
                break
            #if a piece is there already
            elif self.board_dict[translation] is not None: 
                #if the color is the same, break.
                if self.board_dict[translation].color == piece.color:
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
            print("testing translation: " + str(translation))
            #don't add if not a valid square
            if translation not in self.board_dict:
                break
            #if a piece is there already
            elif self.board_dict[translation] is not None: 
                #if the color is the same, break.
                if self.board_dict[translation].color == piece.color:
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
            print("testing translation: " + str(translation))
            #don't add if not a valid square
            if translation not in self.board_dict:
                print("not in the board dict")
                break
            #if a piece is there already
            elif self.board_dict[translation] is not None: 
                print("found somethingin the square")
                #if the color is the same, break.
                if self.board_dict[translation].color == piece.color:
                    break
                #if the color is different, allow move but break
                else: 
                    possible_moves.add(translation)
                    break
            #if the squre is empty
            else: 
                print("adding up left move")
                possible_moves.add(translation)
        print("printing possible moves from bishop function")
        print(possible_moves)
        return possible_moves 

    #returns the set of possible moves for the given queen 
    def queenMoves(self, piece):
        return self.bishopMoves(piece) | self.rookMoves(piece)

    #returns the set of possible moves for the given king
    def kingMoves(self, piece): 
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
        print(translations)
        for move in translations:
            print("testing move: " + str(move))
            if move in self.board_dict:
                if self.board_dict[move] is None:
                    possible_moves.add(move)
                if self.board_dict[move] is not None and self.board_dict[move].color != piece.color:
                    possible_moves.add(move)
        return possible_moves


game = board()
    

###animates the piece movement
##def animateMove(piece, new_position):
    ##change_x = SQUARE_SIZE * (convertX(new_position[0]) - convertX(piece.position[0]))
    ##change_y = SQUARE_SIZE * int(new_position[1]) - int(piece.position[1])
    ##step_x = change_x/animation_speed
    ##step_y = change_y/animation_speed
    ##def animateHelper(piece):
        ##canvas.move(piece.image, step_x, step_y)
        ##canvas.after(50, animateHelper(piece))
    ##animateHelper(piece)