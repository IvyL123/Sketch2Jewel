# -*- coding: utf-8 -*-
"""设计图预处理：仅裁切+方形化（标注保留；干净版可由元宝生成后替换）"""
from PIL import Image

SRC = r"C:\Users\Mavis\.zcode\workspace\draft-c487a057-1004-49d8-94d6-d0be05ad5252\jewelry-platform\sketches\concept-sixwing-front.png"
im = Image.open(SRC).convert("RGB")
W, H = im.size
im = im.crop((0, 0, W, int(H * 0.78)))
w, h = im.size
side = max(w, h)
canvas = Image.new("RGB", (side, side), (248, 246, 242))
canvas.paste(im, ((side - w) // 2, (side - h) // 2))
canvas = canvas.resize((1024, 1024), Image.LANCZOS)
out = SRC.replace("concept-sixwing-front.png", "concept-sixwing-1024.png")
canvas.save(out)
print("saved:", out, canvas.size)
