import pybullet as p
import time
import tkinter as tk

def get_input():
    weight_input = weight_entry.get()

window = tk.Tk() #Create a UI
label = tk.Label(window, text="Adjust the value according to your needs!")
label.grid(row=0, column=0)

#Text labels
weight_label = tk.Label(window, text="Weight (gr):")
size_label = tk.Label(window, text="Size:")
weight_label.grid(row=1,column=0)
size_label.grid(row=2, column=0)
#Input Fields
weight_entry = tk.Entry(window)
weight_entry.grid(row=1,column=1)
size_entry = tk.Entry(window)
size_entry.grid(row=2,column=1)





window.mainloop() #Launch the UI




# Initialize PyBullet
p.connect(p.GUI)
p.setGravity(0, 0, -9.8)

# Create the plane
plane_id = p.createCollisionShape(p.GEOM_PLANE)
plane_visual_id = p.createVisualShape(p.GEOM_PLANE, rgbaColor=[0.5, 0.5, 0.5, 1])
plane_body_id = p.createMultiBody(0, plane_id, plane_visual_id)

# Create the phone
base_size = 0.1  # Size of the phone base
base_height = 0.01  # Height of the phone base
phone_id = p.createCollisionShape(p.GEOM_BOX, halfExtents=[base_size, base_size, base_height])
phone_visual_id = p.createVisualShape(p.GEOM_BOX, halfExtents=[base_size, base_size, base_height], rgbaColor=[1, 0, 0, 1])
phone_body_id = p.createMultiBody(1, phone_id, phone_visual_id)
p.resetBasePositionAndOrientation(phone_body_id, [0, 0, 1], [0, 0, 0, 1])

# Run the simulation
for i in range(1000):
    p.stepSimulation()
    time.sleep(1/240)  # Delay to control the simulation speed

# Keep the window open until explicitly closed
while True:
    p.getCameraImage(640, 480)  # Call a PyBullet function to keep the window open
    time.sleep(0.01)
