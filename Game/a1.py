import os, sys
import getopt

# E importaremos o pygame tambem para esse exemplo
import pygame
from pygame.locals import *

images_dir = os.path.join( "..", "imagens" )


class Background:
    """
        Esta classe representa o ator "Fundo" do jogo.
    """
    image = None
    
    def __init__( self ):
        screen = pygame.display.get_surface()
        back   = pygame.Surface( screen.get_size() ).convert()
        back.fill( ( 0, 0, 0 ) )
        self.image = back


    def update( self, dt ):
        pass # Ainda não faz nada
    # update()



    def draw( self, screen ):
        screen.blit( self.image, ( 0, 0 ) )
    # draw()
# Background



class Game:
    screen      = None
    screen_size = None
    run         = True
    background  = None    
    
    def __init__( self, size, fullscreen ):
        """
            Esta é a função que inicializa o pygame, 
            define a resolução da tela,
            caption, 
            e disabilitamos o mouse dentro desta.
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
        self.background = Background()

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