import pygame


class NotLuminousParticle:
    def __init__(self, luminosity: float, position: list[float], base_color: list[int] = [255, 255, 255], base_radius: int = 5):
        self.luminosity = luminosity
        self.base_color = base_color
        self.base_radius = base_radius
        self.REPEAT = 3
        self.PRECISEMENT = 5
        self.position = position
        size = 500
        self.surface = pygame.Surface([size, size], pygame.SRCALPHA)
        self.surf_pos = [0, 0]
        self.render()

    def render(self):
        size = self.surface.get_height()
        self.surf_pos = [self.position[0] - size // 2, self.position[1] - size // 2]
        center = [size//2,size//2]
        max_rep = self.REPEAT * self.PRECISEMENT + 1
        for depth in reversed(range(1, max_rep)):
            opacity = min(int(255 * self.luminosity * (max_rep - depth -1) / max_rep), 255)
            radius = self.base_radius * depth ** 1.4 / max_rep
            pygame.draw.circle(self.surface,
                               [*self.base_color, opacity],
                               center,
                               radius)
            
        self.surface.convert()

    def draw(self, surface: pygame.Surface):
        surface.blit(self.surface, self.surf_pos)
