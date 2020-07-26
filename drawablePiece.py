import pygame as pg
import chessgame
from piece import Piece, Pawn, Rook, Knight, Bishop, Queen, King

class DrawablePiece(Piece):
    def __init__(self, pos, color, img, size, rotate=False):
        Piece.__init__(self, pos, color, rotate)
        self.size = chessgame.Rule.transform_size_table2piece(size)
        self.click = False
        self.image= pg.image.load(r'resources/icon/{}'.format(img)) 
        self.image = pg.transform.scale(self.image, self.size)
        if rotate:
            self.image = pg.transform.rotate(self.image, 180)
        self.rect = chessgame.Rule.transform_pos2rect(self.size, pos)
                
        
    def show(self, surface):
        surface.blit(self.image, self.rect)
            
    
    def update(self, board, pieces):
        """if move (stored on self.next_pos) was possible do it. and switch turn"""
        removed_piece = Piece.update(self, board, pieces)
        self.rect.center = chessgame.Rule.transform_pos2rect(self.size, self.pos).center    
        return removed_piece
    
        
class DrawablePawn(Pawn, DrawablePiece):
    def __init__(self, pos, color, dir, size, rotate=False):
        img = 'pawn-{}.png'.format(color)
        Pawn.__init__(self, pos, color, dir, rotate)
        DrawablePiece.__init__(self, pos, color, img, size, rotate)
    
    def copy(self):
        return Pawn(self.pos, self.color, self.dir, self.rotate) 
       
    
            
class DrawableRook(Rook, DrawablePiece):        
    def __init__(self, pos, color, size, rotate=False):
        img = 'rook-{}.png'.format(color)
        Rook.__init__(self, pos, color, rotate)
        DrawablePiece.__init__(self, pos, color, img, size, rotate)
    
    def copy(self):
        return Rook(self.pos, self.color, self.rotate)                  
                        
class DrawableKnight(Knight, DrawablePiece):        
    def __init__(self, pos, color, size, rotate=False):
        img = 'knight-{}.png'.format(color)
        Knight.__init__(self, pos ,color, rotate)
        DrawablePiece.__init__(self, pos, color, img, size, rotate)
    
    def copy(self):
        return Knight(self.pos, self.color, self.rotate) 
        
class DrawableBishop(Bishop, DrawablePiece):        
    def __init__(self, pos, color, size, rotate=False):
        img = 'bishop-{}.png'.format(color)
        Bishop.__init__(self, pos, color, rotate)
        DrawablePiece.__init__(self, pos, color, img, size, rotate)
    
    def copy(self):
        return Bishop(self.pos, self.color, self.rotate) 
    
class DrawableQueen(Queen, DrawablePiece):        
    def __init__(self, pos, color=None, size=None, rotate=False):
        img = 'queen-{}.png'.format(color)
        Queen.__init__(self, pos, color, rotate)
        DrawablePiece.__init__(self, pos, color, img, size, rotate)
    
    def copy(self):
        return Queen(self.pos, self.color, self.rotate) 
        
class DrawableKing(King, DrawablePiece):        
    def __init__(self, pos, color, size, rotate=False):
        img = 'king-{}.png'.format(color)
        King.__init__(self, pos, color, rotate)
        DrawablePiece.__init__(self, pos, color, img, size, rotate)
    
    def copy(self):
        return King(self.pos, self.color, self.rotate) 
        
