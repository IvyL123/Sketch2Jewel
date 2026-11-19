# -*- coding: utf-8 -*-
"""Blender 浇铸模式：把 AI 生成的薄壳/钢筋网格变成实心铸造珠宝。

关键工序（治"钢筋感"的完整方案）：
  1) Solidify 加厚  —— 细管/薄壳获得真实壁厚（0.9mm 铸造壁厚）
  2) Voxel 重拓扑   —— 体素均匀化，充满空隙，呈现"浇铸出来"的实心体积
  3) Laplacian 平滑 —— 铸面圆润
  4) Decimate 减面  —— 打印友好规模
用法: blender.exe --background --python blender_cast.py -- <in.glb> <out.glb> <out.stl> [壁厚mm] [体素mm]
"""
import bpy
import sys

argv = sys.argv[sys.argv.index("--") + 1:]
IN_GLB, OUT_GLB, OUT_STL = argv[0], argv[1], argv[2]
THICK = float(argv[3]) if len(argv) > 3 else 0.9       # 壁厚 mm
VOXEL = float(argv[4]) if len(argv) > 4 else 0.38      # 体素 mm
TARGET_MM = 40.0

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=IN_GLB)

meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
print("[cast] imported meshes:", len(meshes))
for o in meshes:
    o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
if len(meshes) > 1:
    bpy.ops.object.join()
obj = bpy.context.view_layer.objects.active
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# 标定 40mm
dims = obj.dimensions
max_edge = max(dims.x, dims.y, dims.z) or 1.0
s = TARGET_MM / max_edge
obj.scale = (s, s, s)
bpy.ops.object.transform_apply(scale=True)
print("[cast] calibrated 40mm; tris:", len(obj.data.polygons))

# ① Solidify 加厚：薄壳获得铸造壁厚
sol = obj.modifiers.new("Solidify", "SOLIDIFY")
sol.thickness = THICK
sol.offset = 0.0            # 双向加厚，保持轮廓居中
sol.use_even_offset = True
sol.use_rim = True
sol.use_rim_only = False
bpy.ops.object.modifier_apply(modifier="Solidify")
print("[cast] solidified +" + str(THICK) + "mm; tris:", len(obj.data.polygons))

# ② Voxel 重拓扑：浇铸实心感
rm = obj.modifiers.new("Remesh", "REMESH")
rm.mode = "VOXEL"
rm.voxel_size = VOXEL
bpy.ops.object.modifier_apply(modifier="Remesh")
print("[cast] voxel remeshed @" + str(VOXEL) + "mm; tris:", len(obj.data.polygons))

# ③ 铸面平滑
sm = obj.modifiers.new("Smooth", "SMOOTH")
sm.iterations = 3
sm.factor = 0.4
bpy.ops.object.modifier_apply(modifier="Smooth")

# ④ 减面至打印规模
dec = obj.modifiers.new("Decimate", "DECIMATE")
dec.ratio = 0.55
bpy.ops.object.modifier_apply(modifier="Decimate")
print("[cast] tris after decimate:", len(obj.data.polygons))

bpy.ops.export_scene.gltf(filepath=OUT_GLB, export_format="GLB", export_apply=True)
bpy.ops.wm.stl_export(filepath=OUT_STL)
print("[cast] exported:", OUT_GLB, OUT_STL)
print("[cast] DONE")
