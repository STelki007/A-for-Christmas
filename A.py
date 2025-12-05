import pygame

# Konstanten
TILE_SIZE = 25
GRID_WIDTH = 25
GRID_HEIGHT = 25
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE


class Area:
    """
    Repräsentiert eine Fläche aus 25x25 Quadraten.
    Jedes Quadrat kann später z.B. Objekte, Farben oder Zustände speichern.
    """
    def __init__(self):
        # 2D-Liste (Matrix) für die Tiles
        # Du kannst hier beliebige Werte speichern (0,1,Farbe,Objekt usw.)
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    def set_value(self, x, y, value):
        """Setzt den Tile-Wert an Position (x,y)."""
        if not self._in_bounds(x, y):
            return
        self.grid[y][x] = value

    def get_value(self, x, y):
        """Gibt den Tile-Wert an Position (x,y) zurück."""
        if not self._in_bounds(x, y):
            return None
        return self.grid[y][x]

    def draw(self, surface):
        """Zeichnet die komplette Area."""
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                value = self.grid[y][x]

                # Farbe abhängig vom Wert
                if value == 0:
                    color = (200, 200, 200)
                elif value == 1:
                    color = (255, 100, 100)
                else:
                    color = (100, 255, 100)

                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, (50, 50, 50), rect, 1)  # Grid-Linien

    def _in_bounds(self, x, y):
        """Überprüft, ob die Koordinaten in der Area liegen."""
        return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT


# -----------------------------------------------------------

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

area = Area()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Linksklick: setze Tile = 1
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            gx = mx // TILE_SIZE
            gy = my // TILE_SIZE
            area.set_value(gx, gy, 1)

        # Rechtsklick: setze Tile = 0
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mx, my = pygame.mouse.get_pos()
            gx = mx // TILE_SIZE
            gy = my // TILE_SIZE
            area.set_value(gx, gy, 0)

    screen.fill((0, 0, 0))
    area.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
