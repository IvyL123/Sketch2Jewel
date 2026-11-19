# -*- coding: utf-8 -*-
"""一笔成珠 Sketch2Jewel 参赛报告书 PDF 生成"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                Table, TableStyle, PageBreak, HRFlowable, KeepTogether)

ROOT = r"C:\Users\Mavis\.zcode\workspace\draft-c487a057-1004-49d8-94d6-d0be05ad5252\jewelry-platform"
OUT = os.path.join(ROOT, "docs", "report", "Sketch2Jewel-项目报告书.pdf")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

pdfmetrics.registerFont(TTFont("Hei", r"C:\Windows\Fonts\simhei.ttf"))
pdfmetrics.registerFont(TTFont("YH", r"C:\Windows\Fonts\msyh.ttc", subfontIndex=0))

GOLD = colors.HexColor("#8a6c2c")
DARK = colors.HexColor("#1c1926")
GREY = colors.HexColor("#5a5566")

def P(text, size=10.5, font="YH", color=DARK, leading=16, space=6, align=0):
    return Paragraph(text, ParagraphStyle("s", fontName=font, fontSize=size,
        textColor=color, leading=leading, spaceAfter=space, alignment=align))

def H1(text):
    return Paragraph(text, ParagraphStyle("h1", fontName="Hei", fontSize=17,
        textColor=GOLD, leading=24, spaceBefore=10, spaceAfter=8))

def H2(text):
    return Paragraph(text, ParagraphStyle("h2", fontName="Hei", fontSize=13,
        textColor=DARK, leading=19, spaceBefore=8, spaceAfter=6))

def img(path, w):
    from PIL import Image as PILImage
    im = PILImage.open(path)
    r = im.size[1] / im.size[0]
    return Image(path, width=w, height=w * r)

def cover_strip(paths, w_each, caption):
    cells = [img(p, w_each) for p in paths]
    t = Table([cells], colWidths=[w_each + 6] * len(cells))
    t.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc"))]))
    cap = P(caption, 8.5, "YH", GREY, align=1, space=2)
    return [t, cap]

doc = SimpleDocTemplate(OUT, pagesize=A4,
    leftMargin=18*mm, rightMargin=18*mm, topMargin=16*mm, bottomMargin=16*mm,
    title="一笔成珠 Sketch2Jewel 项目报告书", author="IvyL123")
E = []

# ---------- 封面 ----------
E.append(Spacer(1, 8))
E.append(Paragraph("一笔成珠 Sketch2Jewel", ParagraphStyle("t", fontName="Hei",
    fontSize=26, textColor=GOLD, leading=36, alignment=1)))
E.append(Paragraph("让只会画平面草图的设计师，几分钟拿到能发工厂打样的 3D 珠宝模型",
    ParagraphStyle("st", fontName="YH", fontSize=12, textColor=DARK, leading=18, alignment=1)))
E.append(Spacer(1, 4))
E.append(Paragraph("2026 群核 Aholo 全球 3D AI 黑客松 · 参赛作品报告 · 3D 生成：Aholo Lux3D (img-to-3d)",
    ParagraphStyle("m", fontName="YH", fontSize=9, textColor=GREY, leading=14, alignment=1)))
E.append(Spacer(1, 8))
E += cover_strip([
    os.path.join(ROOT, "sketches", "enhanced", "enhanced-pendant.png"),
    os.path.join(ROOT, "reference", "note-img-1.png"),
    os.path.join(ROOT, "reference", "note-img-3.png"),
], 52*mm, "真实基准《星环以外》：手绘草图 → 建模师 CAD 渲染（@OneDayJeweler）→ 实物照片")
E.append(Spacer(1, 10))
E.append(HRFlowable(width="100%", thickness=1, color=GOLD))

# ---------- 01 创意来源 ----------
E.append(H1("01 · 创意来源：一个真实发生过的故事"))
E.append(P("作者为《三体·死神永生》设计过一件主题胸针《星环以外》：手绘草图中，剑与羽毛、"
    "雏菊与百合、镰刀与半幅桂冠以颜色语义标注（金=黄、银=灰、宝石=紫）。草图落地成实物"
    "的过程：委托建模师沟通设计意图 → 手工 CAD 建模（数天）→ 打样确认 → 浇铸交付。成品很美，"
    "但这段路花了近一周、以数百元计。"))
E.append(P("<b>世界上有大量「会画图、不会建模」的独立设计师与小众爱好者被卡在同一条路上</b>："
    "Rhino/Blender 学习曲线以月计，外包沟通以天计、改稿每轮收费。如果草图能直接变成可打样的"
    "模型呢？本项目就是对这个问题的回答，并以《星环以外》真实案例作为复现基准——"
    "<b>平台目标是在不依赖建模师的前提下，从同源草图产出可交工厂打样的模型。</b>"))

# ---------- 02 问题定义 ----------
E.append(H1("02 · 问题定义"))
t = Table([
    [P("用户", 9, "Hei", colors.white), P("痛点", 9, "Hei", colors.white), P("现有方案缺陷", 9, "Hei", colors.white)],
    [P("独立珠宝设计师"), P("会画图不会建模"), P("Rhino 等软件学习以月计，珠宝曲面工艺另学")],
    [P("小众定制爱好者"), P("一人一件不值得外包"), P("外包建模数天起、每轮收费、改稿难")],
    [P("小型工作室"), P("打样前沟通成本高"), P("缺少统一工程语言：尺寸/克重/水密性")],
], colWidths=[36*mm, 46*mm, 92*mm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), GOLD),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#bbbbbb")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
]))
E.append(t)
E.append(P("<b>关键洞察：</b>工厂打样真正需要的不是「完美模型」，而是「合格的工程输入」——"
    "毫米级尺寸、实体克重估计、水密网格（能否直接出蜡模）。这三样恰恰是可程序化检验的几何问题，"
    "也是 AI 生成与工厂制造之间缺失的「最后一公里」。", space=4))
E.append(P("<b>交互式配置（宜家式选购体验）：</b>点击模型部件即可——① 更换金属材质（18K 金/玫瑰金/"
    "925 银/铂金/镀黑铑/做旧银，基于物理渲染 PBR + 程序化棚拍环境光，含氧化包浆与拉丝表面）；"
    "② 镶嵌宝石：8 种切工（圆形明亮式 57 刻面、公主方、祖母绿阶梯切、阿舍尔、椭圆形、梨形、马眼形、枕形）"
    "× 12 种宝石（钻石/红宝石/蓝宝石/黄色蓝宝石/紫色蓝宝石/紫色尖晶石/祖母绿/尖晶石/海蓝宝/坦桑石/紫水晶/欧泊/珍珠，"
    "按折射率与密度做透射与色散渲染），点击部位即时换切工、换宝石、调主石直径，镶嵌自动生成包镶/爪镶"
    "金属连接结构；③ 点击部位显示参数：主石显示长宽厚、切割方式与估算克拉（按实际网格体积 × 密度换算），"
    "戒圈可两点卡钳测量内直径并自动匹配港码/美码。"))
E.append(P("<b>AI 设计图增强（潦草草图 → 成熟设计图）：</b>潦草手绘并非理想的图生 3D 输入。平台集成"
    "GLM-4V-Flash（视觉理解）与 CogView-4（图像生成）：GLM-4V 读取草图并转写专业设计指令，CogView-4 "
    "据此绘制成熟珠宝设计图，再交由 Lux3D 生成——「潦草草图 + 一句话」即可达到专业设计图水准。"
    "该步骤亦兼容外部工具（案例中的设计图由腾讯元宝生成，平台可直接采用其成品）。"))

# ---------- 03 方案 ----------
E.append(H1("03 · 方案总览"))
E.append(P("手绘草图（手机拍照）→ ① 预处理管线（纸张白平衡/颜色语义增强/方形居中）→ "
    "<b>② Aholo Lux3D img-to-3d 生成（核心）</b> → ③ 平台工程化：3D 工作台预览、尺寸标定、"
    "实体体积与克重、水密性初检 → ④ 一键导出打样 STL（mm）与工厂交付单。"))
t = Table([
    [P("环节", 9, "Hei", colors.white), P("实现", 9, "Hei", colors.white)],
    [P("图生 3D"), P("Aholo Lux3D img-to-3d（G1-Turbo/G1，enablePBR，GLB 输出）——本项目核心能力")],
    [P("双通道容错"), P("API 直连（自动）与官网生成+拖入（联动）并存，零 Key 也能完整演示，保证 Demo 稳定可运行")],
    [P("输入工程化"), P("Python/Pillow 预处理：四角采样白平衡、黑/白点拉伸、饱和度+25% 增强金/银/紫语义、1024 方形画布")],
    [P("3D 工作台"), P("three.js r128 本地打包：转台/拖拽/缩放、金银双色棚拍布光，完全离线可演示")],
    [P("交付单"), P("尺寸标定（目标佩戴尺寸等比缩放）、带符号四面体体积分、925 银 10.36g/cm³ 估重、量化顶点合并边界边检测（水密性初检）")],
    [P("导出"), P("二进制 STL（毫米标定，直发蜡模打印）+ 渲染图导出")],
], colWidths=[30*mm, 144*mm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), GOLD),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#bbbbbb")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
E.append(t)

# ---------- 04 与 Aholo 技术栈结合 ----------
E.append(H1("04 · Aholo Lux3D 承担的核心作用（评审维度 01）"))
E.append(P("Lux3D 承担本项目最核心的环节：<b>草图 → 3D</b>。没有图生 3D，零建模门槛无从谈起。"
    "平台在 Lux3D 输出之上做珠宝工程化加工：Lux3D 解决「形」，平台解决「厂」。"))
E.append(P("API 集成细节：平台经本地代理调用 api.aholo3d.cn 全链路——asset/v1/token 取上传凭证 → "
    "OUS 单文件直传 → img-to-3d 任务创建（imgs/version/faceCount/outputFormat=glb/enablePbr/aiPredictSize）→ "
    "task/get 轮询至 status=3 → 解析 outputs 拉取 GLB。该集成经真实调用验证（任务号 8353940 / 8354240）。"))
E.append(Spacer(1, 2))
E.append(KeepTogether([
    img(os.path.join(ROOT, "docs", "video", "ui-moneyshot-v3.png"), 148*mm),
    P("平台全景：左侧草图输入与 Lux3D 生成面板 · 中间 3D 工作台（18K 金材质 + 椭圆红宝石镶嵌，草图与模型同框） · 右侧工厂交付单（含 18K 金估重与镶嵌清单）",
        8.5, "YH", GREY, align=1, space=2),
]))

# ---------- 05 成果 ----------
E.append(KeepTogether([
    H1("05 · 成果：两件真实设计的全链路交付（含专业软件后处理）"),
]))
row = [img(os.path.join(ROOT, "docs", "video", "report-m1.jpg"), 55*mm),
       img(os.path.join(ROOT, "docs", "video", "report-m2.jpg"), 55*mm)]
t = Table([row], colWidths=[61*mm, 61*mm])
t.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")]))
E.append(t)
E.append(P("左：草图①「剑穿双环吊坠」生成结果（剑、双环、珠粒镶边、三颗宝石盘、锁骨链弧线均与草图对应）· "
    "右：草图②「剑羽花环」生成结果（镰刀弯弧、花环珠链带、宝石圆盘、竖贯之剑）",
    8.5, "YH", GREY, align=1, space=4))
t = Table([
    [P("指标", 9, "Hei", colors.white), P("剑坠（G1-Turbo）", 9, "Hei", colors.white), P("花环（G1-Turbo）", 9, "Hei", colors.white)],
    [P("生成耗时"), P("约 80 秒"), P("约 150 秒")],
    [P("网格三角形"), P("255,938"), P("255,716")],
    [P("标定尺寸 (mm)"), P("27.6 × 39.5 × 40.0"), P("27.6 × 39.5 × 40.0")],
    [P("水密性初检"), P("通过 · 开放边 0"), P("通过 · 开放边 0")],
    [P("925 银估重"), P("2.1 g"), P("2.1 g")],
    [P("可否直发蜡模"), P("是（按交付单结论）"), P("是（按交付单结论）")],
], colWidths=[40*mm, 65*mm, 69*mm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), GOLD),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#bbbbbb")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
E.append(t)
E.append(P("<b>诚实边界：</b>AI 直出模型与建模师手工精修仍有差距（细节锐度、镶嵌位精度）。"
    "平台定位是「打样级」而非「量产免修级」：从数天等待变为分钟级自提，迭代自由度发生质变"
    "（不满意立刻重生成）。交付单上的水密性初检与尺寸标定正是为此设计的工程护栏，打样后工厂复核仍是必要环节。"))
E.append(H2("与专业珠宝建模师的关系：对照、区分与愿景"))
E.append(P("<b>重要区分：</b>社交媒体（小红书）上《星环以外》的 CAD 建模图，为专业珠宝建模师"
    "（@OneDayJeweler）受托制作的<b>人工精修成果</b>，属于设计委托的交付物；本平台产出的模型为"
    "AI 生成 + 程序化工程化的<b>另一独立版本</b>，两者不可混同。报告中使用设计师作品仅作"
    "「人工基准对照」，以衡量 AI 工作流的差距与进步空间。"))
E.append(P("<b>当前差距（诚实陈述）：</b>人工建模在结构语义（羽毛就是羽毛、花就是花）、细节锐度、"
    "镶嵌位精度上仍显著优于 AI 直出；AI 对线稿的解读存在形状收敛，两份不同草图可能产出相似结构。"))
E.append(P("<b>平台的迭代能力（为什么值得尝试）：</b>① 工作流可复现——草图→设计图→3D→打样文件"
    "全程自动化，新人十分钟上手；② 迭代零沟通成本——不满意立即重生成，而人工改稿每轮都要排期；"
    "③ 模型在快速进化——图生 3D 的语义理解随基础模型升级直接受益，平台的预处理与工程化管线"
    "持续积累；④ 人机分工——AI 出形打样，设计师出精修，两者是上下游而非替代关系。"
    "对独立设计师而言，这是一个「当天看到实物雏形」的快速验证工具。"))

# ---------- 专业软件后处理 ----------
E.append(H2("专业软件后处理（三段式工作流的最后一环）"))
E.append(P("平台导出的毫米级 GLB/STL 可直接进入专业软件：内置 <b>Blender headless 自动化管线</b>"
    "（Solidify 加厚 0.75mm 铸造壁厚 → Voxel 0.28mm 重拓扑 → Laplacian 平滑 → 减面至 29k → "
    "导出 GLB+二进制 STL，每件约 1 分钟）——<b>Solidify+Voxel 组合将 AI 线稿的薄壳网格转化为"
    "实心铸造体积</b>，是消除「线框感」、达到浇铸质感的关键工序。亦兼容 Rhino 导入精修。"))
E.append(Spacer(1, 2))
E.append(KeepTogether([
    img(os.path.join(ROOT, "docs", "video", "wreath-cast-yaw180.jpg"), 92*mm),
    P("《花环剑》Blender 浇铸化处理后：实心银质铸造体积，镂空花丝纹理转化为表面肌理",
        8.5, "YH", GREY, align=1, space=2),
]))

# ---------- 06 路线图 ----------
E.append(H1("06 · 路线图"))
E.append(P("戒圈号自动匹配（内径→国际圈口号）→ 分部件材质映射（草图颜色→金银石自动分件）→ "
    "LuxReal 佩戴效果视频 → 工厂报价参数（克重×金价×工费）→ 草图直传增强管线内置化。"))

# ---------- 07 链接 ----------
t = Table([
    [P("项目源代码", 9, "Hei", colors.white), P("https://github.com/IvyL123/Sketch2Jewel")],
    [P("Demo 视频", 9, "Hei", colors.white), P("见提交附件（真实运行录屏 + 转台展示）")],
    [P("小红书传播", 9, "Hei", colors.white), P("#Aholo黑客松 帖子（提交表单内回填链接）")],
    [P("运行方式", 9, "Hei", colors.white), P("仓库 app/index.html 双击即用，完全离线；服务端模式 py serve.py")],
], colWidths=[36*mm, 138*mm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), GOLD),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#bbbbbb")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
]))
E.append(KeepTogether([H1("07 · 材料链接"), t]))
E.append(Spacer(1, 8))
E.append(Paragraph("3D 生成能力由群核 Aholo Lux3D 提供 · 基准案例《星环以外》草图与实物版权归原设计师所有，仅供评审对照",
    ParagraphStyle("f", fontName="YH", fontSize=8, textColor=GREY, leading=12, alignment=1)))

doc.build(E)
print("PDF built:", OUT, os.path.getsize(OUT), "bytes")
