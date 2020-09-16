# General imports
import tkinter as tk
from scipy import constants as const
import numpy as np


class Pendulum():
    def __init__(self, pos: np.ndarray, radi: float, length: float, width: int = 3):
        """Creates a Pendulum with a given position, velocity, length and mass.
        width represent the width of the rope of the pendulum.
        The size of the pendulum is proportional to its mass."""

        self.pos = pos
        self.radi = radi
        self.length = length
        self.width = width


class App(tk.Tk):
    def __init__(self,
                 pendulum_1: Pendulum, pendulum_2: Pendulum, gap: float, temps_exec: float, temps: np.ndarray,
                 width: int = 1200, height: int = 600,
                 offset_width: int = 600, offset_height: int = 300,
                 dt: float = 0.05, count: int = 0):
        """Initialize the widget for the double pendulum animation.

        offset_width and offset_height represent the x and y offsets from the
        top left corner of the canvas to place the first pendulum."""

        # Setting attributes
        self.width = width
        self.height = height
        self.offset_width = offset_width
        self.offset_height = offset_height
        self.temps = temps
        self.dt = dt
        self.count = count
        self.pendulum_1 = pendulum_1
        self.pendulum_2 = pendulum_2
        self.gap = gap
        self.temps_exec = temps_exec
        self.escala_moviment = 0.95 * (width - escala * (4. * R + gap)) / (2.*np.max(A) * escala)
        print(self.escala_moviment)

        # Setting canvas widget
        tk.Tk.__init__(self)
        self.title("Newton's Cradle")
        self.canvas = tk.Canvas(self,
                                width=self.width, height=self.height)
        self.canvas.pack(side="top")

        # Action
        self.after(20, self.draw_frame)

    def update_pendulums_positions(self):
        """Update the angle positions and velocities of the two pendulums"""
        # Update the velocities and positions
        i = 1
        while self.temps[self.count+i] < self.temps[self.count] + self.dt:
            i += 1
        self.count += i

    def draw_pendulums(self):
        """Draw the two pendulums"""

        # Cartesian coordinates
        x1 = self.pendulum_1.pos[self.count]*self.escala_moviment
        # y1 = self.pendulum_1.length

        x2 = self.pendulum_2.pos[self.count]*self.escala_moviment + self.pendulum_2.radi + self.pendulum_2.radi + self.gap
        # y2 = self.pendulum_2.length

        # Draw the first pendulum
        """self.canvas.create_line(
            self.offset_width, self.offset_height,
            self.offset_width + x1, self.offset_height + y1,
            width=self.pendulum_1.width, fill='red', tags='pendulum', alpha=0
        )"""
        self.canvas.create_oval(
            self.offset_width - self.pendulum_1.radi + x1,
            # self.offset_height - self.pendulum_1.radi + y1,
            self.offset_height - self.pendulum_1.radi,
            self.offset_width + self.pendulum_1.radi + x1,
            # self.offset_height + self.pendulum_1.radi + y1,
            self.offset_height + self.pendulum_1.radi,
            fill='red', outline='red', tags='pendulum'
        )

        # Draw the second pendulum
        """self.canvas.create_line(
            self.offset_width + self.pendulum_2.radi + self.pendulum_2.radi + self.gap, self.offset_height,
            self.offset_width + x2, self.offset_height + y2,
            width=self.pendulum_2.width, fill='blue', tags='pendulum', alpha=0
        )"""
        self.canvas.create_oval(
            self.offset_width - self.pendulum_2.radi + x2,
            # self.offset_height - self.pendulum_2.radi + y2,
            self.offset_height - self.pendulum_2.radi,
            self.offset_width + self.pendulum_2.radi + x2,
            # self.offset_height + self.pendulum_2.radi + y2,
            self.offset_height + self.pendulum_2.radi,
            fill='blue', outline='blue', tags='pendulum'
        )


    def draw_frame(self):
        """Draw the current frame"""

        # Delete objects on the canvas to redraw
        self.canvas.delete('pendulum')
        self.canvas.delete('text')

        # Update the positions and draw the frame
        self.update_pendulums_positions()
        self.draw_pendulums()
        self.canvas.create_text(50, 30, font = ("Helvetica", 20), anchor='nw',
                                text="t/T0 = %.2f \ngap = %.1f mm \nR = %.1f mm" % (self.temps[self.count]/T0, gap * 1e3, R * 1e3), tags='text')

        # print((self.pendulum_1.pos[self.count], self.pendulum_1.pos[self.count]))
        print(self.temps[self.count]/T0)

        # Repeat
        self.after(20, self.draw_frame)


if __name__ == '__main__':
    pass

escala = 350

g = const.g

nom_inp = "../Simulacions/Gaps200dmm/Gaps_2_0_GG_200dmm"
metadata = open(nom_inp + ".dat", "r")

N = int(metadata.readline())
g = float(metadata.readline())
L = float(metadata.readline())
R = float(metadata.readline())
eta = float(metadata.readline())
gamma = float(metadata.readline())
pas = float(metadata.readline())
num_osc = float(metadata.readline())
gap = float(metadata.readline())

A = metadata.readline().split(" ")[:-1]
m = metadata.readline().split(" ")[:-1]
E = metadata.readline().split(" ")[:-1]
j = metadata.readline().split(" ")[:-1]

A = np.array([float(i) for i in A])
m = np.array([float(i) for i in m])
E = np.array([float(i) for i in E])
j = np.array([float(i) for i in j])


T0 = 2*const.pi*np.sqrt(L/g)               #periode dels pèndols

temps_exec = num_osc*T0                    #temps d'execució

data = np.genfromtxt(nom_inp+".csv", delimiter=",")
pos1 = data[:,1]
pos2 = data[:,2]
temps = data[:,0]

pos1 = pos1*escala
pos2 = pos2*escala


# Initialization of the two pendulums


pendulum_1_parameters = {
    "pos": pos1,
    "radi": R*escala,
    "length": L*escala
}

pendulum_2_parameters = {
    "pos": pos2,
    "radi": R*escala,
    "length":L*escala
}

pendulum_1 = Pendulum(**pendulum_1_parameters)
pendulum_2 = Pendulum(**pendulum_2_parameters)

# Run the animation
animation_parameters = {
    "pendulum_1": pendulum_1,
    "pendulum_2": pendulum_2,
    "gap": gap*escala,
    "temps_exec": temps_exec,
    "temps": temps,
    "dt": 0.01
}
app = App(**animation_parameters)
app.mainloop()
