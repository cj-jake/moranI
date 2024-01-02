import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import imageio

# Create sample data
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
x, y = np.meshgrid(x, y)
z = np.sin(np.sqrt(x**2 + y**2))

# Create a 3D figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the 3D surface
ax.plot_surface(x, y, z, cmap='viridis')

# Set titles and labels
ax.set_title('3D Surface Plot')
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
plt.show(block=False)
# Generate and save animation as GIF using imageio
filename = '3dplot.gif'
frames = []
for i in range(0, 360, 2):
    ax.view_init(elev=i, azim=i)
    fig.canvas.draw()
    frame = np.array(fig.canvas.renderer.buffer_rgba())
    frames.append(frame)

# Save frames as GIF using imageio
imageio.mimsave(filename, frames, duration=50)  # Set the duration in milliseconds per frame
print()
