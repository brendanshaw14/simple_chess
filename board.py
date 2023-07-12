import tkinter as tk
from PIL import Image, ImageTk
from piece import *
from move_node import *

# Board class for the simple chess game
# Author: Brendan Shaw, April 2023
#   The board class stores the chess board's parameters and piece values as class variables, 
#   while the __init__ function initializes the game's variables, loads the canvas, and begins
#   the event loop. The class imports the piece and move classes- piece.py and move.py. 
# The game currently implements all piece movement correctly excluding castling and pawn promotion, 
# which will be added next, along with the minimax algorithm and move generation components.  

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
  
    #creates the canvas and initializes main variables, starts the event loop
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
            if self.turn == "white":
                #set piece_selected to the piece at the position clicked on the board
                self.piece_selected = self.board_dict[click_position]
        else: 
            #if the same piece was clicked twice, unselect the piece
            if self.piece_selected == self.board_dict[click_position]:
                self.piece_selected = None
            else: 
                #if a new spot was selected
                #verify that move was valid
                possibleMoves = self.piece_selected.getMoves(self.piece_selected, self.board_dict)
                if possibleMoves is not None:  
                    for move in possibleMoves:
                        if move == click_position:
                            self.handleMove(self.piece_selected, click_position)
                            node = move_node(None, None, self.piece_set, self.board_dict, "black", 0)
                            next_move = node.minimax()
                            self.handleMove(next_move.piece, next_move.position)
                            self.piece_selected = None
                            break
                    self.piece_selected = None
                else: 
                    self.piece_selected = None
                #get the next move
                #node = move_node(None, None, self.piece_set, self.board_dict, "white", 0)
                #print("Current Value:")
                #print(move_node.getValue(node))

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
            self.turn = "black"
        else: 
            self.turn = "white"
        #update board
        self.drawBoard()
        self.drawPieces()

    #captures the given piece, removing it from the board and from the piece array
    def handleCapture(self, piece):
        self.board_dict[piece.position] = None
        self.piece_set.remove(piece)


game = board()
    
