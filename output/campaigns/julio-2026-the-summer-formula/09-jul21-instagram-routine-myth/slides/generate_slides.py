"""
Slide generator — 09 · Routine Myth
Open/Provocation · 3 Slides
Campaign: The Summer Formula · July 2026
"""

from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR  = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/tmp/slidefonts"

BONE     = "#F5F0E8"
INK      = "#1A1A18"
LAB_SAGE = "#BBD1C6"
LAB_MIST = "#DAE9DF"

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
    img, draw = new_canvas(INK)
    f_dm = dmsans(42)
    f_fr = fraunces(68)
    f_sm = dmsans(18)

    dm_lines = ["You don't need", "a summer routine.", "You need to understand"]
    spotlight = "your barrier."

    total_h = (sum(th(draw, l, f_dm) + 12 for l in dm_lines) +
               th(draw, spotlight, f_fr))
    y = (H - total_h) // 2 - 10

    r, g, b = hex_to_rgb(BONE)
    for line in dm_lines:
        draw.text((cx(draw, line, f_dm), y), line, font=f_dm, fill=(r, g, b))
        y += th(draw, line, f_dm) + 12
    draw.text((cx(draw, spotlight, f_fr), y), spotlight, font=f_fr, fill=(r, g, b))

    handle = "@skinlabeditorial"
    draw.text((W - MARGIN - tw(draw, handle, f_sm), H - 50),
              handle, font=f_sm, fill=(r, g, b, 128))

    img.save(os.path.join(OUT_DIR, "slide-01.png"))
    print("slide-01.png saved")

def slide_02():
    img, draw = new_canvas(BONE)
    f_head = dmsans(38, bold=True)
    f_lg   = dmsans(26)
    f_body = dmsans(23)

    y = 90
    r, g, b = hex_to_rgb(INK)
    draw.text((MARGIN, y), "What summer actually changes.", font=f_head, fill=(r, g, b))
    y += th(draw, "X", f_head) + 20
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(r, g, b, 102), width=1)
    y += 28

    short_lines = ["Not your skin type.",
                   "Not your skin's fundamental needs.",
                   "What changes: the set of external stressors acting on your barrier."]
    for line in short_lines:
        draw.text((MARGIN, y), line, font=f_lg, fill=(r, g, b))
        y += th(draw, line, f_lg) + 10
    y += 22

    paras = [
        "UV radiation degrades ceramides. Heat increases transepidermal water loss. Sweat disrupts the acid mantle. Increased cleansing removes lipids.",
        "These are not signals to overhaul your routine. They are signals to understand what your barrier needs to stay intact.",
        "A lighter texture does not mean a lighter barrier. An SPF you actually apply does more than a high-factor one that sits in your bag.",
    ]
    for para in paras:
        y = draw_wrap(draw, para, f_body, MARGIN, y, W - MARGIN*2, INK, sp=1.5)
        y += 16

    img.save(os.path.join(OUT_DIR, "slide-02.png"))
    print("slide-02.png saved")

def slide_03():
    img, draw = new_canvas(LAB_MIST)
    f_head = dmsans(38, bold=True)
    f_bold = dmsans(24, bold=True)
    f_reg  = dmsans(22)
    f_foot = dmsans(18)

    y = 90
    r, g, b = hex_to_rgb(INK)
    draw.text((MARGIN, y), "What your barrier actually needs.", font=f_head, fill=(r, g, b))
    y += th(draw, "X", f_head) + 20
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(r, g, b, 102), width=1)
    y += 28

    items = [
        ("Ceramides and fatty acids", "to restore what UV and cleansing remove."),
        ("Niacinamide", "to regulate sebum and support ceramide synthesis under heat."),
        ("SPF", "applied in sufficient quantity. Reapplied."),
        ("A non-stripping cleanser", "because the acid mantle is already under pressure."),
    ]
    for name, desc in items:
        draw.text((MARGIN, y), name + ":", font=f_bold, fill=(r, g, b))
        name_w = tw(draw, name + ": ", f_bold)
        # wrap desc after name on same line or next
        full = name + ": " + desc
        y2 = draw_wrap(draw, full, f_reg, MARGIN, y, W - MARGIN*2, INK, sp=1.4)
        # override: draw name bold, then desc on next line
        # Simpler: just draw both as wrapped combined
        y = y2 + 18

    y += 8
    final = "That is a summer formula. It is not a new routine. It is the same understanding, adjusted for conditions."
    y = draw_wrap(draw, final, f_bold, MARGIN, y, W - MARGIN*2, INK, sp=1.4)

    footer = "Ingredients, decoded.  ·  @skinlabeditorial"
    draw.text((MARGIN, H - 50), footer, font=f_foot, fill=(r, g, b, 102))

    img.save(os.path.join(OUT_DIR, "slide-03.png"))
    print("slide-03.png saved")

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    slide_01(); slide_02(); slide_03()
    print("Done — 3 slides generated.")
