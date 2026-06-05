"""
Slide generator — 12 · Brand Study: Understanding Medik8
Brand Study · 8 Slides
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

def body_slide(bg, n, headline, paras, txt=INK, rule_col=INK, lbl_col=None):
    if lbl_col is None: lbl_col = txt
    img, draw = new_canvas(bg)
    slide_label(draw, n, 8, color=lbl_col)
    f_head = dmsans(38, bold=True)
    f_body = dmsans(23)
    y = 90
    r, g, b = hex_to_rgb(txt)
    draw.text((MARGIN, y), headline, font=f_head, fill=(r, g, b))
    y += th(draw, headline, f_head) + 20
    y = hr(draw, y, rule_col, 100)
    for para in paras:
        y = draw_wrap(draw, para, f_body, MARGIN, y, W - MARGIN*2, txt, sp=1.5)
        y += 20
    return img

def slide_01():
    img, draw = new_canvas(BONE)
    f_label  = dmsans(36)
    f_brand  = fraunces(96)
    f_small  = dmsans(20)

    r, g, b = hex_to_rgb(INK)
    y = int(H * 0.30)
    draw.text((cx(draw, "Understanding", f_label), y), "Understanding", font=f_label, fill=(r, g, b, 165))
    y += th(draw, "Understanding", f_label) + 14
    brand = "Medik8"
    draw.text((cx(draw, brand, f_brand), y), brand, font=f_brand, fill=(r, g, b))
    y += th(draw, brand, f_brand) + 56

    label = "Brand Study · @skinlabeditorial"
    draw.text((cx(draw, label, f_small), y), label, font=f_small, fill=(r, g, b, 115))

    img.save(os.path.join(OUT_DIR, "slide-01.png"))
    print("slide-01.png saved")

def slide_02():
    paras = [
        "Medik8 was founded in 2009 in the UK by pharmacist Elliot Isaacs. Initially sold exclusively through dermatologists, cosmetic clinics, and aesthetic practitioners. Direct-to-consumer distribution came later.",
        "The founding philosophy: 'SEE, PROTECT, PREVENT' — vitamin C (antioxidant morning), SPF (photoprotection), retinol (cellular turnover evening). This maps to the routine with the strongest combined clinical evidence for long-term skin health.",
        "The brand operates at the intersection of pharmaceutical rigour and cosmetics — which explains both its pricing and its clinical credibility.",
    ]
    img = body_slide(LAB_FROST, 2, "Origin and philosophy.", paras)
    img.save(os.path.join(OUT_DIR, "slide-02.png"))
    print("slide-02.png saved")

def slide_03():
    paras = [
        "Medik8's C-Tetra range uses tetrahexyldecyl ascorbate (THD ascorbate) — a fat-soluble vitamin C ester that is more stable than L-ascorbic acid and penetrates the lipid-rich skin environment differently.",
        "The Fresh C and Vitamin C lines use L-ascorbic acid — less stable but the most biologically studied form.",
        "Strategic significance: Medik8 acknowledges that different vitamin C forms have different stability and delivery profiles, and offers both. This reflects genuine formulation philosophy.",
        "For summer: THD ascorbate's greater stability may outweigh the clinical evidence advantage of LAA, when oxidation rate is elevated.",
    ]
    img = body_slide(LAB_MIST, 3, "Hero ingredients: vitamin C.", paras)
    img.save(os.path.join(OUT_DIR, "slide-03.png"))
    print("slide-03.png saved")

def slide_04():
    paras = [
        "Medik8's Advanced Day Total Protect SPF 50 combines Tinosorb M and Tinosorb S (EU-approved modern filters) with zinc oxide. Photostable. No whitening. Full-spectrum.",
        "The Clean Screen range uses zinc oxide-only — for users who prefer physical-only formulas.",
        "Both lines address the main SPF trade-off: mineral formulas compromise texture for safety preference; older chemical systems raise filter questions. Medik8's modern chemical filters are photostable and cosmetically elegant.",
    ]
    img = body_slide(BONE, 4, "Hero ingredients: SPF.", paras)
    img.save(os.path.join(OUT_DIR, "slide-04.png"))
    print("slide-04.png saved")

def slide_05():
    paras = [
        "Medik8's Crystal Retinal range uses retinaldehyde (retinal) rather than retinol. Retinal is one step closer to retinoic acid in the conversion pathway — one fewer enzymatic step in skin.",
        "Clinical data suggests retinal is approximately 11× more potent than retinol at equivalent concentrations, with faster visible results. More likely to cause irritation at high doses.",
        "Concentration range: Crystal Retinal 1 (0.01%), 3 (0.03%), 6 (0.06%), 10 (0.1%), 20 (0.2%). The step-up system directly addresses the irritation risk inherent in the potency advantage.",
    ]
    img = body_slide(LAB_FROST, 5, "Hero ingredients: retinol.", paras)
    img.save(os.path.join(OUT_DIR, "slide-05.png"))
    print("slide-05.png saved")

def slide_06():
    img, draw = new_canvas(INK)
    slide_label(draw, 6, 8, color=BONE)
    f_head  = dmsans(38, bold=True)
    f_body  = dmsans(23)
    f_label = dmsans(22, bold=True)

    r, g, b = hex_to_rgb(BONE)
    y = 90
    draw.text((MARGIN, y), "Formulation architecture.", font=f_head, fill=(r, g, b))
    y += th(draw, "X", f_head) + 20
    rr, rg, rb = hex_to_rgb(LAB_SAGE)
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(rr, rg, rb, 180), width=1)
    y += 24

    intro = "The 'SEE, PROTECT, PREVENT' framework is not just marketing — it is the clinical routine with the best evidence for long-term skin health, built into the product architecture."
    y = draw_wrap(draw, intro, f_body, MARGIN, y, W - MARGIN*2, BONE, sp=1.5)
    y += 24

    steps = [
        ("Vitamin C (morning):", "Antioxidant protection against UV-induced free radical damage before photoprotection is applied."),
        ("SPF (over the top):", "Primary photoprotection."),
        ("Retinol/retinal (evening):", "Cellular turnover, collagen stimulation, long-term structural intervention."),
    ]
    # Draw with a thin connecting line on the left
    line_x = MARGIN - 20
    step_ys = []
    for name, desc in steps:
        step_ys.append(y)
        draw.text((MARGIN, y), name, font=f_label, fill=(r, g, b))
        y += th(draw, name, f_label) + 6
        y = draw_wrap(draw, desc, f_body, MARGIN + 8, y, W - MARGIN*2 - 8, BONE, sp=1.4)
        y += 18

    # Draw connecting line
    if len(step_ys) >= 2:
        draw.line([(line_x, step_ys[0] + 6), (line_x, step_ys[-1] + 6)],
                  fill=(*hex_to_rgb(LAB_SAGE), 150), width=2)
        for sy in step_ys:
            draw.ellipse([line_x - 4, sy + 2, line_x + 4, sy + 10],
                        fill=hex_to_rgb(LAB_SAGE))

    img.save(os.path.join(OUT_DIR, "slide-06.png"))
    print("slide-06.png saved")

def slide_07():
    img, draw = new_canvas(LAB_SAGE)
    slide_label(draw, 7, 8)
    f_head  = dmsans(44, bold=True)
    f_label = dmsans(22, bold=True)
    f_val   = dmsans(22)
    f_score = dmsans(48, bold=True)

    r, g, b = hex_to_rgb(INK)
    y = 80
    draw.text((MARGIN, y), "Lab assessment.", font=f_head, fill=(r, g, b))
    y += th(draw, "Lab assessment.", f_head) + 20
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(r, g, b, 100), width=1)
    y += 24

    rows = [
        ("Formulation quality:", "High. Evidence of genuine ingredient selection rationale."),
        ("Clinical evidence:", "Above average for a cosmetics brand. Especially strong on retinoid and SPF lines."),
        ("Price positioning:", "Premium but justifiable. Margin supports formulation investment."),
        ("Limitations:", "Some products use fragrance. THD ascorbate has less direct clinical evidence than LAA for specific outcomes."),
    ]
    for label, val in rows:
        draw.text((MARGIN, y), label, font=f_label, fill=(r, g, b))
        y += th(draw, label, f_label) + 6
        y = draw_wrap(draw, val, f_val, MARGIN + 8, y, W - MARGIN*2 - 8, INK, sp=1.35)
        y += 18

    y += 16
    score_label = "Lab Brand Score:"
    score_val = "8.8 / 10"
    draw.text((MARGIN, y), score_label, font=f_label, fill=(r, g, b))
    y += th(draw, score_label, f_label) + 8
    draw.text((MARGIN, y), score_val, font=f_score, fill=(r, g, b))

    img.save(os.path.join(OUT_DIR, "slide-07.png"))
    print("slide-07.png saved")

def slide_08():
    img, draw = new_canvas(BONE)
    f_head  = dmsans(40, bold=True)
    f_sub   = dmsans(28)
    f_body  = dmsans(24)
    f_small = dmsans(18)

    r, g, b = hex_to_rgb(INK)
    lines = [("Brand Study.", f_head, 255),
             ("The brands behind the formulas.", f_sub, 178),
             ("", None, 0),
             ("Questions or brands to audit? Leave them below.", f_body, 153),
             ("", None, 0),
             ("@skinlabeditorial  ·  Ingredients, decoded.", f_small, 115)]

    lhs = [th(draw, t or "X", fn or f_small) for t, fn, _ in lines]
    total = sum(lhs) + 16 * len(lines)
    y = (H - total) // 2
    for i, (text, font, opacity) in enumerate(lines):
        if text and font:
            draw.text((cx(draw, text, font), y), text, font=font, fill=(r, g, b, opacity))
        y += lhs[i] + 16

    img.save(os.path.join(OUT_DIR, "slide-08.png"))
    print("slide-08.png saved")

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    for fn in [slide_01,slide_02,slide_03,slide_04,slide_05,slide_06,slide_07,slide_08]:
        fn()
    print("Done — 8 slides generated.")
