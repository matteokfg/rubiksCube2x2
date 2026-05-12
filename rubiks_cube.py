import math
import random
import sys
from collections import deque
from dataclasses import dataclass

pygame = None
gl = None
glu = None

Vector = tuple[int, int, int]

FACE_COLORS = {
    "U": (0.98, 0.96, 0.88),
    "D": (1.00, 0.82, 0.05),
    "R": (0.88, 0.03, 0.02),
    "L": (1.00, 0.34, 0.02),
    "F": (0.02, 0.18, 0.85),
    "B": (0.02, 0.55, 0.20),
}

FACE_DEFS = {
    "R": {"axis": 0, "layer": 1, "normal": (1, 0, 0)},
    "L": {"axis": 0, "layer": -1, "normal": (-1, 0, 0)},
    "U": {"axis": 1, "layer": 1, "normal": (0, 1, 0)},
    "D": {"axis": 1, "layer": -1, "normal": (0, -1, 0)},
    "F": {"axis": 2, "layer": 1, "normal": (0, 0, 1)},
    "B": {"axis": 2, "layer": -1, "normal": (0, 0, -1)},
}

NORMAL_TO_FACE = {
    (0, 1, 0): "U",
    (0, -1, 0): "D",
    (1, 0, 0): "R",
    (-1, 0, 0): "L",
    (0, 0, 1): "F",
    (0, 0, -1): "B",
}

MOVE_KEYS = {
    "u": "U",
    "d": "D",
    "r": "R",
    "l": "L",
    "f": "F",
    "b": "B",
}

CUBIE_HALF = 0.47
CUBIE_CENTER = 0.515
STICKER_BORDER = 0.385
STICKER_HALF = 0.335
TURN_SPEED = 360.0


@dataclass
class Cubie:
    position: Vector
    stickers: dict[Vector, str]


@dataclass
class TurnAnimation:
    move: str
    quarter_turns: int
    record_history: bool
    angle: float = 0.0
    finished: bool = False

    @property
    def axis(self) -> int:
        return FACE_DEFS[self.move]["axis"]

    @property
    def layer(self) -> int:
        return FACE_DEFS[self.move]["layer"]

    @property
    def target_angle(self) -> float:
        return 90.0 * self.quarter_turns

    def update(self, dt: float) -> None:
        if self.finished:
            return

        target = self.target_angle
        direction = 1.0 if target > self.angle else -1.0
        self.angle += direction * TURN_SPEED * dt

        if (direction > 0 and self.angle >= target) or (
            direction < 0 and self.angle <= target
        ):
            self.angle = target
            self.finished = True


