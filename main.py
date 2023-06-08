import pybullet as p
import time
import tkinter as tk
import math

def run_simulation():

    # Initialize PyBullet
    p.connect(p.GUI)
    #Set the gravity to point downwards
    p.setGravity(0, 0, -9.8)

    # Create the plane
    plane_id = p.createCollisionShape(p.GEOM_PLANE)
    plane_visual_id = p.createVisualShape(p.GEOM_PLANE, rgbaColor=[0.5, 0.5, 0.5, 1])
    plane_body_id = p.createMultiBody(0, plane_id, plane_visual_id)

    # Create the phone
    phone_weight = float(weight_entry.get())/1000 #convert gr to kg

    base_width = float(width_entry.get())
    base_depth = float(depth_entry.get())
    base_height = float(height_entry.get())
    drop_height = float(drop_height_entry.get())
    
    phone_id = p.createCollisionShape(p.GEOM_BOX, halfExtents=[base_width, base_depth, base_height])
    phone_visual_id = p.createVisualShape(p.GEOM_BOX, halfExtents=[base_width, base_depth, base_height], rgbaColor=[1, 0, 0, 1])
    phone_body_id = p.createMultiBody(phone_weight, phone_id, phone_visual_id)
    p.resetBasePositionAndOrientation(phone_body_id, [0, 0, drop_height],
                                      [float(orientation_entry[0].get()), float(orientation_entry[1].get()), float(orientation_entry[2].get()), 1])

    max_impact_energy = 0
    # Run the simulation
    for i in range(1000):
        p.stepSimulation()
        time.sleep(1/240)  # Delay to control the simulation speed

        #Calculating the impact energy (one of the ways for the damage)
        phone_mass = p.getDynamicsInfo(phone_body_id,-1)[0]
        phone_velocity, phone_angular_velocity = p.getBaseVelocity(phone_body_id)
        phone_velocity_magnitude = math.pow(math.pow(phone_velocity[0], 2) + math.pow(phone_velocity[1], 2) + math.pow(phone_velocity[2], 2), 0.5)
        impact_energy = 0.5*phone_mass*phone_velocity_magnitude
        print(f"Impact energy: {impact_energy}")
        if impact_energy>max_impact_energy:
            max_impact_energy   = impact_energy
    # Keep the window open until explicitly closed
    print(f"Maximum impact energy: {max_impact_energy}")

    while True:
        p.getCameraImage(640, 480)  # Call a PyBullet function to keep the window open
        time.sleep(0.01)

def fill_dimension_values(weight, width, depth, height):
    weight_entry.delete(0, weight_entry.__sizeof__())
    width_entry.delete(0, width_entry.__sizeof__())
    depth_entry.delete(0, depth_entry.__sizeof__())
    height_entry.delete(0, height_entry.__sizeof__())
    weight_entry.insert(0, weight)
    width_entry.insert(0, width)
    depth_entry.insert(0, depth)
    height_entry.insert(0, height)

window = tk.Tk() #Create a UI
label = tk.Label(window, text="Adjust the value according to your needs!")
label.grid(row=0, column=0, columnspan=2)


weight_label = tk.Label(window, text="Weight (gr):")
weight_label.grid(row=1, column=0)
weight_entry = tk.Entry(window)
weight_entry.grid(row=1, column=1)
weight_entry.insert(0, 1000)

width_label = tk.Label(window, text="Width (m):")
width_label.grid(row=2, column=0)
width_entry = tk.Entry(window)
width_entry.grid(row=2, column=1)
width_entry.insert(0, 1)

depth_label = tk.Label(window, text="Depth (m):")
depth_label.grid(row=3, column=0)
depth_entry = tk.Entry(window)
depth_entry.grid(row=3, column=1)
depth_entry.insert(0, 1)

height_label = tk.Label(window, text="Height (m):")
height_label.grid(row=4, column=0)
height_entry = tk.Entry(window)
height_entry.grid(row=4, column=1)
height_entry.insert(0, 1)

drop_height_label = tk.Label(window, text="Drop Height (m):")
drop_height_label.grid(row=5, column=0)
drop_height_entry = tk.Entry(window)
drop_height_entry.grid(row=5, column=1)
drop_height_entry.insert(0, 5)

orientation_entry_label = tk.Label(window, text="Orientation° (x, y, z): ")
orientation_entry_label.grid(row=6, column=0)
orientation_entry = tk.Entry(window), tk.Entry(window), tk.Entry(window)
orientation_entry[0].grid(row=6, column=1)  # x
orientation_entry[0].insert(0, 0)
orientation_entry[1].grid(row=6, column=2)  # y
orientation_entry[1].insert(0, 0)
orientation_entry[2].grid(row=6, column=3)  # z
orientation_entry[2].insert(0, 0)

simulation_button = tk.Button(window, text="Begin Simulation",command=lambda:run_simulation())
simulation_button.grid(row=7, column=0, columnspan=4)

presets_label = tk.Label(window, text="Presets")
presets_label.grid(row=0, column=2, columnspan=2)

preset1_button = tk.Button(window, text="Phone", command=lambda:fill_dimension_values(175, 0.075, 0.008, 0.16))
preset1_button.grid(row=2, column=2, columnspan=2)

preset2_button = tk.Button(window, text="Tablet", command=lambda:fill_dimension_values(400, 0.160, 0.007, 0.24))
preset2_button.grid(row=4, column=2, columnspan=2)

window.mainloop() #Launch the UI in an endless loop
