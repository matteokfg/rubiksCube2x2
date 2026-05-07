import math
from pygame.locals import *
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

# Variáveis globais
pos_x, pos_y, pos_z = 0, 0, -10
angulo_rotacao_x = 45 # inicia o cubo inclinado, aparece o branco
angulo_rotacao_y = -45 # inicia o cubo inclinado, aparece o vermelho
angulo_rotacao_z = 0 # aparece o azul
escala_obj = 1.0
eixo_x = 0
eixo_y = 0
eixo_z = 0


def mini_cubo_1(): #branco,azul,vermelho
    glBegin(GL_QUADS)

    #face externa 1 (branco)
    glColor3f(1, 1, 1)
    glVertex3f(0, 1, 1)
    glVertex3f(0, 1, 0)
    glVertex3f(1, 1, 0)
    glVertex3f(1, 1, 1)
    

    #face externa 2 (azul)
    glColor3f(0, 0, 1)
    glVertex3f(0, 1, 1)
    glVertex3f(0, 0, 1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 1, 1)

    #face interna 1
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(0, 1, 1)
    glVertex3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 1, 0)

    #face interna 2
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    glVertex3f(1, 0, 0)
    glVertex3f(1, 0, 1)
    
    #face interna 3
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(0, 1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(1, 0, 0)
    glVertex3f(1, 1, 0)

    #face externa 3 (vermelho)
    glColor3f(1, 0, 0)
    glVertex3f(1, 1, 1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 0, 0)
    glVertex3f(1, 1, 0)
    glEnd()

def mini_cubo_2(): #branco,azul,magenta
    glBegin(GL_QUADS)

    #face externa 1 (branco)
    glColor3f(1, 1, 1)
    glVertex3f(0, 1, 1)
    glVertex3f(0, 1, 0)
    glVertex3f(-1, 1, 0)
    glVertex3f(-1, 1, 1)
    

    #face externa 2 (azul)
    glColor3f(0, 0, 1)
    glVertex3f(0, 1, 1)
    glVertex3f(0, 0, 1)
    glVertex3f(-1, 0, 1)
    glVertex3f(-1, 1, 1)

    #face interna 1
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(0, 1, 1)
    glVertex3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 1, 0)

    #face interna 2
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    glVertex3f(-1, 0, 0)
    glVertex3f(-1, 0, 1)
    
    #face interna 3
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(0, 1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(-1, 0, 0)
    glVertex3f(-1, 1, 0)

    #face externa 3 (magenta)
    glColor3f(1, 0.05, 1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, 0, 1)
    glVertex3f(-1, 0, 0)
    glVertex3f(-1, 1, 0)
    glEnd()

def mini_cubo_3(): #branco,verde,magenta
    glBegin(GL_QUADS)

    #face interna 3
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(0, 0, 0)
    glVertex3f(-1, 0, 0)
    glVertex3f(-1, 1, 0)
    glVertex3f(0, 1, 0)

    #face interna 2
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(0, 0, 0)
    glVertex3f(-1, 0, 0)
    glVertex3f(-1, 0, -1)
    glVertex3f(0, 0, -1)

    #face interna 1
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, -1)
    glVertex3f(0, 1, -1)
    glVertex3f(0, 1, 0)

    #face externa 1 (branco)
    glColor3f(1, 1, 1)
    glVertex3f(-1, 1, -1)
    glVertex3f(0, 1, -1)
    glVertex3f(0, 1, 0)
    glVertex3f(-1, 1, 0)

    #face externa 2 (verde)
    glColor3f(0, 1, 0)
    glVertex3f(-1, 1, -1)
    glVertex3f(0, 1, -1)
    glVertex3f(0, 0, -1)
    glVertex3f(-1, 0, -1)

    #face externa 3 (magenta)
    glColor3f(1, 0.05, 1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, 0, -1)
    glVertex3f(-1, 0, 0)
    glVertex3f(-1, 1, 0)
    glEnd()

