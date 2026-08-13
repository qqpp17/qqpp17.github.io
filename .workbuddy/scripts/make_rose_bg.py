"""Generate ROSE-themed background with strong visible colors"""
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import os, random

OUT_DIR = r"D:\college\blog\qqpp17.github.io\static\img"

W, H = 1920, 1200

def generate_bg(base_color, blobs, out_name):
    img = Image.new('RGB', (W, H), base_color)
    draw = ImageDraw.Draw(img)
    
    for cx, cy, r, color, alpha_base in blobs:
        blob = Image.new('RGB', (W, H), base_color)
        bd = ImageDraw.Draw(blob)
        steps = 100
        for i in range(steps):
            radius = int(r * (i + 1) / steps)
            alpha = (1 - (i / steps) ** 1.2) * alpha_base
            bc = [int(base_color[j]) for j in range(3)]
            c = tuple(int(color[j] * alpha + bc[j] * (1 - alpha)) for j in range(3))
            bd.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=c)
        blob = blob.filter(ImageFilter.GaussianBlur(radius=80))
        img = Image.blend(img, blob, 0.65)
    
    # 加噪点
    noise = Image.new('RGB', (W, H), base_color)
    nd = ImageDraw.Draw(noise)
    random.seed(123)
    if base_color == (255, 245, 248):  # light
        for _ in range(12000):
            x, y = random.randint(0, W-1), random.randint(0, H-1)
            c = random.choice([(255, 220, 228), (255, 180, 195), (255, 160, 180)])
            nd.point((x, y), fill=c)
    else:
        for _ in range(12000):
            x, y = random.randint(0, W-1), random.randint(0, H-1)
            c = random.choice([(60, 20, 35), (80, 25, 50), (40, 15, 25)])
            nd.point((x, y), fill=c)
    noise = noise.filter(ImageFilter.GaussianBlur(1.5))
    img = Image.blend(img, noise, 0.12)
    
    # 增强对比
    enh = ImageEnhance.Contrast(img)
    img = enh.enhance(1.2)
    
    img.save(os.path.join(OUT_DIR, out_name), 'JPEG', quality=85, optimize=True)
    print(f"{out_name}: {os.path.getsize(os.path.join(OUT_DIR, out_name))} bytes")

# Light: 樱花粉 + 玫瑰粉+蜜桃+浅紫
light_blobs = [
    (350, 280, 600, (255, 80, 140), 0.6),     # 亮玫红
    (1550, 180, 750, (255, 120, 160), 0.55),  # 蜜桃粉
    (1300, 950, 800, (255, 180, 200), 0.45),  # 浅粉
    (200, 1000, 650, (255, 160, 180), 0.5),   # 樱花粉
    (950, 550, 500, (255, 140, 170), 0.4),    # 中粉
]
generate_bg((255, 245, 248), light_blobs, 'rose-bg.jpg')

# Dark: 深玫瑰 + 暗粉紫
random.seed(456)
dark_blobs = [
    (300, 200, 650, (244, 67, 130), 0.55),   # 玫红
    (1500, 350, 750, (173, 20, 87), 0.5),     # 深玫
    (1100, 1050, 850, (40, 15, 30), 0.45),    # 深暗
    (150, 950, 600, (244, 67, 130), 0.45),    # 玫红
    (900, 500, 450, (136, 14, 79), 0.4),      # 暗玫瑰
]
generate_bg((28, 14, 22), dark_blobs, 'rose-bg-dark.jpg')

# 生成玫瑰装饰花瓣图 (small rose watermark for light)
petal_img = Image.new('RGBA', (120, 120), (255, 255, 255, 0))
petal = ImageDraw.Draw(petal_img)
# 简单玫瑰轮廓
petal.ellipse([30, 15, 90, 65], fill=(255, 80, 140, 120))
petal.ellipse([25, 30, 70, 75], fill=(255, 120, 160, 100))
petal.ellipse([50, 35, 95, 80], fill=(255, 100, 150, 110))
petal.ellipse([40, 55, 85, 95], fill=(255, 140, 180, 90))
petal_img.save(os.path.join(OUT_DIR, 'rose-petal.png'))
print(f"rose-petal.png: {os.path.getsize(os.path.join(OUT_DIR, 'rose-petal.png'))} bytes")

print("All rose backgrounds generated!")
