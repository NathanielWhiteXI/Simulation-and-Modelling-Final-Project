import pygame
import math

#Colours the program uses
RED = (255, 0, 0)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)

# Draws axes to better show what the simulation looks like
def draw_axes(window):
    pygame.draw.line(window, WHITE, (0, 300), (800,300), 1)
    pygame.draw.line(window, WHITE, (400, 0), (400,600), 1)

# Draws each mass on the screen.
def draw(system, screen):
    def to_screen(v):
        return (400 + int(v[0]), 300 + int(v[1]))

    # --- Joint + Arm Geometry ---
    elbow_pos = pygame.Vector2(0, 0)
    elbow_screen = to_screen(elbow_pos)

    # Upper arm (fixed)
    shoulder_pos = pygame.Vector2(0, -80)
    shoulder_screen = to_screen(shoulder_pos)
    pygame.draw.line(screen, WHITE, to_screen(shoulder_pos), elbow_screen, 6)

    # Forearm endpoint
    L = system.length * 200
    forearm_end = pygame.Vector2(
        L * math.cos(system.theta),
        L * math.sin(system.theta)
    )
    forearm_screen = to_screen(forearm_end)

    # Draw forearm
    pygame.draw.line(screen, GREEN, elbow_screen, forearm_screen, 8)

    # --- Thicker Arm Segments ---
    
    # Upper arm (thicker)
    pygame.draw.line(screen, (160, 160, 175), shoulder_screen, elbow_screen, 14)

    # Forearm (thicker)
    pygame.draw.line(screen, (0, 200, 100), elbow_screen, forearm_screen, 12)

    # --- Muscle Bands (Thickness = Activation) --- 

    # Bicep attachment point
    biceps_origin = shoulder_pos
    biceps_insert = forearm_end * 0.30

    # Tricep attachment point
    triceps_origin = shoulder_pos + pygame.Vector2(-20, 0)
    triceps_insert = forearm_end * 0.15

    # convert to line thickness
    biceps_width = 5 + int(system.visual_biceps * 9)
    triceps_width = 5 + int(system.visual_triceps * 9)

    # Draw biceps (red)
    pygame.draw.line(
        screen,
        (255, 80, 80),
        to_screen(biceps_origin),
        to_screen(biceps_insert),
        biceps_width
    )

    # Draw triceps (blue)
    pygame.draw.line(
        screen,
        (80, 150, 255),
        to_screen(triceps_origin),
        to_screen(triceps_insert),
        triceps_width
    )

    # Draw elbow + hand
    pygame.draw.circle(screen, RED, elbow_screen, 10)
    pygame.draw.circle(screen, GREEN, forearm_screen, 12)

    # ---------------------------------------------------------
    # MUSCLE VISUALIZATION
    # ---------------------------------------------------------

    # Biceps (flexor)
    biceps_origin = pygame.Vector2(0, -80)          # shoulder
    biceps_insert = forearm_end * 0.30              # near elbow
    pygame.draw.line(
        screen, RED,
        to_screen(biceps_origin),
        to_screen(biceps_insert),
        4
    )

    # Triceps (extensor)
    triceps_origin = pygame.Vector2(0, -80) + pygame.Vector2(-20, 0)
    triceps_insert = forearm_end * 0.15             # slightly different insertion
    pygame.draw.line(
        screen, (0, 150, 255),                      # blue-ish color
        to_screen(triceps_origin),
        to_screen(triceps_insert),
        4
    )