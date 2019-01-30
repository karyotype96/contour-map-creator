import tkinter as tk
import tkinter.font as font
import tkinter.messagebox as msg
from math import *
from colour import Color
import time

def map_coordinates(x, y, dim):
    mapped_x = (x * dim) + 400
    mapped_y = (-y * dim) + 250
    return mapped_x, mapped_y

def unmap_coordinates(x, y, dim):
    unmapped_x = (x - 400) / dim
    unmapped_y = (y - 250) / -dim
    return unmapped_x, unmapped_y

def constrain(value, minimum, maximum):
    if value > maximum:
        value = maximum
    elif value < minimum:
        value = minimum
        
    return value

def gradient_map(value, gradient, value_minimum, value_maximum):
    grad_pos = constrain(ceil((value - value_minimum) / (value_maximum - value_minimum) * 1023), 0, 1024)
    
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
            ctx.delete("all")
            gradient = list(Color("white").range_to(Color("black"), 1024))
            tester = 0
            for i in range(0, 500, ceil(self.dim)):
                for j in range(0, 800, ceil(self.dim)):
                    x, y = unmap_coordinates(j, i, self.scaling)
                    try:
                        tester = eval(function)
                        ctx.create_rectangle(j-self.dim/2.0, i-self.dim/2.0, \
                                j+self.dim/2.0, i+self.dim/2.0, \
                                fill=gradient_map(eval(function), \
                                gradient, \
                                high_threshold, low_threshold), \
                                width=0)
                    
                    except ZeroDivisionError:
                        pass
                    except TypeError:
                        ctx.create_rectangle(j-self.dim/2.0, i-self.dim/2.0, \
                                j+self.dim/2.0, i+self.dim/2.0, \
                                fill="blue", \
                                width=0)
                    except ValueError:
                        ctx.create_rectangle(j-self.dim/2.0, i-self.dim/2.0, \
                                j+self.dim/2.0, i+self.dim/2.0, \
                                fill="blue", \
                                width=0)
                    except IndexError:
                        ctx.create_rectangle(j-self.dim/2.0, i-self.dim/2.0, \
                                j+self.dim/2.0, i+self.dim/2.0, \
                                fill="blue", \
                                width=0)

                ctx.update_idletasks()
                
        
        except NameError:
            msg.showwarning("Equation Invalid", "Make sure your function is written in terms of x and y.")

root = tk.Tk()
root.title("Contour Graph Renderer")
root.resizable(False, False)

normalFont = font.Font(family="Consolas", size = 10)
boldFont = font.Font(family="Consolas", size=10, weight="bold")

viewer = tk.LabelFrame(root, text="Rendering Pane", bd = 4, relief = "raised", font=boldFont)
viewer.grid(row = 0, column = 0, padx = 4, pady = 4)
settings = tk.LabelFrame(root, text="Settings", bd = 4, relief = "raised", font=boldFont)
settings.grid(row = 0, column = 1, padx = 4, pady = 4)

ctx = tk.Canvas(viewer, width = 800, height = 500)
ctx.pack()

g = Grapher()

equationFieldLabel = tk.Label(settings, text="Equation: ")
equationFieldLabel.grid(row = 0, column = 0, padx = 2, pady = 2)
equationField = tk.Entry(settings)
equationField.insert(tk.END, "sin(x)*cos(y)")
equationField.grid(row = 0, column = 2, padx = 2, pady = 2)
equationFieldButton = tk.Button(settings, text="Render!", command=lambda: construct(viewer, ctx))
equationFieldButton.grid(row = 0, column = 3, padx = 2, pady = 2)

lowBoundLabel = tk.Label(settings, text="Low bound:")
lowBoundLabel.grid(row = 1, column = 0, padx = 2, pady = 2)
lowBoundEntry = tk.Entry(settings)
lowBoundEntry.insert(tk.END, "-1")
lowBoundEntry.grid(row = 1, column = 1, padx = 2, pady = 2)
highBoundLabel = tk.Label(settings, text = "High bound: ")
highBoundLabel.grid(row = 1, column = 2, padx = 2, pady = 2)
highBoundEntry = tk.Entry(settings)
highBoundEntry.insert(tk.END, "1")
highBoundEntry.grid(row = 1, column = 3, padx = 2, pady = 2)

resLabel = tk.Label(settings, text="Resolution: ")
resLabel.grid(row = 2, column = 0, padx = 2, pady = 2)
resSlider = tk.Scale(settings, from_=1, to_=5, orient=tk.HORIZONTAL)
resSlider.grid(row = 2, column = 1, padx = 2, pady = 2)

def construct(viewer, ctx):
    function = equationField.get()
    low_bound = int(lowBoundEntry.get())
    high_bound = int(highBoundEntry.get())
    res = resSlider.get()
    g.set_resolution(res)
    g.graph_points(viewer, ctx, function, low_bound, high_bound)

tk.mainloop()
