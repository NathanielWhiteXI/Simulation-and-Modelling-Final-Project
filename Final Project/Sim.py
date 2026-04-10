import pygame
import Util as utimil
import Muscle as ms
import math

class Simulation:

    def __init__(self, title):
        self.paused = True
        self.complete = False
        self.title = title
        self.cur_time = 0
        self.dt = 0.001
        self.system = ms.Elbow()

    def update(self):
        if not self.paused:
            if not self.complete:
                self.system.rk4_step(self.dt)
                self.cur_time += self.dt

            # visual-only gradual muscle change
            grow_speed = 4.0   # how fast thickness changes

            if self.system.omega < 0:
                # concentric: biceps grows, triceps shrinks
                target_biceps = 1.5
                target_triceps = 0.025
            elif self.system.omega > 0:
                # eccentric: biceps shrinks, triceps grows
                target_biceps = 0.025
                target_triceps = 1.5
            else:
                # neutral
                target_biceps = 0.5
                target_triceps = 0.5

            self.system.visual_biceps += (target_biceps - self.system.visual_biceps) * grow_speed * self.dt
            self.system.visual_triceps += (target_triceps - self.system.visual_triceps) * grow_speed * self.dt

#Sets up Pygame Window
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("2D Arm Simulation")
clock = pygame.time.Clock()

sim = Simulation("2D Arm Simulation")

#Message to user
print("Welcome to the 2D Arm Simulation!")
print("Press R to start simulation")
print("Press P to stop simulation")
print("Press Space to see the next step")

#Main loop
running = True
while running:
    clock.tick(30)
    screen.fill(utimil.BLACK)
    utimil.draw_axes(screen)

    # input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: #Pauses Program
                print("Sim Resumed")
                sim.paused = False
            if event.key == pygame.K_p: #Resumes Program
                print("Sim Paused")
                sim.paused = True
            if event.key == pygame.K_SPACE and sim.paused: #Increments the program by 1 step.
                print("Sim Incremented")
                sim.paused=False
                sim.update()
                sim.paused=True

            # --- Muscle Controls ---
            if event.key == pygame.K_1:
                sim.system.biceps.activation = min(1.0, sim.system.biceps.activation + 0.1)

            if event.key == pygame.K_2:
                sim.system.biceps.activation = max(0.0, sim.system.biceps.activation - 0.1)

            if event.key == pygame.K_3:
                sim.system.triceps.activation = min(1.0, sim.system.triceps.activation + 0.1)

            if event.key == pygame.K_4:
                sim.system.triceps.activation = max(0.0, sim.system.triceps.activation - 0.1)

    # update + draw
    sim.update()
    utimil.draw(sim.system, screen)

    pygame.display.update()

pygame.quit()