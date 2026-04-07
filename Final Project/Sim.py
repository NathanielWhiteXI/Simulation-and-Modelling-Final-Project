import pygame
import Util as util
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

            # if self.system.theta > 1.55 and not self.complete:
            #     print("One full contraction complete")
            #     self.complete = True

#Sets up Pygame Window
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("2D Arm Simulation")
clock = pygame.time.Clock()

sim = Simulation("2D Arm Simulation")

#Message to user
print("The red mass is connected to the origin via a spring")
print("The green mass is connected to the red Orb via a spring")
print("Press R to start simulation")
print("Press P to stop simulation")
print("Press Space to see the next step")

#Main loop
running = True
while running:
    clock.tick(30)
    screen.fill(util.BLACK)
    util.draw_axes(screen)

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

    # update + draw
    sim.update()
    util.draw(sim.system, screen)

    pygame.display.update()

pygame.quit()