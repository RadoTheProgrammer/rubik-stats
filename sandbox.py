import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Data over time
labels = ['A', 'B', 'C', 'D']
data = [
    [324, 20, 40, 10],   # Time step 1
    [300, 50, 30, 14],   # Time step 2
    [280, 60, 50, 20],   # Time step 3
    [260, 90, 40, 30],   # Time step 4
]
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']

# Initial plot
#fig, ax = plt.subplots(figsize=(6, 6))
plt.figure(figsize=(7, 7))
#plt.subplots_adjust(bottom=0.2)  # Space for the button
wedges, texts, autotexts = plt.pie(data[0], labels=labels, colors=colors, autopct='',startangle=140)

# Function to update the pie chart
current_index = [0]  # Mutable container to track index
s=sum(data[0])
def update_chart(event):
    current_index[0] = (current_index[0] + 1) % len(data)  # Cycle through data
    sizes = data[current_index[0]]
    for i, wedge in enumerate(wedges):
        print(type(wedge))
        wedge.set_width(sizes[i]/sum(sizes))  # Update slice size
    for i, autotext in enumerate(autotexts):
        autotext.set_text(str(sizes[i]))  # Update text
    plt.draw()

# Add a button to switch data
ax_button = plt.axes([0.4, 0.05, 0.2, 0.075])  # Position
button = Button(ax_button, 'Next Step')
button.on_clicked(update_chart)

plt.axis('equal')
plt.title("Size Distribution Over Time")
plt.show()
