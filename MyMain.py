import os, sys
import pygame as pg
import chessgame
from player import HumanPlayer, MinMaxAbPlayer, RandomPlayer
      
def graphic_loop(surface, game):
    surface.blit(game.board.image, (0,0))
    
    game_event_loop(game)
    
    for piece in game.pieces:
        piece.show(surface)

    if not game.is_finished():
        if game.player1.__class__ == HumanPlayer or game.player2.__class__ == HumanPlayer:
            game.handel_human_moves()
        else:
            global timer
            if timer == 1:
                game.handel_machine_moves()        
                timer = 0
    else:
        print('The End.')
               
            
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



            
                    
# game window size:
WINDOW_SIZE = (830, 830)                

if __name__ == "__main__":
    # os.chdir(r'/home/itsme/workspace/python/chess/')
    
    pg.init()
    pg.display.set_caption('A Chess')
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
          
        
        