class RubiksCube2x2:
    def __init__(self) -> None:
        self.cubies: list[Cubie] = []
        self.move_history: list[str] = []
        self.move_queue: deque[tuple[str, int, bool]] = deque()
        self.animation: TurnAnimation | None = None
        self.reset()

    def reset(self) -> None:
        self.cubies = []
        for x in (-1, 1):
            for y in (-1, 1):
                for z in (-1, 1):
                    stickers = {}
                    for normal, face_name in NORMAL_TO_FACE.items():
                        axis_value = (x, y, z)[axis_index(normal)]
                        if axis_value == signed_axis(normal):
                            stickers[normal] = face_name
                    self.cubies.append(Cubie((x, y, z), stickers))

        self.move_history.clear()
        self.move_queue.clear()
        self.animation = None

    def enqueue_move(self, move: str, inverse: bool = False, record_history: bool = True) -> None:
        base_move = move.upper()
        if base_move not in FACE_DEFS:
            return

        layer = FACE_DEFS[base_move]["layer"]
        clockwise_quarter_turn = -layer
        quarter_turns = -clockwise_quarter_turn if inverse else clockwise_quarter_turn
        self.move_queue.append((base_move, quarter_turns, record_history))

    def enqueue_algorithm(self, moves: list[str], record_history: bool = True) -> None:
        for move in moves:
            inverse = move.endswith("'")
            self.enqueue_move(move[0], inverse=inverse, record_history=record_history)

    def scramble(self, length: int = 18) -> None:
        options = list(FACE_DEFS)
        generated = []
        previous = None

        for _ in range(length):
            move = random.choice(options)
            while previous and FACE_DEFS[move]["axis"] == FACE_DEFS[previous]["axis"]:
                move = random.choice(options)
            previous = move
            if random.choice((False, True)):
                move += "'"
            generated.append(move)

        self.enqueue_algorithm(generated)

    def undo_last_move(self) -> None:
        if not self.move_history:
            return

        last_move = self.move_history.pop()
        self.enqueue_move(last_move[0], inverse=not last_move.endswith("'"), record_history=False)

    def update(self, dt: float) -> None:
        if self.animation is None and self.move_queue:
            move, quarter_turns, record_history = self.move_queue.popleft()
            self.animation = TurnAnimation(move, quarter_turns, record_history)

        if self.animation is None:
            return

        self.animation.update(dt)
        if not self.animation.finished:
            return

        self.apply_turn(self.animation.move, self.animation.quarter_turns)
        if self.animation.record_history:
            self.move_history.append(format_move(self.animation.move, self.animation.quarter_turns))
        self.animation = None

    def apply_turn(self, move: str, quarter_turns: int) -> None:
        face = FACE_DEFS[move]
        axis = face["axis"]
        layer = face["layer"]

        for cubie in self.cubies:
            if cubie.position[axis] != layer:
                continue

            cubie.position = rotate_vector(cubie.position, axis, quarter_turns)
            cubie.stickers = {
                rotate_vector(normal, axis, quarter_turns): color
                for normal, color in cubie.stickers.items()
            }

    def is_solved(self) -> bool:
        for face_name, face in FACE_DEFS.items():
            axis = face["axis"]
            layer = face["layer"]
            normal = face["normal"]
            for cubie in self.cubies:
                if cubie.position[axis] == layer and cubie.stickers.get(normal) != face_name:
                    return False
        return True

    def state_signature(self) -> tuple:
        return tuple(
            sorted(
                (cubie.position, tuple(sorted(cubie.stickers.items())))
                for cubie in self.cubies
            )
        )


def axis_index(vector: Vector) -> int:
    return next(index for index, value in enumerate(vector) if value != 0)


def signed_axis(vector: Vector) -> int:
    return vector[axis_index(vector)]


def rotate_vector(vector: Vector, axis: int, quarter_turns: int) -> Vector:
    x, y, z = vector
    for _ in range(quarter_turns % 4):
        if axis == 0:
            y, z = -z, y
        elif axis == 1:
            x, z = z, -x
        else:
            x, y = -y, x
    return x, y, z


def format_move(move: str, quarter_turns: int) -> str:
    return move if quarter_turns == -FACE_DEFS[move]["layer"] else f"{move}'"


def inverse_algorithm(moves: list[str]) -> list[str]:
    inverse = []
    for move in reversed(moves):
        inverse.append(move[0] if move.endswith("'") else move + "'")
    return inverse


def load_graphics_dependencies() -> None:
    global pygame, gl, glu

    import pygame as pygame_module
    from OpenGL import GL as gl_module
    from OpenGL import GLU as glu_module

    pygame = pygame_module
    gl = gl_module
    glu = glu_module


def setup_display(size: tuple[int, int]) -> None:
    pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)
    pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
    pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
    pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)
    pygame.display.set_caption(
        "2x2 Rubik's Cube | U D R L F B | Shift=inverso | Mouse=girar | Espaco=embaralhar"
    )


def configure_projection(width: int, height: int) -> None:
    gl.glViewport(0, 0, width, height)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    glu.gluPerspective(42.0, width / max(1, height), 0.1, 80.0)
    gl.glMatrixMode(gl.GL_MODELVIEW)


def configure_scene() -> None:
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glDepthFunc(gl.GL_LEQUAL)
    gl.glEnable(gl.GL_MULTISAMPLE)
    gl.glShadeModel(gl.GL_SMOOTH)

    gl.glEnable(gl.GL_LIGHTING)
    gl.glEnable(gl.GL_LIGHT0)
    gl.glEnable(gl.GL_LIGHT1)
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, (4.0, 6.0, 7.0, 1.0))
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, (0.95, 0.92, 0.85, 1.0))
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_SPECULAR, (0.95, 0.95, 0.92, 1.0))
    gl.glLightfv(gl.GL_LIGHT1, gl.GL_POSITION, (-4.0, 2.5, -3.0, 1.0))
    gl.glLightfv(gl.GL_LIGHT1, gl.GL_DIFFUSE, (0.20, 0.28, 0.42, 1.0))
    gl.glLightfv(gl.GL_LIGHT1, gl.GL_SPECULAR, (0.10, 0.12, 0.16, 1.0))
    gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, (0.18, 0.18, 0.20, 1.0))
    gl.glLightModeli(gl.GL_LIGHT_MODEL_TWO_SIDE, gl.GL_TRUE)

    gl.glEnable(gl.GL_COLOR_MATERIAL)
    gl.glColorMaterial(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE)
    gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_SPECULAR, (0.35, 0.35, 0.35, 1.0))
    gl.glMaterialf(gl.GL_FRONT_AND_BACK, gl.GL_SHININESS, 48.0)


