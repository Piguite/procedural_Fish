#!/usr/bin/env python3
import pygame
from snake import Snake
from fish import Fish
import math
import datetime

def draw_water_overlay(screen, width, height, nenuphar_img):
    # Surface transparente
    water_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    # Filtre bleu léger
    blue_tint = pygame.Surface((width, height), pygame.SRCALPHA)
    blue_tint.fill((30, 100, 200, 40))
    water_surface.blit(blue_tint, (0, 0))

    t = pygame.time.get_ticks() / 1000.0
    center_points = [
        (width * 0.3, height * 0.4),
        (width * 0.5, height * 0.5),
        (width * 0.3, height * 0.9),
        (width * 0.8, height * 0.7),
        (width * 0.2, height * 0.1),
        (width * 0.9, height * 0.6),
        (width * 0.1, height * 0.9),
    ]

    for (cx, cy) in center_points:
        for i in range(3):
            radius = 60 + 30 * i + 10 * math.sin(t * 2 + i)
            alpha = int(40 - i * 10)
            color = (180, 220, 250, alpha)
            pygame.draw.circle(water_surface, color, (int(cx), int(cy)), int(radius), width=2)

    nenuphar_rect = nenuphar_img.get_rect(bottomright=(width, height))
    water_surface.blit(nenuphar_img, nenuphar_rect)
    screen.blit(water_surface, (0, 0))

def date(font_large, font_small):
    now = datetime.datetime.now()
    day_name = now.strftime("%A").capitalize()
    date_str = now.strftime("%d/%m/%Y")
    time_str = now.strftime("%Hh%M")

    # Rendu du texte
    text_day = font_large.render(day_name, True, (255, 255, 255))
    text_date = font_small.render(f"{date_str} {time_str}", True, (200, 200, 200))

    # Position du haut-centre
    padding_top = 20
    text_day_rect = text_day.get_rect(midtop=(screen_width // 2, padding_top))
    text_date_rect = text_date.get_rect(midtop=(screen_width // 2, text_day_rect.bottom + 5))

    screen.blit(text_day, text_day_rect)
    screen.blit(text_date, text_date_rect)

pygame.init()
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
screen_width, screen_height = screen.get_size()
clock = pygame.time.Clock()
nenuphar_img = pygame.image.load("img/test2.png").convert_alpha()
font_large = pygame.font.SysFont("Arial", 48)
font_small = pygame.font.SysFont("Arial", 36)

snake = Snake((screen_width / 2, screen_height / 2))

fish_list = [
    Fish((screen_width / 4, screen_height / 2), body_color=(58, 124, 165), fin_color=(129, 195, 215)),
    Fish((screen_width / 3, screen_height / 3), body_color=(200, 100, 50), fin_color=(220, 150, 80)),
    Fish((screen_width / 2, screen_height / 4), body_color=(100, 200, 150), fin_color=(150, 230, 190)),
    Fish((screen_width * 0.75, screen_height / 2), body_color=(255, 100, 180), fin_color=(255, 150, 210)),
]

running = True
has_focus = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((20, 30, 60))

    # snake.update_auto(screen_width, screen_height)
    # snake.display(screen)
    # snake.debug_display(screen)
    for fish in fish_list:
        fish.update_auto(screen_width, screen_height)
        fish.display(screen)
        # fish.debug_display(screen)

    draw_water_overlay(screen, screen_width, screen_height, nenuphar_img)

    date(font_large, font_small)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
