import math
import numpy as np
from pygame.locals import *
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
# Variáveis globais
pos_x, pos_y, pos_z = 0, 0, -10


escala_obj = 0.1

class Cubie:
    def __init__(self, initial_pos, colors):
        """
        initial_pos: tupla ou lista com (x, y, z) iniciais. Ex: (1, 1, 1)
        colors: dicionário ou lista com as cores das 6 faces.
        """
        # Posição de origem (nunca muda, usada para a renderização)
        self.initial_pos = np.array(initial_pos, dtype=float)
        
        # Posição atual (muda a cada movimento, usada para selecionar a peça)
        self.current_pos = np.array(initial_pos, dtype=float)
        
        # Matriz Identidade 4x4 - Começa sem nenhuma rotação
        self.transform_matrix = np.identity(4, dtype=float)
        
        self.colors = colors
        self.size = 0.98 # Levemente menor que 1.0 para criar a "linha preta" entre as peças

    def update_state(self, rotation_matrix_4x4):
        """
        Atualiza a matriz de transformação e a posição lógica após um movimento de 90 graus.
        rotation_matrix_4x4: Matriz numpy 4x4 representando a rotação (X, Y ou Z).
        """
        # 1. Atualizar a Matriz de Transformação (Acumular a rotação)
        # Multiplicamos a nova rotação pela matriz atual. 
        # A ordem importa! Global_Rotation @ Current_Matrix
        self.transform_matrix = rotation_matrix_4x4 @ self.transform_matrix
        
        # 2. Atualizar a Posição Lógica Atual
        # Transformamos a posição inicial (x,y,z) usando a NOVA matriz acumulada
        # Para multiplicar um vetor 3D por uma matriz 4x4, adicionamos w=1
        pos_4d = np.array([self.initial_pos[0], self.initial_pos[1], self.initial_pos[2], 1.0])
        new_pos_4d = self.transform_matrix @ pos_4d
        
        # Arredondamos para evitar erros de ponto flutuante (ex: 0.999999 vira 1.0)
        self.current_pos = np.round(new_pos_4d[:3])

    def draw(self, temp_anim_matrix=None):
        """
        Desenha o Cubie na tela usando OpenGL.
        temp_anim_matrix: Matriz 4x4 usada APENAS durante os frames de animação.
        """
        glPushMatrix()
        
        # 1. Aplicar Rotação da Animação (se a face estiver girando neste momento)
        if temp_anim_matrix is not None:
            # OpenGL usa matrizes column-major, por isso transpomos (.T) a matriz do numpy
            glMultMatrixf(temp_anim_matrix.T.astype(np.float32))

        # 2. Aplicar a Rotação Acumulada Permanente do estado da peça
        glMultMatrixf(self.transform_matrix.T.astype(np.float32))
        # 3. Transladar para a posição inicial
        glTranslatef(self.initial_pos[0], self.initial_pos[1], self.initial_pos[2])
        
        # 4. Desenhar o cubo em volta de sua própria origem (0,0,0 local)
        self._draw_geometry()
        
        glPopMatrix()

    def _draw_geometry(self):
        """
        Desenha as 6 faces do cubo usando GL_QUADS.
        Cada vértice é definido de -size/2 até size/2 para manter a peça centralizada.
        """
        s = self.size # / 2.0
        
        # Vértices baseados na origem
        vertices = [
            [[s,-s,-s], [s,s,-s], [-s,s,-s], [-s,-s,-s]], # Trás
            [[s,-s,s], [s,s,s], [-s,s,s], [-s,-s,s]], # Frente
            [[s,-s,s], [s,s,s], [s,s,-s], [s,-s,-s]], #lateral
            [[-s,s,-s], [-s,-s,-s], [-s,-s,s], [-s,s,s]], #lateral
            [[s,s,-s], [s,s,s], [-s,s,s], [-s,s,-s]], #lateral
            [[-s,-s,s], [-s,-s,-s], [s,-s,-s], [s,-s,s]] #lateral
        ]
        
        # Lógica de desenho (simplificada para o exemplo)
        glBegin(GL_QUADS)

        for i, vertice in enumerate(vertices):
            for v, color in zip(vertice, self.colors):
                glColor3fv(self.colors[color])
                glVertex3f(v[0], v[1], v[2])
        
        glEnd()

def get_rotation_matrix_X(angle_degrees):
    rad = math.radians(angle_degrees)
    c = np.cos(rad)
    s = np.sin(rad)
    return np.array([
        [1,  0,  0, 0],
        [0,  c, -s, 0],
        [0,  s,  c, 0],
        [0,  0,  0, 1]
    ])

def get_rotation_matrix_Y(angle_degrees):
    rad = math.radians(angle_degrees)
    c = np.cos(rad)
    s = np.sin(rad)
    return np.array([
        [ c, 0, s, 0],
        [ 0, 1, 0, 0],
        [-s, 0, c, 0],
        [ 0, 0, 0, 1]
    ])

