import math
from pygame.locals import *
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

# Variáveis globais
pos_x, pos_y, pos_z = 0, 0, -10

angulos = [
    [45,315,0],
    [45,45,0],
    [45,135,0],
    [45,225,0],
    [45,315,270],
    [45,45,270],
    [45,135,270],
    [45,225,270],
]

quartetos = {
    "x_superior": [0,1,4,5],
    "x_inferior": [2,3,6,7],
    "y_superior": [0,1,2,3],
    "y_inferior": [4,5,6,7],
    "z_superior": [0,3,7,4],
    "z_inferior": [1,2,5,6],
}

escala_obj = 0.1

class MiniCubo():
    def __init__(self, cor1, cor2, cor3):
        self.cor1 = cor1
        self.cor2 = cor2
        self.cor3 = cor3

    def _cores(self, cor):
        match cor:
            case "vermelho":
                return glColor3f(1, 0, 0)
            case "branco":
                return glColor3f(1, 1, 1)
            case "verde":
                return glColor3f(0, 1, 0)
            case "azul":
                return glColor3f(0, 0, 1)
            case "amarelo":
                return glColor3f(1, 1, 0)
            case "laranja":
                return glColor3f(1, 0.05, 1)

    def desenha(self):
        glBegin(GL_QUADS)

        #face externa 1 (branco)
        self._cores(self.cor1)
        glVertex3f(0, 1, 1)
        glVertex3f(0, 1, 0)
        glVertex3f(1, 1, 0)
        glVertex3f(1, 1, 1)
        

        #face externa 2 (azul)
        self._cores(self.cor2)
        glVertex3f(0, 1, 1)
        glVertex3f(0, 0, 1)
        glVertex3f(1, 0, 1)
        glVertex3f(1, 1, 1)

        #face externa 3 (vermelho)
        self._cores(self.cor3)
        glVertex3f(1, 1, 1)
        glVertex3f(1, 0, 1)
        glVertex3f(1, 0, 0)
        glVertex3f(1, 1, 0)

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
        glEnd()

mini_cubo_0 = MiniCubo("branco", "vermelho", "azul")
mini_cubo_1 = MiniCubo("branco", "azul", "laranja")
mini_cubo_2 = MiniCubo("branco", "laranja", "verde")
mini_cubo_3 = MiniCubo("branco", "verde", "vermelho")
mini_cubo_4 = MiniCubo("azul", "vermelho", "amarelo")
mini_cubo_5 = MiniCubo("laranja", "azul", "amarelo")
mini_cubo_6 = MiniCubo("verde", "laranja", "amarelo")
mini_cubo_7 = MiniCubo("vermelho", "verde", "amarelo")



