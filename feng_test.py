import trimesh

mesh_path = "/home/hanxiao/Desktop/Research/proj-qqtt/proj-QQTT/data/feng_version/feng_sloth_0907_0001_long/shape/matching/final_mesh.glb"

mesh = trimesh.load(mesh_path)
mesh.export("sloth.obj")

# Test function to load the mesh
