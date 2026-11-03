# Membuat aset UI "gaya game blok" Lomax Launcher (semua orisinal, digambar prosedural).
# Hasil: branding/res/drawable/*.png (9-patch) dan branding/res/drawable-nodpi/lomax_tile.png
import os, random
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "res", "drawable")
DN = os.path.join(HERE, "res", "drawable-nodpi")
os.makedirs(D, exist_ok=True); os.makedirs(DN, exist_ok=True)

BLACK = (12, 14, 16, 255)


def block(w, h, fill, light, dark, px=2, pressed=False):
    """Tombol blok: outline hitam, bevel terang kiri-atas, bevel gelap kanan-bawah, sedikit noise."""
    im = Image.new("RGBA", (w, h), BLACK)
    d = ImageDraw.Draw(im)
    o = px  # tebal outline
    b = px  # tebal bevel
    tl, br = (dark, light) if pressed else (light, dark)
    d.rectangle([o, o, w - o - 1, h - o - 1], fill=fill)
    d.rectangle([o, o, w - o - 1, o + b - 1], fill=tl)          # atas
    d.rectangle([o, o, o + b - 1, h - o - 1], fill=tl)          # kiri
    d.rectangle([o, h - o - b, w - o - 1, h - o - 1], fill=br)  # bawah
    d.rectangle([w - o - b, o, w - o - 1, h - o - 1], fill=br)  # kanan
    rnd = random.Random(7)
    for _ in range((w * h) // 40 if w > 30 else 0):  # noise halus (hanya preview; 9-patch polos agar stretch bersih)
        x = rnd.randrange(o + b, w - o - b); y = rnd.randrange(o + b, h - o - b)
        c = fill if rnd.random() < .5 else tuple(max(0, v - 10) for v in fill[:3]) + (255,)
        im.putpixel((x, y), c)
    return im


def ninepatch(img, cap, pad_x, pad_y, name):
    """Bungkus jadi .9.png: area stretch di tengah, padding konten pad_x/pad_y."""
    w, h = img.size
    out = Image.new("RGBA", (w + 2, h + 2), (0, 0, 0, 0))
    out.paste(img, (1, 1))
    k = (0, 0, 0, 255)
    for x in range(1 + cap, w + 1 - cap): out.putpixel((x, 0), k)
    for y in range(1 + cap, h + 1 - cap): out.putpixel((0, y), k)
    for x in range(1 + pad_x, w + 1 - pad_x): out.putpixel((x, h + 1), k)
    for y in range(1 + pad_y, h + 1 - pad_y): out.putpixel((w + 1, y), k)
    out.save(os.path.join(D, name))


# Tombol menu (batu teal gelap)
STONE = (46, 74, 80, 255); STONE_L = (92, 134, 140, 255); STONE_D = (24, 40, 44, 255)
ninepatch(block(24, 24, STONE, STONE_L, STONE_D), 6, 6, 4, "lomax_block_btn.9.png")
ninepatch(block(24, 24, (36, 60, 66, 255), STONE_L, STONE_D, pressed=True), 6, 6, 4, "lomax_block_btn_pressed.9.png")

# Tombol MAIN (oranye) menimpa 9-patch bawaan mine_button_*
OR = (232, 146, 44, 255); OR_L = (255, 206, 110, 255); OR_D = (150, 82, 18, 255)
ninepatch(block(24, 24, OR, OR_L, OR_D), 6, 6, 4, "mine_button_unfocused.9.png")
ninepatch(block(24, 24, (204, 120, 30, 255), OR_L, OR_D, pressed=True), 6, 6, 4, "mine_button_focused.9.png")

# Tekstur latar 16x16 (batu gelap kebiruan, kontras rendah agar teks tetap terbaca)
rnd = random.Random(42)
t = Image.new("RGBA", (16, 16))
base = (26, 38, 44)
for y in range(16):
    for x in range(16):
        v = rnd.choice([-6, -3, 0, 0, 0, 3, 5])
        t.putpixel((x, y), tuple(max(0, min(255, c + v)) for c in base) + (255,))
for (x, y) in [(3, 4), (4, 4), (11, 9), (12, 10), (7, 13), (1, 11), (13, 2)]:  # bintik
    t.putpixel((x, y), (40, 58, 64, 255))
for i in range(16):  # garis sambungan blok
    t.putpixel((i, 15), (18, 27, 31, 255)); t.putpixel((15, i), (18, 27, 31, 255))
t.resize((64, 64), Image.NEAREST).save(os.path.join(DN, "lomax_tile.png"))

# Preview untuk dicek mata
prev = Image.new("RGBA", (360, 200))
for y in range(0, 200, 64):
    for x in range(0, 360, 64):
        prev.paste(Image.open(os.path.join(DN, "lomax_tile.png")), (x, y))
prev.paste(block(150, 44, STONE, STONE_L, STONE_D, 3), (20, 20))
prev.paste(block(150, 44, (36, 60, 66, 255), STONE_L, STONE_D, 3, True), (190, 20))
prev.paste(block(320, 54, OR, OR_L, OR_D, 3), (20, 120))
prev.resize((720, 400), Image.NEAREST).save(os.path.join(HERE, "preview_ui.png"))
print("ok")
