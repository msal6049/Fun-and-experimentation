import tkinter as tk
from tkinter import messagebox
import numpy as np
from scipy.integrate import odeint
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Gravitational constant
G = 6.67430e-11 # m^3 kg^-1 s^-2

# Define the system of ODEs
def three_body(Y, t, masses):
    r1, v1, r2, v2, r3, v3 = Y.reshape(6, -1)
    r12 = np.linalg.norm(r2 - r1)
    r13 = np.linalg.norm(r3 - r1)
    r23 = np.linalg.norm(r3 - r2)
    
    dv1dt = G * masses[1] * (r2 - r1) / r12**3 + G * masses[2] * (r3 - r1) / r13**3
    dv2dt = G * masses[0] * (r1 - r2) / r12**3 + G * masses[2] * (r3 - r2) / r23**3
    dv3dt = G * masses[0] * (r1 - r3) / r13**3 + G * masses[1] * (r2 - r3) / r23**3
    
    dr1dt = v1
    dr2dt = v2
    dr3dt = v3
    
    return np.concatenate((dr1dt, dv1dt, dr2dt, dv2dt, dr3dt, dv3dt))

def simulate():
    try:
        # Define the initial conditions and parameters
        masses = np.array([5.972e24, 1.989e30, 7.348e22])  # masses of earth, sun, and moon

        r1 = np.array([0, 0, 0])  # initial position of earth
        v1 = np.array([0, 0, 0])  # initial velocity of earth

        r2 = np.array([1.496e11, 0, 0])  # initial position of sun
        v2 = np.array([0, 0, 0])  # initial velocity of sun

        r3 = np.array([0, 3.844e8, 0])  # initial position of moon
        v3 = np.array([0, 0, 0])  # initial velocity of moon

        Y0 = np.concatenate((r1, v1, r2, v2, r3, v3))

        # Time array
        t = np.linspace(0, 365*24*60*60, 1000)  # one year

        # Solve the system of ODEs
        Y = odeint(three_body, Y0, t, args=(masses,))

        # Plot the solution
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111, projection='3d')

        ax.plot(Y[:, 0], Y[:, 1], Y[:, 2], label='Earth')  # earth
        ax.plot(Y[:, 6], Y[:, 7], Y[:, 8], label='Sun') 
