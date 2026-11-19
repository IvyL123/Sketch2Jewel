# -*- coding: utf-8 -*-
"""花环剑草图预处理：白底方形 1024，轻度增强（数字原图，无需重处理）"""
from PIL import Image, ImageEnhance

SRC = r"C:\Users\Mavis\Desktop\设计草图1.jpg"
im = Image.open(SRC).convert("RGB")
W, H = im.size
print("src:", W, H)

# 轻度增强：对比 + 饱和度（黄/灰语义更清晰），无需白平衡（数字白底）
im = ImageEnhance.Contrast(im).enhance(1.08)
im = ImageEnhance.Color(im).enhance(1.2)

# 方形白底
side = max(W, H)
canvas = Image.new("RGB", (side, side), (252, 251, 248))
canvas.paste(im, ((side - W) // 2, (side - H) // 2))
canvas = canvas.resize((1024, 1024), Image.LANCZOS)
out = r"C:\Users\Mavis\.zcode\workspace\draft-c487a057-1004-49d8-94d6-d0be05ad5252\jewelry-platform\sketches\wreath-clean-1024.png"
canvas.save(out)
print("saved:", out)
