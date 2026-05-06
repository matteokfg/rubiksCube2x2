import pygame
import math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Variáveis globais
pos_x, pos_y, pos_z = 0, 0, -10
angulo_rotacao = 0
outro_angulo_rotacao = 0 
escala_obj = 1.0

def desenhar_cena():
    # Desativa o Culling para garantir que a face apareça de qualquer lado
    glDisable(GL_CULL_FACE)

    # farol traseiro
    glBegin(GL_TRIANGLES)
    glColor3f(1, 0.1, 0)
    glVertex3f( 3.75,  0.8, 1)
    glVertex3f( 3.75,  0.40, 1)
    glVertex3f( 3.35,  0.8, 1)

    # farol dianteiro
    glColor3f(1, 0.90, 0)
    glVertex3f( -3.75,  0.6, 1)
    glVertex3f( -3.75,  0.30, 1)
    glVertex3f( -3.35,  0.6, 1)
    glEnd()

    # roda da frente (menor)
    glBegin(GL_POLYGON)
    glColor3f(1, 1, 1)
    sides = 32
    radius = 0.75
    for i in range(sides):
        # Calculate the angle for this vertex
        angle = 2.0 * math.pi * i / sides
        
        # Calculate x and y coordinates
        cx = -2 + (math.cos(angle) * radius)
        cy = -1.1 + (math.sin(angle) * radius)
        
        glVertex3f(cx, cy, 1)
    glEnd()

    # roda de tras (maior)
    glBegin(GL_POLYGON)
    glColor3f(1, 1, 1)
    sides = 32
    radius = 0.85
    for i in range(sides):
        # Calculate the angle for this vertex
        angle = 2.0 * math.pi * i / sides
        
        # Calculate x and y coordinates
        cx = 2 + (math.cos(angle) * radius)
        cy = -1 + (math.sin(angle) * radius)
        
        glVertex3f(cx, cy, 1)
    glEnd()

    # pintura do chassi
    glBegin(GL_QUADS)
    glColor3f(0, 0.05, 1)
    glVertex3f(-3.75,  -1, 1)
    glVertex3f( 3.75,  -0.95,   1)
    glVertex3f( 3.75,  0.55,   1)
    glVertex3f(-3.75,  0.1, 1)

    # chassi
    glColor3f(0.55, 0.55, 0.55)
    glVertex3f(-3.75, -1.25, 1)
    glVertex3f( 3.75, -1.25, 1)
    glVertex3f( 3.75,  0.85, 1)
    glVertex3f(-3.75,  0.65, 1)

    # para brisa
    glColor3f(1, 1, 1)
    glVertex3f(-2,  1.65, 1)
    glVertex3f(-2.75,  0.65, 1)
    glVertex3f( 2,  0.75, 1)
    glVertex3f( 1,  1.75, 1)

    # aerofolio
    glColor3f(0.45, 0.45, 0.45)
    glVertex3f( 3.45,  1.7, 1)
    glVertex3f( 3.35,  0.85,   1)
    glVertex3f( 3.60,  0.85,   1)
    glVertex3f( 3.65,  1.7, 1)
    glEnd()

def outra_pilha():
    glBegin(GL_TRIANGLES)
    glColor3f(0, 1, 0)
    glVertex3f( -3.75,  0.6, 1)
    glVertex3f( -3.75,  0.30, 1)
    glVertex3f( -3.35,  0.6, 1)
    glEnd()


def main():
    global pos_x, pos_y, pos_z, angulo_rotacao, escala_obj, outro_angulo_rotacao
   
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
                if event.key == K_LEFT:
                    pos_x -= 0.1 # translada para esquerda
                if event.key == K_RIGHT:
                    pos_x += 0.1 # translada para direita
                if event.key == K_UP:
                    pos_y += 0.1 # translada para cima
                if event.key == K_DOWN:
                    pos_y -= 0.1 # translada para baixo
                if event.key == K_r:
                    angulo_rotacao = 0 if angulo_rotacao >= 360 else angulo_rotacao + 10 # rotaciona sentido anti horario
                if event.key == K_z:
                    outro_angulo_rotacao = 0 if outro_angulo_rotacao >= 360 else outro_angulo_rotacao + 10

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: # scroll up
                    escala_obj += 0.1 # aumenta zoom
                if event.button == 5: # scrool down
                    escala_obj -= 0.1 # diminui zoom
       
        # Fundo preto
        glClearColor(0, 0, 0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
       
        glLoadIdentity()


        #desenhar_cena()
        
        
        glPushMatrix()
        
        
        # Posicionamento (transformacoes geometricas)
        glTranslatef(pos_x, pos_y, pos_z)
        glRotatef(outro_angulo_rotacao, 0, 0, 1)
        glScalef(escala_obj, escala_obj, escala_obj)
        outra_pilha()
        glPopMatrix()
        

        glTranslatef(pos_x, pos_y, pos_z)
        glRotatef(angulo_rotacao, 0, 0, 1)
        glScalef(escala_obj, escala_obj, escala_obj)
        desenhar_cena()
        
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main() 