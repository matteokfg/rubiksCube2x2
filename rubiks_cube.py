import math
from pygame.locals import *
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

# Variáveis globais
pos_x, pos_y, pos_z = 0, 0, -10
# angulo_rotacao_x = 45 # inicia o cubo inclinado, aparece o branco
# angulo_rotacao_y = -45 # inicia o cubo inclinado, aparece o vermelho
# angulo_rotacao_z = 0 # aparece o azul

angulos = [
    [45,-45,0],
    [45,-45,0],
    [45,-45,0],
    [45,-45,0],
    [45,-45,0],
    [45,-45,0],
    [45,-45,0],
    [45,-45,0],
]

escala_obj = 0.1
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
    global angulos
   
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
                if event.key == K_q: # rotaciona eixo y sentido anti horario lado superior
                    angulos[0][1] = -45 if angulos[0][1] >= 360 else angulos[0][1] + 90 
                    angulos[1][1] = -45 if angulos[1][1] >= 360 else angulos[1][1] + 90 
                    angulos[2][1] = -45 if angulos[2][1] >= 360 else angulos[2][1] + 90 
                    angulos[3][1] = -45 if angulos[3][1] >= 360 else angulos[3][1] + 90
                if event.key == K_p: # rotaciona eixo y sentido horario lado superior
                    angulos[0][1] = -45 if angulos[0][1] <= -360 else angulos[0][1] - 90 
                    angulos[1][1] = -45 if angulos[1][1] <= -360 else angulos[1][1] - 90 
                    angulos[2][1] = -45 if angulos[2][1] <= -360 else angulos[2][1] - 90 
                    angulos[3][1] = -45 if angulos[3][1] <= -360 else angulos[3][1] - 90
                if event.key == K_s: # rotaciona eixo y sentido anti horario lado inferior
                    angulos[4][1] = -45 if angulos[4][1] >= 360 else angulos[4][1] + 90 
                    angulos[5][1] = -45 if angulos[5][1] >= 360 else angulos[5][1] + 90 
                    angulos[6][1] = -45 if angulos[6][1] >= 360 else angulos[6][1] + 90 
                    angulos[7][1] = -45 if angulos[7][1] >= 360 else angulos[7][1] + 90
                if event.key == K_l: # rotaciona eixo y sentido anti horario lado inferior
                    angulos[4][1] = -45 if angulos[4][1] <= -360 else angulos[4][1] - 90 
                    angulos[5][1] = -45 if angulos[5][1] <= -360 else angulos[5][1] - 90 
                    angulos[6][1] = -45 if angulos[6][1] <= -360 else angulos[6][1] - 90 
                    angulos[7][1] = -45 if angulos[7][1] <= -360 else angulos[7][1] - 90



                if event.key == K_w: # rotaciona eixo z sentido anti horario lado superior
                    angulos[0][2] = 0 if angulos[0][2] >= 360 else angulos[0][2] + 90 
                    angulos[1][2] = 0 if angulos[1][2] >= 360 else angulos[1][2] + 90 
                    angulos[6][2] = 0 if angulos[6][2] >= 360 else angulos[6][2] + 90 
                    angulos[7][2] = 0 if angulos[7][2] >= 360 else angulos[7][2] + 90
                if event.key == K_o: # rotaciona eixo z sentido horario lado superior
                    angulos[0][2] = 0 if angulos[0][2] <= -360 else angulos[0][2] - 90 
                    angulos[1][2] = 0 if angulos[1][2] <= -360 else angulos[1][2] - 90 
                    angulos[6][2] = 0 if angulos[6][2] <= -360 else angulos[6][2] - 90 
                    angulos[7][2] = 0 if angulos[7][2] <= -360 else angulos[7][2] - 90
                if event.key == K_d: # rotaciona eixo z sentido anti horario lado inferior
                    angulos[2][2] = 0 if angulos[2][2] >= 360 else angulos[2][2] + 90 
                    angulos[3][2] = 0 if angulos[3][2] >= 360 else angulos[3][2] + 90 
                    angulos[4][2] = 0 if angulos[4][2] >= 360 else angulos[4][2] + 90 
                    angulos[5][2] = 0 if angulos[5][2] >= 360 else angulos[5][2] + 90
                if event.key == K_k: # rotaciona eixo z sentido anti horario lado inferior
                    angulos[2][2] = 0 if angulos[2][2] <= -360 else angulos[2][2] - 90 
                    angulos[3][2] = 0 if angulos[3][2] <= -360 else angulos[3][2] - 90 
                    angulos[4][2] = 0 if angulos[4][2] <= -360 else angulos[4][2] - 90 
                    angulos[5][2] = 0 if angulos[5][2] <= -360 else angulos[5][2] - 90



                if event.key == K_e: # rotaciona eixo x sentido anti horario lado superior
                    angulos[0][0] = 45 if angulos[0][0] >= 360 else angulos[0][0] + 90 
                    angulos[3][0] = 45 if angulos[3][0] >= 360 else angulos[3][0] + 90 
                    angulos[4][0] = 45 if angulos[4][0] >= 360 else angulos[4][0] + 90 
                    angulos[7][0] = 45 if angulos[7][0] >= 360 else angulos[7][0] + 90
                if event.key == K_i: # rotaciona eixo x sentido horario lado superior
                    angulos[0][0] = 45 if angulos[0][0] <= -360 else angulos[0][0] - 90 
                    angulos[3][0] = 45 if angulos[3][0] <= -360 else angulos[3][0] - 90 
                    angulos[4][0] = 45 if angulos[4][0] <= -360 else angulos[4][0] - 90 
                    angulos[7][0] = 45 if angulos[7][0] <= -360 else angulos[7][0] - 90
                if event.key == K_f: # rotaciona eixo x sentido anti horario lado inferior
                    angulos[1][0] = 45 if angulos[1][0] >= 360 else angulos[1][0] + 90 
                    angulos[2][0] = 45 if angulos[2][0] >= 360 else angulos[2][0] + 90 
                    angulos[5][0] = 45 if angulos[5][0] >= 360 else angulos[5][0] + 90 
                    angulos[6][0] = 45 if angulos[6][0] >= 360 else angulos[6][0] + 90
                if event.key == K_j: # rotaciona eixo x sentido anti horario lado inferior
                    angulos[1][0] = 45 if angulos[1][0] <= -360 else angulos[1][0] - 90 
                    angulos[2][0] = 45 if angulos[2][0] <= -360 else angulos[2][0] - 90 
                    angulos[5][0] = 45 if angulos[5][0] <= -360 else angulos[5][0] - 90 
                    angulos[6][0] = 45 if angulos[6][0] <= -360 else angulos[6][0] - 90
                

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: # scroll up
                    escala_obj += 0.1 # aumenta zoom
                if event.button == 5: # scrool down
                    escala_obj -= 0.1 # diminui zoom
        
        # Fundo preto
        glClearColor(0, 0, 0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
       
        glLoadIdentity()

        glPushMatrix()
        glTranslatef(pos_x, pos_y, pos_z)
        glRotatef(angulos[0][0], 1, 0, 0)
        glRotatef(angulos[0][1], 0, 1, 0)
        glRotatef(angulos[0][2], 0, 0, 1)
        mini_cubo_1()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(pos_x, pos_y, pos_z)
        glRotatef(angulos[1][0], 1, 0, 0)
        glRotatef(angulos[1][1], 0, 1, 0)
        glRotatef(angulos[1][2], 0, 0, 1)
        mini_cubo_2()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(pos_x, pos_y, pos_z)
        glRotatef(angulos[2][0], 1, 0, 0)
        glRotatef(angulos[2][1], 0, 1, 0)
        glRotatef(angulos[2][2], 0, 0, 1)
        mini_cubo_3()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(pos_x, pos_y, pos_z)
        glRotatef(angulos[3][0], 1, 0, 0)
        glRotatef(angulos[3][1], 0, 1, 0)
        glRotatef(angulos[3][2], 0, 0, 1)
        mini_cubo_4()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(pos_x, pos_y, pos_z)
        glRotatef(angulos[4][0], 1, 0, 0)
        glRotatef(angulos[4][1], 0, 1, 0)
        glRotatef(angulos[4][2], 0, 0, 1)
        mini_cubo_5()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(pos_x, pos_y, pos_z)
        glRotatef(angulos[5][0], 1, 0, 0)
        glRotatef(angulos[5][1], 0, 1, 0)
        glRotatef(angulos[5][2], 0, 0, 1)
        mini_cubo_6()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(pos_x, pos_y, pos_z)
        glRotatef(angulos[6][0], 1, 0, 0)
        glRotatef(angulos[6][1], 0, 1, 0)
        glRotatef(angulos[6][2], 0, 0, 1)
        mini_cubo_7()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(pos_x, pos_y, pos_z)
        glRotatef(angulos[7][0], 1, 0, 0)
        glRotatef(angulos[7][1], 0, 1, 0)
        glRotatef(angulos[7][2], 0, 0, 1)
        mini_cubo_8()
        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main() 