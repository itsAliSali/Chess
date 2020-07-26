import chessgame

class Piece:
    AN = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    
    def __init__(self, pos, color, rotate=False):
        self.color = color
        self.rotate = rotate     
        self.pos = pos
        self.next_pos = None
        self.prev_pos = None
    
    def pos_AN(self):
        return Piece.AN[self.pos[0]] + str(8 - self.pos[1])    
    
    def update(self, board, pieces):
        """if move (stored on self.next_pos) was possible do it. and switch turn"""
        removed_piece = None
        if self.next_pos != None and self.next_pos != self.pos:
            removed_piece = board.update(pieces, self)           
        return removed_piece
    
    def undo(self, board, pieces, piece_removed):
        if self.prev_pos != None:
            self.next_pos = self.prev_pos
            if piece_removed == None:
                self.update(board, pieces)
            else:
                self.update(board, pieces)
                pieces.append(piece_removed)
                board.place_pieces(pieces)                     
        else:
            print('undo:: there is no prev_pos')

        
    def next_pos_calc(self, move): 
        """calculate next position"""
        next_pos = [None, None]
        next_pos[0] = self.pos[0] + move[0]
        next_pos[1] = self.pos[1] + move[1]
        return next_pos
    
    def all_possible_moves(self, board):
        """implement this for each piece."""
        pass
    
    def find_drawable_twin(self, drawable_pieces):
        for piece in drawable_pieces:
            if piece == self:
                return piece
               
    def __repr__(self):
        return self.pos_AN()
    
    def __hash__(self):
        x, y = self.pos
        return (self.color =='b')*13*x + 27*x**2 + 13*y + (self.color =='w')*y + y**x + \
                 (self.color =='b')*17*x*y + y**((x+3)//2) + (x % 3)*7
        
    def __eq__(self, obj):
        if not isinstance(obj, Piece):
            return False
        if self.pos != obj.pos or self.color != obj.color:
            return False
        return True
        
class Pawn(Piece):
    def __init__(self, pos, color, dir, rotate=None):
        Piece.__init__(self, pos, color, rotate)
        self.dir = dir

    def get_value(self):
        return 1
        
    def all_possible_moves(self, board):
        # TODO: implement: en passant.
        # TODO: implement: if reached end substitute.
        moves = []
        if self.dir == 'up':
            max_move = -1
            if self.pos[1] == 6:
                max_move = -2
            for i in range(-1, max_move-1, -1):
                move = (0, i)   
                next_pos = self.next_pos_calc(move)
                if chessgame.Rule.is_in_range(next_pos):
                    if chessgame.Rule.collision_check(board, self, next_pos) == None:
                        moves.append(move)
                    else:
                        break # break if collided to anything 
                else:
                    break     
            candid_move = [(1,-1), (-1,-1)]
            for move in candid_move:
                next_pos = self.next_pos_calc(move)
                if chessgame.Rule.is_in_range(next_pos):    
                    if chessgame.Rule.collision_check(board, self, next_pos) == 'enemy':
                        moves.append(move)
            
        if self.dir == 'down':
            max_move = 1
            if self.pos[1] == 1:
                max_move = 2
            for i in range(1, max_move+1):
                move = (0, i)   
                next_pos = self.next_pos_calc(move)
                if chessgame.Rule.is_in_range(next_pos):    
                    if chessgame.Rule.collision_check(board, self, next_pos) == None:
                        moves.append(move)
                    else:
                        break # break if collided to anything    
                else:
                    break     
            candid_move = [(1,1), (-1,1)]
            for move in candid_move:
                next_pos = self.next_pos_calc(move)
                if chessgame.Rule.is_in_range(next_pos):    
                    if chessgame.Rule.collision_check(board, self, next_pos) == 'enemy':
                        moves.append(move)
                    
        return moves        
    
            
class Rook(Piece):        
    def __init__(self, pos, color=None, rotate=False):
        Piece.__init__(self, pos, color, rotate)
    
    def get_value(self):
        return 5
    
    def all_possible_moves(self, board):
        return chessgame.Rule.hor_ver_moves(board, self)                
                     
                     
                        
class Knight(Piece):        
    def __init__(self, pos, color='b', rotate=False):
        Piece.__init__(self, pos, color, rotate)
    
    def get_value(self):
        val = 3
        # if self.pos[0] == 0 or not self.pos[1] == 0 or self.pos[0] == 7 or not self.pos[1] == 7:
        #     val -= 1
        # if self.pos[0] <= 1 or not self.pos[1] <= 1 or self.pos[0] >= 6 or not self.pos[1] >= 6:
        #     val -= 1    
        return val # Knights in middle are better
        
    def all_possible_moves(self, board):
        moves = []
        candid_moves = [(i,j) for i in [1,-1] for j in [2,-2]]
        candid_moves.extend([(i,j) for i in [2,-2] for j in [1,-1]])
        for move in candid_moves:
            next_pos = self.next_pos_calc(move)
            if chessgame.Rule.is_in_range(next_pos):
                if chessgame.Rule.collision_check(board, self, next_pos) == 'friend':
                    continue
                moves.append(move)
 
        return moves    
        
class Bishop(Piece):        
    def __init__(self, pos, color='b', rotate=False):
        Piece.__init__(self, pos, color, rotate)
    
    def get_value(self):
        return 3
    
    def all_possible_moves(self, board):
        return chessgame.Rule.diag_moves(board, self) 
    
class Queen(Piece):        
    def __init__(self, pos, color=None, rotate=False):
        Piece.__init__(self, pos, color, rotate)
    
    def get_value(self):
        return 15
    
    def all_possible_moves(self, board):
        moves = chessgame.Rule.hor_ver_moves(board, self)
        moves.extend(chessgame.Rule.diag_moves(board, self))
        return moves 
        
class King(Piece):        
    def __init__(self, pos, color=None, rotate=False):
        Piece.__init__(self, pos, color, rotate)
    
    def get_value(self):
        return 15
        
    def all_possible_moves(self, board):
        moves = []
        candid_moves = [(i,j) for i in range(-1,2) for j in range(-1,2)]
        candid_moves.remove((0,0))
        for move in candid_moves:
            next_pos = self.next_pos_calc(move)
            if chessgame.Rule.is_in_range(next_pos):
                if chessgame.Rule.collision_check(board, self, next_pos) == 'friend':
                    continue
                moves.append(move)
                     
        return moves


    
        