import pybullet as p
import time
import tkinter as tk



window = tk.Tk() #Create a UI
label = tk.Label(window, text="Adjust the value according to your needs!")
label.grid(row=0, column=0)


weight_label = tk.Label(window, text="Weight (gr):")
weight_label.grid(row=1,column=0)

width_label = tk.Label(window, text="Width:")
width_label.grid(row=2, column=0)
width_entry = tk.Entry(window)
width_entry.grid(row=2,column=1)

depth_label = tk.Label(window, text="Depth:")
depth_label.grid(row=2, column=2)
depth_entry = tk.Entry(window)
depth_entry.grid(row=2,column=3)

height_label = tk.Label(window, text="Height:")
height_label.grid(row=2, column=4)
height_entry = tk.Entry(window)
height_entry.grid(row=2,column=5)




window.mainloop() #Launch the UI




# Initialize PyBullet
p.connect(p.GUI)
#Set the gravity to point downwards
p.setGravity(0, 0, -9.8)

# Create the plane
plane_id = p.createCollisionShape(p.GEOM_PLANE)
plane_visual_id = p.createVisualShape(p.GEOM_PLANE, rgbaColor=[0.5, 0.5, 0.5, 1])
plane_body_id = p.createMultiBody(0, plane_id, plane_visual_id)

# Create the phone
base_width = 0.1 
base_depth = 0.1 # Size of the phone base
base_height = 0.01  # Height of the phone base
phone_id = p.createCollisionShape(p.GEOM_BOX, halfExtents=[base_width, base_depth, base_height])
phone_visual_id = p.createVisualShape(p.GEOM_BOX, halfExtents=[base_width, base_depth, base_height], rgbaColor=[1, 0, 0, 1])
phone_body_id = p.createMultiBody(1, phone_id, phone_visual_id)
p.resetBasePositionAndOrientation(phone_body_id, [0, 0, 1], [0, 0, 0, 1])

max_impact_energy = 0
# Run the simulation
for i in range(1000):
    p.stepSimulation()
    time.sleep(1/240)  # Delay to control the simulation speed

    #Calculating the impact energy (one of the ways for the damage)
    phone_mass = p.getDynamicsInfo(phone_body_id,-1)[0]
    phone_velocity,_ = p.getBaseVelocity(phone_body_id)
    phone_velocity_magnitude = (phone_velocity[0]**2 + phone_velocity[1]**2 + phone_velocity[2]**2)**0.5
    impact_energy = 0.5*phone_mass*phone_velocity_magnitude
    print(f"Impact energy: {impact_energy}")
    if impact_energy>max_impact_energy:
        max_impact_energy   = impact_energy
# Keep the window open until explicitly closed
print(f"Maximum impact energy: {max_impact_energy}")

while True:
    p.getCameraImage(640, 480)  # Call a PyBullet function to keep the window open
    time.sleep(0.01)
