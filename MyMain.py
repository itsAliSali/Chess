import os, sys
import pygame as pg
import chessgame
from player import HumanPlayer, MinMaxAbPlayer, RandomPlayer
      
def graphic_loop(surface, game):
    surface.blit(game.board.image, (0,0))
    
    game_event_loop(game)
    
    for piece in game.pieces:
        piece.show(surface)

    handel_moves(game)
               
            
def game_event_loop(game):
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            if game.player1.__class__ == HumanPlayer:
                for piece in game.player1.drawable_pieces:
                    if piece.rect.collidepoint(event.pos):
                        piece.click = True
            if game.player2.__class__ == HumanPlayer:
                for piece in game.player2.drawable_pieces:
                    if piece.rect.collidepoint(event.pos):
                        piece.click = True
                                        
        elif event.type == pg.MOUSEBUTTONUP:
            for piece in game.pieces:
                piece.click = False
                if piece.rect.collidepoint(event.pos):
                    if game.player1.__class__ == HumanPlayer:
                        game.player1.place_piece(game, piece)
                    if game.player2.__class__ == HumanPlayer:
                        game.player2.place_piece(game, piece)
                    
                    
        elif event.type == pg.QUIT:
            pg.quit()
            sys.exit()


def handel_moves(game):
    if game.player1.__class__ == HumanPlayer or  game.player2.__class__ == HumanPlayer:
        if game.turn == game.player1.color:
            if game.player1.__class__ == HumanPlayer:
                game.player1.draw_pieces(game) 
            else:
                foo = False
                # for piece in game.pieces:
                #     if piece.click:
                #         foo = True
                if not foo:
                    game.player1.do_move(game)            
        
        if game.turn == game.player2.color:
            if game.player2.__class__ == HumanPlayer:
                game.player2.draw_pieces(game)
            else:
                foo = False
                # for piece in game.pieces:
                #     if piece.click:
                #         foo = True
                if not foo:
                    game.player2.do_move(game)
                        

    else:
        global timer
        if timer == 1:
            if game.player1.color == game.turn:
                game.player1.do_move(game)
            else:
                game.player2.do_move(game)
            timer = 0
            
                    
# game window size:
WINDOW_SIZE = (830, 830)                

if __name__ == "__main__":
    # os.chdir(r'/home/itsme/workspace/python/chess/')
    
    pg.init()
    pg.display.set_caption('A chess')
    Screen = pg.display.set_mode(WINDOW_SIZE)
    
    # timer is used for automated palyers (ie. RandomPlayer and MinMaxPlayer)
    my_clock = pg.time.Clock()
    residue = pg.time.get_ticks() % 100
    global timer
    timer = 0
    
    # you can choose palyers from HumanPlayer, MinMaxAbPlayer, RandomPlayer:
    game = chessgame.Game(WINDOW_SIZE, HumanPlayer,
                                        MinMaxAbPlayer)
    
    while True:
        graphic_loop(Screen, game)
       
        pg.display.update()
        
        my_clock.tick(1500)  
        if pg.time.get_ticks() % 100 == residue:
            timer += 1
          
        
        
