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
    # Convert simulation coordinates to screen coordinates
    def to_screen(v):
        return (400 + int(v[0]), 300 + int(v[1]))

    # --- Joint + Arm Geometry ---
    elbow_pos = pygame.Vector2(0, 0)        # elbow at origin of sim space
    elbow_screen = to_screen(elbow_pos)

    # Upper arm (fixed)
    shoulder_pos = pygame.Vector2(0, -80)
    pygame.draw.line(screen, WHITE, to_screen(shoulder_pos), elbow_screen, 6)

    # Forearm endpoint based on theta
    L = system.length * 200   # scale to pixels
    forearm_end = pygame.Vector2(
        L * math.cos(system.theta),
        L * math.sin(system.theta)
    )
    forearm_screen = to_screen(forearm_end)

    # Draw forearm
    pygame.draw.line(screen, GREEN, elbow_screen, forearm_screen, 8)

    # Draw elbow joint
    pygame.draw.circle(screen, RED, elbow_screen, 10)

    # Draw hand
    pygame.draw.circle(screen, GREEN, forearm_screen, 12)

    # Optional: draw muscle line (biceps)
    muscle_attach_shoulder = to_screen(pygame.Vector2(0, -80))
    muscle_attach_forearm = to_screen(forearm_end * 0.3)  # attach near elbow
    pygame.draw.line(screen, RED, muscle_attach_shoulder, muscle_attach_forearm, 3)
