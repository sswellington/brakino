#!/usr/bin/env python

from copy import copy
import pygame
from pygame.locals import *
from pygame.sprite import Sprite, RenderUpdates

class Bola( Sprite ):
    def __init__( self, pos, *grupos ):
        Sprite.__init__( self, *grupos )
        self.rect = Rect( 0, 0, 100, 100 )
        self.rect.center = pos
        # Cria imagem
        self.image = pygame.Surface( self.rect.size )
        self.image.set_colorkey( ( 0, 0, 0 ) )
        self.image.fill( ( 0, 0, 0 ) )
        pygame.draw.circle( self.image,
                            ( 255, 255, 255 ),
                            ( self.rect.width / 2,
                              self.rect.height / 2 ),
                            self.rect.width / 2 )
    # __init__()


    def move( self, x, y ):
        self.rect.move_ip( x, y )
    # move()
# Bola



# ConfiguraÃ§Ãµes iniciais
pygame.init()
tela  = pygame.display.set_mode( ( 640, 480 ) )
grupo = RenderUpdates()
bola  = Bola( tela.get_rect().center, grupo )
clock = pygame.time.Clock()

fundo = pygame.Surface( tela.get_size() )
fundo.fill( ( 0, 0, 255 ) )
tela.blit( fundo, ( 0, 0 ) )
pygame.display.flip()


key = { K_UP: False, K_DOWN: False,
        K_LEFT: False, K_RIGHT: False }

# LaÃ§o principal
while True:
    clock.tick( 24 )
    # Trata eventos    
    for e in pygame.event.get( [ KEYUP, KEYDOWN ] ):
        valor = ( e.type == KEYDOWN )
        if   e.key == K_ESCAPE:
            raise SystemExit
        elif e.key in key.keys():
            key[ e.key ] = valor
    # Movimenta a bola de acordo com as teclas
    if key[ K_UP ]:    bola.move(   0, -10 )
    if key[ K_DOWN ]:  bola.move(   0,  10 )
    if key[ K_LEFT ]:  bola.move( -10,   0 )
    if key[ K_RIGHT ]: bola.move(  10,   0 )

    grupo.clear( tela, fundo )
    pygame.display.update( grupo.draw( tela ) )
    