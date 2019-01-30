import tkinter as tk
import tkinter.font as font
import tkinter.messagebox as msg
from math import *
from colour import Color
import time

def map_coordinates(x, y, dim):
    mapped_x = (x * dim) + 500
    mapped_y = (-y * dim) + 250
    return mapped_x, mapped_y

def unmap_coordinates(x, y, dim):
    unmapped_x = (x - 500) / dim
    unmapped_y = (y - 250) / -dim
    return unmapped_x, unmapped_y

def gradient_map(value, gradient, value_minimum, value_maximum):
    grad_pos = floor((value - value_minimum) / (value_maximum - value_minimum) * 255)
    
    color = "%s" % gradient[grad_pos]
    return color

class Grapher:
    def __init__(self):
        self.dim = 20.0 / 2.0 ** 4.0
        self.scaling = 50.0
        
    def set_resolution(self, resolution):
        self.dim = 20.0 / 2.0 ** resolution
        
    def set_scaling(self, scaling):
        self.scaling = scaling
        
    def graph_points(self, viewer, ctx, function, low_threshold, high_threshold):
        try:
            gradient = list(Color("white").range_to(Color("black"), 255))
            for i in range(0, 500, ceil(self.dim)):
                for j in range(0, 1000, ceil(self.dim)):
                    x, y = unmap_coordinates(j, i, self.scaling)
                    try:
                        ctx.create_rectangle(j-self.dim/2.0, i-self.dim/2, \
                                j+self.dim/2, i+self.dim/2, \
                                fill=gradient_map(eval(function), \
                                gradient, \
                                high_threshold, low_threshold), \
                                width=0)
                    
                    except ZeroDivisionError:
                        pass

        
        
        except NameError:
            msg.showwarning("Equation Invalid", "Make sure your function is written in terms of x and y.")

root = tk.Tk()
root.title("2D Implicit Function Graph Renderer")
root.resizable(False, False)

normalFont = font.Font(family="Consolas", size = 10)
boldFont = font.Font(family="Consolas", size=10, weight="bold")

viewer = tk.LabelFrame(root, text="Rendering Pane", bd = 4, relief = "raised", font=boldFont)
viewer.grid(row = 0, column = 0, padx = 4, pady = 4)
settings = tk.LabelFrame(root, text="Settings", bd = 4, relief = "raised", font=boldFont)
settings.grid(row = 0, column = 1, padx = 4, pady = 4)

ctx = tk.Canvas(viewer, width = 1000, height = 500)
ctx.pack()

g = Grapher()
g.set_resolution(4)
g.graph_points(viewer, ctx, "sin(x / y)", -10, 10)

tk.mainloop()
