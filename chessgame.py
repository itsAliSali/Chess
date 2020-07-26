import pygame as pg
from piece import Pawn, Rook, Knight, Bishop, Queen, King
from random import choice as RAND
from random import shuffle as rand_shuffle
from copy import deepcopy
import player, drawableBoard, board
import drawablePiece


class Game:
    def __init__(self, WIN_SIZE, Player1_cls, Player2_cls):
        player1_color = RAND(['b', 'w'])
        player2_color = 'w' if player1_color == 'b' else 'b'
        self.player1 = Player1_cls("DOWN PLAYER NAME", player1_color, 'down', WIN_SIZE)
        self.player2 = Player2_cls("UP PLAYER NAME", player2_color, 'up', WIN_SIZE)     
        
        self.pieces = list(self.player1.drawable_pieces)
        self.pieces.extend(self.player2.drawable_pieces)
        
        self.board = drawableBoard.DrawableBoard(WIN_SIZE)
        self.board.place_pieces(self.pieces)
        self.turn = 'w' 
        
    def pieces_as_Piece(self):
        """self.pieces are drawable but pices aint"""
        return Rule.drawable_pieces_as_piece(self.pieces) 
 
    
    def switch_turns(self):
        self.turn = 'w' if self.turn == 'b' else 'b'
        color = 'Black' if self.turn == 'b' else 'White'
        print("turn: ", color, ':', sep="")


    
    def update(self, piece, move):
        piece.next_pos = piece.next_pos_calc(move)
        removed_piece = None
        if piece.next_pos != None and piece.next_pos != piece.pos:
            removed_piece = self.board.update(self.pieces, piece)           
        
        if removed_piece != None:
            if removed_piece in self.player1.drawable_pieces:
                self.player1.drawable_pieces.remove(removed_piece)
            elif removed_piece in self.player2.drawable_pieces:
                self.player2.drawable_pieces.remove(removed_piece)
        if isinstance(piece, drawablePiece.DrawablePiece):
            piece.rect.center = Rule.transform_pos2rect(piece.size, piece.pos).center    
        
        return removed_piece
    
