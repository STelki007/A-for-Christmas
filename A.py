import pygame
import heapq
import random

TILE_SIZE = 25
GRID_WIDTH = 25
GRID_HEIGHT = 25
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE


class Area:

    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.path = []
        self.start = None
        self.end = None

    def set_value(self, x, y, value):
        if not self._in_bounds(x, y):
            return
        self.grid[y][x] = value

    def get_value(self, x, y):
        if not self._in_bounds(x, y):
            return None
        return self.grid[y][x]

    def _in_bounds(self, x, y):
        return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT

    def _manhattan_distance(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def _get_neighbors(self, x, y):
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self._in_bounds(nx, ny) and self.grid[ny][nx] == 0:
                neighbors.append((nx, ny))

        return neighbors

    def get_path(self, start_x: int, start_y: int, end_x: int, end_y: int) -> tuple[tuple[int, int]]:
        if not self._in_bounds(start_x, start_y):
            raise IndexError(f"Startkoordinate ({start_x}, {start_y}) liegt außerhalb des Rasters")
        if not self._in_bounds(end_x, end_y):
            raise IndexError(f"Zielkoordinate ({end_x}, {end_y}) liegt außerhalb des Rasters")

        if self.grid[start_y][start_x] == 1:
            raise IndexError(f"Startkoordinate ({start_x}, {start_y}) ist belegt")
        if self.grid[end_y][end_x] == 1:
            raise IndexError(f"Zielkoordinate ({end_x}, {end_y}) ist belegt")

        open_set = []
        heapq.heappush(open_set, (0, start_x, start_y))

        came_from = {}
        g_score = {(start_x, start_y): 0}
        f_score = {(start_x, start_y): self._manhattan_distance(start_x, start_y, end_x, end_y)}

        while open_set:
            _, current_x, current_y = heapq.heappop(open_set)

            if current_x == end_x and current_y == end_y:
                path = []
                while (current_x, current_y) in came_from:
                    path.append((current_x, current_y))
                    current_x, current_y = came_from[(current_x, current_y)]
                path.append((start_x, start_y))
                path.reverse()
                return tuple(path)

            for neighbor_x, neighbor_y in self._get_neighbors(current_x, current_y):
                tentative_g_score = g_score[(current_x, current_y)] + 1

                if (neighbor_x, neighbor_y) not in g_score or tentative_g_score < g_score[(neighbor_x, neighbor_y)]:
                    came_from[(neighbor_x, neighbor_y)] = (current_x, current_y)
                    g_score[(neighbor_x, neighbor_y)] = tentative_g_score
                    f_score[(neighbor_x, neighbor_y)] = tentative_g_score + self._manhattan_distance(neighbor_x,
                                                                                                     neighbor_y, end_x,
                                                                                                     end_y)
                    heapq.heappush(open_set, (f_score[(neighbor_x, neighbor_y)], neighbor_x, neighbor_y))

        return tuple()

    def generate_maze(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                self.grid[y][x] = 1

        start_x = random.randrange(0, GRID_WIDTH, 2)
        start_y = random.randrange(0, GRID_HEIGHT, 2)
        self.grid[start_y][start_x] = 0

        walls = []

        def add_walls(x, y):
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                wx, wy = x + dx // 2, y + dy // 2
                if self._in_bounds(nx, ny) and self.grid[ny][nx] == 1:
                    walls.append((wx, wy, nx, ny))

        add_walls(start_x, start_y)

        while walls:
            wx, wy, nx, ny = random.choice(walls)
            walls.remove((wx, wy, nx, ny))

            if self.grid[ny][nx] == 1:
                self.grid[wy][wx] = 0
                self.grid[ny][nx] = 0
                add_walls(nx, ny)

    def draw(self, surface):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                value = self.grid[y][x]

                if value == 0:
                    color = (200, 200, 200)
                elif value == 1:
                    color = (60, 60, 60)
                else:
                    color = (100, 255, 100)

                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, (50, 50, 50), rect, 1)

        for i, (px, py) in enumerate(self.path):
            rect = pygame.Rect(px * TILE_SIZE + 5, py * TILE_SIZE + 5, TILE_SIZE - 10, TILE_SIZE - 10)
            t = i / max(1, len(self.path) - 1)
            color = (int(100 + 155 * t), int(200 - 100 * t), 100)
            pygame.draw.rect(surface, color, rect, 0, 5)

        if self.start:
            pygame.draw.circle(surface, (0, 255, 0),
                               (self.start[0] * TILE_SIZE + TILE_SIZE // 2,
                                self.start[1] * TILE_SIZE + TILE_SIZE // 2), 8)
        if self.end:
            pygame.draw.circle(surface, (255, 0, 0),
                               (self.end[0] * TILE_SIZE + TILE_SIZE // 2,
                                self.end[1] * TILE_SIZE + TILE_SIZE // 2), 8)


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Weihnachtsmann Wegfindung - [M]aze, [C]lear, [S]tart, [E]nde")
clock = pygame.time.Clock()

area = Area()
running = True
mode = 'wall'

print("Steuerung:")
print("  Linke Maustaste: Wand setzen")
print("  Rechte Maustaste: Wand entfernen")
print("  M-Taste: Labyrinth generieren")
print("  C-Taste: Alles löschen")
print("  S-Taste: Startpunkt-Modus")
print("  E-Taste: Endpunkt-Modus")
print("  Leertaste: Pfad berechnen")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            gx = mx // TILE_SIZE
            gy = my // TILE_SIZE

            if mode == 'start':
                area.start = (gx, gy)
                area.set_value(gx, gy, 0)
            elif mode == 'end':
                area.end = (gx, gy)
                area.set_value(gx, gy, 0)
            else:
                area.set_value(gx, gy, 1)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mx, my = pygame.mouse.get_pos()
            gx = mx // TILE_SIZE
            gy = my // TILE_SIZE
            area.set_value(gx, gy, 0)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                area.generate_maze()
                area.path = []
                print("Labyrinth generiert!")

            elif event.key == pygame.K_c:
                area = Area()
                print("Raster gelöscht!")

            elif event.key == pygame.K_s:
                mode = 'start'
                print("Startpunkt-Modus aktiviert - Klicke auf ein Feld")

            elif event.key == pygame.K_e:
                mode = 'end'
                print("Endpunkt-Modus aktiviert - Klicke auf ein Feld")

            elif event.key == pygame.K_SPACE:
                if area.start and area.end:
                    try:
                        path = area.get_path(area.start[0], area.start[1],
                                             area.end[0], area.end[1])
                        area.path = list(path)
                        print(f"Pfad gefunden mit {len(path)} Schritten!")
                    except IndexError as e:
                        print(f"Fehler: {e}")
                        area.path = []
                else:
                    print("Bitte Start (S) und Ende (E) festlegen!")

                mode = 'wall'

    screen.fill((0, 0, 0))
    area.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()