def set_material(color: tuple[float, float, float], specular: float, shininess: float) -> None:
    gl.glColor3f(*color)
    gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_SPECULAR, (specular, specular, specular, 1.0))
    gl.glMaterialf(gl.GL_FRONT_AND_BACK, gl.GL_SHININESS, shininess)


def draw_background() -> None:
    gl.glDisable(gl.GL_DEPTH_TEST)
    gl.glDisable(gl.GL_LIGHTING)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glPushMatrix()
    gl.glLoadIdentity()
    gl.glOrtho(0, 1, 0, 1, -1, 1)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glPushMatrix()
    gl.glLoadIdentity()

    gl.glBegin(gl.GL_QUADS)
    gl.glColor3f(0.055, 0.060, 0.070)
    gl.glVertex2f(0, 0)
    gl.glVertex2f(1, 0)
    gl.glColor3f(0.17, 0.19, 0.22)
    gl.glVertex2f(1, 1)
    gl.glVertex2f(0, 1)
    gl.glEnd()

    gl.glPopMatrix()
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glPopMatrix()
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glEnable(gl.GL_LIGHTING)
    gl.glEnable(gl.GL_DEPTH_TEST)


def draw_floor() -> None:
    gl.glDisable(gl.GL_LIGHTING)
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    gl.glColor4f(0.05, 0.055, 0.065, 0.72)
    gl.glBegin(gl.GL_QUADS)
    gl.glVertex3f(-3.8, -1.34, -3.4)
    gl.glVertex3f(3.8, -1.34, -3.4)
    gl.glVertex3f(3.8, -1.34, 3.4)
    gl.glVertex3f(-3.8, -1.34, 3.4)
    gl.glEnd()

    gl.glBegin(gl.GL_TRIANGLE_FAN)
    gl.glColor4f(0.0, 0.0, 0.0, 0.33)
    gl.glVertex3f(0.0, -1.32, 0.0)
    segments = 48
    for index in range(segments + 1):
        angle = 2.0 * math.pi * index / segments
        gl.glColor4f(0.0, 0.0, 0.0, 0.0)
        gl.glVertex3f(math.cos(angle) * 2.05, -1.32, math.sin(angle) * 1.55)
    gl.glEnd()

    gl.glDisable(gl.GL_BLEND)
    gl.glEnable(gl.GL_LIGHTING)


def draw_cube(cube: RubiksCube2x2) -> None:
    animation = cube.animation
    for cubie in cube.cubies:
        gl.glPushMatrix()
        if animation and cubie.position[animation.axis] == animation.layer:
            axis_vector = [0.0, 0.0, 0.0]
            axis_vector[animation.axis] = 1.0
            gl.glRotatef(animation.angle, *axis_vector)
        draw_cubie(cubie)
        gl.glPopMatrix()


def draw_cubie(cubie: Cubie) -> None:
    center = tuple(component * CUBIE_CENTER for component in cubie.position)
    draw_body(center)

    for normal, face_name in cubie.stickers.items():
        draw_sticker_base(center, normal)
        draw_sticker(center, normal, FACE_COLORS[face_name])

    draw_body_edges(center)


