import pygame
import math
import Util as util

#Gravitational Constant.
g = 9.81

class Muscle:
    def __init__(self):
        #Elbow angle params
        self.theta = math.radians(60)
        self.omega = 0 #Angular Velocity

        #Forearm params
        self.length = 0.3
        self.mass = 2.0
        self.I = (1/3) * self.mass * self.length**2 #Moment of inertia

        #Muscle Tendon params
        self.L_rest = 0.25              # resting muscle length
        self.k_passive = 150.0          # passive stiffness
        self.c_damp = -8.0              # damping
        self.F_max = 300.0              # max contractile force
        self.moment_arm = 0.04          # meters

        # Activation level (0–1)
        self.activation = 0.0
    
    def muscle_length(self, theta):
        # Simple geometric model: muscle shortens as elbow flexes
        return self.L_rest - 0.03 * math.sin(theta)

    # Function to compute forces
    def forces(self):

        L = self.muscle_length(self.theta)

        # Passive force (only when stretched)
        F_passive = 0.0
        if L > self.L_rest:
            F_passive = self.k_passive * (L - self.L_rest)

        # Active force (scaled by activation)
        F_active = self.activation * self.F_max

        # Total muscle force
        F_total = F_active + F_passive

        # Convert to torque
        tau_muscle = F_total * self.moment_arm

        # Gravity torque on forearm
        tau_gravity = self.mass * g * (self.length/2) * math.sin(self.theta)

        # Damping torque
        tau_damp = self.c_damp * self.omega

        # Net torque
        tau_net = tau_muscle - tau_gravity + tau_damp

        return tau_net

    #RK4 Integrator for each step
    def rk4_step(self, dt):
        '''
        ODE Variables
        Velocity in X, Y direction
        Acceleration in the Spring Direction, and Gravity Acceleration
        '''
        def f(state):
            theta, omega = state
            self.theta, self.omega = theta, omega
        
            tau = self.forces()

            if self.theta < 0.05:
                tau += 50 * (0.05 - self.theta)
            if self.theta > 2.3:
                tau -= 50 * (self.theta - 2.3)

            alpha = tau / self.I  # angular acceleration

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
