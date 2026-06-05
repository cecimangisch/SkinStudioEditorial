"""
Slide generator — 03 · The Label: Altruist Mineral SPF 50
The Label · 8 Slides
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

def tw(draw, text, font):
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0]

def th(draw, text, font):
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[3] - bb[1]

def cx(draw, text, font):
    return (W - tw(draw, text, font)) // 2

def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w2 in words:
        t = (cur + " " + w2).strip()
        if tw(draw, t, font) <= max_w:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w2
    if cur: lines.append(cur)
    return lines

def draw_wrap(draw, text, font, x, y, max_w, color, sp=1.5):
    lines = wrap(draw, text, font, max_w)
    lh = th(draw, "Ag", font)
    for line in lines:
        r, g, b = hex_to_rgb(color)
        draw.text((x, y), line, font=font, fill=(r, g, b))
        y += int(lh * sp)
    return y

def slide_label(draw, n, total, color=INK):
    f = dmsans(16)
    label = f"{n:02d} / {total:02d}"
    r, g, b = hex_to_rgb(color)
    draw.text((W - MARGIN - tw(draw, label, f), 40), label, font=f, fill=(r, g, b, 102))

def headline_rule(draw, y, headline, font, text_color, rule_color=INK, rule_opacity=100):
    r, g, b = hex_to_rgb(text_color)
    draw.text((MARGIN, y), headline, font=font, fill=(r, g, b))
    y += th(draw, headline, font) + 20
    rr, rg, rb = hex_to_rgb(rule_color)
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(rr, rg, rb, rule_opacity), width=1)
    return y + 28

def ingredient_block(draw, name, desc, y, name_font, desc_font, name_color, desc_color):
    r, g, b = hex_to_rgb(name_color)
    draw.text((MARGIN, y), name, font=name_font, fill=(r, g, b))
    y += th(draw, name, name_font) + 6
    y = draw_wrap(draw, desc, desc_font, MARGIN, y, W - MARGIN*2, desc_color, sp=1.4)
    return y + 20

# ── SLIDE 1 ────────────────────────────────────────────────────────────────────
def slide_01():
    img, draw = new_canvas(BONE)
    f_col   = dmsans(28)
    f_name  = fraunces(88)
    f_desc  = dmsans(32)
    f_tag   = dmsans(22)
    f_small = dmsans(18)

    total_h = (th(draw, "The Label:", f_col) + 12 +
               th(draw, "Altruist", f_name) + 12 +
               th(draw, "Mineral SPF 50", f_desc) + 60 +
               th(draw, "We read the INCI so you don't have to.", f_tag))

    y = (H - total_h) // 2 - 20
    r, g, b = hex_to_rgb(INK)
    draw.text((cx(draw, "The Label:", f_col), y), "The Label:", font=f_col, fill=(r, g, b, 153))
    y += th(draw, "The Label:", f_col) + 12
    draw.text((cx(draw, "Altruist", f_name), y), "Altruist", font=f_name, fill=hex_to_rgb(INK))
    y += th(draw, "Altruist", f_name) + 12
    draw.text((cx(draw, "Mineral SPF 50", f_desc), y), "Mineral SPF 50", font=f_desc, fill=(r, g, b, 200))
    y += th(draw, "Mineral SPF 50", f_desc) + 60
    draw.text((cx(draw, "We read the INCI so you don't have to.", f_tag), y),
              "We read the INCI so you don't have to.", font=f_tag, fill=(r, g, b, 140))

    draw.text((cx(draw, "@skinlabeditorial", f_small), H - 52),
              "@skinlabeditorial", font=f_small, fill=(r, g, b, 115))

    img.save(os.path.join(OUT_DIR, "slide-01.png"))
    print("slide-01.png saved")

# ── SLIDE 2 ────────────────────────────────────────────────────────────────────
def slide_02():
    img, draw = new_canvas(LAB_FROST)
    slide_label(draw, 2, 8)
    f_head = dmsans(40, bold=True)
    f_item = dmsans(24)
    f_note = dmsans(22)

    y = headline_rule(draw, 90, "What the pack says.", f_head, INK)

    claims = [
        "SPF 50 UVB protection",
        "Broad-spectrum (UVA + UVB)",
        "Mineral / physical filters only",
        "Suitable for sensitive skin",
        "Dermatologist-developed",
        "Approx. €3–5 for 200ml",
    ]
    r, g, b = hex_to_rgb(LAB_SAGE)
    for claim in claims:
        draw.rectangle([MARGIN, y + 6, MARGIN + 12, y + 18], fill=hex_to_rgb(LAB_SAGE))
        ri, gi, bi = hex_to_rgb(INK)
        draw.text((MARGIN + 24, y), claim, font=f_item, fill=(ri, gi, bi))
        y += th(draw, claim, f_item) + 16

    y += 16
    note = "The claim we are testing: does the formulation support these statements?"
    y = draw_wrap(draw, note, f_note, MARGIN, y, W - MARGIN*2, INK, sp=1.4)

    img.save(os.path.join(OUT_DIR, "slide-02.png"))
    print("slide-02.png saved")

# ── SLIDE 3 ────────────────────────────────────────────────────────────────────
def slide_03():
    img, draw = new_canvas(INK)
    slide_label(draw, 3, 8, color=BONE)
    f_head  = dmsans(40, bold=True)
    f_name  = dmsans(26, bold=True)
    f_desc  = dmsans(22)
    f_assess = dmsans(20)

    y = headline_rule(draw, 90, "The UV filters.", f_head, BONE, rule_color=LAB_SAGE, rule_opacity=180)

    ingredients = [
        ("Zinc Oxide",
         "Broad-spectrum: UVB, UVA2, UVA1. Photostable. Anti-inflammatory secondary effect. Primary filter."),
        ("Titanium Dioxide",
         "Excellent UVB coverage, weaker UVA1. Works synergistically with zinc oxide to extend spectrum."),
    ]
    for name, desc in ingredients:
        r, g, b = hex_to_rgb(BONE)
        draw.text((MARGIN, y), name, font=f_name, fill=(r, g, b))
        y += th(draw, name, f_name) + 8
        y = draw_wrap(draw, desc, f_desc, MARGIN, y, W - MARGIN*2, BONE, sp=1.4)
        y += 24

    y += 8
    assess = "Assessment: UV filter system appropriate and effective for SPF 50 claim."
    r, g, b = hex_to_rgb(LAB_MIST)
    y = draw_wrap(draw, assess, f_assess, MARGIN, y, W - MARGIN*2, LAB_MIST, sp=1.4)

    img.save(os.path.join(OUT_DIR, "slide-03.png"))
    print("slide-03.png saved")

# ── SLIDE 4 ────────────────────────────────────────────────────────────────────
def slide_04():
    img, draw = new_canvas(LAB_MIST)
    slide_label(draw, 4, 8)
    f_head = dmsans(40, bold=True)
    f_name = dmsans(26, bold=True)
    f_desc = dmsans(22)

    y = headline_rule(draw, 90, "The moisturising base.", f_head, INK)

    ingredients = [
        ("Glycerin", "Humectant. Draws water to the stratum corneum. Standard, effective, well-tolerated."),
        ("Caprylic/Capric Triglyceride", "Lightweight emollient. Non-comedogenic. Improves spreadability of mineral filters."),
        ("Panthenol (Vitamin B5)", "Skin-conditioning with minor anti-inflammatory effect. Standard in sensitive-skin formulas."),
        ("Allantoin", "Soothing agent. Reduces transepidermal water loss. Well-documented for skin tolerance."),
    ]
    for name, desc in ingredients:
        draw.text((MARGIN, y), name, font=f_name, fill=hex_to_rgb(INK))
        y += th(draw, name, f_name) + 6
        y = draw_wrap(draw, desc, f_desc, MARGIN, y, W - MARGIN*2, INK, sp=1.4)
        y += 18

    img.save(os.path.join(OUT_DIR, "slide-04.png"))
    print("slide-04.png saved")

# ── SLIDE 5 ────────────────────────────────────────────────────────────────────
def slide_05():
    img, draw = new_canvas(BONE)
    slide_label(draw, 5, 8)
    f_head = dmsans(38, bold=True)
    f_name = dmsans(26, bold=True)
    f_desc = dmsans(22)

    y = headline_rule(draw, 90, "The emulsifiers and stabilisers.", f_head, INK)

    ingredients = [
        ("Cetearyl Alcohol / Ceteareth-20",
         "Fatty alcohol / emulsifier pair. Stabilise the oil-water emulsion. Cetearyl alcohol is a skin-conditioning emollient — not an irritant."),
        ("Dimethicone",
         "Silicone emollient. Improves texture and slip. Reduces the chalky drag of high-percentage mineral formulas."),
        ("Phenoxyethanol / Ethylhexylglycerin",
         "Preservative system. Industry standard. Concentration-dependent safety profile is well-established."),
    ]
    for name, desc in ingredients:
        draw.text((MARGIN, y), name, font=f_name, fill=hex_to_rgb(INK))
        y += th(draw, name, f_name) + 6
        y = draw_wrap(draw, desc, f_desc, MARGIN, y, W - MARGIN*2, INK, sp=1.4)
        y += 20

    img.save(os.path.join(OUT_DIR, "slide-05.png"))
    print("slide-05.png saved")

# ── SLIDE 6 ────────────────────────────────────────────────────────────────────
def slide_06():
    img, draw = new_canvas(LINEN)
    slide_label(draw, 6, 8)
    f_head = dmsans(40, bold=True)
    f_item = dmsans(26)
    f_note = dmsans(22)

    y = headline_rule(draw, 90, "What is not in the formula.", f_head, INK)

    absences = [
        "No chemical UV filters (oxybenzone, avobenzone, octinoxate)",
        "No added fragrance or parfum",
        "No alcohol denat.",
        "No known irritating botanical extracts",
    ]
    r, g, b = hex_to_rgb(INK)
    for item in absences:
        draw.text((MARGIN, y), "–", font=f_item, fill=hex_to_rgb(LAB_SAGE))
        draw.text((MARGIN + 30, y), item, font=f_item, fill=(r, g, b))
        y += th(draw, item, f_item) + 18

    y += 20
    note = "The absence of fragrance and chemical filters is clinically meaningful for sensitive, reactive, or rosacea-prone skin. It is not a marketing claim."
    y = draw_wrap(draw, note, f_note, MARGIN, y, W - MARGIN*2, INK, sp=1.5)

    img.save(os.path.join(OUT_DIR, "slide-06.png"))
    print("slide-06.png saved")

# ── SLIDE 7 ────────────────────────────────────────────────────────────────────
def slide_07():
    img, draw = new_canvas(LAB_SAGE)
    slide_label(draw, 7, 8)
    f_verdict = dmsans(72, bold=True)
    f_score   = dmsans(44, bold=True)
    f_body    = dmsans(22)

    r, g, b = hex_to_rgb(INK)
    verdict = "WORTH IT"
    draw.text((cx(draw, verdict, f_verdict), 120), verdict, font=f_verdict, fill=(r, g, b))
    y = 120 + th(draw, verdict, f_verdict) + 20

    score = "8.5 / 10"
    draw.text((cx(draw, score, f_score), y), score, font=f_score, fill=(r, g, b))
    y += th(draw, score, f_score) + 28

    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(r, g, b, 100), width=1)
    y += 24

    body = (
        "The formulation supports every claim on the packaging. Dual mineral filters provide genuine "
        "broad-spectrum SPF 50 coverage. The moisturising base is functional and the absence of "
        "fragrance makes it suitable for sensitive presentations. "
        "Main limitation: whitening on deeper skin tones due to titanium dioxide particle size. "
        "At this price point, no equivalent exists in the EU mineral sunscreen market."
    )
    draw_wrap(draw, body, f_body, MARGIN, y, W - MARGIN*2, INK, sp=1.5)

    img.save(os.path.join(OUT_DIR, "slide-07.png"))
    print("slide-07.png saved")

# ── SLIDE 8 ────────────────────────────────────────────────────────────────────
def slide_08():
    img, draw = new_canvas(BONE)
    f_head  = dmsans(40, bold=True)
    f_sub   = dmsans(28)
    f_body  = dmsans(24)
    f_small = dmsans(18)

    texts = [
        ("The Label.", f_head, INK, 255),
        ("Every formula, decoded.", f_sub, INK, 178),
        ("", None, None, 0),
        ("We read the INCI so you don't have to.", f_body, INK, 153),
        ("", None, None, 0),
        ("@skinlabeditorial", f_body, INK, 200),
        ("Ingredients, decoded.", f_small, INK, 115),
    ]

    lhs = []
    for text, font, color, _ in texts:
        lhs.append(th(draw, text or "X", font or f_small))

    total = sum(lhs) + 18 * len(texts)
    y = (H - total) // 2

    for i, (text, font, color, opacity) in enumerate(texts):
        if text and font:
            r2, g2, b2 = hex_to_rgb(color)
            draw.text((cx(draw, text, font), y), text, font=font, fill=(r2, g2, b2, opacity))
        y += lhs[i] + 18

    img.save(os.path.join(OUT_DIR, "slide-08.png"))
    print("slide-08.png saved")

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    for fn in [slide_01, slide_02, slide_03, slide_04, slide_05, slide_06, slide_07, slide_08]:
        fn()
    print("Done — 8 slides generated.")
