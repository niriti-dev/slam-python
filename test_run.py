import numpy as np
from matplotlib import pyplot as plt 

# Camera parameters (example values)

def generate_essential(): 
    focal_length = 1000  # Focal length in pixels
    principal_point = (500, 500)  # Principal point (cx, cy) in pixels
    baseline = 10  # Baseline in arbitrary units

    # Generate essential matrices for pure translation motion along the x-axis
    num_poses = 10  # Number of poses along the line
    translations = np.linspace(0, 50, num_poses)  # Generate translations along x-axis (horizontal)
    essential_matrices = []

    for translation in translations:
        # Translation vector (tx, ty, tz)
        translation_vector = np.array([translation, 0, 0])

        # Construct essential matrix
        essential_matrix = np.eye(3, 4)
        essential_matrix[:, 3] = -translation_vector * baseline  # Update translation based on baseline

        essential_matrices.append(essential_matrix)

    return essential_matrices
# Print the generated essential matrices
# for i, E in enumerate(essential_matrices):
#     print(f"Essential Matrix {i + 1}:")
#     print(E)
#     print()



def generate_essential_with_rotation():
    # Camera parameters (example values)
    focal_length = 1000  # Focal length in pixels
    principal_point = (500, 500)  # Principal point (cx, cy) in pixels
    baseline = 10  # Baseline in arbitrary units

    # Generate essential matrices for rotation around the z-axis
    num_poses = 10  # Number of poses
    rotation_angles = np.linspace(0, 2 * np.pi, num_poses)  # Generate rotation angles
    essential_matrices = []

    for angle in rotation_angles:
        # Rotation matrix around z-axis
        rotation_matrix = np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1]
        ])

        # Construct essential matrix with zero translation along x and y axes
        essential_matrix = np.zeros((3, 4))
        essential_matrix[:3, :3] = rotation_matrix

        essential_matrices.append(essential_matrix)

    return essential_matrices

def decompose_essential_matrices(essential_matrices):
    # Extract translation vectors from essential matrices
    translations = []
    for E in essential_matrices:
        translations.append(E[:, 3])

    return np.array(translations)

def plot_camera_movement(translations):
    # Plot camera movement in 2D map
    plt.figure(figsize=(8, 6))
    plt.plot(translations[:, 0], np.zeros_like(translations[:, 0]), marker='o', color='b')
    plt.title('Camera Movement in 2D Map')
    plt.xlabel('X position')
    plt.ylabel('Y position')
    plt.grid(True)
    plt.show()

def main(): 
    essentials = generate_essential_with_rotation() 
    translations = decompose_essential_matrices(essentials)
    plot_camera_movement(translations)

main()