def draw_body(center: tuple[float, float, float]) -> None:
    x, y, z = center
    h = CUBIE_HALF
    faces = (
        ((1, 0, 0), ((h, -h, -h), (h, -h, h), (h, h, h), (h, h, -h))),
        ((-1, 0, 0), ((-h, -h, h), (-h, -h, -h), (-h, h, -h), (-h, h, h))),
        ((0, 1, 0), ((-h, h, -h), (h, h, -h), (h, h, h), (-h, h, h))),
        ((0, -1, 0), ((-h, -h, h), (h, -h, h), (h, -h, -h), (-h, -h, -h))),
        ((0, 0, 1), ((-h, -h, h), (-h, h, h), (h, h, h), (h, -h, h))),
        ((0, 0, -1), ((h, -h, -h), (h, h, -h), (-h, h, -h), (-h, -h, -h))),
    )

    set_material((0.015, 0.016, 0.018), 0.55, 64.0)
    gl.glBegin(gl.GL_QUADS)
    for normal, vertices in faces:
        gl.glNormal3f(*normal)
        for vertex in vertices:
            gl.glVertex3f(x + vertex[0], y + vertex[1], z + vertex[2])
    gl.glEnd()


def draw_sticker_base(center: tuple[float, float, float], normal: Vector) -> None:
    set_material((0.004, 0.004, 0.005), 0.35, 32.0)
    draw_face_square(center, normal, STICKER_BORDER, CUBIE_HALF + 0.007)


def draw_sticker(
    center: tuple[float, float, float],
    normal: Vector,
    color: tuple[float, float, float],
) -> None:
    set_material(color, 0.18, 22.0)
    draw_face_square(center, normal, STICKER_HALF, CUBIE_HALF + 0.017)

    lighter = tuple(min(1.0, channel + 0.16) for channel in color)
    gl.glDisable(gl.GL_LIGHTING)
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    draw_face_square(center, normal, STICKER_HALF * 0.45, CUBIE_HALF + 0.02, lighter, 0.16, (-0.12, 0.12))
    gl.glDisable(gl.GL_BLEND)
    gl.glEnable(gl.GL_LIGHTING)


def draw_face_square(
    center: tuple[float, float, float],
    normal: Vector,
    half_size: float,
    offset: float,
    color: tuple[float, float, float] | None = None,
    alpha: float = 1.0,
    local_offset: tuple[float, float] = (0.0, 0.0),
) -> None:
    if color:
        gl.glColor4f(color[0], color[1], color[2], alpha)

    normal_f = tuple(float(value) for value in normal)
    u, v = face_basis(normal)
    cx, cy, cz = center
    ox, oy = local_offset

    face_center = (
        cx + normal_f[0] * offset + u[0] * ox + v[0] * oy,
        cy + normal_f[1] * offset + u[1] * ox + v[1] * oy,
        cz + normal_f[2] * offset + u[2] * ox + v[2] * oy,
    )

    vertices = []
    for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        vertices.append(
            (
                face_center[0] + u[0] * half_size * su + v[0] * half_size * sv,
                face_center[1] + u[1] * half_size * su + v[1] * half_size * sv,
                face_center[2] + u[2] * half_size * su + v[2] * half_size * sv,
            )
        )

    gl.glBegin(gl.GL_QUADS)
    gl.glNormal3f(*normal_f)
    for vertex in vertices:
        gl.glVertex3f(*vertex)
    gl.glEnd()


def face_basis(normal: Vector) -> tuple[Vector, Vector]:
    if normal[0]:
        return (0, 1, 0), (0, 0, 1)
    if normal[1]:
        return (1, 0, 0), (0, 0, 1)
    return (1, 0, 0), (0, 1, 0)


def draw_body_edges(center: tuple[float, float, float]) -> None:
    x, y, z = center
    h = CUBIE_HALF + 0.002
    vertices = [
        (x - h, y - h, z - h),
        (x + h, y - h, z - h),
        (x + h, y + h, z - h),
        (x - h, y + h, z - h),
        (x - h, y - h, z + h),
        (x + h, y - h, z + h),
        (x + h, y + h, z + h),
        (x - h, y + h, z + h),
    ]
    edges = (
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7),
    )

    gl.glDisable(gl.GL_LIGHTING)
    gl.glColor3f(0.0, 0.0, 0.0)
    gl.glLineWidth(1.6)
    gl.glBegin(gl.GL_LINES)
    for a, b in edges:
        gl.glVertex3f(*vertices[a])
        gl.glVertex3f(*vertices[b])
    gl.glEnd()
    gl.glEnable(gl.GL_LIGHTING)


