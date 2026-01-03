import pygame
from .settings import HIGH_QUALITY, DEBUG, scattering
import modules.data as data



def distance(p1: list[int], p2: list[int]):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

class Particle:
    def __init__(self, luminosity: float, position: list[float], base_color: list[int] = [255, 255, 255], base_radius: int = 5):
        self.luminosity = luminosity
        self.base_color = base_color
        self.base_radius = base_radius
        self.REPEAT = min(10, int(3 + luminosity + HIGH_QUALITY + max(0, (scattering - 1) * 10)))
        self.PRECISEMENT = 15 + 25 * HIGH_QUALITY
        self.position = position
        self.size = self.base_radius * (2 ** (1 / self.PRECISEMENT)) ** (self.REPEAT * self.PRECISEMENT-1) * 2
        self.surface = pygame.Surface([self.size, self.size], pygame.SRCALPHA)
        self.mod_surface = None
        self.part = self.size // 2
        self.surf_pos = [0, 0]
        ''' Additional Settings '''
        # How high opacity is defined as High Brightness
        self.HIGH_BRIGHTNESS_DEFINER = 200
        self.high_brightness_radius = 0

        self.render()

    def update(self):
        '''
            Update at the start of every frame pls
        '''
        self.mod_surface = self.surface.copy()

    def shadow(self, mouse_object):
        d = distance(self.position, mouse_object.position)
        print(d)
        data.shadow_on = False
        if d < mouse_object.radius - self.high_brightness_radius or d == 0:
            data.shadow_on = True
            self.mod_surface = pygame.Surface([self.size, self.size], pygame.SRCALPHA)
            return
        if d < mouse_object.radius + self.part:
            data.shadow_on = True
            rel_mouse_pos = [mouse_object.position[0] - self.position[0] + self.part, 
                             mouse_object.position[1] - self.position[1] + self.part]
            y_prop = (self.position[0] - mouse_object.position[0]) / d
            x_prop = (self.position[1] - mouse_object.position[1]) / d
            first_edge = [rel_mouse_pos[0] - x_prop * mouse_object.radius, rel_mouse_pos[1] + y_prop * mouse_object.radius]
            second_edge = [rel_mouse_pos[0] + x_prop * mouse_object.radius, rel_mouse_pos[1] - y_prop * mouse_object.radius]
            end_points = []
            # Which side indexes are touched
            # Indexes:
            #   1 - Top
            #   2 - Right
            #   3 - Left
            #   5 - Bottom
            # These indexes i got after some experemintation in test.py file
            sides_activated = []
            for start_point in [first_edge, second_edge]:
                # 0.0001 is added to escape ZeroDivision error.
                # Probably, not the best way to make optimisation, but not the worst for sure
                y_mod = (start_point[1] - self.part) / (abs(start_point[0] - self.part) + 0.0001)
                x_mod = 1 / (abs(y_mod) + 0.0001)
                if start_point[0] < self.part:
                    x_mod *= -1
                if abs(y_mod) >= 1:
                    if y_mod < 0:
                        sides_activated.append(1)
                    else: 
                        sides_activated.append(5)
                else:
                    if x_mod < 0:
                        sides_activated.append(3)
                    else: 
                        sides_activated.append(2)
                end_points.append([min(max(0, self.part * x_mod + self.part), self.size), 
                                min(max(0, self.part * y_mod + self.part), self.size)])
            additional_points = []
            start_end_point, end_end_point = end_points
            if len(set(sides_activated)) > 1:
                suspicious_number = sides_activated[0] * sides_activated[1]
                # Checking if sides are neighbors 
                if suspicious_number not in {5, 6}:
                    x_mod = sum(sides_activated) % 2
                    y_mod = sum(sides_activated) > 6
                    additional_points.append([self.size * x_mod, self.size * y_mod])
                # Sides are not neighbors
                else:
                    if suspicious_number == 6:
                        y_mod = rel_mouse_pos[1] > self.part
                        additional_points.append([0, self.size * y_mod])
                        additional_points.append([self.size, self.size * y_mod])
                        if y_mod: additional_points.reverse()
                    else:
                        x_mod = rel_mouse_pos[0] > self.part
                        additional_points.append([self.size * x_mod, 0])
                        additional_points.append([self.size * x_mod, self.size])
                        if not x_mod: additional_points.reverse()
            # additional_points = []

            # Shadow
            pygame.draw.polygon(self.mod_surface, 
                                (0, 0, 0, 180), 
                                [first_edge, start_end_point, *additional_points, end_end_point, second_edge])
            if DEBUG:
                for point in end_points:
                    pygame.draw.circle(self.mod_surface, (0, 255, 0), point, 3)
                    pygame.draw.line(self.mod_surface, (0, 0, 255), [self.part, self.part], point, 2)
                if additional_points:
                    point = additional_points[0]
                    pygame.draw.polygon(self.mod_surface, 
                                        (0, 255, 255), 
                                        [[self.part, self.part], start_end_point, *additional_points, end_end_point],
                                        3)
                else:
                    pygame.draw.line(self.mod_surface, (0, 255, 255), end_points[0], end_points[1], 3)
                pygame.draw.circle(self.mod_surface, (255, 0, 0), first_edge, 5)  
                pygame.draw.circle(self.mod_surface, (255, 0, 0), second_edge, 5) 


    def render(self):
        size = self.surface.get_height()
        self.surf_pos = [self.position[0] - size // 2, self.position[1] - size // 2]
        def p(lumi, depth, prec):
            return min(int(255 * lumi / ((3 - scattering) ** (1 / prec)) ** depth), 255)
        for depth in reversed(range(0, self.REPEAT * self.PRECISEMENT)):
            r = self.base_radius * (2 ** (1 / self.PRECISEMENT)) ** depth
            lumi = p(self.luminosity, depth, self.PRECISEMENT)
            print(lumi)
            pygame.draw.circle(self.surface, [*self.base_color, lumi], 
                [self.part, self.part], r)
            if lumi > self.HIGH_BRIGHTNESS_DEFINER and self.high_brightness_radius == 0:
                self.high_brightness_radius = r
        if DEBUG:
            pygame.draw.rect(self.surface, (255, 255, 255), [1, 1, self.size-1, self.size-1], 1)
            
        self.surface.convert()
        self.mod_surface = self.surface.copy()

    def draw(self, surface: pygame.Surface):
        surface.blit(self.mod_surface, self.surf_pos)
