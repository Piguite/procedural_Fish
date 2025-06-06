import pygame
import math
from utils import sub, heading, constrain_angle, from_angle, set_mag

class Chain:
    def __init__(self, origin, joint_count, link_size, angle_constraint = 2 * math.pi):
        self.link_size = link_size
        self.angle_constraint = angle_constraint
        self.joints = [origin]
        self.angles = [0.0]
        for i in range(1, joint_count):
            self.joints.append((self.joints[i-1][0], self.joints[i-1][1] + self.link_size))
            self.angles.append(0.0)

    def resolve(self, pos):
        self.angles[0] = heading(sub(pos, self.joints[0]))
        self.joints[0] = pos
        for i in range(1, len(self.joints)):
            cur_angle = heading(sub(self.joints[i-1], self.joints[i]))
            self.angles[i] = constrain_angle(cur_angle, self.angles[i-1], self.angle_constraint)
            offset = from_angle(self.angles[i])
            offset = set_mag(offset, self.link_size)
            self.joints[i] = (self.joints[i-1][0] - offset[0], self.joints[i-1][1] - offset[1])

    def display(self, screen):
        for i in range(len(self.joints) - 1):
            pygame.draw.line(screen, (255, 255, 255), self.joints[i], self.joints[i+1], 8)
        for joint in self.joints:
            pygame.draw.circle(screen, (42, 44, 53), (int(joint[0]), int(joint[1])), 16)
