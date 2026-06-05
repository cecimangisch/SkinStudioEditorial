"""
Slide generator — 05 · Worth The Price?: €8 SPF vs €45 SPF
Worth The Price? · 6 Slides
Campaign: The Summer Formula · July 2026
"""

from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/tmp/slidefonts"

BONE      = "#F5F0E8"
INK       = "#1A1A18"
LAB_SAGE  = "#BBD1C6"
LAB_MIST  = "#DAE9DF"
LAB_FROST = "#ECF0EE"

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

def slide_label(draw, n, total, color=INK):
    f = dmsans(16)
    label = f"{n:02d} / {total:02d}"
    r, g, b = hex_to_rgb(color)
    draw.text((W - MARGIN - tw(draw, label, f), 40), label, font=f, fill=(r, g, b, 102))

def hr(draw, y, color=INK, opacity=100):
    r, g, b = hex_to_rgb(color)
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(r, g, b, opacity), width=1)
    return y + 24

def spec_row(draw, label, val, y, f_bold, f_reg, color=INK):
    r, g, b = hex_to_rgb(color)
    draw.text((MARGIN, y), label, font=f_bold, fill=(r, g, b))
    x_val = MARGIN + tw(draw, label, f_bold) + 12
    draw.text((x_val, y), val, font=f_reg, fill=(r, g, b, 204))
    return y + th(draw, label, f_bold) + 14

def slide_01():
    img, draw = new_canvas(INK)
    f_fr   = fraunces(68)
    f_big  = dmsans(56, bold=True)
    f_vs   = dmsans(32)
    f_sub  = dmsans(24)
    f_sm   = dmsans(18)

    title = "Worth The Price?"
    t_y = 130
    r, g, b = hex_to_rgb(BONE)
    draw.text((cx(draw, title, f_fr), t_y), title, font=f_fr, fill=(r, g, b))
    y = t_y + th(draw, title, f_fr) + 50

    p1 = "€8 SPF"
    draw.text((cx(draw, p1, f_big), y), p1, font=f_big, fill=(r, g, b))
    y += th(draw, p1, f_big) + 16

    vs = "vs"
    r2, g2, b2 = hex_to_rgb(LAB_SAGE)
    draw.text((cx(draw, vs, f_vs), y), vs, font=f_vs, fill=(r2, g2, b2))
    y += th(draw, vs, f_vs) + 16

    p2 = "€45 SPF"
    draw.text((cx(draw, p2, f_big), y), p2, font=f_big, fill=(r, g, b))
    y += th(draw, p2, f_big) + 50

    sub = "What the price difference actually buys."
    draw.text((cx(draw, sub, f_sub), y), sub, font=f_sub, fill=(r, g, b, 153))

    handle = "@skinlabeditorial"
    draw.text((W - MARGIN - tw(draw, handle, f_sm), H - 50),
              handle, font=f_sm, fill=(r, g, b, 115))

    img.save(os.path.join(OUT_DIR, "slide-01.png"))
    print("slide-01.png saved")

def product_slide(bg, slide_n, price, product_name, specs, path):
    img, draw = new_canvas(bg)
    slide_label(draw, slide_n, 6)
    f_price = dmsans(48, bold=True)
    f_head  = dmsans(30, bold=True)
    f_bold  = dmsans(22, bold=True)
    f_reg   = dmsans(22)

    # Price badge
    badge_text = price
    bw = tw(draw, badge_text, f_price) + 32
    bh = th(draw, badge_text, f_price) + 20
    draw.rounded_rectangle([MARGIN, 80, MARGIN + bw, 80 + bh], radius=8, fill=hex_to_rgb(INK))
    draw.text((MARGIN + 16, 88), badge_text, font=f_price, fill=hex_to_rgb(BONE))

    y = 80 + bh + 20
    draw.text((MARGIN, y), product_name, font=f_head, fill=hex_to_rgb(INK))
    y += th(draw, product_name, f_head) + 16
    y = hr(draw, y, INK, 80)

    for label, val in specs:
        r, g, b = hex_to_rgb(INK)
        draw.text((MARGIN, y), label, font=f_bold, fill=(r, g, b))
        y += th(draw, label, f_bold) + 4
        y = draw_wrap(draw, val, f_reg, MARGIN + 16, y, W - MARGIN*2 - 16, INK, sp=1.35)
        y += 14

    img.save(path)
    print(f"{os.path.basename(path)} saved")

def slide_02():
    specs = [
        ("UV filters:", "Zinc oxide + titanium dioxide"),
        ("Filter type:", "Mineral (physical). Photostable. No systemic absorption."),
        ("Spectrum:", "Broad-spectrum. Full UVA1 coverage via zinc oxide."),
        ("Texture:", "Thicker. White cast visible on medium-dark skin tones."),
        ("Volume:", "200ml"),
        ("Base:", "Glycerin, panthenol, allantoin. No fragrance."),
    ]
    product_slide(BONE, 2, "€8", "Altruist Mineral SPF 50", specs,
                  os.path.join(OUT_DIR, "slide-02.png"))

