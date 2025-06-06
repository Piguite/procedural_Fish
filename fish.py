import pygame
import math
import random
from chain import Chain
from utils import from_angle, set_mag

class Fish:
    def __init__(self, origin, body_color=None, fin_color=None):
        self.spine = Chain(origin, 12, 64, math.pi / 8)
        self.body_color = body_color if body_color else (58, 124, 165) # couleur corps
        self.fin_color = fin_color if fin_color else (129, 195, 215) # couleur nageoire
        self.body_widths = [68, 81, 84, 83, 77, 64, 51, 38, 32, 19]
        self.fin_oscillation_amplitude = 0.15  # oscillation angle nageoire
        self.fin_oscillation_speed = 0.005 # oscillation speed nageoire
        self.angle = random.uniform(0, 2 * math.pi)
        self.target_angle = self.angle 
        self.time = 0.0  # pour les oscillations
        self.change_dir_timer = 0.0 

    def update_auto(self, screen_width, screen_height):
        self.time += 0.05
        self.change_dir_timer += 0.05

        # changer direction cible toutes les 10-15 secondes
        if self.change_dir_timer > random.uniform(10.0, 15.0):
            self.change_dir_timer = 0.0
            if random.random() < 0.5:
                self.target_angle = random.uniform(-math.pi/4, math.pi/4)
            else:
                self.target_angle = random.uniform(math.pi - math.pi/4, math.pi + math.pi/4)

        lerp_factor = 0.05  # smoothing de la rotation
        angle_diff = (self.target_angle - self.angle + math.pi) % (2 * math.pi) - math.pi
        self.angle += angle_diff * lerp_factor
        self.angle %= 2 * math.pi
        # oscillation naturelle
        self.angle += math.sin(self.time * 2) * 0.04
        # vitesse des poissons
        speed_target = 4.0
        target_velocity = set_mag(from_angle(self.angle), speed_target)
        if not hasattr(self, 'current_velocity'):
            self.current_velocity = [0, 0]

        # interpolation linéaire de la vitesse pour lissage inertiel
        lerp_v = 0.1
        self.current_velocity[0] += (target_velocity[0] - self.current_velocity[0]) * lerp_v
        self.current_velocity[1] += (target_velocity[1] - self.current_velocity[1]) * lerp_v

        # gestion collision bord
        x, y = self.spine.joints[0]
        new_x = x + self.current_velocity[0]
        new_y = y + self.current_velocity[1]
        bounced = False
        if new_x < 0 or new_x > screen_width:
            self.angle = math.pi - self.angle
            self.target_angle = self.angle
            bounced = True
        if new_y < 0 or new_y > screen_height:
            self.angle = -self.angle
            self.target_angle = self.angle
            bounced = True
        if bounced:
            self.time += math.pi
        new_x = max(0, min(new_x, screen_width))
        new_y = max(0, min(new_y, screen_height))
        self.spine.resolve((new_x, new_y))

    def display(self, screen):
        t = pygame.time.get_ticks()

        # nageoires pectorales
        angle_offset_pec = self.fin_oscillation_amplitude * math.sin(t * self.fin_oscillation_speed)
        self.draw_fin(screen, index=3, angle_offset=math.pi/3 + angle_offset_pec, rot_offset=-math.pi/4, mirror=False)
        self.draw_fin(screen, index=3, angle_offset=-math.pi/3 - angle_offset_pec, rot_offset=math.pi/4, mirror=True)

        # nageoires ventrales
        angle_offset_vent = self.fin_oscillation_amplitude * math.sin(t * self.fin_oscillation_speed * 1.5)
        self.draw_fin(screen, index=7, angle_offset=math.pi/2 + angle_offset_vent, rot_offset=0, width=80, height=40)
        self.draw_fin(screen, index=7, angle_offset=-math.pi/2 - angle_offset_vent, rot_offset=0, width=80, height=40)

        # corps principal
        pygame.draw.polygon(screen, self.body_color, self.get_body_points())

        # yeux
        pygame.draw.circle(screen, (255, 255, 255),
                           (int(self.get_pos_x(0, math.pi/2, -18)), int(self.get_pos_y(0, math.pi/2, -18))), 12)
        pygame.draw.circle(screen, (255, 255, 255),
                           (int(self.get_pos_x(0, -math.pi/2, -18)), int(self.get_pos_y(0, -math.pi/2, -18))), 12)

    def draw_fin(self, screen, index, angle_offset, rot_offset=0, width=160, height=64, mirror=False):
        cx = self.get_pos_x(index, angle_offset, 0)
        cy = self.get_pos_y(index, angle_offset, 0)
        angle = self.spine.angles[index] + rot_offset
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        ellipse_rect = pygame.Rect(0, 0, width, height)
        pygame.draw.ellipse(surf, self.fin_color, ellipse_rect)
        rotated = pygame.transform.rotate(surf, -math.degrees(angle))
        rect = rotated.get_rect(center=(cx, cy))
        screen.blit(rotated, rect)

    def get_pos_x(self, i, angle_offset, length_offset):
        x, y = self.spine.joints[i]
        angle = self.spine.angles[i] + angle_offset
        return x + math.cos(angle) * (self.body_width(i) + length_offset)

    def get_pos_y(self, i, angle_offset, length_offset):
        x, y = self.spine.joints[i]
        angle = self.spine.angles[i] + angle_offset
        return y + math.sin(angle) * (self.body_width(i) + length_offset)

    def body_width(self, i):
        if i < len(self.body_widths):
            return self.body_widths[i]
        else:
            return 16

    def get_body_points(self):
        points = []
        # côté droit du corps (décalage + pi/2)
        for i in range(len(self.spine.joints)):
            points.append((self.get_pos_x(i, math.pi/2, 0), self.get_pos_y(i, math.pi/2, 0)))

        # point supplémentaire à la queue, au bout de la ligne du corps (exemple : angle + pi)
        tail_index = len(self.spine.joints) - 1
        points.append((self.get_pos_x(tail_index, math.pi, 0), self.get_pos_y(tail_index, math.pi, 0)))

        # côté gauche du corps (décalage - pi/2)
        for i in reversed(range(len(self.spine.joints))):
            points.append((self.get_pos_x(i, -math.pi/2, 0), self.get_pos_y(i, -math.pi/2, 0)))

        # points supplémentaires pour la tête, pour fermer correctement la forme
        points.append((self.get_pos_x(0, -math.pi/6, 0), self.get_pos_y(0, -math.pi/6, 0)))
        points.append((self.get_pos_x(0, 0, 0), self.get_pos_y(0, 0, 0)))
        points.append((self.get_pos_x(0, math.pi/6, 0), self.get_pos_y(0, math.pi/6, 0)))

        return points

    def debug_display(self, screen):
        self.spine.display(screen)
