# Layout kontrol default Lomax Launcher (rancangan sendiri): D-pad kiri, tombol aksi kanan,
# baris tombol kecil di atas. Format: layout versi 8 Amethyst/PojavLauncher.
# Hasil: branding/assets/default.json + branding/preview_controls.png
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets"); os.makedirs(OUT, exist_ok=True)


def argb(a, r, g, b):
    v = (a << 24) | (r << 16) | (g << 8) | b
    return v - (1 << 32) if v >= (1 << 31) else v


DARK = argb(0x66, 0, 0, 0)          # hitam transparan
ORANGE = argb(0x99, 232, 146, 44)   # aksen Lomax
TEAL = argb(0x80, 30, 110, 110)
WHITE = -1

# kunci GLFW / kode khusus
SPACE, W, A, S, D = 32, 87, 65, 83, 68
E, Q, F, T = 69, 81, 70, 84
ESC, TAB, LSHIFT, LCTRL = 256, 258, 340, 341
F1, F2, F3, F5 = 290, 291, 292, 294
KEYBOARD, TOGGLE_GUI, LMB, RMB, MOUSE = -1, -2, -3, -4, -5


def btn(name, key, x, y, w=56, h=56, bg=DARK, radius=30, toggle=False, menu=False,
        swipe=False, stroke=1.2):
    return {
        "name": name, "keycodes": [key, 0, 0, 0],
        "dynamicX": x, "dynamicY": y, "width": w, "height": h,
        "bgColor": bg, "strokeColor": WHITE, "strokeWidth": stroke,
        "cornerRadius": radius, "opacity": 1,
        "isToggle": toggle, "isSwipeable": swipe, "passThruEnabled": False,
        "displayInGame": True, "displayInMenu": menu,
    }


M = "${margin}"
# --- D-pad kiri bawah (kolom c, baris r dari bawah) ---
def lx(c): return f"{M} * {c + 1} + ${{width}} * {c}" if c else M
def by(r): return f"${{bottom}} - {M} * {r + 1} - ${{height}} * {r}" if r else f"${{bottom}} - {M}"
# --- Klaster kanan bawah ---
def rx(c): return f"${{right}} - {M} * {c + 1} - ${{width}} * {c}" if c else f"${{right}} - {M}"

buttons = [
    # D-pad: tombol gerak bisa digeser (swipe) seperti stik
    btn("▲", W, lx(1), by(2), swipe=True),
    btn("◀", A, lx(0), by(1), swipe=True),
    btn("▶", D, lx(2), by(1), swipe=True),
    btn("▼", S, lx(1), by(0), swipe=True),
    btn("■", LSHIFT, lx(1), by(1), bg=TEAL, toggle=True),     # sneak (toggle) di tengah D-pad
    # Klaster aksi kanan
    btn("◆", SPACE, rx(0), by(0), bg=ORANGE, radius=100),  # lompat
    btn("ATK", LMB, rx(1), by(0)),
    btn("USE", RMB, rx(1), by(1)),
    btn("RUN", LCTRL, rx(0), by(1), toggle=True),
    btn("INV", E, rx(0), by(2), menu=True),
    btn("DROP", Q, rx(1), by(2)),
    # Baris atas (kecil)
    btn("II", ESC, M, M, w=44, h=34, menu=True),
    btn("CHAT", T, f"{M} * 2 + px(44) / 100.0 * ${{preferred_scale}}", M, w=52, h=34),
    btn("ABC", KEYBOARD, f"{M} * 3 + px(96) / 100.0 * ${{preferred_scale}}", M, w=48, h=34, menu=True),
    btn("MOUSE", MOUSE, f"{M} * 4 + px(144) / 100.0 * ${{preferred_scale}}", M, w=60, h=34, menu=True),
    btn("F5", F5, f"${{screen_width}} / 2 - ${{width}} - {M}", M, w=44, h=34),
    btn("TAB", TAB, f"${{screen_width}} / 2 + {M}", M, w=44, h=34),
    btn("GUI", TOGGLE_GUI, f"${{right}} - {M}", M, w=44, h=34, menu=True),
]

# Laci "⋯" berisi tombol jarang dipakai
drawer = {
    "orientation": "DOWN",
    "properties": btn("⋯", 0, f"${{right}} - {M} * 2 - px(44) / 100.0 * ${{preferred_scale}}", M, w=44, h=34, menu=True),
    "buttonProperties": [
        btn("OFF", F, "0", "0", w=44, h=34),
        btn("F3", F3, "0", "0", w=44, h=34),
        btn("F1", F1, "0", "0", w=44, h=34),
        btn("F2", F2, "0", "0", w=44, h=34),
    ],
}

layout = {"version": 8, "scaledAt": 100, "mControlDataList": buttons,
          "mDrawerDataList": [drawer], "mJoystickDataList": []}
json.dump(layout, open(os.path.join(OUT, "default.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# ---------- Preview (simulasi layar 2340x1080, density 2.75, margin 2dp) ----------
from PIL import Image, ImageDraw, ImageFont
SW, SH, DEN = 2340, 1080, 2.75
MARGIN = 2 * DEN


def ev(expr, w, h):
    s = (expr.replace("${margin}", str(MARGIN)).replace("${width}", str(w)).replace("${height}", str(h))
         .replace("${right}", str(SW - w)).replace("${bottom}", str(SH - h))
         .replace("${screen_width}", str(SW)).replace("${screen_height}", str(SH))
         .replace("${preferred_scale}", "100"))
    s = re.sub(r"px\(([\d.]+)\)", lambda m: str(float(m.group(1)) * DEN), s)
    return eval(s)


img = Image.new("RGB", (SW, SH), (110, 150, 190))
dr = ImageDraw.Draw(img, "RGBA")
dr.rectangle([0, SH * .55, SW, SH], fill=(90, 120, 60))
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
except Exception:
    font = ImageFont.load_default()


def draw(b, x=None, y=None):
    w, h = b["width"] * DEN, b["height"] * DEN
    x = ev(b["dynamicX"], w, h) if x is None else x
    y = ev(b["dynamicY"], w, h) if y is None else y
    c = b["bgColor"] & 0xFFFFFFFF
    fill = ((c >> 16) & 255, (c >> 8) & 255, c & 255, max(90, c >> 24))
    r = min(w, h) / 2 * b["cornerRadius"] / 100
    dr.rounded_rectangle([x, y, x + w, y + h], r, fill=fill, outline=(255, 255, 255, 220), width=3)
    label = b["name"]
    dr.text((x + w / 2, y + h / 2), label, fill="white", font=font, anchor="mm")
    return x, y, w, h


for b in buttons:
    draw(b)
x, y, w, h = draw(drawer["properties"])
for i, b in enumerate(drawer["buttonProperties"]):  # laci saat terbuka (ke bawah)
    draw(b, x, y + (h + MARGIN) * (i + 1))
img.resize((1170, 540)).save(os.path.join(HERE, "preview_controls.png"))
print("ok", len(buttons), "tombol")
