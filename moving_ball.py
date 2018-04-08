#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 19:39:33 2018

@author: Konrad
"""

import tkinter as tk
import random
import numpy as np
import random

class Ball():
    def __init__(self, canvas, cWidth, cHeight, radius, position, velocity):
        self.radius = radius # defines a radius of the ball object
        self.position = [random.uniform(50, cWidth - 50), random.uniform(50, cHeight - 50)] # defines the position of the ball object as a list of x and y components
        self.vel_comp = velocity # defines the velocity of the moving ball object with an x and y component as a list
        self.colour = "white" # defines the colour of the ball object
        self.cWidth = cWidth
        self.cHeight = cHeight 
        self.ball = canvas.create_oval(self.ball_radius(), fill = self.colour) # creates the ball object in the tkinter window
        while True:
            self.position = self.move_ball()
            velocity = np.sqrt(self.vel_comp[0] ** 2 + self.vel_comp[1] ** 2) # computes the velocity of the moving ball using the x and y components
            velocity = "%.4f" % velocity # 
#            print(velocity)
            velocity_tag = canvas.create_text(15, self.cHeight - 10, text = "Velocity : " + velocity + " m/s",
                                              fill = "black", anchor = "sw") # creates text in the window that displays the velocity of the ball
            canvas.coords(self.ball, self.ball_radius())
            canvas.update()
            canvas.delete(velocity_tag)         
    def ball_radius(self):
        """defines the objects bounds with respect to how tkinter draws ovals"""
        x0, y0 = self.position[0] - self.radius, self.position[1] - self.radius
        x1, y1 = self.position[0] + self.radius, self.position[1] + self.radius
        return [x0, y0, x1, y1]
    def move_ball(self):
        """Function which defines the object's new position components using their respective velocity components.
        Includes conditional statements that define how the ball will behave during wall collisions."""
        if self.position[0] > self.cWidth or self.position[0] < (0 + self.radius):
            self.vel_comp[0] *= -1
        elif self.position[1] > self.cHeight or self.position[1] < (0 + self.radius):
            self.vel_comp[1] *= -1
#        if self.position[0] > self.cWidth + 2 * self.radius:
#            self.position[0] = 0 - 2 * self.radius
#        elif self.position[0] < (0 - 2 * self.radius):
#            self.position[0] = self.cWidth +2 * self.radius
#        elif self.position[1] > self.cHeight + 2 * self.radius:
#            self.position[1] = 0 - 2 * self.radius
#        elif self.position[1] < (0 - 2 * self.radius):
#            self.position[1] = self.cHeight + 2 * self.radius
        x_position = self.position[0] + self.vel_comp[0]
        y_position = self.position[1] + self.vel_comp[1]
        return [x_position, y_position]
def main():
    """Initialises the simulation."""
    root = tk.Tk() # creates a window through tkinter and names it root
    root.title("Bouncing Ball") # gives the root window a title
    Width, Height = 500, 200
    window = tk.Canvas(width = Width, height = Height, bg = "#FBF1D3") # creates a canvas in the root window with specific dimensions and background colour
    window.pack()
    ball1 = Ball(window, Width, Height, 10, [Width/2, Height/2], [random.uniform(0.75, 1.25), random.uniform(0.75, 1.25)]) # initialises the ball on the canvas
    root.mainloop()   
main()