import pygame



class MouseCircle:
    def __init__(self):
        self.radius = 20
        self.color = [200, 100, 100]
    @property
    def position(self):
        return pygame.mouse.get_pos()
    
    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)
