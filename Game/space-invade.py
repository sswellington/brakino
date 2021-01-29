#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

###############################################################################
#
# Mudanças em relação à versão anterior:
#    - Background: agora carrega uma imagem e atualiza a posição durante o
#      jogo, dando a impressão que o fundo desce.
#
###############################################################################

import os, sys
import getopt

# E importaremos o pygame tambem para esse exemplo
import pygame
from pygame.locals import *

images_dir = os.path.join( "..", "docs/img" )


class Background:
    """
    Esta classe representa o ator "Fundo" do jogo.
    """
    image = None
    pos   = None
    
    def __init__( self, image="tile.png" ):
        """
        Com essa função criamos uma superfície, formada de uma repetição da
        imagem passada, de forma a cobrir a tela e um pouco mais.

        Aqui é o único lugar onde podemos carregar a imagem, utilizando
            load( image ).convert(),
        este comando não tem nenhuma relação com o formato de arquivo da
        imagem. Ele converte a imagem para o formato do pixel[1] da tela,
        representando um ganho de até 6X na performance final[2].

        [1] Formato de Pixel: Toda imagem é formada por um conjunto de pixels,
            estes são descritos por uma quantidade de bits que representam as
            cores. Em geral utiliza-se RGB (Red, Green, Blue) ou RGBA (RGB +
            Aplha/Transparência).    Em geral a tela tem um formato de 16 BPP
            (bits per pixel) e as imagens com transparência são 32 BPP (RGBA,
            variação de 256 níveis para cada cor e transparência). Ao converter
            para o formato da tela, você perde a resolução de cores e a
            transparência, como estas não são informações importantes para o
            fundo, é conveniente converter para este formato.
        [2] O ganho de performance se dá à necessidade de mesclar as imagens
            (usando o canal alpha) e então transformar para o formato da tela.
            Ao converter, elimina-se o alpha (e a necessidade de mesclar) e a
            necessidade de converter a cada "blit".
        """

        if isinstance( image, str ):
            image = os.path.join( images_dir, image )
            image = pygame.image.load( image ).convert()

        self.isize = image.get_size()
        self.pos = [ 0, -1 * self.isize[ 1 ] ]
        screen      = pygame.display.get_surface()
        screen_size = screen.get_size()

        from math import ceil
        w = ( ceil( float( screen_size[ 0 ] ) / self.isize[ 0 ] ) + 1 ) * \
            self.isize[ 0 ]
        h = ( ceil( float( screen_size[ 1 ] ) / self.isize[ 1 ] ) + 1 ) * \
            self.isize[ 1 ]

        back = pygame.Surface( ( w, h ) )
        
        for i in range( int( back.get_size()[ 0 ] / self.isize[ 0 ] ) ):
            for j in range( int( back.get_size()[ 1 ] / self.isize[ 1 ] ) ):
                back.blit( image, ( i * self.isize[ 0 ], j * self.isize[ 1 ] ) )

        self.image = back
    # __init__()



    def update( self, dt ):
        self.pos[ 1 ] += 1
        if ( self.pos[ 1 ] > 0 ):
            self.pos[ 1 ] -= self.isize[ 1 ]
    # update()



    def draw( self, screen ):
        screen.blit( self.image, self.pos )
    # draw()
# Background




class Game:
    screen      = None
    screen_size = None
    run         = True
    background  = None    
    
    def __init__( self, size, fullscreen ):
        """
        Esta é a função que inicializa o pygame, define a resolução da tela,
        caption, e disabilitamos o mouse dentro desta.
        """
        actors = {}
        pygame.init()
        flags = DOUBLEBUF
        if fullscreen:
            flags |= FULLSCREEN
        self.screen       = pygame.display.set_mode( size, flags )
        self.screen_size = self.screen.get_size()

        pygame.mouse.set_visible( 0 )
        pygame.display.set_caption( 'Título da Janela' )
    # init()



    def handle_events( self ):
        """
        Trata o evento e toma a ação necessária.
        """
        for event in pygame.event.get():
            t = event.type
            if t in ( KEYDOWN, KEYUP ):
                k = event.key
        
            if t == QUIT:
                self.run = False

            elif t == KEYDOWN:
                if   k == K_ESCAPE:
                    self.run = False
    # handle_events()




    def actors_update( self, dt ):        
        self.background.update( dt )
    # actors_update()



    def actors_draw( self ):
        self.background.draw( self.screen )
    # actors_draw()


    
    def loop( self ):
        """
        Laço principal
        """
        # Criamos o fundo
        self.background = Background( "tile.png" )

        # Inicializamos o relogio e o dt que vai limitar o valor de
        # frames por segundo do jogo
        clock         = pygame.time.Clock()
        dt            = 16


        # assim iniciamos o loop principal do programa
        while self.run:
            clock.tick( 1000 / dt )

            # Handle Input Events
            self.handle_events()

            # Atualiza Elementos
            self.actors_update( dt )

            # Desenhe para o back buffer
            self.actors_draw()
            
            # ao fim do desenho temos que trocar o front buffer e o back buffer
            pygame.display.flip()

            print("FPS: %0.2f" % clock.get_fps())
        # while self.run
    # loop()
# Game


def usage():
    """
    Imprime informações de uso deste programa.
    """
    prog = sys.argv[ 0 ]
    print("Usage:")
    print("\t%s [-f|--fullscreen] [-r <XxY>|--resolution=<XxY>]" % prog)
# usage()



def parse_opts( argv ):
    """
    Pega as informações da linha de comando e retorna 
    """
    # Analise a linha de commando usando 'getopt'
    try:
        opts, args = getopt.gnu_getopt( argv[ 1 : ],
                                        "hfr:",
                                        [ "help",
                                          "fullscreen",
                                          "resolution=" ] )
    except getopt.GetoptError:
        # imprime informacao e sai
        usage()
        sys.exit( 2 )

    options = {
        "fullscreen":  False,
        "resolution": ( 640, 480 ),
        }

    for o, a in opts:
        if o in ( "-f", "--fullscreen" ):
            options[ "fullscreen" ] = True
        elif o in ( "-h", "--help" ):
            usage()
            sys.exit( 0 )
        elif o in ( "-r", "--resolution" ):
            a = a.lower()
            r = a.split( "x" )
            if len( r ) == 2:
                options[ "resolution" ] = r
                continue

            r = a.split( "," )
            if len( r ) == 2:
                options[ "resolution" ] = r
                continue

            r = a.split( ":" )
            if len( r ) == 2:
                options[ "resolution" ] = r
                continue
    # for o, a in opts
    r = options[ "resolution" ]
    options[ "resolution" ] = [ int( r[ 0 ] ), int( r[ 1 ] ) ]
    return options
# parse_opts()



def main( argv ):
    #primeiro vamos verificar que estamos no diretorio certo para conseguir
    #encontrar as imagens e outros recursos, e inicializar o pygame com as
    #opcoes passadas pela linha de comando
    fullpath = os.path.abspath( argv[ 0 ] )
    dir = os.path.dirname( fullpath )
    os.chdir( dir )

    options = parse_opts( argv )
    game = Game( options[ "resolution" ], options[ "fullscreen" ] )
    game.loop()
# main()
        
# este comando fala para o python chamar o main se estao executando o script
if __name__ == '__main__':
    main( sys.argv )