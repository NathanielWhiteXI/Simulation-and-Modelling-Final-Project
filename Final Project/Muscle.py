import pygame
import math
import Util as util

#Gravitational Constant.
g = 9.81

class MuscleUnit:
    def __init__(self, moment_arm, direction=1):
        # +1 = flexor (biceps), -1 = extensor (triceps)
        self.direction = direction

        # Muscle parameters
        self.L_rest = 0.25
        self.k_passive = 150.0
        self.c_damp = 2.0
        self.F_max = 80.0
        self.moment_arm = moment_arm
        
        # Activation (0–1)
        self.activation = 0

    def muscle_length(self, theta):
        # Flexor shortens with flexion; extensor shortens with extension
        return self.L_rest - 0.03 * self.direction * math.sin(theta)

    def force(self, theta, omega):
        L = self.muscle_length(theta)

        # Passive force
        F_passive = 0.0
        if L > self.L_rest:
            F_passive = self.k_passive * (L - self.L_rest)

        # Active force
        F_active = self.activation * self.F_max

        F_active *= max(0.0, 1.0 - 0.1 * abs(omega))

        # Total muscle force
        F_total = F_active + F_passive

        # Convert to torque (direction determines sign)
        tau = self.direction * F_total * self.moment_arm

        # Damping torque
        tau += self.c_damp * omega

        return tau
class Elbow:
    def __init__(self):
        # State
        self.theta = math.radians(60)
        self.omega = 0.0

        # Forearm parameters
        self.length = 0.3
        self.mass = 100.0
        self.I = (1/3) * self.mass * self.length**2

        # Muscles
        self.biceps = MuscleUnit(moment_arm=0.04, direction=+1)
        self.triceps = MuscleUnit(moment_arm=0.03, direction=-1)

        # Visual-only muscle thickness 
        self.visual_biceps = 0.5
        self.visual_triceps = 0.5

    def gravity_torque(self):
        return self.mass * g * (self.length/2) * math.sin(self.theta)

    def net_torque(self):
        tau_bi = self.biceps.force(self.theta, self.omega)
        tau_tri = self.triceps.force(self.theta, self.omega)
        tau_grav = self.gravity_torque()

        return tau_bi + tau_tri - tau_grav

    def rk4_step(self, dt):
        #Stops when a contraction is completed
        if self.theta > 1.55:
            self.omega = 0.1
            self.theta = 1.54
            print("Contraction Completed")
            return

        def f(state):
            theta, omega = state
            self.theta, self.omega = theta, omega

            tau = self.net_torque()

            # Joint limits
            if theta < 0.05:
                tau += 500 * (0.05 - theta)
            if theta > 2.3:
                tau -= 500 * (theta - 2.3)

            alpha = tau / self.I
            return (omega, alpha)

        y = (self.theta, self.omega)

        k1 = f(y)
        y2 = (y[0] + 0.5*dt*k1[0], y[1] + 0.5*dt*k1[1])
        k2 = f(y2)
        y3 = (y[0] + 0.5*dt*k2[0], y[1] + 0.5*dt*k2[1])
        k3 = f(y3)
        y4 = (y[0] + dt*k3[0], y[1] + dt*k3[1])
        k4 = f(y4)

        self.theta += (dt/6)*(k1[0] + 2*k2[0] + 2*k3[0] + k4[0])
        self.omega += (dt/6)*(k1[1] + 2*k2[1] + 2*k3[1] + k4[1])