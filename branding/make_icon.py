# Membuat ikon orisinal "Lomax Launcher": kubus isometrik + huruf L
from PIL import Image, ImageDraw, ImageFont
import os, sys
OUT = os.path.join(os.path.dirname(__file__), "res")
S = 1024

def bg():
    im = Image.new("RGBA", (S, S))
    d = ImageDraw.Draw(im)
    for y in range(S):  # gradien teal -> biru tua
        t = y / S
        c = (int(18+(10-18)*t), int(160+(60-160)*t), int(150+(120-150)*t), 255)
        d.line([(0, y), (S, y)], fill=c)
    return im

def fg():
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy, r = S//2, S//2, 250   # dalam safe-zone 66%
    top = [(cx, cy-r), (cx+r*0.87, cy-r/2), (cx, cy), (cx-r*0.87, cy-r/2)]
    left = [(cx-r*0.87, cy-r/2), (cx, cy), (cx, cy+r), (cx-r*0.87, cy+r/2)]
    right = [(cx, cy), (cx+r*0.87, cy-r/2), (cx+r*0.87, cy+r/2), (cx, cy+r)]
    d.polygon(top, fill=(255, 214, 102))
    d.polygon(left, fill=(230, 150, 40))
    d.polygon(right, fill=(190, 110, 25))
    # huruf L di sisi kiri (koordinat bidang u,v 0..1)
    def P(u, v): return (cx - r*0.87 + u*r*0.87, cy - r/2 + u*r/2 + v*r)
    def rect(u0, v0, u1, v1): d.polygon([P(u0,v0), P(u1,v0), P(u1,v1), P(u0,v1)], fill="white")
    rect(0.28, 0.22, 0.42, 0.80)
    rect(0.28, 0.66, 0.74, 0.80)
    return im

B, F = bg(), fg()
full = Image.alpha_composite(B, F)
sizes = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
for dpi, px in sizes.items():
    d = os.path.join(OUT, f"mipmap-{dpi}"); os.makedirs(d, exist_ok=True)
    a = int(px * 108/48)  # ukuran layer adaptive
    B.resize((a, a), Image.LANCZOS).save(f"{d}/ic_launcher_background.webp")
    F.resize((a, a), Image.LANCZOS).save(f"{d}/ic_launcher_foreground.webp")
    sq = full.resize((px, px), Image.LANCZOS)
    m = Image.new("L", (px, px), 0); ImageDraw.Draw(m).rounded_rectangle([0,0,px-1,px-1], px//5, fill=255)
    sq2 = sq.copy(); sq2.putalpha(m); sq2.save(f"{d}/ic_launcher.webp")
    m2 = Image.new("L", (px, px), 0); ImageDraw.Draw(m2).ellipse([0,0,px-1,px-1], fill=255)
    rd = sq.copy(); rd.putalpha(m2); rd.save(f"{d}/ic_launcher_round.webp")
full.resize((512, 512), Image.LANCZOS).convert("RGB").save(os.path.join(os.path.dirname(__file__), "playstore_icon_512.png"))
print("ok")
