import pygame
from .particle import Particle
from .settings import DEBUG, screen_size, FPS, HIGH_QUALITY
from .mouse_object import MouseCircle
from .debug_settings import get_debug_texts
from .data import frame_data
from random import randint


pygame.init()

run = True
clock = pygame.time.Clock()
frame = 0

display = pygame.display.set_mode(screen_size)
display_surface = pygame.Surface(screen_size, pygame.SRCALPHA)
pygame.display.set_caption("Particle Test")

orig_part = Particle(4, [400, 400], base_radius = 2)

mouse_object = MouseCircle()

sys_font = pygame.font.SysFont("Futura", 24)
fps_surface = pygame.Surface((0, 0))
debug_text_surfaces = [pygame.Surface((0, 0))]
data_surface = pygame.Surface((0, 0))
add_text = ["", ", higher quality is ON"][HIGH_QUALITY]

def main():
    global run, sys_font, display, display_surface, frame, mouse_object, fps_surface, debug_text_surfaces, data_surface
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        display_surface.fill((0, 0, 0))
        display.fill((0, 0, 0))

        # Something that im allowed to touch. 
        # If you are editing this mess, you can also touch this bit
        orig_part.update()
        orig_part.shadow(mouse_object)
        orig_part.draw(display_surface)

        mouse_object.draw(display_surface)
        # Something. Dont touch it pls
        if frame % 10 == 0:
            fps_surface = sys_font.render(f"FPS: {round(clock.get_fps())}{add_text}", True, (255, 255, 255))
            if DEBUG:
                debug_text_surfaces = []
                for text in get_debug_texts():
                    debug_text_surfaces.append(sys_font.render(text, True, (255, 255, 255)))
        display.blit(display_surface, (0, 0))
        if DEBUG:
            h = 0
            for text_surf in debug_text_surfaces:
                display.blit(text_surf, (screen_size[0] - text_surf.get_width() - 10, 10 + h))
                h += text_surf.get_height()+5
            if len(frame_data) > FPS:
                frame_data.pop(0)
        display.blit(fps_surface, (10, 10))
        pygame.display.flip()
        frame += 1
        frame_data.append(round(clock.get_fps()))