def handle_key(event, cube: RubiksCube2x2, view: dict[str, float]) -> bool:
    if event.key == pygame.K_ESCAPE:
        return False

    key_name = pygame.key.name(event.key).lower()
    inverse = bool(event.mod & pygame.KMOD_SHIFT)

    if key_name in MOVE_KEYS:
        cube.enqueue_move(MOVE_KEYS[key_name], inverse=inverse)
    elif event.key == pygame.K_SPACE:
        cube.scramble()
    elif event.key == pygame.K_BACKSPACE:
        cube.reset()
    elif event.key == pygame.K_TAB:
        cube.undo_last_move()
    elif event.key == pygame.K_LEFT:
        view["y"] -= 8.0
    elif event.key == pygame.K_RIGHT:
        view["y"] += 8.0
    elif event.key == pygame.K_UP:
        view["x"] -= 8.0
    elif event.key == pygame.K_DOWN:
        view["x"] += 8.0

    return True


def update_caption(cube: RubiksCube2x2) -> None:
    solved = "resolvido" if cube.is_solved() else "embaralhado"
    queued = len(cube.move_queue) + (1 if cube.animation else 0)
    pygame.display.set_caption(
        "2x2 Rubik's Cube | "
        "U D R L F B | Shift=inverso | Mouse=girar | Espaco=embaralhar | "
        f"Estado: {solved} | Fila: {queued}"
    )


def run_app() -> None:
    load_graphics_dependencies()
    pygame.init()

    size = (1000, 760)
    setup_display(size)
    configure_projection(*size)
    configure_scene()

    clock = pygame.time.Clock()
    cube = RubiksCube2x2()
    view = {"x": 27.0, "y": -38.0, "zoom": -6.2}
    dragging = False
    last_caption_update = 0

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                size = (max(360, event.w), max(300, event.h))
                setup_display(size)
                configure_projection(*size)
                configure_scene()
            elif event.type == pygame.KEYDOWN:
                running = handle_key(event, cube, view)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging = True
                elif event.button == 4:
                    view["zoom"] = min(-3.4, view["zoom"] + 0.35)
                elif event.button == 5:
                    view["zoom"] = max(-10.0, view["zoom"] - 0.35)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                dx, dy = event.rel
                view["y"] += dx * 0.45
                view["x"] += dy * 0.45
                view["x"] = max(-80.0, min(80.0, view["x"]))

        cube.update(dt)

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        draw_background()

        gl.glLoadIdentity()
        gl.glTranslatef(0.0, 0.0, view["zoom"])
        gl.glRotatef(view["x"], 1.0, 0.0, 0.0)
        gl.glRotatef(view["y"], 0.0, 1.0, 0.0)

        draw_floor()
        draw_cube(cube)

        now = pygame.time.get_ticks()
        if now - last_caption_update > 250:
            update_caption(cube)
            last_caption_update = now

        pygame.display.flip()

    pygame.quit()


def run_self_tests() -> None:
    cube = RubiksCube2x2()
    solved = cube.state_signature()

    for move in FACE_DEFS:
        cube.reset()
        cube.apply_turn(move, -FACE_DEFS[move]["layer"])
        cube.apply_turn(move, FACE_DEFS[move]["layer"])
        assert cube.state_signature() == solved, f"{move} inverse failed"

        cube.reset()
        for _ in range(4):
            cube.apply_turn(move, -FACE_DEFS[move]["layer"])
        assert cube.state_signature() == solved, f"{move} four turns failed"

    algorithm = ["R", "U", "F'", "L", "D'", "B", "R'"]
    cube.reset()
    for move in algorithm + inverse_algorithm(algorithm):
        quarter_turns = FACE_DEFS[move[0]]["layer"] if move.endswith("'") else -FACE_DEFS[move[0]]["layer"]
        cube.apply_turn(move[0], quarter_turns)
    assert cube.state_signature() == solved, "algorithm inverse failed"

    for move in FACE_DEFS:
        for inverse in (False, True):
            cube.reset()
            cube.enqueue_move(move, inverse=inverse)
            flush_move_queue(cube)
            cube.undo_last_move()
            flush_move_queue(cube)
            assert cube.state_signature() == solved, f"{move} undo failed"

    print("Mecanicas OK: inversos, quatro giros, algoritmo reverso e undo passaram.")


def flush_move_queue(cube: RubiksCube2x2) -> None:
    while cube.move_queue or cube.animation:
        cube.update(1.0)


if __name__ == "__main__":
    if "--test" in sys.argv:
        run_self_tests()
    else:
        run_app()
