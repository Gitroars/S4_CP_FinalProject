import pybullet as p
import time
import tkinter as tk
import math

def run_simulation():

    # Initialize PyBullet
    p.connect(p.GUI)
    p.setGravity(0, 0, -9.81)

    # Create the plane
    plane_id = p.createCollisionShape(p.GEOM_PLANE)
    plane_visual_id = p.createVisualShape(p.GEOM_PLANE, rgbaColor=[0.5, 0.5, 0.5, 1])
    plane_body_id = p.createMultiBody(0, plane_id, plane_visual_id)

    # Create the phone
    phone_weight = float(weight_entry.get()) / 1000  # convert grams to kilograms

    base_width = float(width_entry.get())
    base_depth = float(depth_entry.get())
    base_height = float(height_entry.get())
    drop_height = float(drop_height_entry.get())

    phone_id = p.createCollisionShape(p.GEOM_BOX, halfExtents=[base_width, base_depth, base_height])
    phone_visual_id = p.createVisualShape(p.GEOM_BOX, halfExtents=[base_width, base_depth, base_height], rgbaColor=[1, 0, 0, 1])
    phone_body_id = p.createMultiBody(phone_weight, phone_id, phone_visual_id)
    p.resetBasePositionAndOrientation(
        phone_body_id, [0, 0, drop_height], [float(orientation_entry[0].get()), float(orientation_entry[1].get()), float(orientation_entry[2].get()), 1]
    )


    phone_rest_threshold = 0.001

    # Damage Thresholds
   

    
    impact_energies = []
    highest_damage_level = 0

    # Run the simulation
    while True:
        p.stepSimulation()
        time.sleep(1 / 240)  # Delay to control the simulation speed

        # Calculating the impact energy
        phone_mass = p.getDynamicsInfo(phone_body_id, -1)[0]
        phone_velocity, phone_angular_velocity = p.getBaseVelocity(phone_body_id)
        phone_velocity_magnitude = math.sqrt(phone_velocity[0] ** 2 + phone_velocity[1] ** 2 + phone_velocity[2] ** 2)
        initial_potential_energy = phone_mass * 9.81 * drop_height
        final_potential_energy = phone_mass * 9.81 * 0
        impact_energy = initial_potential_energy - final_potential_energy

        impact_energies.append(impact_energy)
        
        
        
        if phone_velocity_magnitude < phone_rest_threshold and all(v < 0.01 for v in phone_angular_velocity):
            break

    
    max_impact_energy = 0
    total_energy = 0
    # Calculate the adjusted thresholds based on the maximum impact energy
    for impact_energy in impact_energies:
        total_energy += impact_energy
        max_impact_energy = max(max_impact_energy, impact_energy)

    threshold_minor = 0.5
    threshold_moderate = 1.0
    threshold_severe = 2.0


    # Calculating the damage
    for impact_energy in impact_energies:
        if impact_energy >= threshold_severe:
            highest_damage_level = 4
            print()
        elif impact_energy >= threshold_moderate:
            highest_damage_level = max(highest_damage_level, 3)
        elif impact_energy >= threshold_minor:
            highest_damage_level = max(highest_damage_level, 2)
        else:
            highest_damage_level = max(highest_damage_level, 1)

    if highest_damage_level == 4:
        print("Extensive damage. Barely functional or non-functional")
    elif highest_damage_level == 3:
        print("Moderate damage. Noticeable structural damage.")
    elif highest_damage_level == 2:
        print("Minor damage. Functional with cosmetic damage.")
    else:
        print("No significant damage.")

    # Keep the window open until explicitly closed
    while True:
        p.getCameraImage(640, 480)  # Call a PyBullet function to keep the window open
        time.sleep(0.01)

def fill_dimension_values(weight, width, depth, height):
    weight_entry.delete(0, tk.END)
    width_entry.delete(0, tk.END)
    depth_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    weight_entry.insert(0, weight)
    width_entry.insert(0, width)
    depth_entry.insert(0, depth)
    height_entry.insert(0, height)

window = tk.Tk()  # Create a UI
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
drop_height_entry.insert(0, 0.1)

orientation_entry_label = tk.Label(window, text="Orientation° (x, y, z): ")
orientation_entry_label.grid(row=6, column=0)
orientation_entry = tk.Entry(window), tk.Entry(window), tk.Entry(window)
orientation_entry[0].grid(row=6, column=1)  # x
orientation_entry[0].insert(0, 0)
orientation_entry[1].grid(row=6, column=2)  # y
orientation_entry[1].insert(0, 0)
orientation_entry[2].grid(row=6, column=3)  # z
orientation_entry[2].insert(0, 0)

simulation_button = tk.Button(window, text="Begin Simulation", command=lambda: run_simulation())
simulation_button.grid(row=7, column=0, columnspan=4)

presets_label = tk.Label(window, text="Presets")
presets_label.grid(row=0, column=2, columnspan=2)

preset1_button = tk.Button(window, text="Phone", command=lambda: fill_dimension_values(175, 0.075, 0.008, 0.16))
preset1_button.grid(row=2, column=2, columnspan=2)

preset2_button = tk.Button(window, text="Tablet", command=lambda: fill_dimension_values(400, 0.16, 0.007, 0.24))
preset2_button.grid(row=4, column=2, columnspan=2)

window.mainloop()  # Launch the UI in an endless loop
