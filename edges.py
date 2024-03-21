import os
import cv2

import numpy as np 
# Input and output directories
directory = "project_img"
output_dir = "edge_images"

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iterate over all images in the input directory

for item in sorted(os.listdir(directory)): 
    image_path = os.path.join(directory, item)
    print("image_path: ", image_path)
    image = cv2.imread(image_path)
    original_image = image.copy()  # Make a copy for visualization



    # Convert the image to grayscale (required for Canny Edge Detector)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Compute edges using the Canny Edge Detector
    edges = cv2.Canny(gray_image, 100, 200)  # Adjust the threshold values as needed
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=120)

    # Draw detected lines on the original image
    if lines is not None:
        for rho, theta in lines[:, 0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(original_image, (x1, y1), (x2, y2), (0, 0, 255), 2)
    
    
    # Save the edge-detected image to the output directory
    output_path = os.path.join(output_dir, item)
    cv2.imwrite(output_path, original_image)

    print(f"Edges computed for {item}")

print("Edge computation complete.")
