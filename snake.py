import pygame
import math
import random
from chain import Chain
from utils import from_angle, set_mag

class Snake:
    def __init__(self, origin):
        self.spine = Chain(origin, 48, 64, math.pi / 8)
        self.speed = 4.0
        self.angle = random.uniform(0, 2 * math.pi)
        self.time = 0.0

    def update_auto(self, screen_width, screen_height):
        self.time += 0.05
        self.angle += math.sin(self.time) * 0.03

        velocity = from_angle(self.angle)
        velocity = set_mag(velocity, self.speed)

        x, y = self.spine.joints[0]
        new_x = x + velocity[0]
        new_y = y + velocity[1]

        bounced = False
        if new_x < 0 or new_x > screen_width:
            self.angle = math.pi - self.angle
            bounced = True
        if new_y < 0 or new_y > screen_height:
            self.angle = -self.angle
            bounced = True

        if bounced:
            self.time += math.pi

        new_x = max(0, min(new_x, screen_width))
        new_y = max(0, min(new_y, screen_height))

        self.spine.resolve((new_x, new_y))

    def display(self, screen):
        pygame.draw.polygon(screen, (172, 57, 49), self.get_body_points())
        pygame.draw.circle(screen, (255, 255, 255),
                           (int(self.get_pos_x(0, math.pi/2, -18)), int(self.get_pos_y(0, math.pi/2, -18))), 12)
        pygame.draw.circle(screen, (255, 255, 255),
                           (int(self.get_pos_x(0, -math.pi/2, -18)), int(self.get_pos_y(0, -math.pi/2, -18))), 12)

    def debug_display(self, screen):
        self.spine.display(screen)

    def body_width(self, i):
        if i == 0:
            return 76
        elif i == 1:
            return 80
        else:
            return 64 - i

    def get_pos_x(self, i, angle_offset, length_offset):
        x, y = self.spine.joints[i]
        angle = self.spine.angles[i] + angle_offset
        return x + math.cos(angle) * (self.body_width(i) + length_offset)

    def get_pos_y(self, i, angle_offset, length_offset):
        x, y = self.spine.joints[i]
        angle = self.spine.angles[i] + angle_offset
        return y + math.sin(angle) * (self.body_width(i) + length_offset)

    def get_body_points(self):
        points = []
        for i in range(len(self.spine.joints)):
            points.append((self.get_pos_x(i, math.pi/2, 0), self.get_pos_y(i, math.pi/2, 0)))
        points.append((self.get_pos_x(47, math.pi, 0), self.get_pos_y(47, math.pi, 0)))
        for i in reversed(range(len(self.spine.joints))):
            points.append((self.get_pos_x(i, -math.pi/2, 0), self.get_pos_y(i, -math.pi/2, 0)))
        points.append((self.get_pos_x(0, -math.pi/6, 0), self.get_pos_y(0, -math.pi/6, 0)))
        points.append((self.get_pos_x(0, 0, 0), self.get_pos_y(0, 0, 0)))
        points.append((self.get_pos_x(0, math.pi/6, 0), self.get_pos_y(0, math.pi/6, 0)))
        return points

    def debug_display(self, screen):
        self.spine.display(screen)
