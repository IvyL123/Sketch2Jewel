# -*- coding: utf-8 -*-
"""对比卡 v2：六翼天使 三段式故事（潦草草图 → AI设计图 → 平台3D）"""
from PIL import Image, ImageDraw, ImageFont
import os

ROOT = r"C:\Users\Mavis\.zcode\workspace\draft-c487a057-1004-49d8-94d6-d0be05ad5252\jewelry-platform"
V = os.path.join(ROOT, "docs", "video")
W, H = 720, 952
YH = r"C:\Windows\Fonts\msyh.ttc"
YHB = r"C:\Windows\Fonts\msyhbd.ttc"

def font(path, size):
    return ImageFont.truetype(path, size)

im = Image.new("RGB", (W, H), (13, 11, 19))
d = ImageDraw.Draw(im)
# 顶部金色柔光
glow = Image.new("RGB", (W, H), (0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse((W//2-300, -260, W//2+300, 200), fill=(52, 42, 20))
glow = glow.filter(ImageFilter.GaussianBlur(120)) if False else glow
from PIL import ImageFilter
glow = glow.filter(ImageFilter.GaussianBlur(120))
im = Image.blend(im, Image.composite(glow, im, glow.convert("L")), 0.55)
d = ImageDraw.Draw(im)

GOLD = (236, 199, 120)
TEXT = (236, 232, 240)
MUTED = (154, 148, 168)

d.text((W//2, 78), "潦草草图 → 成熟设计图 → 3D", font=font(YHB, 40), fill=GOLD, anchor="mm")

cells = [
    (os.path.join(ROOT, "sketches", "concept-sixwing-front.png").replace("concept-sixwing-front", "_concept_src_rough"), "① 潦草草图", "用户手绘 · 30 秒", None),
    (os.path.join(ROOT, "sketches", "concept-sixwing-1024.png"), "② AI 设计图", "元宝/AI 增强 · 1 分钟", None),
    (os.path.join(V, "frames-final-m6", "f012.jpg"), "③ 平台 3D", "Lux3D + 平台 · 2 分钟", None),
]
# ① 用六翼潦草草图（用户消息里的原图）—— 若无则用设计图占位
rough_path = None
for cand in [r"C:\Users\Mavis\Documents\xwechat_files\wxid_jh1bddum36ft22_98ef\temp\RWTemp\2026-11\0fd78045af709afcf52f7a52117bb059.png",
             os.path.join(ROOT, "sketches", "concept-sixwing-rough.png")]:
    if os.path.exists(cand):
        rough_path = cand
        break
if rough_path:
    cells[0] = (rough_path, "① 潦草草图", "用户手绘 · 30 秒", None)

cw, ch, gap, y0 = 200, 268, 22, 165
x = (W - 3*cw - 2*gap) // 2
for i, (p, t1, t2, _) in enumerate(cells):
    src = Image.open(p).convert("RGB")
    r = max(cw/src.size[0], ch/src.size[1])
    src = src.resize((int(src.size[0]*r)+1, int(src.size[1]*r)+1))
    l, t = (src.size[0]-cw)//2, (src.size[1]-ch)//2
    cell = src.crop((l, t, l+cw, t+ch))
    cx = x + i*(cw+gap)
    im.paste(cell, (cx, y0))
    d.rectangle((cx, y0, cx+cw, y0+ch), outline=(74, 66, 88), width=2)
    d.text((cx+cw//2, y0+ch+40), t1, font=font(YHB, 25), fill=TEXT, anchor="mm")
    d.text((cx+cw//2, y0+ch+78), t2, font=font(YH, 21), fill=GOLD if i == 2 else MUTED, anchor="mm")
    if i < 2:
        d.text((cx+cw+gap//2, y0+ch//2), "→", font=font(YHB, 30), fill=GOLD, anchor="mm")

d.text((W//2, H-150), "交互配置：换金属 · 镶宝石 · 看参数", font=font(YHB, 30), fill=TEXT, anchor="mm")
d.text((W//2, H-90), "潦草草图也能出可打样的珠宝", font=font(YH, 26), fill=GOLD, anchor="mm")
im.save(os.path.join(V, "card-compare-v2.png"))
print("saved card-compare-v2.png")