def slide_03():
    img, draw = new_canvas(LAB_FROST)
    slide_label(draw, 3, 6)
    f_head = dmsans(38, bold=True)
    f_body = dmsans(23)
    f_bold = dmsans(23, bold=True)

    y = 90
    draw.text((MARGIN, y), "€8 · What you get.", font=f_head, fill=hex_to_rgb(INK))
    y += th(draw, "€8 · What you get.", f_head) + 20
    y = hr(draw, y, INK, 80)

    p1 = "Genuine broad-spectrum SPF 50 protection from a photostable mineral filter system. No systemic absorption concern. Suitable for all skin types including sensitive and reactive."
    y = draw_wrap(draw, p1, f_body, MARGIN, y, W - MARGIN*2, INK, sp=1.5)
    y += 24

    draw.text((MARGIN, y), "What you are missing at €8:", font=f_bold, fill=hex_to_rgb(INK))
    y += th(draw, "X", f_bold) + 10
    p2 = "Elegant texture. No white cast. No advanced chemical filter technology. Silicone formulas that disappear into skin. The kind of formula you will actually reach for every morning."
    y = draw_wrap(draw, p2, f_body, MARGIN, y, W - MARGIN*2, INK, sp=1.5)
    y += 24

    final = "Compliance drives efficacy. If the texture stops you using it, the SPF 50 number is irrelevant."
    draw_wrap(draw, final, f_bold, MARGIN, y, W - MARGIN*2, INK, sp=1.4)

    img.save(os.path.join(OUT_DIR, "slide-03.png"))
    print("slide-03.png saved")

def slide_04():
    specs = [
        ("UV filters:", "Mexoryl SX + Mexoryl XL + Tinosorb S + avobenzone"),
        ("Filter type:", "Chemical (organic). Mexoryl is proprietary to L'Oréal."),
        ("Spectrum:", "Broad-spectrum. Mexoryl SX engineered for deep UVA1 (340–400nm)."),
        ("Photostability:", "High. Mexoryl inherently stable. Tinosorb S stabilises avobenzone."),
        ("Texture:", "Fluid, invisible on skin. No cast on any skin tone."),
        ("Volume:", "50ml"),
    ]
    product_slide(LAB_MIST, 4, "€45", "La Roche-Posay Anthelios Invisible Fluid SPF 50+", specs,
                  os.path.join(OUT_DIR, "slide-04.png"))

def slide_05():
    img, draw = new_canvas(BONE)
    slide_label(draw, 5, 6)
    f_head = dmsans(38, bold=True)
    f_body = dmsans(23)
    f_bold = dmsans(23, bold=True)

    y = 90
    draw.text((MARGIN, y), "€45 · What the price buys.", font=f_head, fill=hex_to_rgb(INK))
    y += th(draw, "€45 · What the price buys.", f_head) + 20
    y = hr(draw, y, INK, 80)

    draw.text((MARGIN, y), "What you are paying for:", font=f_bold, fill=hex_to_rgb(INK))
    y += th(draw, "X", f_bold) + 10
    p1 = "Advanced filter technology with superior UVA1 performance. Fluid texture invisible on all skin tones. A formula that works under makeup without pilling. Formulation aesthetics that drive consistent daily use."
    y = draw_wrap(draw, p1, f_body, MARGIN, y, W - MARGIN*2, INK, sp=1.5)
    y += 24

    draw.text((MARGIN, y), "What you are not paying for:", font=f_bold, fill=hex_to_rgb(INK))
    y += th(draw, "X", f_bold) + 10
    p2 = "Better UVB protection. The SPF 50+ number provides marginally more UVB blocking than SPF 50. The difference is less than 1%."
    y = draw_wrap(draw, p2, f_body, MARGIN, y, W - MARGIN*2, INK, sp=1.5)

    img.save(os.path.join(OUT_DIR, "slide-05.png"))
    print("slide-05.png saved")

def slide_06():
    img, draw = new_canvas(LAB_SAGE)
    slide_label(draw, 6, 6)
    f_head  = dmsans(44, bold=True)
    f_label = dmsans(22, bold=True)
    f_body  = dmsans(22)

    y = 80
    draw.text((MARGIN, y), "The verdict.", font=f_head, fill=hex_to_rgb(INK))
    y += th(draw, "The verdict.", f_head) + 20
    y = hr(draw, y, INK, 100)

    verdicts = [
        ("Daily SPF, fair to medium skin:", "The €8 option provides equivalent UVB protection and adequate UVA coverage. Worth It."),
        ("Daily SPF, medium-dark to dark skin:", "Mineral white cast is a real barrier to consistent use. The €45 formula's aesthetics are functionally meaningful here."),
        ("Extended outdoor or high-altitude use:", "Mexoryl's UVA1 depth is the difference. The €45 price gap is justified."),
    ]
    for label, body in verdicts:
        draw.text((MARGIN, y), label, font=f_label, fill=hex_to_rgb(INK))
        y += th(draw, label, f_label) + 8
        y = draw_wrap(draw, body, f_body, MARGIN, y, W - MARGIN*2, INK, sp=1.4)
        y += 20

    y += 8
    final = "Compliance is the variable that actually determines how protected you are."
    draw_wrap(draw, final, f_label, MARGIN, y, W - MARGIN*2, INK, sp=1.4)

    img.save(os.path.join(OUT_DIR, "slide-06.png"))
    print("slide-06.png saved")

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    for fn in [slide_01, slide_02, slide_03, slide_04, slide_05, slide_06]:
        fn()
    print("Done — 6 slides generated.")