def mini_cubo_4(): #branco,verde,vermelho
    glBegin(GL_QUADS)

    #face externa 1 (branco)
    glColor3f(1, 1, 1)
    glVertex3f(0, 1, -1)
    glVertex3f(0, 1, 0)
    glVertex3f(1, 1, 0)
    glVertex3f(1, 1, -1)
    

    #face externa 2 (verde)
    glColor3f(0, 1, 0)
    glVertex3f(0, 1, -1)
    glVertex3f(0, 0, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 1, -1)

    #face interna 1
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(0, 1, -1)
    glVertex3f(0, 0, -1)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 1, 0)

    #face interna 2
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(0, 0, -1)
    glVertex3f(0, 0, 0)
    glVertex3f(1, 0, 0)
    glVertex3f(1, 0, -1)
    
    #face interna 3
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(0, 1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(1, 0, 0)
    glVertex3f(1, 1, 0)

    #face externa 3 (vermelho)
    glColor3f(1, 0, 0)
    glVertex3f(1, 1, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 0)
    glVertex3f(1, 1, 0)
    glEnd()

def mini_cubo_5(): #amarelo,verde,vermelho
    glBegin(GL_QUADS)

    #face interna 3
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(0, 0, 0)
    glVertex3f(1, 0, 0)
    glVertex3f(1, -1, 0)
    glVertex3f(0, -1, 0)

    #face interna 2
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(0, 0, 0)
    glVertex3f(1, 0, 0)
    glVertex3f(1, 0, -1)
    glVertex3f(0, 0, -1)

    #face interna 1
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, -1)
    glVertex3f(0, -1, -1)
    glVertex3f(0, -1, 0)

    #face externa 1 (amarelo)
    glColor3f(1, 1, 0)
    glVertex3f(1, -1, -1)
    glVertex3f(0, -1, -1)
    glVertex3f(0, -1, 0)
    glVertex3f(1, -1, 0)

    #face externa 2 (verde)
    glColor3f(0, 1, 0)
    glVertex3f(1, -1, -1)
    glVertex3f(0, -1, -1)
    glVertex3f(0, 0, -1)
    glVertex3f(1, 0, -1)

    #face externa 3 (vermelho)
    glColor3f(1, 0, 0)
    glVertex3f(1, -1, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 0)
    glVertex3f(1, -1, 0)
    glEnd()

def mini_cubo_6(): #amarelo,verde,magenta
    glBegin(GL_QUADS)

    #face interna 3
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(0, 0, 0)
    glVertex3f(-1, 0, 0)
    glVertex3f(-1, -1, 0)
    glVertex3f(0, -1, 0)

    #face interna 2
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(0, 0, 0)
    glVertex3f(-1, 0, 0)
    glVertex3f(-1, 0, -1)
    glVertex3f(0, 0, -1)

    #face interna 1
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, -1)
    glVertex3f(0, -1, -1)
    glVertex3f(0, -1, 0)

    #face externa 1 (amarelo)
    glColor3f(1, 1, 0)
    glVertex3f(-1, -1, -1)
    glVertex3f(0, -1, -1)
    glVertex3f(0, -1, 0)
    glVertex3f(-1, -1, 0)

    #face externa 2 (verde)
    glColor3f(0, 1, 0)
    glVertex3f(-1, -1, -1)
    glVertex3f(0, -1, -1)
    glVertex3f(0, 0, -1)
    glVertex3f(-1, 0, -1)

    #face externa 3 (magenta)
    glColor3f(1, 0, 1)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, 0, -1)
    glVertex3f(-1, 0, 0)
    glVertex3f(-1, -1, 0)
    glEnd()

