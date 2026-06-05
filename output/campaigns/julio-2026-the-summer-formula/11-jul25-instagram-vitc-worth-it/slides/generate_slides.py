"""
Slide generator — 11 · Worth The Price?: €12 Vitamin C vs €85 Vitamin C
Worth The Price? · 6 Slides
Campaign: The Summer Formula · July 2026
"""

from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR  = os.path.dirname(os.path.abspath(__file__))
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

def hr(draw, y, color=INK, opacity=80):
    r, g, b = hex_to_rgb(color)
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(r, g, b, opacity), width=1)
    return y + 24

def spec_row_block(draw, name, desc, y, f_name, f_desc, color):
    r, g, b = hex_to_rgb(color)
    draw.text((MARGIN, y), name, font=f_name, fill=(r, g, b))
    y += th(draw, name, f_name) + 6
    y = draw_wrap(draw, desc, f_desc, MARGIN + 8, y, W - MARGIN*2 - 8, color, sp=1.4)
    return y + 16

def slide_01():
    img, draw = new_canvas(INK)
    f_fr   = fraunces(68)
    f_big  = dmsans(56, bold=True)
    f_vs   = dmsans(32)
    f_sub  = dmsans(24)
    f_sm   = dmsans(18)

    r, g, b = hex_to_rgb(BONE)
    y = 110
    title = "Worth The Price?"
    draw.text((cx(draw, title, f_fr), y), title, font=f_fr, fill=(r, g, b))
    y += th(draw, title, f_fr) + 46

    p1 = "€12 Vitamin C"
    draw.text((cx(draw, p1, f_big), y), p1, font=f_big, fill=(r, g, b))
    y += th(draw, p1, f_big) + 14

    vs = "vs"
    r2, g2, b2 = hex_to_rgb(LAB_SAGE)
    draw.text((cx(draw, vs, f_vs), y), vs, font=f_vs, fill=(r2, g2, b2))
    y += th(draw, vs, f_vs) + 14

    p2 = "€85 Vitamin C"
    draw.text((cx(draw, p2, f_big), y), p2, font=f_big, fill=(r, g, b))
    y += th(draw, p2, f_big) + 48

    sub = "Three variables determine vitamin C efficacy."
    draw.text((cx(draw, sub, f_sub), y), sub, font=f_sub, fill=(r, g, b, 153))

    handle = "@skinlabeditorial"
    draw.text((W - MARGIN - tw(draw, handle, f_sm), H - 50),
              handle, font=f_sm, fill=(r, g, b, 115))

    img.save(os.path.join(OUT_DIR, "slide-01.png"))
    print("slide-01.png saved")

def product_slide(bg, n, price, headline, specs, path):
    img, draw = new_canvas(bg)
    slide_label(draw, n, 6)
    f_price = dmsans(44, bold=True)
    f_head  = dmsans(26, bold=True)
    f_name  = dmsans(22, bold=True)
    f_desc  = dmsans(21)

    bw = tw(draw, price, f_price) + 32
    bh = th(draw, price, f_price) + 18
    draw.rounded_rectangle([MARGIN, 80, MARGIN + bw, 80 + bh], radius=8, fill=hex_to_rgb(INK))
    draw.text((MARGIN + 16, 88), price, font=f_price, fill=hex_to_rgb(BONE))

    y = 80 + bh + 18
    draw.text((MARGIN, y), headline, font=f_head, fill=hex_to_rgb(INK))
    y += th(draw, headline, f_head) + 14
    y = hr(draw, y)

    for name, desc in specs:
        y = spec_row_block(draw, name, desc, y, f_name, f_desc, INK)

    img.save(path)
    print(f"{os.path.basename(path)} saved")

def slide_02():
    specs = [
        ("Vitamin C form:", "L-ascorbic acid (LAA) — the most biologically active form."),
        ("Concentration:", "8%. Within the 5–10% effective range for antioxidant effects."),
        ("pH:", "Approximately 3.5 — appropriate for LAA stability and penetration."),
        ("Alpha Arbutin (2%):", "Tyrosinase inhibitor. Adds hyperpigmentation benefit."),
        ("Stability:", "L-ascorbic acid is inherently unstable. Summer heat accelerates oxidation."),
    ]
    product_slide(BONE, 2, "€12", "The Ordinary Ascorbic Acid 8% + Alpha Arbutin 2%",
                  specs, os.path.join(OUT_DIR, "slide-02.png"))

