import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Initial data
sizes = [30, 40, 50]
labels = ['A', 'B', 'C']

fig, ax = plt.subplots()
wedges, _, _ = ax.pie(sizes, labels=labels, autopct='%1.1f%%')

def update(frame):
    global sizes
    sizes = [s + 2 for s in sizes]  # Example: Increase all sizes dynamically
    ax.clear()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')

ani = FuncAnimation(fig, update, frames=5, interval=1000)  # Update every second

plt.show()