class Rule:
    """Just to use as namespace."""
    
    @staticmethod
    def collision_check(board, piece, next_pos):
        """to check collision.
        
        return: enemy or friend or None"""
        
        piece_in_pos = board.arr[next_pos[1]][next_pos[0]]
        if piece_in_pos == None:
            return None
        
        if piece_in_pos.color == piece.color:
            return 'friend'
        else:
            return 'enemy'        
           
    @staticmethod
    def is_move_allowed(pieces, piece, move):
        """"check if the piece takes the move, will a check takeplace."""
        
        pieces = deepcopy(pieces)
        boardd = board.Board()
        boardd.place_pieces(pieces)
        
        if not move in piece.all_possible_moves(boardd):
            return False
        
        for p in pieces:
            if piece == p:
                piece = p
        
        move_allowance = True
        
        piece.next_pos = piece.next_pos_calc(move)
        removed_piece = piece.update(boardd, pieces)
        if Rule.is_check(boardd, pieces, piece.color):
            move_allowance = False
        piece.undo(boardd, pieces, removed_piece)

        if isinstance(removed_piece, King):
            return False
        
        return move_allowance
        
    @staticmethod
    def is_check(board, pieces, color):
        """check if king of player checked or not.\n
        return king or False"""
        # find the king:
        king = None
        for piece in pieces:
            if isinstance(piece, King) and piece.color == color:
                king = piece    
                break
        if king == None:
            return True
        
        b = board
        if Rule.is_Piece_threating_piece(b, king, Pawn) or \
                Rule.is_Piece_threating_piece(b, king, Rook) or \
                Rule.is_Piece_threating_piece(b, king, Knight) or \
                Rule.is_Piece_threating_piece(b, king, Bishop) or \
                Rule.is_Piece_threating_piece(b, king, Queen) or \
                Rule.is_Piece_threating_piece(b, king, King) :
            return king
        else:
            return False              
        
    @staticmethod
    def is_Piece_threating_piece(board, piece, Piece): 
        color_op = piece.color 
        if Piece == Pawn:
            dir_op = 'down' if piece.rotate else 'up'
            piece = Pawn(piece.pos, color_op, dir_op)
        else:
            piece = Piece(piece.pos, color_op,)
        
        moves = piece.all_possible_moves(board)
        pos_possible_piece = [None] * 2
        for move in moves:
            pos_possible_piece[0] = piece.pos[0] + move[0]
            pos_possible_piece[1] = piece.pos[1] + move[1]
            if Rule.is_in_range(pos_possible_piece):
                possible_piece = board.arr[pos_possible_piece[1]][pos_possible_piece[0]]
                if isinstance(possible_piece, Piece):
                    return True     
        return False                   
    
    @staticmethod
    def is_checkmate(board, pieces, turn):
        if Rule.is_check(board, pieces, turn) == None:
            return False
        if isinstance(pieces[0], drawablePiece.DrawablePiece): 
            pieces = Rule.drawable_pieces_as_piece(pieces)
            
        escape_moves = Rule.escape_king(pieces, turn)
        if escape_moves == None:
            return False
        for piece in escape_moves:
            if len(escape_moves[piece]) != 0:
                return False
        return True    
    
    @staticmethod
    def escape_king(dummy_pieces, color):
        dummy_pieces = deepcopy(dummy_pieces)
        dummy_board = board.Board()
        dummy_board.place_pieces(dummy_pieces)
        
        king = Rule.is_check(dummy_board, dummy_pieces, color)
        if king == False:
            # no escape needed:
            return None
        
        escape_moves = dict()
        
        all_moves = Rule.all_possible_move_pieces_color(dummy_board, dummy_pieces, color)        
        
        for piece in all_moves:
            escape_moves.update({piece : []})
            for move in all_moves[piece]:
                piece.next_pos = piece.next_pos_calc(move)
                removed_piece = piece.update(dummy_board, dummy_pieces)
                if Rule.is_check(dummy_board, dummy_pieces, color) == False:
                    piece.undo(dummy_board, dummy_pieces, removed_piece)    
                    escape_moves[piece].append(move)
                else:
                    piece.undo(dummy_board, dummy_pieces, removed_piece)    
            if len(escape_moves[piece]) == 0:
                escape_moves.pop(piece)
                
        return escape_moves     
    
    @staticmethod
    def random_escape_king(pieces, color):
        # pieces_c = Rule.drawable_pieces_as_piece(pieces)
        escape_moves = Rule.escape_king(pieces, color)
        
        piece, move = None, None
        while True:
            piece = RAND(list(escape_moves.keys()))
            if len(escape_moves[piece]) != 0:
                move = RAND(escape_moves[piece])
                break
            
        return piece, move    
                
    @staticmethod        
    def all_possible_move_pieces_color(board, pieces, color): 
        moves = dict()
        rand_shuffle(pieces)
        for piece in pieces:
            if piece.color == color:
                moves_piece = piece.all_possible_moves(board)
                if len(moves_piece) != 0:
                    rand_shuffle(moves_piece)
                    moves.update({piece : moves_piece})

        return moves        
    
    @staticmethod
    def random_move(board, pieces, color):
        moves = Rule.all_possible_move_pieces_color(board, pieces, color)
        keys = []
        for key in moves:
            if len(moves[key]) != 0:
                keys.append(key)
                
        rand_piece = RAND(keys)
        rand_move = RAND(moves[rand_piece])  
        print("Random move. ", rand_piece, rand_move )      
        return (rand_piece, rand_move)         
    
    @staticmethod
    def is_in_range(pos):
        return not (pos[0] > 7 or pos[0] < 0 or pos[1] > 7 or pos[1] < 0)
    
    @staticmethod
    def move_calc(cur_pos, next_pos):
        return (next_pos[0] - cur_pos[0], next_pos[1] - cur_pos[1])
    
    @staticmethod
    def all_moves_direction(board, piece, dir):
        """move till collide to sth.\n
        This could be used for Rook, Bishop and Queen ."""
        moves = []
        for i in range(1, 8):
            move = (i * dir[0], i * dir[1])
            next_pos = piece.next_pos_calc(move)
            if Rule.is_in_range(next_pos):
                if Rule.collision_check(board, piece, next_pos) == 'friend':
                    break
                if Rule.collision_check(board, piece, next_pos) == 'enemy':
                    moves.append(move)
                    break
                moves.append(move)
            else: 
                break              
        return moves
             
    @staticmethod
    def transform_size_table2piece(size):
        coef = 1/10
        return (int(coef * size[0]), int(coef * size[1]))
   
    @staticmethod
    def transform_rect2pos(rect, piece_size):
        x, y = rect[0], rect[1]
        if x < piece_size[0]//2 or x > 8.5 * piece_size[0]:
            print('ERR >> piece is out of board.')
            return (0,0)
        if y < piece_size[1]//2 or y > 8.5 * piece_size[1]:
            print('ERR >> piece is out of board.')
            return (0,0)
        x = x - piece_size[0] // 2
        y = y - piece_size[1] // 2
        
        return (x//piece_size[0], y//piece_size[1])
             
    @staticmethod
    def transform_pos2rect(size_piece, pos):
        x, y = size_piece
        x = x * (pos[0]+1) 
        y = y * (pos[1]+1)   
        return pg.Rect((x-0, y-0), size_piece) # 2 , 5
           
    @staticmethod
    def transform_pos2AN():
        pass        
    
    @staticmethod
    def hor_ver_moves(board, piece):
        """This could be used for Queen moves too."""
        moves = []
        moves = Rule.all_moves_direction(board, piece, (1,0))
        moves.extend(Rule.all_moves_direction(board, piece, (-1,0)))
        moves.extend(Rule.all_moves_direction(board, piece, (0,1)))
        moves.extend(Rule.all_moves_direction(board, piece, (0,-1)))
    
        return moves
    
    @staticmethod
    def diag_moves(board, piece):
        """This could be used for Queen moves too."""
        moves = Rule.all_moves_direction(board, piece, (1,1))
        moves.extend(Rule.all_moves_direction(board, piece, (1,-1)))
        moves.extend(Rule.all_moves_direction(board, piece, (-1,1)))
        moves.extend(Rule.all_moves_direction(board, piece, (-1,-1)))
    
        return moves
    
    @staticmethod
    def drawable_pieces_as_piece(drawable_pieces):
        pieces = []
        for piece in drawable_pieces:
           pieces.append(piece.copy())
        return pieces    
    
    
     
            
    @staticmethod
    def check_situation(board, pieces, color):
        if isinstance(pieces[0], drawablePiece.DrawablePiece):
            pieces = Rule.drawable_pieces_as_piece(pieces)
        if Rule.is_checkmate(board, pieces, color):
            print(color + " is checkmate!")
            return 'checkmate'
        if Rule.is_check(board, pieces, color):
            print(color + " is checked!")
            return 'check'
        return 'move'

    
