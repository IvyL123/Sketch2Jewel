# Blender headless 网格精修：Lux3D 生成模型 → 专业软件后处理
# 用法: blender.exe --background --python blender_clean.py -- <in.glb> <out.glb> <out.stl> [voxel_size|0]
import bpy
import sys

argv = sys.argv[sys.argv.index("--") + 1:]
IN_GLB, OUT_GLB, OUT_STL = argv[0], argv[1], argv[2]
VOXEL = float(argv[3]) if len(argv) > 3 else 0.0
TARGET_MM = 40.0

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=IN_GLB)

meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
print("[s2j] imported meshes:", len(meshes))
for o in meshes:
    o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
if len(meshes) > 1:
    bpy.ops.object.join()
    print("[s2j] joined")
obj = bpy.context.view_layer.objects.active

bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# 标定：最长边 → TARGET_MM
dims = obj.dimensions
max_edge = max(dims.x, dims.y, dims.z) or 1.0
s = TARGET_MM / max_edge
obj.scale = (s, s, s)
bpy.ops.object.transform_apply(scale=True)
print("[s2j] calibrated to", TARGET_MM, "mm; tris before:", len(obj.data.polygons))

# 平滑：轻量 Laplacian（保细节，只去毛刺）
sm = obj.modifiers.new("Smooth", "SMOOTH")
sm.iterations = 2
sm.factor = 0.3
bpy.ops.object.modifier_apply(modifier="Smooth")

# 可选体素重拓扑（均匀网格，治"钢筋感"，耗时较长）
if VOXEL > 0:
    rm = obj.modifiers.new("Remesh", "REMESH")
    rm.mode = "VOXEL"
    rm.voxel_size = VOXEL
    bpy.ops.object.modifier_apply(modifier="Remesh")
    print("[s2j] voxel remeshed @", VOXEL, "mm; tris:", len(obj.data.polygons))

# 减面：控制到打印友好规模
dec = obj.modifiers.new("Decimate", "DECIMATE")
dec.ratio = 0.75
bpy.ops.object.modifier_apply(modifier="Decimate")
print("[s2j] tris after decimate:", len(obj.data.polygons))

bpy.ops.export_scene.gltf(filepath=OUT_GLB, export_format="GLB", export_apply=True)
bpy.ops.wm.stl_export(filepath=OUT_STL)
print("[s2j] exported:", OUT_GLB, OUT_STL)
print("[s2j] DONE")
