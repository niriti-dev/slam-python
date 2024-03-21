import open3d as o3d
import numpy as np

# Load all point clouds
point_clouds = []
for i in range(1, 22):
    pc_path = f"/Users/niriti/slam-python/pt_cloud{i}.ply"
    pc = o3d.io.read_point_cloud(pc_path)
    point_clouds.append(pc)

registered_point_clouds = [point_clouds[0]]  # Initialize with the first point cloud
for i in range(1, len(point_clouds)):
    source = point_clouds[i]
    target = registered_point_clouds[-1]

    # Estimate transformation
    reg_result = o3d.pipelines.registration.registration_icp(
        source, target, max_correspondence_distance=0.02
    )
    transformation = reg_result.transformation

    # Apply transformation to source point cloud
    source.transform(transformation)

    # Add transformed point cloud to the list
    registered_point_clouds.append(source)

# Combine transformations to align all point clouds
aligned_point_cloud = o3d.geometry.PointCloud()
for pc in registered_point_clouds:
    aligned_point_cloud += pc

# Visualize aligned point cloud
o3d.visualization.draw_geometries([aligned_point_cloud])