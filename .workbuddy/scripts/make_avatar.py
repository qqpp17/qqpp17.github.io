"""Generate a colorful, designed avatar (fluid gradient + geometric lines + glass-letter P)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, math

OUT = r"D:\college\blog\qqpp17.github.io\static\img"
os.makedirs(OUT, exist_ok=True)

SIZE = 512

# ---------- 1. 流体多彩背景 ----------
base = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
draw = ImageDraw.Draw(base)

# 多个彩色光斑，位置分散，后面高斯模糊成流体
blobs = [
    # (cx, cy, radius, color)
    (SIZE*0.25, SIZE*0.25, 260, (255, 154, 158, 255)),   # 粉红
    (SIZE*0.78, SIZE*0.22, 240, (255, 179, 71, 255)),    # 珊瑚橙
    (SIZE*0.82, SIZE*0.80, 250, (189, 140, 224, 255)),   # 紫罗兰
    (SIZE*0.22, SIZE*0.82, 230, (132, 216, 255, 255)),   # 天蓝
    (SIZE*0.52, SIZE*0.50, 200, (160, 233, 200, 255)),   # 薄荷绿
    (SIZE*0.50, SIZE*0.10, 180, (255, 226, 159, 255)),   # 暖黄
]
for cx, cy, r, color in blobs:
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color)

# 大幅模糊 -> 流体渐变
fluid = base.filter(ImageFilter.GaussianBlur(radius=120))
# 再叠一层轻微模糊增加层次
fluid = fluid.filter(ImageFilter.GaussianBlur(radius=40))

# ---------- 2. 细线条几何装饰（白色半透明，呼应线条风） ----------
lines = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
ld = ImageDraw.Draw(lines)

# 同心圆
for i in range(1, 7):
    r = i * 34
    ld.ellipse([SIZE//2 - r, SIZE//2 - r, SIZE//2 + r, SIZE//2 + r],
               outline=(255, 255, 255, int(28 - i*2)), width=1)

# 弧形流线（三段不同半径的弧）
for k in range(3):
    rr = 150 + k * 60
    sweep = 200 - k*20
    start = 30 + k*40
    ld.arc([SIZE//2-rr, SIZE//2-rr, SIZE//2+rr, SIZE//2+rr],
           start=start, end=start+sweep,
           fill=(255, 255, 255, 30), width=1)

# 散落小圆点
import random
random.seed(7)
for _ in range(40):
    x = random.randint(20, SIZE-20)
    y = random.randint(20, SIZE-20)
    # 避免中心区域
    if (x-SIZE//2)**2 + (y-SIZE//2)**2 < 120**2:
        continue
    rr = random.randint(1, 3)
    ld.ellipse([x-rr, y-rr, x+rr, y+rr], fill=(255, 255, 255, random.randint(40, 120)))

# ---------- 3. 玫瑰色点睛曲线 ----------
rose = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
rd = ImageDraw.Draw(rose)
rd.arc([SIZE//2-180, SIZE//2-220, SIZE//2+180, SIZE//2+260],
       start=210, end=330, fill=(255, 64, 129, 90), width=3)

# ---------- 4. 字母 P（玻璃空心描边质感） ----------
letter = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
ltd = ImageDraw.Draw(letter)

font_path = None
for p in [
    r"C:\Windows\Fonts\arialbd.ttf",
    r"C:\Windows\Fonts\arial.ttf",
    r"C:\Windows\Fonts\calibrib.ttf",
    r"C:\Windows\Fonts\segoeui.ttf",
]:
    if os.path.exists(p):
        font_path = p
        break
font = ImageFont.truetype(font_path, 300) if font_path else ImageFont.load_default()

text = "P"
bbox = ltd.textbbox((0, 0), text, font=font)
tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
x = (SIZE - tw)//2 - bbox[0]
y = (SIZE - th)//2 - bbox[1] - 14

# 外发光阴影（深色，弱）
ltd.text((x, y), text, font=font, fill=(0, 0, 0, 60))
# 玻璃描边空心字：白色描边 + 半透明填充
ltd.text((x, y), text, font=font, fill=(255, 255, 255, 55),
         stroke_width=10, stroke_fill=(255, 255, 255, 235))
# 内部再描一圈浅色增加立体
ltd.text((x, y), text, font=font, fill=(255, 255, 255, 0),
         stroke_width=3, stroke_fill=(255, 255, 255, 180))

# ---------- 合成 ----------
final = Image.alpha_composite(fluid, lines)
final = Image.alpha_composite(final, rose)
final = Image.alpha_composite(final, letter)

# 圆形裁剪
mask = Image.new('L', (SIZE, SIZE), 0)
ImageDraw.Draw(mask).ellipse((0, 0, SIZE, SIZE), fill=255)
out = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
out.paste(final, (0, 0), mask)

# 轻微内描边（白圈）增加精致感
ring = ImageDraw.Draw(out)
ring.ellipse((6, 6, SIZE-6, SIZE-6), outline=(255, 255, 255, 120), width=3)

out.convert('RGB').save(os.path.join(OUT, "avatar.png"), "PNG", optimize=True)
print("avatar saved:", os.path.getsize(os.path.join(OUT, "avatar.png")), "bytes")

# favicon 64
fav = out.resize((64, 64), Image.LANCZOS)
fav.convert('RGB').save(os.path.join(OUT, "favicon.png"), "PNG", optimize=True)
print("favicon saved")
