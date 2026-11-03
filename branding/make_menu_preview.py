# Perkiraan tampilan menu utama Lomax (bukan screenshot asli; hanya untuk gambaran)
import os
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__))
W, Hh = 1170, 540
im = Image.new("RGB", (W, Hh))
tile = Image.open(f"{H}/res/drawable-nodpi/lomax_tile.png").resize((96, 96), Image.NEAREST)
for y in range(0, Hh, 96):
    for x in range(0, W, 96): im.paste(tile, (x, y))
d = ImageDraw.Draw(im)
px = ImageFont.truetype(f"{H}/res/font/lomax_pixel.ttf", 30)
pxb = ImageFont.truetype(f"{H}/res/font/lomax_pixel.ttf", 44)

def block(x0, y0, x1, y1, fill, light, dark, o=3):
    d.rectangle([x0, y0, x1, y1], fill=(12, 14, 16))
    d.rectangle([x0+o, y0+o, x1-o, y1-o], fill=fill)
    d.rectangle([x0+o, y0+o, x1-o, y0+2*o], fill=light); d.rectangle([x0+o, y0+o, x0+2*o, y1-o], fill=light)
    d.rectangle([x0+o, y1-2*o, x1-o, y1-o], fill=dark); d.rectangle([x1-2*o, y0+o, x1-o, y1-o], fill=dark)

ST = ((46, 74, 80), (92, 134, 140), (24, 40, 44))
# bar akun (atas)
d.rectangle([0, 0, W, 54], fill=(18, 48, 47)); d.rectangle([0, 50, W, 54], fill=(232, 146, 44))
d.ellipse([14, 9, 46, 41], fill=(232, 146, 44)); d.text((60, 27), "Akun Microsoft", font=px, fill="white", anchor="lm")
d.text((W-30, 27), "⚙", font=pxb, fill="white", anchor="mm")
# judul
d.text((W/2+3, 85+3), "LOMAX LAUNCHER", font=pxb, fill=(12, 14, 16), anchor="mm")
d.text((W/2, 85), "LOMAX LAUNCHER", font=pxb, fill=(232, 146, 44), anchor="mm")
labels = ["Wiki", "Discord", "Custom controls", "Execute a .jar", "Share log file", "Open game directory"]
for i, t in enumerate(labels):
    c, r = i % 2, i // 2
    x0 = 30 + c * 560; y0 = 112 + r * 70
    block(x0, y0, x0 + 550, y0 + 62, *ST)
    d.rectangle([x0+22, y0+19, x0+46, y0+43], outline="white", width=3)
    d.text((x0+66+2, y0+31+2), t, font=px, fill=(12, 14, 16), anchor="lm")
    d.text((x0+66, y0+31), t, font=px, fill="white", anchor="lm")
# panel bawah
d.rectangle([0, 330, W, Hh], fill=(42, 30, 20)); d.rectangle([0, 326, W, 330], fill=(12, 14, 16))
block(30, 342, 1060, 402, *ST); d.text((60, 372), "1.21.4  •  Fabric", font=px, fill="white", anchor="lm"); d.text((1030, 372), "▼", font=px, fill="white", anchor="mm")
block(1074, 342, 1140, 402, *ST); d.text((1107, 372), "✎", font=pxb, fill="white", anchor="mm")
block(30, 418, 1140, 510, (232, 146, 44), (255, 206, 110), (150, 82, 18))
d.text((W/2, 464), "MAIN", font=pxb, fill=(26, 18, 8), anchor="mm")
im.save(f"{H}/preview_menu.png"); print("ok")
