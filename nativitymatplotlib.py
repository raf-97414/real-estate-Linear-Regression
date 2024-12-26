# -*- coding: utf-8 -*-
"""nativitymatplotlib.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ua3Kdio7qr_RQez5s7OjtPQbdLAXTmnr
"""

#Nativity scene using K-Means Clustering on matplotlib
#imports
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

#function to plot random number of points anf saving point locations as numpy array for each points location of an element using numpy here just a random spread of points is plotted
def plot_points_for_cluster(center, n_points, spread):
  return np.random.normal(loc=center,scale=spread,size=(n_points,2))

#Creating points for each element representation in the nativity
shed = plot_points_for_cluster([0, 0], 200, 0.5)  # Shed points
joseph = plot_points_for_cluster([-0.5, -0.5], 30, 0.1)
mary = plot_points_for_cluster([0.5, -0.5], 30, 0.1)
baby_jesus = plot_points_for_cluster([0, -1], 20, 0.05)
three_kings = plot_points_for_cluster([2, 2], 50, 0.2)
shepherds = plot_points_for_cluster([-2, 1.5], 50, 0.3)
animals = plot_points_for_cluster([1, -2], 50, 0.4)
angel = plot_points_for_cluster([0, 3], 30, 0.2)
star = plot_points_for_cluster([0, 3.5],1,0)  # Single point for the star
lights = plot_points_for_cluster([0, 0], 100, 3)  # Lights scattered randomly
#combine all the elements into the scene just plots points in row wise stacks
nativity = np.vstack([shed,joseph,mary,baby_jesus,three_kings,shepherds,animals,angel,star,lights])
#Step 2 : Start clustering using KMEANS to form the shape of the elements by creating the clusters , the centroids of those clusters and plotting the points belonging to those clusters based on its numpy array location
clustering = KMeans(n_clusters=9,random_state=42)
element_labels = clustering.fit_predict(nativity)

#Step 3 : Making points colourful by mapping each label to a colour
color = [

    '#8B4513',
    '#ADD8E6',
    '#FF0000',
    '#A52A2A',
    '#FFBF00',
    '#008000',
    '#F5F5DC',
    '#808080',
    '#FFFF99'
]

cluster_names = {
                0:'Shed',
                1:'Joseph',
                2:'Mary',
                3:'Baby Jesus',
                4:'Three Kings',
                5:'Shepherds',
                6:'Animals',
                7:'Angel',
                8:'Star'}

#Step 4 : Plotting the points for visualization
fig,ax = plt.subplots(figsize=(8,8))
fig.set_facecolor('black')
for cluster_id,cluster_name in cluster_names.items():
  cluster_points = nativity[element_labels==cluster_id]
  scatter = ax.scatter(cluster_points[:,0],cluster_points[:,1],c=color[cluster_id])

for cluster_id, cluster_name in cluster_names.items():
    center_x, center_y = clustering.cluster_centers_[cluster_id]  # Get cluster center
    ax.text(center_x, center_y, cluster_name, color='black', fontsize=13,
            ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
ax.set_title("Nativity Scene.....It's a Blessed Christmas")
ax.legend()
ax.axis('off')

plt.show()



#Step 5: Twinkling of lights
from PIL import Image

frames = []  # List to store each frame of the animation
fig, ax = plt.subplots(figsize=(8, 8))

for i in range(30):  # Generate 30 frames for the animation
    ax.clear()  # Clear the axes for the new frame
    fig.set_facecolor('black')  # Set the background color to black
    ax.axis('off')  # Turn off the axes

    # Plot clusters with flickering lights
    for cluster_id, cluster_name in cluster_names.items():
        cluster_points = nativity[element_labels == cluster_id]  # Points for this cluster
        flicker_color = np.random.choice(color)  # Random color for flickering effect
        ax.scatter(cluster_points[:, 0], cluster_points[:, 1], color=flicker_color)
        center_x, center_y = clustering.cluster_centers_[cluster_id]  # Get cluster center
        ax.text(center_x, center_y, cluster_name, color='black', fontsize=13,
            ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))

    ax.set_title("Nativity Scene.....It's a Blessed Christmas")


    # Save the current frame as an image
    plt.tight_layout()
    fig.canvas.draw()

    # Convert the current frame to a Pillow Image
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    pil_image = Image.fromarray(image)
    frames.append(pil_image)  # Add the frame to the list

plt.close()  # Close the Matplotlib figure

# Save the frames as a GIF using Pillow
frames[0].save(
    'nativity_scene_black_background.gif',
    save_all=True,
    append_images=frames[1:],
    duration=100,  # Duration of each frame in milliseconds
    loop=0         # Loop forever
)

print("Animation saved as 'nativity_scene_black_background.gif'")