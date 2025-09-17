#!/usr/bin/env python
# Run the [Channel-Hillslope Integrated Landscape Development](https://csdms.colorado.edu/wiki/Model:CHILD) (CHILD) model in Python through [grpc4bmi](https://grpc4bmi.readthedocs.io).
# 
# CHILD computes the time evolution of a topographic surface *z(x,y,t)* by fluvial and hillslope erosion and sediment transport.
# 
# View the model source code and its BMI at https://github.com/childmodel/child.

# Start by importing some helper libraries.
import os
import pathlib
import numpy as np
import matplotlib.pyplot as plt

# Next, import the grpc4bmi Docker client.
from grpc4bmi.bmi_client_docker import BmiClientDocker

# Set variables:
# * which Docker image to use,
# * the port exposed through the image, and
# * the location of the configuration file used for the model.
DOCKER_IMAGE = "csdms/child-grpc4bmi:latest"
BMI_PORT = 55555
CONFIG_FILE = pathlib.Path("child.in")

# Create a model instance, `m`, through the grpc4bmi Docker client.
# It may take a moment to download the model image from Docker Hub.
m = BmiClientDocker(image=DOCKER_IMAGE, image_port=BMI_PORT, work_dir=".")

# Show the name of the model.
m.get_component_name()

# Start CHILD through its BMI with the configuration file defined above.
m.initialize(str(CONFIG_FILE))

# Show the input and output variables the model exposes through its BMI.
m.get_input_var_names(), m.get_output_var_names()

# Check time information provided by the model.
print("Start time:", m.get_start_time())
print("End time:", m.get_end_time())
print("Current time:", m.get_current_time())
print("Time step:", m.get_time_step())
print("Time units:", m.get_time_units())

# The main output variable for CHILD is topographic elevation
# (using the CSDMS Standard Name `land_surface__elevation`).
# Get the identifier for the grid on which this variable is defined.
grid_id = m.get_var_grid("land_surface__elevation")
print("Grid id:", grid_id)


# Get attributes of the grid.
print("Grid type:", m.get_grid_type(grid_id))

rank = m.get_grid_rank(grid_id)
print("Grid rank:", rank)

size = m.get_grid_size(grid_id)
print("Grid size:", size)

# The elevation values are defined on a 2D unstructured mesh grid.

# Allocate memory for the elevation variable and get its current values from CHILD.
# Note that *get_value* expects a one-dimensional array to receive output.
z = np.empty(size, dtype=float)
m.get_value("land_surface__elevation", z)
print(z)

# Work around an issue in grpc4bmi by loading the x and y coordinate values of the mesh grid saved directly from the CHILD model.
npzfile = np.load("xy_coords.npz")
x = npzfile["x"]
y = npzfile["y"]

# Define a convenience function for plotting.
def zplot(model, var_name, x, y, **kwds):
    gid = model.get_var_grid(var_name)
    gsize = model.get_grid_size(gid)
    z = np.empty(gsize, dtype=float)
    model.get_value(var_name, z)
    n_faces = model.get_grid_face_count(gid)
    face_nodes = np.empty(3 * n_faces, dtype=int)
    model.get_grid_face_nodes(gid, face_nodes)
    tris = face_nodes.reshape((-1, 3))
    plt.tripcolor(x, y, tris, z, **kwds)
    plt.axis("tight")
    plt.gca().set_aspect("equal")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    cbar = plt.colorbar()
    cbar.ax.set_ylabel(f"{var_name} ({model.get_var_units(var_name)})")

# This function generates plots that look like the one below.
# We can see the unstructed grid of triangles that CHILD uses.
zplot(m, "land_surface__elevation", x, y, edgecolors="k", vmin=-200, vmax=200, cmap="BrBG_r")
plt.savefig("view_grid.png", dpi=96)
plt.close()

# CHILD initializes elevations with random noise centered at 0.
# Change this to use elevations above and below sea level.
y_shore = 15000.0
z[y < y_shore] -= 100
z[y >= y_shore] += 100

# All nodes above `y=y_shore` are land, and all nodes below `y=y_shore` are sea. 
# Set the new elevation values in the model through its BMI.
m.set_value("land_surface__elevation", z)

# Display the new elevations.
zplot(m, "land_surface__elevation", x, y, edgecolors="k", vmin=-200, vmax=200, cmap="BrBG_r")
plt.savefig("initial_elevation.png", dpi=96)
plt.close()

# Now run the model until the year 5000. (This takes a few moments.)
m.update_until(5000.0)

# Plot the elevation values to see how they've evolved with time.
zplot(m, "land_surface__elevation", x, y, edgecolors="k", vmin=-200, vmax=200, cmap="BrBG_r")
plt.savefig("final_elevation.png", dpi=96)
plt.close()

# Stop the model and clean up the resources it allocates.
m.finalize()

# Stop the container running through grpc4bmi.
# This is needed by grpc4bmi to properly deallocate the resources it uses.
# It may take a few moments.
del m
