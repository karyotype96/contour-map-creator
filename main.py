from tkinter import *
from tkinter.font import *
from math import *

def map_coordinates(x, y, dim):
    mapped_x = (x * dim) + 500
    mapped_y = (-y * dim) + 250
    return mapped_x, mapped_y

def unmap_coordinates(x, y, dim):
    unmapped_x = (x - 500) / dim
    unmapped_y = (y - 250) / -dim
    return unmapped_x, unmapped_y

class Grapher:
    def __init__(self):
        self.dim = 20.0 / 2.0 ** 4.0
        self.scaling = 50.0
        
    def set_resolution(self, resolution):
        self.dim = 20.0 / 2.0 ** resolution
        
    def set_scaling(self, scaling):
        self.scaling = scaling
        
    def graph_points(self, ctx, left_side, right_side, threshold):
        try:
            for i in range(0, 500, floor(self.dim)):
                for j in range(0, 1000, floor(self.dim)):
                    x, y = unmap_coordinates(j, i, self.scaling)
                    try:
                        if abs(eval(left_side) - eval(right_side)) <= threshold:
                            ctx.create_rectangle(j-self.dim/2.0, i-self.dim/2, j+self.dim/2, i+self.dim/2, fill="red", width=0)
                    
                    except ZeroDivisionError:
                        pass
        
        
        except NameError:
            print("invalid equation")

root = Tk()
root.title("2D Implicit Function Graph Renderer")
root.resizable(False, False)

normalFont = Font(family="Consolas", size = 10)
boldFont = Font(family="Consolas", size=10, weight="bold")

viewer = LabelFrame(root, text="Rendering Pane", bd = 4, relief = "raised", font=boldFont)
viewer.grid(row = 0, column = 0, padx = 4, pady = 4)
settings = LabelFrame(root, text="Settings", bd = 4, relief = "raised", font=boldFont)
settings.grid(row = 0, column = 1, padx = 4, pady = 4)

ctx = Canvas(viewer, width = 1000, height = 500)
ctx.pack()

g = Grapher()
g.graph_points(ctx, "sin(x)*cos(y)", "0", 0.1)

mainloop()