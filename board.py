import piece as pc
import chessgame
from random import randint

class Board:
    def __init__(self):
        self.arr = None
        
    def place_pieces(self, pieces):
        arr = [[None] * 8 for i in range(8)] 
        for piece in pieces:
            arr[piece.pos[1]][piece.pos[0]]  = piece
        
        self.arr = arr   
    
                    
    def update(self, pieces, piece):
        removed_piece =  None
        if self.arr[piece.next_pos[1]][piece.next_pos[0]] == None:
            self.arr[piece.next_pos[1]][piece.next_pos[0]] = piece
            
        else:
            removed_piece = self.arr[piece.next_pos[1]][piece.next_pos[0]] 
            pieces.remove(removed_piece)
            self.arr[piece.next_pos[1]][piece.next_pos[0]] = piece
        
        self.arr[piece.pos[1]][piece.pos[0]] = None
        piece.prev_pos = piece.pos
        piece.pos = piece.next_pos
        
        return removed_piece
           
    
    def print(self):
        for row in self.arr:
            print(row)
    
    def evaluate(self, pieces, color):
        """Evaluate the board.
        Besed on the color of the available pieces.  
        ....
        Returns
        -------
        int
            an integer that represents the board value.
        """
        
        # initializing the output value with a little bit of randomness:
        value = randint(-1, 1)
        
        color_op = 'b' if color == 'w' else 'w'
    
        # value of checkmate:
        if chessgame.Rule.is_checkmate(self, pieces, color_op):
            return float('inf')
        if chessgame.Rule.is_checkmate(self, pieces, color):
            return float('-inf')
        
        # value of a check:
        if chessgame.Rule.is_check(self, pieces, color_op):
            value += 5
        if chessgame.Rule.is_check(self, pieces, color):
            value -= 5
        
        # accumulating the value of each pieace:
        for piece in pieces:
            v = piece.get_value()
            if piece.color == color:
                value += v
            else:
                value -= v
        
        # a board with more possible move is a better board:
        poss_moves = chessgame.Rule.all_possible_move_pieces_color(self, pieces, color)
        count_poss_moves = 0
        for piece in poss_moves:
            for moves in poss_moves[piece]:
                count_poss_moves += len(moves)

        poss_moves_op = chessgame.Rule.all_possible_move_pieces_color(self, pieces, color_op)
        count_poss_moves_op = 0
        for piece in poss_moves_op:
            for moves in poss_moves_op[piece]:
                count_poss_moves_op += len(moves)

        # a constant to contol the value of move with respect to pieces value.
        poss_moves_constant = 15         
        value = value + (count_poss_moves - count_poss_moves_op)//poss_moves_constant 
        
        return value