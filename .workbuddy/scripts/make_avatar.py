"""Generate a hand-drawn illustration avatar with Morandi low-saturation colors."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, math, random

OUT = r"D:\college\blog\qqpp17.github.io\static\img"
os.makedirs(OUT, exist_ok=True)

SIZE = 512
CW = SIZE // 2

# ---------- 莫兰迪低饱和调色板 ----------
MORANDI = {
    "dusty_pink":  (201, 173, 167, 255),
    "sage":        (163, 177, 138, 255),
    "muted_blue":  (142, 154, 175, 255),
    "taupe":       (184, 169, 157, 255),
    "lavender":    (184, 169, 201, 255),
    "cream":       (220, 208, 192, 255),
    "clay":        (196, 162, 148, 255),
}

# ---------- 1. 柔和流体背景（莫兰迪色） ----------
base = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
draw = ImageDraw.Draw(base)
blobs = [
    (SIZE*0.28, SIZE*0.26, 280, MORANDI["dusty_pink"]),
    (SIZE*0.78, SIZE*0.24, 250, MORANDI["lavender"]),
    (SIZE*0.80, SIZE*0.80, 270, MORANDI["sage"]),
    (SIZE*0.22, SIZE*0.82, 240, MORANDI["muted_blue"]),
    (SIZE*0.50, SIZE*0.52, 220, MORANDI["cream"]),
    (SIZE*0.52, SIZE*0.12, 200, MORANDI["clay"]),
]
for cx, cy, r, color in blobs:
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color)
fluid = base.filter(ImageFilter.GaussianBlur(radius=130))
fluid = fluid.filter(ImageFilter.GaussianBlur(radius=45))

# ---------- 2. 手绘插画层（星星 / 波浪 / 小花 / 光点） ----------
art = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
ad = ImageDraw.Draw(art)

def star(cx, cy, r, fill, rot=0.0):
    pts = []
    for i in range(10):
        a = math.pi/5 * i - math.pi/2 + rot
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad*math.cos(a), cy + rad*math.sin(a)))
    ad.polygon(pts, fill=fill)

def flower(cx, cy, r, stroke):
    # 5 片花瓣
    for k in range(5):
        a = math.pi*2/5 * k - math.pi/2
        px = cx + r*0.55*math.cos(a)
        py = cy + r*0.55*math.sin(a)
        ad.ellipse([px-r*0.42, py-r*0.42, px+r*0.42, py+r*0.42],
                   outline=stroke, width=2)
    ad.ellipse([cx-r*0.18, cy-r*0.18, cx+r*0.18, cy+r*0.18], fill=stroke)

# 柔光晕（几团淡淡白光，增加手绘温柔感）
glow = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for cx, cy, r in [(150, 140, 90), (370, 360, 110), (300, 130, 70)]:
    gd.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(255, 255, 255, 38))
glow = glow.filter(ImageFilter.GaussianBlur(radius=35))
art = Image.alpha_composite(art, glow)
ad = ImageDraw.Draw(art)

# 手绘星星（白色半透明，大小不一，不规则散落）
random.seed(11)
star_pos = [(120, 150, 16), (390, 150, 12), (340, 330, 20), (160, 360, 14),
            (250, 200, 10), (410, 280, 9), (95, 300, 11)]
for cx, cy, r in star_pos:
    star(cx, cy, r, (255, 255, 255, random.randint(120, 200)), rot=random.random()*0.6)

# 波浪线（有机手绘曲线，白色描边）
def wavy(y0, amp, color, width=2, alpha=70):
    pts = []
    for x in range(20, SIZE-20, 6):
        y = y0 + amp * math.sin((x/70.0)) + 6*math.sin(x/22.0)
        pts.append((x, y))
    ad.line(pts, fill=(*color[:3], alpha), width=width, joint="curve")

wavy(120, 10, MORANDI["cream"])
wavy(400, 12, MORANDI["cream"])
wavy(250, 8,  MORANDI["taupe"])

# 小花（右下角，白色描边）
flower(385, 400, 34, (255, 255, 255, 110))

# 散落小圆点（莫兰迪色 + 白）
dots = [(200, 110, 3, MORANDI["clay"]), (430, 200, 4, MORANDI["sage"]),
        (110, 230, 3, MORANDI["muted_blue"]), (300, 420, 3, MORANDI["lavender"]),
        (260, 300, 2, (255,255,255,140)), (180, 420, 2, (255,255,255,120))]
for cx, cy, r, c in dots:
    ad.ellipse([cx-r, cy-r, cx+r, cy+r], fill=c)

# 轻微模糊，模拟手绘柔边
art = art.filter(ImageFilter.GaussianBlur(radius=0.6))

# ---------- 3. 合成 + 圆形裁剪 ----------
final = Image.alpha_composite(fluid, art)
mask = Image.new('L', (SIZE, SIZE), 0)
ImageDraw.Draw(mask).ellipse((0, 0, SIZE, SIZE), fill=255)
# 边缘柔化
mask = mask.filter(ImageFilter.GaussianBlur(radius=2))
out = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
out.paste(final, (0, 0), mask)

# 细描边（莫兰迪陶土色，比纯白更柔和）
ring = ImageDraw.Draw(out)
ring.ellipse((5, 5, SIZE-5, SIZE-5), outline=(196, 162, 148, 150), width=3)

# 关键：保留 RGBA 透明通道，不要转成 RGB（否则透明角落会变成黑色方块）
out.save(os.path.join(OUT, "avatar.png"), "PNG", optimize=True)
print("avatar saved:", os.path.getsize(os.path.join(OUT, "avatar.png")), "bytes")

fav = out.resize((64, 64), Image.LANCZOS)
fav.save(os.path.join(OUT, "favicon.png"), "PNG", optimize=True)
print("favicon saved")
