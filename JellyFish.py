import pygame
import math
import random
from chain import Chain
from utils import from_angle, set_mag

class Jellyfish:
    def __init__(self, origin, body_color=None, tentacle_color=None):
        self.body_color = body_color if body_color else (210, 130, 230)
        self.tentacle_color = tentacle_color if tentacle_color else (180, 100, 220)
        self.radius = 60
        self.tentacle_count = 6
        self.body = Chain(origin, 1, 0, math.pi / 8)
        self.tentacles = []
        self.origin = list(origin)
        self.vel = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.time = 0.0
        for i in range(self.tentacle_count):
            base_angle = (i - (self.tentacle_count - 1) / 2) * (math.pi / 10)
            self.tentacles.append({
                "chain": Chain(origin, 8, 28, math.pi),
                "angle_offset": base_angle,
                "phase": random.uniform(0, 2 * math.pi)
            })
        
    def update_auto(self, screen_width, screen_height):
        self.time += 0.04
        self.origin[0] += self.vel[0] + math.cos(self.time * 0.8) * 0.3
        self.origin[1] += self.vel[1] + math.sin(self.time * 0.6) * 0.2
        margin = self.radius * 1.5

        if self.origin[0] < margin or self.origin[0] > screen_width - margin:
            self.vel[0] *= -1
        if self.origin[1] < margin or self.origin[1] > screen_height - margin:
            self.vel[1] *= -1

        direction_angle = math.atan2(self.vel[1], self.vel[0])
        self.body.resolve(tuple(self.origin))

        for i, t in enumerate(self.tentacles):
            phase = t["phase"]
            wave_angle = math.sin(self.time * 2 + phase) * 0.5
            back_angle = direction_angle + math.pi  # côté !déplacement
            angle = back_angle + t["angle_offset"] + wave_angle
            base_offset = from_angle(angle)
            base_offset = set_mag(base_offset, self.radius * 0.7)
            base_pos = (
                self.origin[0] + base_offset[0],
                self.origin[1] + base_offset[1]
            )
            t["chain"].resolve(base_pos)

    def display(self, screen):
        # halo gélatineux tête
        for i in range(3):
            alpha = 80 - i * 20
            surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                surf, (*self.body_color, alpha),
                (self.radius, self.radius),
                self.radius - i * 5
            )
            screen.blit(surf, (self.origin[0] - self.radius, self.origin[1] - self.radius))

        # tête
        pygame.draw.circle(
            screen,
            self.body_color,
            (int(self.origin[0]), int(self.origin[1])),
            int(self.radius * 0.8)
        )

        #  halo tentacules
        for t in self.tentacles:
            chain = t["chain"]
            jelly_surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            for i in range(len(chain.joints) - 1):
                pygame.draw.line(
                    jelly_surf,
                    (*self.tentacle_color, 40),
                    chain.joints[i],
                    chain.joints[i + 1],
                    10
                )
            screen.blit(jelly_surf, (0, 0))

            for i in range(len(chain.joints) - 1):
                pygame.draw.line(
                    screen,
                    self.tentacle_color,
                    chain.joints[i],
                    chain.joints[i + 1],
                    3
                )

    def debug_display(self, screen):
        self.body.display(screen)
        for t in self.tentacles:
            t["chain"].display(screen)