def slide_03():
    img, draw = new_canvas(LAB_FROST)
    slide_label(draw, 3, 6)
    f_head = dmsans(38, bold=True)
    f_body = dmsans(23)
    f_bold = dmsans(23, bold=True)

    y = 90
    r, g, b = hex_to_rgb(INK)
    draw.text((MARGIN, y), "€12 · What you get.", font=f_head, fill=(r, g, b))
    y += th(draw, "X", f_head) + 20
    y = hr(draw, y)

    p1 = "At 8% L-ascorbic acid at pH 3.5, this formulation is within the clinical efficacy range for antioxidant protection and modest brightening. The alpha arbutin adds a hyperpigmentation mechanism."
    y = draw_wrap(draw, p1, f_body, MARGIN, y, W - MARGIN*2, INK, sp=1.5)
    y += 20

    p2 = "At €12 for 30ml: the price means you can replace it monthly — exactly what an unstable vitamin C formula requires in summer."
    y = draw_wrap(draw, p2, f_body, MARGIN, y, W - MARGIN*2, INK, sp=1.5)
    y += 20

    draw.text((MARGIN, y), "What you are missing:", font=f_bold, fill=(r, g, b))
    y += th(draw, "X", f_bold) + 10
    p3 = "The synergistic antioxidant system of L-ascorbic acid + vitamin E + ferulic acid — which has the strongest clinical evidence for photoprotective effect. And you are at 8%, not 15%."
    draw_wrap(draw, p3, f_body, MARGIN, y, W - MARGIN*2, INK, sp=1.5)

    img.save(os.path.join(OUT_DIR, "slide-03.png"))
    print("slide-03.png saved")

def slide_04():
    specs = [
        ("Vitamin C form:", "L-ascorbic acid — same form as The Ordinary."),
        ("Concentration:", "15%. High-efficacy range. Clinical studies use 10–20%."),
        ("pH:", "2.5–3.5 — optimal for LAA stability and maximum penetration."),
        ("Vitamin E (1%):", "Antioxidant. Synergistic effect with L-ascorbic acid."),
        ("Ferulic Acid (0.5%):", "Doubles the photoprotective antioxidant effect (Pinnell 2005). Stabilises LAA in the formula."),
    ]
    product_slide(LAB_MIST, 4, "€85", "SkinCeuticals C E Ferulic",
                  specs, os.path.join(OUT_DIR, "slide-04.png"))

def slide_05():
    img, draw = new_canvas(BONE)
    slide_label(draw, 5, 6)
    f_head = dmsans(38, bold=True)
    f_body = dmsans(23)
    f_bold = dmsans(23, bold=True)

    y = 90
    r, g, b = hex_to_rgb(INK)
    draw.text((MARGIN, y), "€85 · What the price buys.", font=f_head, fill=(r, g, b))
    y += th(draw, "X", f_head) + 20
    y = hr(draw, y)

    p1 = "The Pinnell 2005 study is the clinical foundation: 15% LAA + 1% vitamin E + 0.5% ferulic acid at pH 2.5–3.5 doubled the photoprotective effect versus LAA alone."
    y = draw_wrap(draw, p1, f_body, MARGIN, y, W - MARGIN*2, INK, sp=1.5)
    y += 20

    p2 = "Ferulic acid does two things: extends the antioxidant effect of vitamin C and E, and stabilises L-ascorbic acid — meaning this formula degrades slower than an LAA-only product."
    y = draw_wrap(draw, p2, f_body, MARGIN, y, W - MARGIN*2, INK, sp=1.5)
    y += 20

    draw.text((MARGIN, y), "What you are paying for:", font=f_bold, fill=(r, g, b))
    y += th(draw, "X", f_bold) + 10
    p3 = "Higher concentration. Tri-antioxidant system with the strongest clinical evidence. Better stability. Price reflects the formulation and clinical investment."
    draw_wrap(draw, p3, f_body, MARGIN, y, W - MARGIN*2, INK, sp=1.5)

    img.save(os.path.join(OUT_DIR, "slide-05.png"))
    print("slide-05.png saved")

def slide_06():
    img, draw = new_canvas(LAB_SAGE)
    slide_label(draw, 6, 6)
    f_head  = dmsans(44, bold=True)
    f_label = dmsans(22, bold=True)
    f_body  = dmsans(22)

    y = 80
    r, g, b = hex_to_rgb(INK)
    draw.text((MARGIN, y), "The verdict.", font=f_head, fill=(r, g, b))
    y += th(draw, "The verdict.", f_head) + 20
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(r, g, b, 100), width=1)
    y += 24

    verdicts = [
        ("In summer:", "A €85 formula stored in a hot, light-exposed bathroom for 3 months is worse than a €12 formula replaced monthly and stored correctly."),
        ("For daily antioxidant protection:", "The €12 option is within the efficacy range. Replace every 4–6 weeks in summer. Worth It."),
        ("For maximum photoprotective antioxidant effect:", "SkinCeuticals tri-antioxidant system has the strongest clinical evidence. The €85 price is justified for this outcome."),
    ]
    for label, body in verdicts:
        draw.text((MARGIN, y), label, font=f_label, fill=(r, g, b))
        y += th(draw, label, f_label) + 8
        y = draw_wrap(draw, body, f_body, MARGIN, y, W - MARGIN*2, INK, sp=1.4)
        y += 20

    y += 8
    final = "Storage and replacement discipline is the variable that determines real-world outcome."
    draw_wrap(draw, final, f_label, MARGIN, y, W - MARGIN*2, INK, sp=1.4)

    img.save(os.path.join(OUT_DIR, "slide-06.png"))
    print("slide-06.png saved")

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    for fn in [slide_01,slide_02,slide_03,slide_04,slide_05,slide_06]:
        fn()
    print("Done — 6 slides generated.")
