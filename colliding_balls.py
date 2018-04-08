#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 23:14:09 2018
@author: Konrad
"""

import tkinter as tk
import math
import random

class Particle():
    def __init__(self, canvas, cWidth, cHeight, colour):
        """Initialises the Particle object with specific parameters."""
        self.radius = 10
        self.cWidth = cWidth
        self.cHeight = cHeight
        # determines the particle's position based on a randomly generated x and y values within the bounds of the canvas
        self.position = [random.uniform(self.radius, cWidth - self.radius),
                         random.uniform(self.radius, cHeight - self.radius)]
        # determines the particle's velocity based on a randomly generated x and y components
        self.vel_comp = [random.uniform(-1, 1),
                         random.uniform(-1, 1)]
        # determines the mass of the particle as a fraction of its diameter
        self.mass = 0.1 * (2 * self.radius)
        # defines the particles colour either randomly or with the colour white.
        if colour == "standard":
            self.colour = ["white", "black"]
        elif colour == "coloured":
            self.colour = self.random_colour()
        self.canvas = canvas
        self.ball = self.draw()
    def draw(self):
        """Draws the Bubble object on the canvas."""
        return self.canvas.create_oval(self.particle_dimensions(), fill = self.colour[0], outline = self.colour[1])
    def particle_dimensions(self):
        """Defines the objects bounds with respect to how tkinter draws ovals."""
        x0, y0 = self.position[0] - self.radius, self.position[1] - self.radius
        x1, y1 = self.position[0] + self.radius, self.position[1] + self.radius
        return [x0, y0, x1, y1]
    def move_ball(self, bounds):
        """Function which defines the object's new position components using
        their respective velocity components. Includes conditional statements
        that define how the ball will behave during wall collisions."""
        if bounds == "rebound":
            if self.position[0] > (self.cWidth - self.radius) or self.position[0] < (0 + self.radius):
                self.vel_comp[0] *= -1
            elif self.position[1] > (self.cHeight - self.radius) or self.position[1] < (0 + self.radius):
                self.vel_comp[1] *= -1
        elif bounds == "infinite":
            if self.position[0] > self.cWidth + self.radius:
                self.position[0] = 0 - self.radius
            elif self.position[0] < (0 - self.radius):
                self.position[0] = self.cWidth + self.radius
            elif self.position[1] > self.cHeight + self.radius:
                self.position[1] = 0 - self.radius
            elif self.position[1] < (0 - self.radius):
                self.position[1] = self.cHeight + self.radius
        # assigns a new x and y position for the particle based on its current velocity
        self.position[0] += self.vel_comp[0]
        self.position[1] += self.vel_comp[1]
        # updates the particles position based on it's newly calculated positions
        self.canvas.coords(self.ball, self.particle_dimensions())
    def random_colour(self):
        colour_fill = ["RoyalBlue1", "SteelBlue1", "SeaGreen1", "green2", "yellow2", "orange1", "red1", "HotPink1", "Purple1"]
        colour_outline = ["RoyalBlue3", "SteelBlue3", "SeaGreen3", "green3", "yellow3", "orange3", "red3", "HotPink3", "Purple3"]
        rand_colour = random.randrange(0, len(colour_fill), 1)
        return [colour_fill[rand_colour], colour_outline[rand_colour]]

def particle_collision(particle1, particle2):
    def velocity_angle(velocity, angle):
        rotated_velocities = [velocity[0] * math.cos(angle) - velocity[1] * math.sin(angle),
                             velocity[0] * math.sin(angle) + velocity[1] * math.cos(angle)]
        return rotated_velocities
    delta_x_vel = particle1.vel_comp[0] - particle2.vel_comp[0]
    delta_y_vel = particle1.vel_comp[1] - particle2.vel_comp[1]
    x_dist = particle2.position[0] - particle1.position[0]
    y_dist = particle2.position[1] - particle1.position[1]
    if delta_x_vel * x_dist + delta_y_vel * y_dist >= 0:
# determines the initial angle before the particles collide
        angle = -math.atan2(particle2.position[1] - particle1.position[1], particle2.position[0] - particle1.position[0])
# determines the initital velcocities between the two colliding particles
        u1 = velocity_angle(particle1.vel_comp, angle)
        u2 = velocity_angle(particle2.vel_comp, angle)
# determines the pseudo-final velcocities between the two colliding particles        
        v1 = [u1[0] * (particle1.mass - particle1.mass) / (particle1.mass + particle1.mass) + u2[0] * 2 * particle1.mass / (particle1.mass + particle1.mass), u1[1]]
        v2 = [u2[0] * (particle1.mass - particle1.mass) / (particle1.mass + particle1.mass) + u1[0] * 2 * particle1.mass / (particle1.mass + particle1.mass), u2[1]]
# determines the final velcocities between the two colliding particles now including the leaving angle from the collision     
        final_velocity_par1 = velocity_angle(v1, -angle)
        final_velocity_par2 = velocity_angle(v2, -angle)
        particle1.vel_comp[0], particle1.vel_comp[1] = final_velocity_par1[0], final_velocity_par1[1]
        particle2.vel_comp[0], particle2.vel_comp[1] = final_velocity_par2[0], final_velocity_par2[1]
def mean_velocity(particles):
    """Function used to determine the mean velocity of all particles initialised in the canvas."""
    summation = 0
    for i in range(0, len(particles)):
        summation += math.sqrt(particles[i].vel_comp[0] ** 2 + particles[i].vel_comp[1] ** 2)
    mean_vel = summation / len(particles)
    return ("%.4f" % mean_vel)
    
def setup():
    """Setup Function Initialises the program and ensures the program runs in
    correct order. Dealing with window creation for the program, initialising 
    the particles and dealing with collision detection. """
# creates a window through tkinter and names it root
    root = tk.Tk()
# gives the root window a title
    root.title("Colliding Particles") 
    Width, Height = 500, 500
# creates a canvas in the root window with specific dimensions and background colour
    window = tk.Canvas(width = Width, height = Height, highlightthickness=0, bg = "white") #FBF1D3
    window.pack()
# list where particle objects are stored with all their information
    particles = []
# defines how the particle will behave when it reaches the bounds of the canvas
    bounds = "infinite" # options: infinite, rebound
    colour = "coloured" # options: coloured, standard
    for i in range(0, 100):
# initialises a particle on the canvas, due to the loop, initialises a number of particles 
        particles.append(Particle(window, Width, Height, colour)) 
    while True:
# while True: ensures the particles are always moving, whilst also detecting for particle collisions
        for i in range(0, len(particles)):
            particles[i].move_ball(bounds)
            for j in range(0, len(particles)):
                d = math.sqrt((particles[i].position[0] - particles[j].position[0]) ** 2 + (particles[i].position[1] - particles[j].position[1]) ** 2)
                if d < particles[i].radius + particles[j].radius:
                    particle_collision(particles[i], particles[j])
# creates a line of text displaying the mean velocity of the particles
        mean_vel_text = window.create_text(10, Height - 10, text = "Mean Velocity: " + mean_velocity(particles) + " m/s", fill = "black", anchor = "sw")
# updates the canvas to display the new positions of the particles 
        window.update()
# deletes the text from the canvas so that the mean velocity is later updated
# without overpopulating the canvas with text objects
        window.delete(mean_vel_text)
# ensures the program window is always open
    root.mainloop() 

# runs the program           
setup()