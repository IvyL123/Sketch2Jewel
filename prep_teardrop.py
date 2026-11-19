# -*- coding: utf-8 -*-
"""水滴剑效果图预处理：方形白底 1024，抹除右下角元宝水印"""
from PIL import Image, ImageDraw

SRC = r"C:\Users\Mavis\Documents\xwechat_files\wxid_jh1bddum36ft22_98ef\temp\RWTemp\2026-11\ed0c01d9c8c1ea2caa8599fd256a402b.png"
im = Image.open(SRC).convert("RGB")
W, H = im.size
print("src:", W, H)
# 方形白底
side = max(W, H)
canvas = Image.new("RGB", (side, side), (255, 255, 255))
canvas.paste(im, ((side - W) // 2, (side - H) // 2))
canvas = canvas.resize((1024, 1024), Image.LANCZOS)
# 抹右下角水印（贴边白块）
d = ImageDraw.Draw(canvas)
d.rectangle((int(1024 * 0.78), int(1024 * 0.925), 1024, 1024), fill=(255, 255, 255))
out = r"C:\Users\Mavis\.zcode\workspace\draft-c487a057-1004-49d8-94d6-d0be05ad5252\jewelry-platform\sketches\teardrop-concept-1024.png"
canvas.save(out)
print("saved:", out)
