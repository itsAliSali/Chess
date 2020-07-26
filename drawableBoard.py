import pygame as pg
from board import Board

class DrawableBoard(Board):
    def __init__(self, size):
        Board.__init__(self)
        self.image = pg.image.load('resources/board.jpg')      
        self.image = pg.transform.scale(self.image, size)
        
    
    
