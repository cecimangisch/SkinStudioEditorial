"""
Slide generator — 06 · Niacinamide, Exactly.
Ingredient School · 9 Slides
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
LINEN     = "#F1EAE1"

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

def body_slide(bg, slide_n, headline, paras, txt_color=INK, rule_color=INK, label_color=None):
    if label_color is None:
        label_color = txt_color
    img, draw = new_canvas(bg)
    slide_label(draw, slide_n, 9, color=label_color)
    f_head = dmsans(40, bold=True)
    f_body = dmsans(24)

    y = 90
    r, g, b = hex_to_rgb(txt_color)
    draw.text((MARGIN, y), headline, font=f_head, fill=(r, g, b))
    y += th(draw, headline, f_head) + 20
    rr, rg, rb = hex_to_rgb(rule_color)
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(rr, rg, rb, 120), width=1)
    y += 28

    for para in paras:
        y = draw_wrap(draw, para, f_body, MARGIN, y, W - MARGIN*2, txt_color, sp=1.5)
        y += 20

    return img

def slide_01():
    img, draw = new_canvas(LAB_MIST)
    f_title = fraunces(80)
    f_sub   = dmsans(26)
    f_small = dmsans(20)

    t1 = "Niacinamide,"
    t2 = "Exactly."
    sub = "It doesn't shrink your pores. Here is what it actually does."
    label = "Ingredient School · @skinlabeditorial"

    y = int(H * 0.26)
    r, g, b = hex_to_rgb(INK)
    draw.text((cx(draw, t1, f_title), y), t1, font=f_title, fill=(r, g, b))
    y += th(draw, t1, f_title) + 8
    draw.text((cx(draw, t2, f_title), y), t2, font=f_title, fill=(r, g, b))
    y += th(draw, t2, f_title) + 52

    for line in wrap(draw, sub, f_sub, 720):
        draw.text((cx(draw, line, f_sub), y), line, font=f_sub, fill=(r, g, b, 191))
        y += th(draw, line, f_sub) + 10
    y += 50
    draw.text((cx(draw, label, f_small), y), label, font=f_small, fill=(r, g, b, 115))

    img.save(os.path.join(OUT_DIR, "slide-01.png"))
    print("slide-01.png saved")

def slide_02():
    paras = [
        "Niacinamide is the amide form of vitamin B3 (niacin). It is water-soluble, stable across pH 3.5–7.5, and formulates well with most other actives.",
        "INCI name: Niacinamide",
        "It is distinct from niacin (nicotinic acid), which causes flushing. Niacinamide does not cause flushing. It is also distinct from oral supplements nicotinamide riboside and NMN, which function differently.",
    ]
    img = body_slide(BONE, 2, "What it is.", paras)
    img.save(os.path.join(OUT_DIR, "slide-02.png"))
    print("slide-02.png saved")

def slide_03():
    paras = [
        "Niacinamide upregulates the synthesis of ceramides, fatty acids, and cholesterol in the stratum corneum — the three lipid classes that form the skin's barrier structure.",
        "Regular topical use measurably increases ceramide content in the stratum corneum, reduces transepidermal water loss (TEWL), and improves overall barrier integrity.",
        "This is why niacinamide performs particularly well in summer, when heat-induced TEWL is elevated.",
    ]
    img = body_slide(LAB_FROST, 3, "What it does: the barrier.", paras)
    img.save(os.path.join(OUT_DIR, "slide-03.png"))
    print("slide-03.png saved")

def slide_04():
    paras = [
        "Niacinamide reduces sebum excretion rate (SER) by inhibiting the activity of sebaceous glands. The mechanism involves modulation of triglyceride synthesis in sebocytes.",
        "Clinical studies show statistically significant reduction in SER at concentrations of 2–4% with consistent daily use over 4–8 weeks.",
        "This is why it is used in formulations for oily and acne-prone skin. It does not block pores. It reduces the rate of sebum production. The result is smaller-appearing pores and less congestion — not pore 'shrinking'.",
    ]
    img = body_slide(INK, 4, "What it does: sebum regulation.",
                     paras, txt_color=BONE, rule_color=LAB_SAGE, label_color=BONE)
    img.save(os.path.join(OUT_DIR, "slide-04.png"))
    print("slide-04.png saved")

def slide_05():
    img, draw = new_canvas(LINEN)
    slide_label(draw, 5, 9)
    f_head = dmsans(40, bold=True)
    f_body = dmsans(24)

    y = 90
    r, g, b = hex_to_rgb(INK)
    draw.text((MARGIN, y), "What it does: inflammation.", font=f_head, fill=(r, g, b))
    y += th(draw, "X", f_head) + 20
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(r, g, b, 100), width=1)
    y += 28

    intro = "Niacinamide inhibits pro-inflammatory cytokines including IL-1β, IL-6, and TNF-α, and reduces migration of inflammatory cells to skin."
    y = draw_wrap(draw, intro, f_body, MARGIN, y, W - MARGIN*2, INK, sp=1.5)
    y += 20

    draw.text((MARGIN, y), "This anti-inflammatory action is why niacinamide is effective in:", font=f_body, fill=(r, g, b))
    y += th(draw, "X", f_body) + 14

    bullets = [
        "Acne formulations (reduces inflammatory lesion count)",
        "Rosacea management (calms persistent redness)",
        "Post-UV exposure support (reduces UV-induced cytokine response)",
    ]
    for b_text in bullets:
        draw.rectangle([MARGIN, y + 7, MARGIN + 10, y + 17], fill=hex_to_rgb(LAB_SAGE))
        draw.text((MARGIN + 22, y), b_text, font=f_body, fill=(r, g, b))
        y += th(draw, b_text, f_body) + 14

    img.save(os.path.join(OUT_DIR, "slide-05.png"))
    print("slide-05.png saved")

def slide_06():
    paras = [
        "Niacinamide inhibits the transfer of melanosomes from melanocytes to keratinocytes — the step where melanin moves from where it is produced to where it causes visible darkening.",
        "It does not inhibit melanin synthesis directly (that is tyrosinase inhibition — a different mechanism). It interrupts the transfer.",
        "Clinical evidence supports efficacy for post-inflammatory hyperpigmentation and UV-induced pigmentation at concentrations of 4–10% with consistent use over 8–12 weeks.",
    ]
    img = body_slide(LAB_MIST, 6, "What it does: hyperpigmentation.", paras)
    img.save(os.path.join(OUT_DIR, "slide-06.png"))
    print("slide-06.png saved")

def slide_07():
    img, draw = new_canvas(BONE)
    slide_label(draw, 7, 9)
    f_head = dmsans(40, bold=True)
    f_body = dmsans(24)
    f_bold = dmsans(24, bold=True)

    y = 90
    r, g, b = hex_to_rgb(INK)
    draw.text((MARGIN, y), "How to use it.", font=f_head, fill=(r, g, b))
    y += th(draw, "X", f_head) + 20
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(r, g, b, 100), width=1)
    y += 28

    ranges = [
        ("2–4%:", "Sebum regulation and anti-inflammatory effects dominant."),
        ("5%:", "Clinical barrier improvement and hyperpigmentation effects."),
        ("10%:", "Targeted treatments for pigmentation and acne. Good tolerance for most skin types."),
    ]
    for label, val in ranges:
        draw.text((MARGIN, y), label, font=f_bold, fill=(r, g, b))
        lw = tw(draw, label, f_bold) + 12
        draw.text((MARGIN + lw, y), val, font=f_body, fill=(r, g, b, 204))
        y += th(draw, label, f_bold) + 18

    y += 16
    note = "Niacinamide does not require an acidic pH to function. It performs at pH 3.5–7.5. It pairs well with vitamin C, retinol, and AHAs — the concern about niacinamide converting to niacin at low pH is not supported by evidence at typical use concentrations."
    draw_wrap(draw, note, f_body, MARGIN, y, W - MARGIN*2, INK, sp=1.5)

    img.save(os.path.join(OUT_DIR, "slide-07.png"))
    print("slide-07.png saved")

def slide_08():
    paras = [
        "Niacinamide is not a pore-shrinker or a brightener. It is a multifunctional B vitamin that does several specific, evidence-backed things: supports ceramide synthesis, regulates sebum production, reduces pro-inflammatory cytokines, and interrupts melanin transfer.",
        "One of the most well-tolerated actives in skincare. Works across multiple concerns without complex formulation conditions.",
        "In summer, its barrier-supporting and sebum-regulating effects directly address the two most common heat-related skin issues.",
        "Concentration matters. Use it consistently.",
    ]
    img, draw = new_canvas(INK)
    slide_label(draw, 8, 9, color=BONE)
    f_head = dmsans(44, bold=True)
    f_body = dmsans(24)

    y = 90
    r, g, b = hex_to_rgb(BONE)
    draw.text((MARGIN, y), "The takeaway.", font=f_head, fill=(r, g, b))
    y += th(draw, "X", f_head) + 20
    rr, rg, rb = hex_to_rgb(LAB_SAGE)
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(rr, rg, rb, 180), width=1)
    y += 28
    for para in paras:
        y = draw_wrap(draw, para, f_body, MARGIN, y, W - MARGIN*2, BONE, sp=1.5)
        y += 20

    img.save(os.path.join(OUT_DIR, "slide-08.png"))
    print("slide-08.png saved")

def slide_09():
    img, draw = new_canvas(LAB_MIST)
    f_head  = dmsans(36, bold=True)
    f_sub   = dmsans(28)
    f_body  = dmsans(24)
    f_small = dmsans(22)

    lines = [
        ("Ingredient School.", f_head, INK, 255),
        ("One ingredient. The complete picture.", f_sub, INK, 204),
        ("", None, None, 0),
        ("Every week at @skinlabeditorial", f_body, INK, 255),
        ("", None, None, 0),
        ("Ingredients, decoded.", f_small, INK, 153),
    ]

    lhs = [th(draw, t or "X", fn or f_small) for t, fn, _, _ in lines]
    total = sum(lhs) + 18 * len(lines)
    y = (H - total) // 2

    for i, (text, font, color, opacity) in enumerate(lines):
        if text and font:
            r2, g2, b2 = hex_to_rgb(color)
            draw.text((cx(draw, text, font), y), text, font=font, fill=(r2, g2, b2, opacity))
        y += lhs[i] + 18

    img.save(os.path.join(OUT_DIR, "slide-09.png"))
    print("slide-09.png saved")

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    for fn in [slide_01,slide_02,slide_03,slide_04,slide_05,slide_06,slide_07,slide_08,slide_09]:
        fn()
    print("Done — 9 slides generated.")