def mini_cubo_7(): #amarelo,azul,magenta
    glBegin(GL_QUADS)

    #face interna 3
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(0, 0, 0)
    glVertex3f(-1, 0, 0)
    glVertex3f(-1, -1, 0)
    glVertex3f(0, -1, 0)

    #face interna 2
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(0, 0, 0)
    glVertex3f(-1, 0, 0)
    glVertex3f(-1, 0, 1)
    glVertex3f(0, 0, 1)

    #face interna 1
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 1)
    glVertex3f(0, -1, 1)
    glVertex3f(0, -1, 0)

    #face externa 1 (amarelo)
    glColor3f(1, 1, 0)
    glVertex3f(-1, -1, 1)
    glVertex3f(0, -1, 1)
    glVertex3f(0, -1, 0)
    glVertex3f(-1, -1, 0)

    #face externa 2 (azul)
    glColor3f(0, 0, 1)
    glVertex3f(-1, -1, 1)
    glVertex3f(0, -1, 1)
    glVertex3f(0, 0, 1)
    glVertex3f(-1, 0, 1)

    #face externa 3 (magenta)
    glColor3f(1, 0.05, 1)
    glVertex3f(-1, -1, 1)
    glVertex3f(-1, 0, 1)
    glVertex3f(-1, 0, 0)
    glVertex3f(-1, -1, 0)
    glEnd()

def mini_cubo_8(): #amarelo,azul,vermelho
    glBegin(GL_QUADS)

    #face externa 1 (amarelo)
    glColor3f(1, 1, 0)
    glVertex3f(0, -1, 1)
    glVertex3f(0, -1, 0)
    glVertex3f(1, -1, 0)
    glVertex3f(1, -1, 1)
    

    #face externa 2 (azul)
    glColor3f(0, 0, 1)
    glVertex3f(0, -1, 1)
    glVertex3f(0, 0, 1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, -1, 1)

    #face interna 1
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(0, -1, 1)
    glVertex3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    glVertex3f(0, -1, 0)

    #face interna 2
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    glVertex3f(1, 0, 0)
    glVertex3f(1, 0, 1)
    
    #face interna 3
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(0, -1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(1, 0, 0)
    glVertex3f(1, -1, 0)

    #face externa 3 (vermelho)
    glColor3f(1, 0, 0)
    glVertex3f(1, -1, 1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 0, 0)
    glVertex3f(1, -1, 0)
    glEnd()



def main():
    global pos_x, pos_y, pos_z, angulo_rotacao_x, angulo_rotacao_y, angulo_rotacao_z, escala_obj, eixo_x, eixo_y, eixo_z
   
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
   
    # Configuração básica de renderização
    glViewport(0, 0, 800, 600)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (800/600), 0.1, 100.0)
   
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
   
    glEnable(GL_DEPTH_TEST)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
           
            if event.type == KEYDOWN:
                if event.key == K_x: # rotaciona eixo x
                    angulo_rotacao_x = 45 if angulo_rotacao_x >= 405 else angulo_rotacao_x + 90 # mantem o cubo inclinado para sempre ver 3 faces
                    eixo_x = 1
                    eixo_y = 0
                    eixo_z = 0
                if event.key == K_y: # rotaciona eixo y
                    angulo_rotacao_y = 45 if angulo_rotacao_y > 405 else angulo_rotacao_y + 90 # mantem o cubo inclinado para sempre ver 3 faces
                    eixo_x = 0
                    eixo_y = 1
                    eixo_z = 0
                if event.key == K_z: # rotaciona eixo z
                    angulo_rotacao_z = 0 if angulo_rotacao_z >= 360 else angulo_rotacao_z + 90 # mantem o cubo inclinado para sempre ver 3 faces
                    eixo_x = 0
                    eixo_y = 0
                    eixo_z = 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: # scroll up
                    escala_obj += 0.1 # aumenta zoom
                if event.button == 5: # scrool down
                    escala_obj -= 0.1 # diminui zoom
       
        # Fundo preto
        glClearColor(0, 0, 0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
       
        glLoadIdentity()
        
        #glPushMatrix()
        glTranslatef(pos_x, pos_y, pos_z)

        glRotatef(angulo_rotacao_x, 1, 0, 0)
        glRotatef(angulo_rotacao_y, 0, 1, 0)
        glRotatef(angulo_rotacao_z, 0, 0, 1)
        
        glScalef(escala_obj, escala_obj, escala_obj)
        mini_cubo_8()
        mini_cubo_7()
        mini_cubo_6()
        mini_cubo_5()
        mini_cubo_4()
        mini_cubo_3()
        mini_cubo_2()
        mini_cubo_1()
        #glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main() 