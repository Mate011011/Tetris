import pygame
import random
import copy

pygame.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block
block_size = 30
score = 0
running = True
clock = pygame.time.Clock()
placed_pieces = []

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

shapes = [
    [[1, 5, 9, 13], [4, 5, 6, 7]],  # I
    [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],  # J
    [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  # L
    [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  # T
    [[1, 2, 4, 5], [1, 5, 6, 10]],  # S
    [[1, 2, 6, 7], [1, 4, 5, 8]],  # Z
    [[1, 2, 5, 6]]  # O
]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

grid_positions = [(x, y) for y in range(100, 700, 30) for x in range(250, 550, 30)]
grid_p = []
for index, tuple in enumerate(grid_positions):
    if (index + 1) % 10 == 0:
        grid_p.append(grid_positions[index - 9:index + 1])

placed_pieces_coordinates = []


# WINDOW
window = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Tetris")

# SURFACES
tetris_font = pygame.font.Font(None, 40)
tetris_text = tetris_font.render("Tetris", False, "white")


# CLASSES
class Shape:
    def __init__(self, shape):
        self.rotation = 0
        self.past_rotation = 0
        self.shape = shape
        self.colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
        self.rectangles = []
        self.y_level = -20
        self.x_level = 370
        self.placed = False

    def get_rectangle(self):
        for cords in self.shape[self.rotation]:
            self.rectangles.append(pygame.Rect(cords[0], cords[1], 30, 30))

        for c in self.rectangles:
            if (c.y + self.y_level) % 30 == 0:
                c.y += self.y_level
            else:
                c.y += (self.y_level + 20)

            if self.x_level > 370:
                c.x += (self.x_level - 370)
            elif self.x_level < 370:
                c.x -= (370 - self.x_level)

    def draw(self):
        if not self.rectangles or self.rotation == self.past_rotation:
            if len(self.shape) == 2:
                if self.past_rotation == 1:
                    self.past_rotation = 0
                elif self.past_rotation == 0:
                    self.past_rotation = 1
            if len(self.shape) == 1:
                self.past_rotation = 1
            if len(self.shape) == 4:
                if self.past_rotation >= 0 and self.past_rotation < 3:
                    self.past_rotation += 1
                elif self.past_rotation == 3:
                    self.past_rotation = 0
            self.rectangles = []
            self.get_rectangle()

        for x in range(len(self.rectangles)):
            pygame.draw.rect(window, self.colors[pieces.index(self.shape)], self.rectangles[x])
            try:
                self.y_level = self.rectangles[self.rotation].y
                self.x_level = self.rectangles[self.rotation].x
            except:
                pass


# FUNCTIONS
def display_grid(surface):
    for l in range(top_left_x, 550, 30):
        pygame.draw.line(surface, "white", (l, 100), (l, 700), 1)
    for j in range(top_left_y, 700, 30):
        pygame.draw.line(surface, "white", (top_left_x, j), (550, j), 1)
    pygame.draw.rect(surface, "red", (top_left_x, top_left_y, play_width + 1, play_height), 1)


def get_shape(shape):
    shape_cords = []
    for i in shape:
        for s in i:
            if s <= 3:
                shape_cords.append((340 + (30 * s), -20))
            elif s <= 7 and s > 3:
                shape_cords.append((340 + (30 * (s - 4)), 10))
            elif s <= 11 and s > 7:
                shape_cords.append((340 + (30 * (s - 8)), 40))
            elif s <= 15 and s > 11:
                shape_cords.append((340 + (30 * (s - 12)), 70))

    if len(shape_cords) == 4:
        shape_cords = [shape_cords[:4]]
    if len(shape_cords) == 8:
        shape_cords = [shape_cords[:4], shape_cords[4:]]
    if len(shape_cords) == 16:
        shape_cords = [shape_cords[:4], shape_cords[4:8], shape_cords[8:12], shape_cords[12:16]]

    return shape_cords


def collision_right(piece):
    for r in piece.rectangles:
        if r.right == 550:
            return False
    return True


def collision_left(piece):
    for left in piece.rectangles:
        if left.left == 250:
            return False
    return True


def collision_bottom(piece):
    for b in piece.rectangles:
        if b.bottom == 700:
            return False
    return True


def check_position():
    for a in current_piece.rectangles:
        for q in placed_pieces:
            for f in q.rectangles:
                temp_r = pygame.Rect((a.x + 30, a.y), (30, 30))
                if pygame.Rect.colliderect(temp_r, f):
                    if a.right == f.left:
                        return False
                temp_l = pygame.Rect((a.x - 30, a.y), (30, 30))
                if pygame.Rect.colliderect(temp_l, f):
                    if a.left == f.right:
                        return False
                temp_br = pygame.Rect((a.x + 30, a.y + 30), (30, 30))
                if pygame.Rect.colliderect(temp_br, f):
                    if a.right == f.left:
                        return False
                temp_bl = pygame.Rect((a.x - 30, a.y + 30), (30, 30))
                if pygame.Rect.colliderect(temp_bl, f):
                    if a.left == f.right:
                        return False
    return True


def check_position_right():
    for a in current_piece.rectangles:
        for q in placed_pieces:
            for f in q.rectangles:
                temp_r = pygame.Rect((a.x + 30, a.y), (30, 30))
                if pygame.Rect.colliderect(temp_r, f):
                    if a.right == f.left:
                        return False
    return True


def check_position_left():
    for a in current_piece.rectangles:
        for q in placed_pieces:
            for f in q.rectangles:
                temp_l = pygame.Rect((a.x - 30, a.y), (30, 30))
                if pygame.Rect.colliderect(temp_l, f):
                    if a.left == f.right:
                        return False
    return True


def check_lines():
    run_once = 0
    global placed_pieces_coordinates, placed_pieces, score, scoreSurf
    for indexs, line in enumerate(grid_p):
        if all(elem in placed_pieces_coordinates for elem in line):
            for m in placed_pieces:
                for rec in m.rectangles:
                    if (rec.x, rec.y) in line:
                        m.rectangles.remove(rec)
                    if (rec.x, rec.y) in placed_pieces_coordinates:
                        placed_pieces_coordinates.remove((rec.x, rec.y))

            for m in placed_pieces:
                for rec in m.rectangles:
                    if (rec.x, rec.y) in line:
                        m.rectangles.remove(rec)
            for m in placed_pieces:
                for rec in m.rectangles:
                    if (rec.x, rec.y) in line:
                        m.rectangles.remove(rec)
            for m in placed_pieces:
                for rec in m.rectangles:
                    if rec.y < line[0][1]:
                        rec.y += 30

            score += 100
            scoreSurf = scoreFont.render('Score: ' + str(score), False, 'White')

# SURFACES
background = pygame.Surface((1000, 1000))

scoreFont = pygame.font.Font(None, 50)
scoreSurf = scoreFont.render('Score: ' + str(score), False, 'White')

nextPieceFont = pygame.font.Font(None, 50)
nextPieceSurf = nextPieceFont.render("Next", False, "White")

# OBJECTS
I_cords = get_shape(shapes[0])
J_cords = get_shape(shapes[1])
L_cords = get_shape(shapes[2])
T_cords = get_shape(shapes[3])
S_cords = get_shape(shapes[4])
Z_cords = get_shape(shapes[5])
O_cords = get_shape(shapes[6])

pieces = [I_cords, J_cords, L_cords, T_cords, S_cords, Z_cords, O_cords]

current_piece = Shape(random.choice(pieces))
next_piece = Shape(random.choice(pieces))

# EVENTS
fall_timer = pygame.USEREVENT + 1
pygame.time.set_timer(fall_timer, 900)


while True:
    if running:
        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == fall_timer and collision_bottom(current_piece) and not current_piece.placed:
                for rect in current_piece.rectangles:
                    rect.y += 30

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and collision_left(current_piece) and collision_bottom(current_piece) and not current_piece.placed and check_position_left():
                    for rect in current_piece.rectangles:
                        rect.x -= 30

                if event.key == pygame.K_d and collision_right(current_piece) and collision_bottom(current_piece) and not current_piece.placed and check_position_right():
                    for rect in current_piece.rectangles:
                        rect.x += 30

                if event.key == pygame.K_w and collision_bottom(current_piece) and not current_piece.placed and check_position():
                    if len(current_piece.shape) == 1:
                        current_piece.rotation = 0

                    if len(current_piece.shape) == 2:
                        if current_piece.rotation == 0:
                            current_piece.rotation = 1
                        elif current_piece.rotation == 1:
                            current_piece.rotation = 0

                    if len(current_piece.shape) == 4:
                        if current_piece.rotation >= 0 and current_piece.rotation < 4:
                            current_piece.rotation += 1
                        if current_piece.rotation == 4:
                            current_piece.rotation = 0

                if event.key == pygame.K_s and collision_bottom(current_piece) and not current_piece.placed:
                    for rect in current_piece.rectangles:
                        rect.y += 30

        # DISPLAYING
        window.blit(background, (0, 0))
        window.blit(tetris_text, (360, 30))

        window.blit(scoreSurf, (580, 150))
        window.blit(nextPieceSurf, (580, 230))

        for k in next_piece.shape[0]:
            pygame.draw.rect(window, next_piece.colors[pieces.index(next_piece.shape)], pygame.Rect(k[0] + 250, k[1] + 300, 30, 30))

        current_piece.draw()

        for p in placed_pieces:
            p.draw()

        display_grid(window)

        # COLLISION
        for i in current_piece.rectangles:
            if i.left < 250:
                for v in current_piece.rectangles:
                    v.left += 30
            if i.right > 550:
                for g in current_piece.rectangles:
                    g.right -= 30
            if i.bottom > 700:
                for b in current_piece.rectangles:
                    b.bottom -= 30

        for g in placed_pieces:
            for r in g.rectangles:
                for h in current_piece.rectangles:
                    temp_rect = pygame.Rect((h.x, h.y + 30), (30, 30))
                    if pygame.Rect.colliderect(temp_rect, r):
                        if (h.y + 30) - r.top == 0:
                            current_piece.placed = True

        for s in placed_pieces:
            for h in s.rectangles:
                if h.top <= 100:
                    running = False

        check_position()

        check_lines()

        # MANAGING NEXT PIECE
        if not collision_bottom(current_piece):
            current_piece.placed = True

        if current_piece.placed:
            placed_pieces.append(current_piece)
            current_piece = next_piece
            next_piece = Shape(random.choice(pieces))

        if placed_pieces:
            for i in placed_pieces:
                for z in i.rectangles:
                    if (z.x, z.y) not in placed_pieces_coordinates:
                        placed_pieces_coordinates.append((z.x, z.y))

    else:
        pygame.quit()
        exit()