def get_rotation_matrix_Z(angle_degrees):
    rad = math.radians(angle_degrees)
    c = np.cos(rad)
    s = np.sin(rad)
    return np.array([
        [c, -s, 0, 0],
        [s,  c, 0, 0],
        [0,  0, 1, 0],
        [0,  0, 0, 1]
    ])


class Cube:
    def __init__(self):
        self.cubies = []
        self.is_animating = False
        self.animation_progress = 0  # 0 a 90 graus
        self.current_move = None     # Guarda info do movimento atual
        
        # Gerar os 8 cubies
        # Posições: (-1,-1,-1), (-1,-1,1), (-1,1,-1) ... (1,1,1)
        for x in [-1, 1]:
            for y in [-1, 1]:
                for z in [-1, 1]:
                    # Aqui você passaria as cores reais baseadas na posição
                    colors = self._get_colors_for_pos(x, y, z)
                    self.cubies.append(Cubie((x, y, z), colors))

    def _get_colors_for_pos(self, x, y, z):
        # Lógica para definir quais faces do cubinho são coloridas
        # Se x == 1, a face da direita é Vermelha. Se x == -1, a esquerda é Laranja, etc.
        # Cores padrão: U:Branco, D:Amarelo, R:Vermelho, L:Laranja, F:Verde, B:Azul
        return {
            'up':    [1, 1, 1] if y > 0 else [0.1, 0.1, 0.1],
            'down':  [1, 1, 0] if y < 0 else [0.1, 0.1, 0.1],
            'right': [1, 0, 0] if x > 0 else [0.1, 0.1, 0.1],
            'left':  [1, 0.5, 0] if x < 0 else [0.1, 0.1, 0.1],
            'front': [0, 1, 0] if z > 0 else [0.1, 0.1, 0.1],
            'back':  [0, 0, 1] if z < 0 else [0.1, 0.1, 0.1],
        }

    def start_move(self, move_name):
        """
        move_name: 'R', 'L', 'U', 'D', 'F', 'B'
        """
        if self.is_animating: return
        
        # Mapeamento: Face -> (Eixo, Direção, Condição de Seleção)
        # 0:X, 1:Y, 2:Z
        move_map = {
            'R': (0, -1, lambda c: c.current_pos[0] > 0),
            'L': (0,  1, lambda c: c.current_pos[0] < 0),
            'U': (1, -1, lambda c: c.current_pos[1] > 0),
            'D': (1,  1, lambda c: c.current_pos[1] < 0),
            'F': (2, -1, lambda c: c.current_pos[2] > 0),
            'B': (2,  1, lambda c: c.current_pos[2] < 0)
        }
        
        axis, direction, condition = move_map[move_name]
        
        # Seleciona os 4 cubinhos que vão girar
        moving_cubies = [c for c in self.cubies if condition(c)]
        
        self.current_move = {
            'axis': axis,
            'direction': direction,
            'cubies': moving_cubies,
            'angle': 0
        }
        self.is_animating = True

    def update(self, speed=5):
        """ Atualiza o ângulo da animação a cada frame """
        if not self.is_animating: return

        self.current_move['angle'] += speed
        
        if self.current_move['angle'] >= 90:
            # Fim da animação: consolidar o estado físico
            angle = 90 * self.current_move['direction']
            axis = self.current_move['axis']
            
            # Criar a matriz de rotação final de 90 graus
            if axis == 0: rot_mat = get_rotation_matrix_X(angle)
            elif axis == 1: rot_mat = get_rotation_matrix_Y(angle)
            else: rot_mat = get_rotation_matrix_Z(angle)
            
            # Aplicar permanentemente em cada cubie
            for cubie in self.current_move['cubies']:
                cubie.update_state(rot_mat)
                
            self.is_animating = False
            self.current_move = None

    def draw(self):
        for cubie in self.cubies:
            temp_mat = None
            
            # Se este cubie está no meio de um movimento, calcula a matriz temporária
            if self.is_animating and cubie in self.current_move['cubies']:
                angle = self.current_move['angle'] * self.current_move['direction']
                axis = self.current_move['axis']
                if axis == 0: temp_mat = get_rotation_matrix_X(angle)
                elif axis == 1: temp_mat = get_rotation_matrix_Y(angle)
                else: temp_mat = get_rotation_matrix_Z(angle)
            
            cubie.draw(temp_mat)

teste = None

def main():
    global pos_x, pos_y, pos_z, escala_obj, teste
    #global angulos

    cubo = Cube()
   
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
    glShadeModel(GL_FLAT)
    glDisable(GL_LIGHTING)

    print("cheguei aqui")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    teste = 'R'
                if event.key == K_l:
                    teste = 'L'
                if event.key == K_u:
                    teste = 'U'
                if event.key == K_d:
                    teste = 'D'
                if event.key == K_f:
                    teste = 'F'
                if event.key == K_b:
                    teste = 'B'

        # Fundo preto
        glClearColor(0, 0, 0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
       
        glLoadIdentity()
        glTranslatef(pos_x, pos_y, pos_z)
        #print("cheguei aqui 2")
        if teste is not None:
            cubo.start_move(teste)
            print("cheguei aqui 1")

        cubo.draw()

        teste = None
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main() 