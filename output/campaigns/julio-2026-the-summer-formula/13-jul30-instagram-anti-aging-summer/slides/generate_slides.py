"""
Slide generator — 13 · Anti-Aging Summer
Open/Provocation · 2 Slides
Campaign: The Summer Formula · July 2026
"""

from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR  = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/tmp/slidefonts"

BONE     = "#F5F0E8"
INK      = "#1A1A18"
LAB_SAGE = "#BBD1C6"

W, H = 1080, 1080
MARGIN = 80

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def load_font(name, size):
    p = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(p, size)
    except Exception:
        return ImageFont.load_default()

def fraunces(size):
    for name in ["Fraunces[wght].ttf", "Fraunces-Regular.ttf"]:
        p = os.path.join(FONT_DIR, name)
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def dmsans(size, bold=False):
    return load_font("DMSans-Bold.ttf" if bold else "DMSans-Regular.ttf", size)

def new_canvas(bg):
    img = Image.new("RGB", (W, H), hex_to_rgb(bg))
    return img, ImageDraw.Draw(img)

def th(draw, text, font):
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[3] - bb[1]

def tw(draw, text, font):
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0]

def cx(draw, text, font):
    return (W - tw(draw, text, font)) // 2

def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        t = (cur + " " + word).strip()
        if tw(draw, t, font) <= max_w:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = word
    if cur: lines.append(cur)
    return lines

def draw_wrap(draw, text, font, x, y, max_w, color, sp=1.5):
    lines = wrap(draw, text, font, max_w)
    lh = th(draw, "Ag", font)
    r, g, b = hex_to_rgb(color)
    for line in lines:
        draw.text((x, y), line, font=font, fill=(r, g, b))
        y += int(lh * sp)
    return y

def slide_01():
    img, draw = new_canvas(BONE)
    f_dm = dmsans(44)
    f_fr = fraunces(72)
    f_sm = dmsans(18)

    lines_dm = ["The best anti-aging", "move this summer"]
    spotlight = "costs nothing."

    total_h = (sum(th(draw, l, f_dm) + 12 for l in lines_dm) +
               th(draw, spotlight, f_fr))
    y = (H - total_h) // 2 - 10

    r, g, b = hex_to_rgb(INK)
    for line in lines_dm:
        draw.text((cx(draw, line, f_dm), y), line, font=f_dm, fill=(r, g, b))
        y += th(draw, line, f_dm) + 12
    draw.text((cx(draw, spotlight, f_fr), y), spotlight, font=f_fr, fill=(r, g, b))

    handle = "@skinlabeditorial"
    draw.text((W - MARGIN - tw(draw, handle, f_sm), H - 50),
              handle, font=f_sm, fill=(r, g, b, 128))

    img.save(os.path.join(OUT_DIR, "slide-01.png"))
    print("slide-01.png saved")

def slide_02():
    img, draw = new_canvas(INK)
    f_head = dmsans(38, bold=True)
    f_body = dmsans(23)
    f_bold = dmsans(23, bold=True)
    f_foot = dmsans(18)

    y = 90
    r, g, b = hex_to_rgb(BONE)
    draw.text((MARGIN, y), "Here is the mechanism.", font=f_head, fill=(r, g, b))
    y += th(draw, "X", f_head) + 20
    rr, rg, rb = hex_to_rgb(LAB_SAGE)
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(rr, rg, rb, 180), width=1)
    y += 28

    paras = [
        "Every anti-aging intervention — retinol, vitamin C, peptides, professional treatments — works on damage that has already occurred. Cellular repair. Collagen stimulation. Pigmentation correction. These are downstream effects.",
        "There is one intervention that works upstream of the damage itself: not acquiring it.",
        "UV radiation is responsible for approximately 80–90% of visible skin aging. The mechanism: UV induces matrix metalloproteinases that degrade collagen, forms reactive oxygen species that damage DNA and lipids, and directly damages melanocytes.",
        "SPF applied at 2mg/cm², every morning, every day — the most evidence-based anti-aging intervention available. At any price point.",
    ]
    for para in paras:
        y = draw_wrap(draw, para, f_body, MARGIN, y, W - MARGIN*2, BONE, sp=1.5)
        y += 18

    y += 8
    final = "Everything else is catching up."
    y = draw_wrap(draw, final, f_bold, MARGIN, y, W - MARGIN*2, BONE, sp=1.4)

    footer = "Ingredients, decoded.  ·  @skinlabeditorial"
    draw.text((MARGIN, H - 50), footer, font=f_foot, fill=(r, g, b, 102))

    img.save(os.path.join(OUT_DIR, "slide-02.png"))
    print("slide-02.png saved")

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    slide_01(); slide_02()
    print("Done — 2 slides generated.")
