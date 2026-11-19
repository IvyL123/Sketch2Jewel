# -*- coding: utf-8 -*-
"""铸造打样版说明卡"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

V = r"C:\Users\Mavis\.zcode\workspace\draft-c487a057-1004-49d8-94d6-d0be05ad5252\jewelry-platform\docs\video"
W, H = 720, 952
YH = r"C:\Windows\Fonts\msyh.ttc"
YHB = r"C:\Windows\Fonts\msyhbd.ttc"

im = Image.new("RGB", (W, H), (13, 11, 19))
glow = Image.new("RGB", (W, H), (0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse((W//2-300, -260, W//2+300, 200), fill=(52, 42, 20))
glow = glow.filter(ImageFilter.GaussianBlur(120))
im = Image.blend(im, Image.composite(glow, im, glow.convert("L")), 0.55)
d = ImageDraw.Draw(im)

def font(p, s): return ImageFont.truetype(p, s)
GOLD = (236, 199, 120); TEXT = (236, 232, 240); MUTED = (154, 148, 168)

d.text((W//2, 150), "铸造打样版", font=font(YHB, 56), fill=GOLD, anchor="mm")
d.text((W//2, 240), "Blender 专业后处理", font=font(YH, 28), fill=TEXT, anchor="mm")
lines = [
    "① Solidify 加厚 —— 细壳获得 0.75mm 铸造壁厚",
    "② Voxel 重拓扑 —— 实心浇铸体积，告别钢筋感",
    "③ Laplacian 平滑 —— 铸面圆润自然",
    "④ 减面至打印规模 + 40mm 标定",
    "⑤ 导出打样 STL，直发 3D 打印蜡模",
]
y = 340
for ln in lines:
    d.text((W//2, y), ln, font=font(YH, 24), fill=TEXT, anchor="mm")
    y += 56
d.text((W//2, H-170), "设计预览版 ↔ 铸造打样版", font=font(YHB, 34), fill=GOLD, anchor="mm")
d.text((W//2, H-100), "AI 负责形 · 专业软件负责厂", font=font(YH, 24), fill=MUTED, anchor="mm")
im.save(os.path.join(V, "card-cast.png"))
print("saved card-cast.png")