def main():
    global pos_x, pos_y, pos_z, angulo_rotacao_x, angulo_rotacao_y, angulo_rotacao_z, escala_obj
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
                    print("Tecla Q")
                    for mini_cubo in quartetos["y_superior"]:
                        angulos[mini_cubo][1] = 45 if angulos[mini_cubo][1] + 90 >= 360 else angulos[mini_cubo][1] + 90
                    #atualiza mapa dos minicubos
                    quartetos["y_superior"] = [quartetos["y_superior"][i-1 if i-1 < 4 else 0] for i, mini_cubo in enumerate(quartetos["y_superior"])]

                    quartetos["x_superior"][0] = quartetos["y_superior"][0]
                    quartetos["x_superior"][1] = quartetos["y_superior"][1]
                    quartetos["x_inferior"][0] = quartetos["y_superior"][2]
                    quartetos["x_inferior"][1] = quartetos["y_superior"][3]
                    quartetos["z_superior"][0] = quartetos["y_superior"][0]
                    quartetos["z_superior"][1] = quartetos["y_superior"][3]
                    quartetos["z_inferior"][0] = quartetos["y_superior"][1]
                    quartetos["z_inferior"][1] = quartetos["y_superior"][2]
                if event.key == K_p: # rotaciona eixo y sentido horario lado superior
                    print("Tecla P")
                    for mini_cubo in quartetos["y_superior"]:
                        angulos[mini_cubo][1] = 315 if angulos[mini_cubo][1] - 90 <= 0 else angulos[mini_cubo][1] - 90
                    quartetos["y_superior"] = [quartetos["y_superior"][i+1 if i+1 < 4 else 0] for i, mini_cubo in enumerate(quartetos["y_superior"])]

                    quartetos["x_superior"][0] = quartetos["y_superior"][0]
                    quartetos["x_superior"][1] = quartetos["y_superior"][1]
                    quartetos["x_inferior"][0] = quartetos["y_superior"][2]
                    quartetos["x_inferior"][1] = quartetos["y_superior"][3]
                    quartetos["z_superior"][3] = quartetos["y_superior"][0]
                    quartetos["z_superior"][2] = quartetos["y_superior"][3]
                    quartetos["z_inferior"][0] = quartetos["y_superior"][1]
                    quartetos["z_inferior"][1] = quartetos["y_superior"][2]
                if event.key == K_s: # rotaciona eixo y sentido anti horario lado inferior
                    print("Tecla S")
                    for mini_cubo in quartetos["y_inferior"]:
                        angulos[mini_cubo][1] = 45 if angulos[mini_cubo][1] + 90 >= 360 else angulos[mini_cubo][1] + 90
                    quartetos["y_inferior"] = [quartetos["y_inferior"][i-1 if i-1 < 4 else 0] for i, mini_cubo in enumerate(quartetos["y_inferior"])]

                    quartetos["x_superior"][2] = quartetos["y_inferior"][0]
                    quartetos["x_superior"][3] = quartetos["y_inferior"][1]
                    quartetos["x_inferior"][2] = quartetos["y_inferior"][2]
                    quartetos["x_inferior"][3] = quartetos["y_inferior"][3]
                    quartetos["z_superior"][2] = quartetos["y_inferior"][0]
                    quartetos["z_superior"][3] = quartetos["y_inferior"][3]
                    quartetos["z_inferior"][2] = quartetos["y_inferior"][1]
                    quartetos["z_inferior"][3] = quartetos["y_inferior"][2]
                if event.key == K_l: # rotaciona eixo y sentido horario lado inferior
                    print("Tecla L")
                    for mini_cubo in quartetos["y_inferior"]:
                        angulos[mini_cubo][1] = 315 if angulos[mini_cubo][1] - 90 <= 0 else angulos[mini_cubo][1] - 90
                    quartetos["y_inferior"] = [quartetos["y_inferior"][i+1 if i+1 < 4 else 0] for i, mini_cubo in enumerate(quartetos["y_inferior"])]

                    quartetos["x_superior"][2] = quartetos["y_inferior"][0]
                    quartetos["x_superior"][3] = quartetos["y_inferior"][1]
                    quartetos["x_inferior"][2] = quartetos["y_inferior"][2]
                    quartetos["x_inferior"][3] = quartetos["y_inferior"][3]
                    quartetos["z_superior"][2] = quartetos["y_inferior"][0]
                    quartetos["z_superior"][3] = quartetos["y_inferior"][3]
                    quartetos["z_inferior"][2] = quartetos["y_inferior"][1]
                    quartetos["z_inferior"][3] = quartetos["y_inferior"][2]


                if event.key == K_w: # rotaciona eixo z sentido anti horario lado superior
                    print("Tecla W")
                    for mini_cubo in quartetos["z_superior"]:
                        # angulos[mini_cubo][2] = 90 if angulos[mini_cubo][2] + 90 >= 360 else angulos[mini_cubo][2] + 90
                        angulos[mini_cubo][2] = 0 if angulos[mini_cubo][2] == 270 else 270
                    #atualiza mapa dos minicubos
                    quartetos["z_superior"] = [quartetos["z_superior"][i+1 if i+1 < 4 else 0] for i, mini_cubo in enumerate(quartetos["z_superior"])]
                    # quartetos["x_superior"] = [quartetos["z_superior"][quartetos["z_superior"].index(mini_cubo)-1 if quartetos["z_superior"].index(mini_cubo)-1 < 4 else 0] if mini_cubo in quartetos["z_superior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["x_superior"])]
                    # quartetos["x_inferior"] = [quartetos["z_superior"][quartetos["z_superior"].index(mini_cubo)-1 if quartetos["z_superior"].index(mini_cubo)-1 < 4 else 0] if mini_cubo in quartetos["z_superior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["x_inferior"])]
                    # quartetos["y_superior"] = [quartetos["z_superior"][quartetos["z_superior"].index(mini_cubo)-1 if quartetos["z_superior"].index(mini_cubo)-1 < 4 else 0] if mini_cubo in quartetos["z_superior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["y_superior"])]
                    # quartetos["y_inferior"] = [quartetos["z_superior"][quartetos["z_superior"].index(mini_cubo)-1 if quartetos["z_superior"].index(mini_cubo)-1 < 4 else 0] if mini_cubo in quartetos["z_superior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["y_inferior"])]
                    quartetos["x_superior"][0] = quartetos["z_superior"][0]
                    quartetos["x_superior"][2] = quartetos["z_superior"][3]
                    quartetos["x_inferior"][1] = quartetos["z_superior"][1]
                    quartetos["x_inferior"][3] = quartetos["z_superior"][2]
                    quartetos["y_superior"][0] = quartetos["z_superior"][0]
                    quartetos["y_superior"][3] = quartetos["z_superior"][1]
                    quartetos["y_inferior"][0] = quartetos["z_superior"][3]
                    quartetos["y_inferior"][3] = quartetos["z_superior"][2]
                if event.key == K_o: # rotaciona eixo z sentido horario lado superior
                    print("Tecla O")
                    for mini_cubo in quartetos["z_superior"]:
                        angulos[mini_cubo][2] = 270 if angulos[mini_cubo][2] - 90 < 0 else angulos[mini_cubo][2] - 90
                    quartetos["z_superior"] = [quartetos["z_superior"][i+1 if i+1 < 4 else 0] for i, mini_cubo in enumerate(quartetos["z_superior"])]
                    quartetos["x_superior"] = [quartetos["z_superior"][quartetos["z_superior"].index(mini_cubo)+1 if quartetos["z_superior"].index(mini_cubo)+1 < 4 else 0] if mini_cubo in quartetos["z_superior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["x_superior"])]
                    quartetos["x_inferior"] = [quartetos["z_superior"][quartetos["z_superior"].index(mini_cubo)+1 if quartetos["z_superior"].index(mini_cubo)+1 < 4 else 0] if mini_cubo in quartetos["z_superior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["x_inferior"])]
                    quartetos["y_superior"] = [quartetos["z_superior"][quartetos["z_superior"].index(mini_cubo)+1 if quartetos["z_superior"].index(mini_cubo)+1 < 4 else 0] if mini_cubo in quartetos["z_superior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["y_superior"])]
                    quartetos["y_inferior"] = [quartetos["z_superior"][quartetos["z_superior"].index(mini_cubo)+1 if quartetos["z_superior"].index(mini_cubo)+1 < 4 else 0] if mini_cubo in quartetos["z_superior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["y_inferior"])]
                if event.key == K_d: # rotaciona eixo z sentido anti horario lado inferior
                    print("Tecla D")
                    for mini_cubo in quartetos["z_inferior"]:
                        angulos[mini_cubo][2] = 90 if angulos[mini_cubo][2] + 90 > 360 else angulos[mini_cubo][2] + 90
                    #atualiza mapa dos minicubos
                    quartetos["z_inferior"] = [quartetos["z_inferior"][i-1 if i-1 < 4 else 0] for i, mini_cubo in enumerate(quartetos["z_inferior"])]
                    quartetos["x_superior"] = [quartetos["z_inferior"][quartetos["z_inferior"].index(mini_cubo)+1 if quartetos["z_inferior"].index(mini_cubo)+1 < 4 else 0] if mini_cubo in quartetos["z_inferior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["x_superior"])]
                    quartetos["x_inferior"] = [quartetos["z_inferior"][quartetos["z_inferior"].index(mini_cubo)+1 if quartetos["z_inferior"].index(mini_cubo)+1 < 4 else 0] if mini_cubo in quartetos["z_inferior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["x_inferior"])]
                    quartetos["y_superior"] = [quartetos["z_inferior"][quartetos["z_inferior"].index(mini_cubo)+1 if quartetos["z_inferior"].index(mini_cubo)+1 < 4 else 0] if mini_cubo in quartetos["z_inferior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["y_superior"])]
                    quartetos["y_inferior"] = [quartetos["z_inferior"][quartetos["z_inferior"].index(mini_cubo)+1 if quartetos["z_inferior"].index(mini_cubo)+1 < 4 else 0] if mini_cubo in quartetos["z_inferior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["y_inferior"])]
                if event.key == K_k: # rotaciona eixo z sentido horario lado inferior
                    print("Tecla K")
                    for mini_cubo in quartetos["z_inferior"]:
                        angulos[mini_cubo][2] = 270 if angulos[mini_cubo][2] - 90 < 0 else angulos[mini_cubo][2] - 90
                    #atualiza mapa dos minicubos
                    quartetos["z_inferior"] = [quartetos["z_inferior"][i+1 if i+1 < 4 else 0] for i, mini_cubo in enumerate(quartetos["z_inferior"])]
                    quartetos["x_superior"] = [quartetos["z_inferior"][quartetos["z_inferior"].index(mini_cubo)-1 if quartetos["z_inferior"].index(mini_cubo)-1 < 4 else 0] if mini_cubo in quartetos["z_inferior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["x_superior"])]
                    quartetos["x_inferior"] = [quartetos["z_inferior"][quartetos["z_inferior"].index(mini_cubo)-1 if quartetos["z_inferior"].index(mini_cubo)-1 < 4 else 0] if mini_cubo in quartetos["z_inferior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["x_inferior"])]
                    quartetos["y_superior"] = [quartetos["z_inferior"][quartetos["z_inferior"].index(mini_cubo)-1 if quartetos["z_inferior"].index(mini_cubo)-1 < 4 else 0] if mini_cubo in quartetos["z_inferior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["y_superior"])]
                    quartetos["y_inferior"] = [quartetos["z_inferior"][quartetos["z_inferior"].index(mini_cubo)-1 if quartetos["z_inferior"].index(mini_cubo)-1 < 4 else 0] if mini_cubo in quartetos["z_inferior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["y_inferior"])]

                if event.key == K_v: 
                    print("Tecla V")
                    for mini_cubo in quartetos["x_superior"]:
                        angulos[mini_cubo][2] = 270 if angulos[mini_cubo][2] - 90 < 0 else angulos[mini_cubo][2] - 90
                        angulos[mini_cubo][1] = 315 if angulos[mini_cubo][1] - 90 <= 0 else angulos[mini_cubo][1] - 90
                    #atualiza mapa dos minicubos
                    # quartetos["z_inferior"] = [quartetos["z_inferior"][i+1 if i+1 < 4 else 0] for i, mini_cubo in enumerate(quartetos["z_inferior"])]
                    # quartetos["x_superior"] = [quartetos["z_inferior"][quartetos["z_inferior"].index(mini_cubo)-1 if quartetos["z_inferior"].index(mini_cubo)-1 < 4 else 0] if mini_cubo in quartetos["z_inferior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["x_superior"])]
                    # quartetos["x_inferior"] = [quartetos["z_inferior"][quartetos["z_inferior"].index(mini_cubo)-1 if quartetos["z_inferior"].index(mini_cubo)-1 < 4 else 0] if mini_cubo in quartetos["z_inferior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["x_inferior"])]
                    # quartetos["y_superior"] = [quartetos["z_inferior"][quartetos["z_inferior"].index(mini_cubo)-1 if quartetos["z_inferior"].index(mini_cubo)-1 < 4 else 0] if mini_cubo in quartetos["z_inferior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["y_superior"])]
                    # quartetos["y_inferior"] = [quartetos["z_inferior"][quartetos["z_inferior"].index(mini_cubo)-1 if quartetos["z_inferior"].index(mini_cubo)-1 < 4 else 0] if mini_cubo in quartetos["z_inferior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["y_inferior"])]



                if event.key == K_e: # rotaciona eixo x sentido anti horario lado superior
                    print("Tecla E")
                    for mini_cubo in quartetos["x_superior"]:
                        angulos[mini_cubo][0] = 45 if angulos[mini_cubo][0] + 90 >= 360 else angulos[mini_cubo][0] + 90
                    #atualiza mapa dos minicubos
                    quartetos["x_superior"] = [quartetos["x_superior"][i-1 if i-1 < 4 else 0] for i, mini_cubo in enumerate(quartetos["x_superior"])]
                    quartetos["y_superior"] = [quartetos["x_superior"][quartetos["x_superior"].index(mini_cubo)+1 if quartetos["x_superior"].index(mini_cubo)+1 < 4 else 0] if mini_cubo in quartetos["x_superior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["y_superior"])]
                    quartetos["y_inferior"] = [quartetos["x_superior"][quartetos["x_superior"].index(mini_cubo)+1 if quartetos["x_superior"].index(mini_cubo)+1 < 4 else 0] if mini_cubo in quartetos["x_superior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["y_inferior"])]
                    quartetos["z_superior"] = [quartetos["x_superior"][quartetos["x_superior"].index(mini_cubo)+1 if quartetos["x_superior"].index(mini_cubo)+1 < 4 else 0] if mini_cubo in quartetos["x_superior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["z_superior"])]
                    quartetos["z_inferior"] = [quartetos["x_superior"][quartetos["x_superior"].index(mini_cubo)+1 if quartetos["x_superior"].index(mini_cubo)+1 < 4 else 0] if mini_cubo in quartetos["x_superior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["z_inferior"])]
                if event.key == K_i: # rotaciona eixo x sentido horario lado superior
                    print("Tecla i")
                    for mini_cubo in quartetos["x_superior"]:
                        angulos[mini_cubo][0] = 315 if angulos[mini_cubo][0] - 90 <= 0 else angulos[mini_cubo][0] - 90
                    #atualiza mapa dos minicubos
                    quartetos["x_superior"] = [quartetos["x_superior"][i+1 if i+1 < 4 else 0] for i, mini_cubo in enumerate(quartetos["x_superior"])]
                    quartetos["y_superior"] = [quartetos["x_superior"][quartetos["x_superior"].index(mini_cubo)-1 if quartetos["x_superior"].index(mini_cubo)-1 < 4 else 0] if mini_cubo in quartetos["x_superior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["y_superior"])]
                    quartetos["y_inferior"] = [quartetos["x_superior"][quartetos["x_superior"].index(mini_cubo)-1 if quartetos["x_superior"].index(mini_cubo)-1 < 4 else 0] if mini_cubo in quartetos["x_superior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["y_inferior"])]
                    quartetos["z_superior"] = [quartetos["x_superior"][quartetos["x_superior"].index(mini_cubo)-1 if quartetos["x_superior"].index(mini_cubo)-1 < 4 else 0] if mini_cubo in quartetos["x_superior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["z_superior"])]
                    quartetos["z_inferior"] = [quartetos["x_superior"][quartetos["x_superior"].index(mini_cubo)-1 if quartetos["x_superior"].index(mini_cubo)-1 < 4 else 0] if mini_cubo in quartetos["x_superior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["z_inferior"])]
                if event.key == K_f: # rotaciona eixo x sentido anti horario lado inferior
                    print("Tecla F")
                    for mini_cubo in quartetos["x_inferior"]:
                        angulos[mini_cubo][0] = 45 if angulos[mini_cubo][0] + 90 >= 360 else angulos[mini_cubo][0] + 90
                    #atualiza mapa dos minicubos
                    quartetos["x_inferior"] = [quartetos["x_inferior"][i-1 if i-1 < 4 else 0] for i, mini_cubo in enumerate(quartetos["x_inferior"])]
                    quartetos["y_superior"] = [quartetos["x_inferior"][quartetos["x_inferior"].index(mini_cubo)+1 if quartetos["x_inferior"].index(mini_cubo)+1 < 4 else 0] if mini_cubo in quartetos["x_inferior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["y_superior"])]
                    quartetos["y_inferior"] = [quartetos["x_inferior"][quartetos["x_inferior"].index(mini_cubo)+1 if quartetos["x_inferior"].index(mini_cubo)+1 < 4 else 0] if mini_cubo in quartetos["x_inferior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["y_inferior"])]
                    quartetos["z_superior"] = [quartetos["x_inferior"][quartetos["x_inferior"].index(mini_cubo)+1 if quartetos["x_inferior"].index(mini_cubo)+1 < 4 else 0] if mini_cubo in quartetos["x_inferior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["z_superior"])]
                    quartetos["z_inferior"] = [quartetos["x_inferior"][quartetos["x_inferior"].index(mini_cubo)+1 if quartetos["x_inferior"].index(mini_cubo)+1 < 4 else 0] if mini_cubo in quartetos["x_inferior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["z_inferior"])]
                if event.key == K_j: # rotaciona eixo x sentido horario lado inferior
                    print("Tecla J")
                    for mini_cubo in quartetos["x_inferior"]:
                        angulos[mini_cubo][0] = 315 if angulos[mini_cubo][0] - 90 <= 0 else angulos[mini_cubo][0] - 90
                    #atualiza mapa dos minicubos
                    quartetos["x_inferior"] = [quartetos["x_inferior"][i+1 if i+1 < 4 else 0] for i, mini_cubo in enumerate(quartetos["x_inferior"])]
                    quartetos["y_superior"] = [quartetos["x_inferior"][quartetos["x_inferior"].index(mini_cubo)-1 if quartetos["x_inferior"].index(mini_cubo)-1 < 4 else 0] if mini_cubo in quartetos["x_inferior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["y_superior"])]
                    quartetos["y_inferior"] = [quartetos["x_inferior"][quartetos["x_inferior"].index(mini_cubo)-1 if quartetos["x_inferior"].index(mini_cubo)-1 < 4 else 0] if mini_cubo in quartetos["x_inferior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["y_inferior"])]
                    quartetos["z_superior"] = [quartetos["x_inferior"][quartetos["x_inferior"].index(mini_cubo)-1 if quartetos["x_inferior"].index(mini_cubo)-1 < 4 else 0] if mini_cubo in quartetos["x_inferior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["z_superior"])]
                    quartetos["z_inferior"] = [quartetos["x_inferior"][quartetos["x_inferior"].index(mini_cubo)-1 if quartetos["x_inferior"].index(mini_cubo)-1 < 4 else 0] if mini_cubo in quartetos["x_inferior"] else mini_cubo for i, mini_cubo in enumerate(quartetos["z_inferior"])]
                for i in quartetos:
                    print(quartetos[i])
                print("-----------------------------\n")
                for i in angulos:
                    print(i)
                print("=============================\n")

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
        mini_cubo_0.desenha()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(pos_x, pos_y, pos_z)
        glRotatef(angulos[1][0], 1, 0, 0)
        glRotatef(angulos[1][1], 0, 1, 0)
        glRotatef(angulos[1][2], 0, 0, 1)
        mini_cubo_1.desenha()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(pos_x, pos_y, pos_z)
        glRotatef(angulos[2][0], 1, 0, 0)
        glRotatef(angulos[2][1], 0, 1, 0)
        glRotatef(angulos[2][2], 0, 0, 1)
        mini_cubo_2.desenha()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(pos_x, pos_y, pos_z)
        glRotatef(angulos[3][0], 1, 0, 0)
        glRotatef(angulos[3][1], 0, 1, 0)
        glRotatef(angulos[3][2], 0, 0, 1)
        mini_cubo_3.desenha()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(pos_x, pos_y, pos_z)
        glRotatef(angulos[4][0], 1, 0, 0)
        glRotatef(angulos[4][1], 0, 1, 0)
        glRotatef(angulos[4][2], 0, 0, 1)
        mini_cubo_4.desenha()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(pos_x, pos_y, pos_z)
        glRotatef(angulos[5][0], 1, 0, 0)
        glRotatef(angulos[5][1], 0, 1, 0)
        glRotatef(angulos[5][2], 0, 0, 1)
        mini_cubo_5.desenha()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(pos_x, pos_y, pos_z)
        glRotatef(angulos[6][0], 1, 0, 0)
        glRotatef(angulos[6][1], 0, 1, 0)
        glRotatef(angulos[6][2], 0, 0, 1)
        mini_cubo_6.desenha()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(pos_x, pos_y, pos_z)
        glRotatef(angulos[7][0], 1, 0, 0)
        glRotatef(angulos[7][1], 0, 1, 0)
        glRotatef(angulos[7][2], 0, 0, 1)
        mini_cubo_7.desenha()
        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main() 