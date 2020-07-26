from drawablePiece import *
import chessgame, board
import pygame as pg
from time import sleep
from copy import deepcopy
 
class Player:
    def __init__(self, name, color, position, WIN_SIZE):
        self.drawable_pieces = Player.init_drawable_pieces(color, position, WIN_SIZE); 
        self.turn = color == 'w'
        self.color = color
        self.name = name       
    

    def switch_turn(self):
        self.turn = not self.turn    


    @staticmethod
    def init_drawable_pieces(color, position, WIN_SIZE):
        pieces = []
        if position == 'up':
            pown_pos = 1
            royal_pos= 0
            direction = 'down'
            rotate = True    
        elif position=='down':
            pown_pos = 6
            royal_pos= 7
            direction= 'up'
            rotate = False
        else:
            print('ERR>> invalid player position(up/down).')            
            
        for i in range(8):
            pieces.append(DrawablePawn((i, pown_pos), color,
                                        direction, WIN_SIZE, rotate))
        
        pieces.append(DrawableRook((0, royal_pos), color, WIN_SIZE, rotate))
        pieces.append(DrawableRook((7, royal_pos), color, WIN_SIZE, rotate))
        pieces.append(DrawableKnight((1, royal_pos), color, WIN_SIZE, rotate))
        pieces.append(DrawableKnight((6, royal_pos), color, WIN_SIZE, rotate))
        pieces.append(DrawableBishop((2, royal_pos), color, WIN_SIZE, rotate))
        pieces.append(DrawableBishop((5, royal_pos), color, WIN_SIZE, rotate))
        
        pieces.append(DrawableKing((4, royal_pos), color, WIN_SIZE, rotate))
        pieces.append(DrawableQueen((3, royal_pos), color, WIN_SIZE, rotate))
                
        return pieces    
                        
class HumanPlayer(Player):
    def __init__(self, name, color, position, WIN_SIZE):
        Player.__init__(self, name, color, position, WIN_SIZE)
        
    def do_move(self, game):
        pass 
    
    def draw_pieces(self, game):
        for piece in self.drawable_pieces:
            if piece.click:
                piece.rect.center = pg.mouse.get_pos()
            
    def place_piece(self, game, piece):
        pieces_c = chessgame.Rule.drawable_pieces_as_piece(game.pieces)
        piece.rect.center = pg.mouse.get_pos()
        next_pos = chessgame.Rule.transform_rect2pos(piece.rect, piece.size)
        move = chessgame.Rule.move_calc(piece.pos, next_pos)
        if chessgame.Rule.is_move_allowed(pieces_c, piece, move): 
            game.update(piece, move)
            
            # print("--", piece)
            # print(len(game.pieces), len(game.player1.drawable_pieces), len(game.player2.drawable_pieces))
            game.switch_turns() 
            return 
        else:
            piece.rect.center = chessgame.Rule.transform_pos2rect(piece.size, piece.pos).center
            return
                    

class MinMaxAbPlayer(Player):
    def __init__(self, name, color, position, WIN_SIZE):
        Player.__init__(self, name, color, position, WIN_SIZE)
        
    def do_move(self, game, depth=2, i=20):
        pieces_c = chessgame.Rule.drawable_pieces_as_piece(game.pieces)
        situation = chessgame.Rule.check_situation(game.board, game.pieces, self.color)

        if situation == 'move':
            _, (piece, move) = MinMaxAbPlayer.alpha_beta(pieces_c, depth, depth, self.color, self.color)
            print("MinMax move: ", piece, move)
            piece = piece.find_drawable_twin(game.pieces)
            if not chessgame.Rule.is_move_allowed(pieces_c, piece, move):
                self.do_move(game, i-1)
                if i == 0:
                    print('Could not found a MinMax move.')
                    
            else:
                game.update(piece, move)
                game.switch_turns()
    
        elif situation == 'check':
            piece, move = chessgame.Rule.random_escape_king(pieces_c, self.color)
            print("MinMax move:(checked. random escape.) ", piece, move)    
            piece = piece.find_drawable_twin(game.pieces)
            game.update(piece, move)
            game.switch_turns()
        
        elif situation == 'checkmate':
            print(self.name, ' is checkmate!' )    
        
    @staticmethod
    def alpha_beta(pieces, max_depth, depth, color, turn, a=float('-inf'), b=float('inf'), best=None): # call ex: 'b', 'b'
        pieces = deepcopy(pieces)
        board_c = board.Board()
        board_c.place_pieces(pieces)
        
        best_value = float('-inf')
        result = None
        
        all_moves = chessgame.Rule.all_possible_move_pieces_color(board_c, pieces, turn)
        
        if depth == 0:
            return (board_c.evaluate(pieces, color), result)
        
        if turn == color:
            value = float('-inf')
            for piece in all_moves:
                for move in all_moves[piece]:
                    piece.next_pos = piece.next_pos_calc(move)
                    removed_piece = piece.update(board_c, pieces)
                    
                    next_turn = 'b' if turn=='w' else 'w'
                    c, _ = MinMaxAbPlayer.alpha_beta(pieces, max_depth, depth-1, color, next_turn, a, b, best_value)
                    value = max(value, c) 
                    a = max(a, value)
                    piece.undo(board_c, pieces, removed_piece) 
                    
                    if depth == max_depth:
                        if value > best_value:
                            best_value = value
                            result = (piece, move)
            
                    if a >= b: 
                        return value, result             
                        
        else:
            value = float('inf')
            for piece in all_moves:
                for move in all_moves[piece]:
                    piece.next_pos = piece.next_pos_calc(move)
                    removed_piece = piece.update(board_c, pieces)
                    
                    next_turn = 'b' if turn=='w' else 'w'
                    c, _ = MinMaxAbPlayer.alpha_beta(pieces, max_depth, depth-1, color, next_turn, a, b, best_value)
                    value = min(value, c)
                    b = min(value, b) 

                    piece.undo(board_c, pieces, removed_piece) 
                    
                    if a >= b: 
                        return value, result

        return value, result      
    
class RandomPlayer(Player):
    def __init__(self, name, color, position, WIN_SIZE):
        Player.__init__(self, name, color, position, WIN_SIZE)
        
    def do_move(self, game, i=300):
        pieces_c = chessgame.Rule.drawable_pieces_as_piece(game.pieces)
        situation = chessgame.Rule.check_situation(game.board, game.pieces, self.color)
        if situation == 'move':
            piece, move = chessgame.Rule.random_move(game.board, game.pieces, self.color)
            # piece = piece.find_drawable_twin(game.pieces)
            if not chessgame.Rule.is_move_allowed(pieces_c, piece, move):
                self.do_move(game, i-1)
                if i == 0:
                    print('Could not found a random move.')
                    return False
            else:
                game.update(piece, move)
                game.switch_turns()
              
        elif situation == 'check':
            piece, move = chessgame.Rule.random_escape_king(pieces_c, self.color)    
            print("Randon move:(checked. random escape.) ", piece, move)    
            piece = piece.find_drawable_twin(game.pieces)
            game.update(piece, move)
            game.switch_turns()
        
        elif situation == 'checkmate':
            print(self.name, ' is checkmate!' )    
        
        