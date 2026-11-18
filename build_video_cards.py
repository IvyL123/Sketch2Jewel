# -*- coding: utf-8 -*-
"""Demo 视频卡片生成：标题卡 / 三联对比卡 / 结尾卡，720x952 统一尺寸"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

ROOT = r"C:\Users\Mavis\.zcode\workspace\draft-c487a057-1004-49d8-94d6-d0be05ad5252\jewelry-platform"
V = os.path.join(ROOT, "docs", "video")
W, H = 720, 952
YH = r"C:\Windows\Fonts\msyh.ttc"
YHB = r"C:\Windows\Fonts\msyhbd.ttc"

def font(path, size):
    return ImageFont.truetype(path, size)

def bg():
    im = Image.new("RGB", (W, H), (13, 11, 19))
    d = ImageDraw.Draw(im)
    # 顶部金色柔光
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((W//2-300, -260, W//2+300, 200), fill=(52, 42, 20))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    im = Image.blend(im, Image.composite(glow, im, glow.convert("L")), 0.55)
    return im, ImageDraw.Draw(im)

GOLD = (236, 199, 120)
TEXT = (236, 232, 240)
MUTED = (154, 148, 168)

# ---------- 标题卡 ----------
im, d = bg()
d.text((W//2, H//2-90), "一笔成珠", font=font(YHB, 88), fill=GOLD, anchor="mm")
d.text((W//2, H//2+5), "Sketch2Jewel", font=font(YHB, 54), fill=TEXT, anchor="mm")
d.text((W//2, H//2+105), "手绘草图 → 3D 珠宝 → 工厂打样", font=font(YH, 30), fill=MUTED, anchor="mm")
d.text((W//2, H-120), "3D 生成 · Aholo Lux3D", font=font(YH, 24), fill=MUTED, anchor="mm")
im.save(os.path.join(V, "card-title.png"))

# ---------- 三联对比卡 ----------
im, d = bg()
d.text((W//2, 84), "同一张草图 · 三种结局", font=font(YHB, 44), fill=GOLD, anchor="mm")
cells = [
    (os.path.join(ROOT, "sketches", "enhanced", "enhanced-pendant.png"), "① 手绘草图", "设计师 5 分钟"),
    (os.path.join(ROOT, "reference", "note-img-1.png"), "② 建模师 CAD", "沟通 + 建模 · 数天"),
    (os.path.join(ROOT, "docs", "video", "report-m1.jpg"), "③ 本平台生成", "Lux3D · 约 80 秒"),
]
cw, ch, gap, y0 = 196, 262, 24, 170
x = (W - 3*cw - 2*gap) // 2
for i, (p, t1, t2) in enumerate(cells):
    src = Image.open(p).convert("RGB")
    r = max(cw/src.size[0], ch/src.size[1])
    src = src.resize((int(src.size[0]*r)+1, int(src.size[1]*r)+1))
    l, t = (src.size[0]-cw)//2, (src.size[1]-ch)//2
    cell = src.crop((l, t, l+cw, t+ch))
    cx = x + i*(cw+gap)
    im.paste(cell, (cx, y0))
    d.rectangle((cx, y0, cx+cw, y0+ch), outline=(74, 66, 88), width=2)
    d.text((cx+cw//2, y0+ch+42), t1, font=font(YHB, 26), fill=TEXT, anchor="mm")
    d.text((cx+cw//2, y0+ch+82), t2, font=font(YH, 22), fill=GOLD if i == 2 else MUTED, anchor="mm")
d.text((W//2, H-110), "从「数天等待」到「分钟自提」", font=font(YHB, 34), fill=GOLD, anchor="mm")
im.save(os.path.join(V, "card-compare.png"))

# ---------- 结尾卡 ----------
im, d = bg()
d.text((W//2, H//2-120), "一笔成珠 Sketch2Jewel", font=font(YHB, 48), fill=GOLD, anchor="mm")
d.text((W//2, H//2-40), "设计师只管画 · 建模交给平台", font=font(YH, 30), fill=TEXT, anchor="mm")
d.text((W//2, H//2+60), "开源：github.com/IvyL123/Sketch2Jewel", font=font(YH, 26), fill=MUTED, anchor="mm")
d.text((W//2, H//2+130), "#Aholo黑客松", font=font(YHB, 34), fill=GOLD, anchor="mm")
d.text((W//2, H-100), "2026 群核 Aholo 全球 3D AI 黑客松", font=font(YH, 22), fill=MUTED, anchor="mm")
im.save(os.path.join(V, "card-end.png"))
print("cards done")
