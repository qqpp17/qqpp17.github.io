"""Generate avatar PNG: 渐变背景 + 字母 P (拉丁字母，多彩炫酷)"""
from PIL import Image, ImageDraw, ImageFont
import os, glob

OUT = r"D:\college\blog\qqpp17.github.io\static\img"
os.makedirs(OUT, exist_ok=True)

def make_gradient(size, colors):
    """线性渐变（对角线）"""
    img = Image.new('RGB', (size, size))
    pixels = img.load()
    for y in range(size):
        t_y = y / (size - 1)
        for x in range(size):
            t_x = x / (size - 1)
            t = (t_x + t_y) / 2
            seg = t * (len(colors) - 1)
            idx = int(seg)
            frac = seg - idx
            if idx >= len(colors) - 1:
                r, g, b = colors[-1]
            else:
                r1, g1, b1 = colors[idx]
                r2, g2, b2 = colors[idx+1]
                r = int(r1 + (r2-r1)*frac)
                g = int(g1 + (g2-g1)*frac)
                b = int(b1 + (b2-b1)*frac)
            pixels[x, y] = (r, g, b)
    return img

size = 400
# 紫粉橙日落渐变（和 autumn 主题搭配）
gradient_colors = [
    (255, 154, 158),  # 粉橙 #ff9a9e
    (254, 140, 158),  # 橙红 #fe8c9e
    (189, 140, 224),  # 紫罗兰 #bd8ce0
    (91, 80, 145),    # 深紫 #5b5091
]

avatar = make_gradient(size, gradient_colors)

# 蒙版：圆形
mask = Image.new('L', (size, size), 0)
ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)

final = Image.new('RGBA', (size, size), (0, 0, 0, 0))
final.paste(avatar.convert('RGBA'), (0, 0), mask)

# 写字母 "P" 拉丁字母
draw = ImageDraw.Draw(final)

# 用系统支持的字体（拉丁字母用 arial）
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

font = ImageFont.truetype(font_path, 260) if font_path else ImageFont.load_default()

text = "P"
bbox = draw.textbbox((0, 0), text, font=font)
text_w = bbox[2] - bbox[0]
text_h = bbox[3] - bbox[1]
x = (size - text_w) // 2 - bbox[0]
y = (size - text_h) // 2 - bbox[1] - 10

# 文字阴影
shadow_offset = 6
draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=(0, 0, 0, 100))
# 白色文字
draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))

# 输出
avatar_path = os.path.join(OUT, "avatar.png")
final.convert('RGB').save(avatar_path, "PNG", optimize=True)
print(f"avatar saved: {avatar_path}, size={os.path.getsize(avatar_path)} bytes")

# 生成 favicon 64x64
favicon = final.resize((64, 64), Image.LANCZOS)
favicon_path = os.path.join(OUT, "favicon.png")
favicon.convert('RGB').save(favicon_path, "PNG", optimize=True)
print(f"favicon saved: {favicon_path}")
