"""草图增强预处理：把手机拍的手绘图变成 Lux3D img-to-3d 的优质输入。

处理链：纸张白平衡(角落采样) -> 黑点/白点拉伸 -> 轻度饱和度提升(颜色语义) ->
中值滤波去纸纹 -> 边距裁切 -> 方形画布居中 -> 输出 1024x1024 PNG
"""
import os
from PIL import Image, ImageEnhance, ImageFilter

SRC = r"C:\Users\Mavis\.zcode\workspace\draft-c487a057-1004-49d8-94d6-d0be05ad5252\jewelry-platform\sketches"
OUT = os.path.join(SRC, "enhanced")
os.makedirs(OUT, exist_ok=True)

FILES = {
    "sketch-right-sword-pendant.png": "enhanced-pendant.png",   # 剑穿双环吊坠（简单款，先生成）
    "sketch-left-sword-wreath.png": "enhanced-wreath.png",      # 剑羽花环（复杂款）
}

def corner_paper_color(im):
    """取四角 24x24 中位数作为纸张底色。"""
    w, h = im.size
    px = im.load()
    rs, gs, bs = [], [], []
    for (cx, cy) in [(8, 8), (w - 32, 8), (8, h - 32), (w - 32, h - 32)]:
        for dx in range(24):
            for dy in range(24):
                r, g, b = px[cx + dx, cy + dy][:3]
                rs.append(r); gs.append(g); bs.append(b)
    rs.sort(); gs.sort(); bs.sort()
    return rs[len(rs)//2], gs[len(gs)//2], bs[len(bs)//2]

def process(name, out_name):
    im = Image.open(os.path.join(SRC, name)).convert("RGB")
    # 1) 纸张白平衡：按底色把纸张拉到接近纯白
    pr, pg, pb = corner_paper_color(im)
    scale = [min(255 / max(pr, 1), 2.2), min(255 / max(pg, 1), 2.2), min(255 / max(pb, 1), 2.2)]
    lut_r = [min(255, int(i * scale[0])) for i in range(256)]
    lut_g = [min(255, int(i * scale[1])) for i in range(256)]
    lut_b = [min(255, int(i * scale[2])) for i in range(256)]
    im = im.point(lut_r + lut_g + lut_b)
    # 2) 对比拉伸：黑点 40 / 白点 248
    im = Image.eval(im, lambda x: max(0, min(255, int((x - 40) * 255 / (248 - 40)))))
    # 3) 去纸纹（轻中值）+ 锐化
    im = im.filter(ImageFilter.MedianFilter(3))
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=3))
    # 4) 饱和度 +25%：金/银/紫语义更清楚
    im = ImageEnhance.Color(im).enhance(1.25)
    # 5) 内容 bbox 裁切（阈值 235 找非白像素），加 8% 边距
    gray = im.convert("L").point(lambda x: 0 if x > 235 else 255)
    bbox = gray.getbbox()
    if bbox:
        l, t, r, b = bbox
        pw, ph = im.size
        margin_x = int((r - l) * 0.08); margin_y = int((b - t) * 0.08)
        l = max(0, l - margin_x); t = max(0, t - margin_y)
        r = min(pw, r + margin_x); b = min(ph, b + margin_y)
        im = im.crop((l, t, r, b))
    # 6) 方形白底画布，最长边 1024
    w, h = im.size
    side = max(w, h)
    canvas = Image.new("RGB", (side, side), (250, 249, 246))
    canvas.paste(im, ((side - w) // 2, (side - h) // 2))
    canvas = canvas.resize((1024, 1024), Image.LANCZOS)
    out = os.path.join(OUT, out_name)
    canvas.save(out, "PNG")
    print(name, "->", out, canvas.size)

for src, dst in FILES.items():
    process(src, dst)
print("DONE")
