"""
Slide generator — 10 · The Label: CeraVe AM Facial Moisturising Lotion SPF 25
The Label · 8 Slides
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
PETAL     = "#E6D2D0"

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

def ingr_block(draw, name, desc, y, f_name, f_desc, txt_color):
    r, g, b = hex_to_rgb(txt_color)
    draw.text((MARGIN, y), name, font=f_name, fill=(r, g, b))
    y += th(draw, name, f_name) + 6
    y = draw_wrap(draw, desc, f_desc, MARGIN + 8, y, W - MARGIN*2 - 8, txt_color, sp=1.4)
    return y + 18

def slide_01():
    img, draw = new_canvas(BONE)
    f_col   = dmsans(28)
    f_name  = fraunces(88)
    f_desc  = dmsans(30)
    f_tag   = dmsans(22)
    f_small = dmsans(18)

    r, g, b = hex_to_rgb(INK)
    y = int(H * 0.22)
    draw.text((cx(draw, "The Label:", f_col), y), "The Label:", font=f_col, fill=(r, g, b, 153))
    y += th(draw, "The Label:", f_col) + 10
    draw.text((cx(draw, "CeraVe", f_name), y), "CeraVe", font=f_name, fill=(r, g, b))
    y += th(draw, "CeraVe", f_name) + 8
    for line in ["AM Facial Moisturising", "Lotion SPF 25"]:
        draw.text((cx(draw, line, f_desc), y), line, font=f_desc, fill=(r, g, b, 200))
        y += th(draw, line, f_desc) + 6
    y += 52
    tag = "We read the INCI so you don't have to."
    draw.text((cx(draw, tag, f_tag), y), tag, font=f_tag, fill=(r, g, b, 140))
    draw.text((cx(draw, "@skinlabeditorial", f_small), H - 52),
              "@skinlabeditorial", font=f_small, fill=(r, g, b, 115))

    img.save(os.path.join(OUT_DIR, "slide-01.png"))
    print("slide-01.png saved")

def slide_02():
    img, draw = new_canvas(LAB_FROST)
    slide_label(draw, 2, 8)
    f_head = dmsans(40, bold=True)
    f_item = dmsans(24)
    f_note = dmsans(22)

    y = hr(draw, 90 + th(draw, "X", f_head) + 20, INK, 80)
    r, g, b = hex_to_rgb(INK)
    # Re-draw properly
    img, draw = new_canvas(LAB_FROST)
    slide_label(draw, 2, 8)
    y = 90
    draw.text((MARGIN, y), "What the pack says.", font=f_head, fill=(r, g, b))
    y += th(draw, "X", f_head) + 20
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(r, g, b, 80), width=1)
    y += 24

    claims = ["SPF 25 broad-spectrum protection",
              "Ceramides NP, AP, EOP + cholesterol",
              "Hyaluronic acid + niacinamide",
              "MVE (MultiVesicular Emulsion) technology",
              "Non-comedogenic. Fragrance-free.",
              "Suitable for normal to dry skin"]
    for claim in claims:
        draw.rectangle([MARGIN, y + 6, MARGIN + 12, y + 18], fill=hex_to_rgb(LAB_SAGE))
        draw.text((MARGIN + 24, y), claim, font=f_item, fill=(r, g, b))
        y += th(draw, claim, f_item) + 14
    y += 16
    note = "The claims we are testing: ceramide formulation credibility, SPF system performance, MVE technology."
    draw_wrap(draw, note, f_note, MARGIN, y, W - MARGIN*2, INK, sp=1.4)

    img.save(os.path.join(OUT_DIR, "slide-02.png"))
    print("slide-02.png saved")

def slide_03():
    img, draw = new_canvas(INK)
    slide_label(draw, 3, 8, color=BONE)
    f_head  = dmsans(40, bold=True)
    f_name  = dmsans(24, bold=True)
    f_desc  = dmsans(22)
    f_note  = dmsans(19)

    y = 90
    r, g, b = hex_to_rgb(BONE)
    draw.text((MARGIN, y), "The UV filters.", font=f_head, fill=(r, g, b))
    y += th(draw, "X", f_head) + 20
    rr, rg, rb = hex_to_rgb(LAB_SAGE)
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(rr, rg, rb, 180), width=1)
    y += 24

    ingrs = [
        ("Zinc Oxide (9.4%)", "Mineral UV filter. Broad-spectrum: UVB, UVA2, UVA1. Photostable. Anti-inflammatory."),
        ("Octinoxate (6%)", "Chemical UVB filter. Effective UVB coverage, limited UVA. Hybrid system with zinc oxide provides complete spectrum."),
    ]
    for name, desc in ingrs:
        draw.text((MARGIN, y), name, font=f_name, fill=(r, g, b))
        y += th(draw, name, f_name) + 6
        y = draw_wrap(draw, desc, f_desc, MARGIN + 8, y, W - MARGIN*2 - 8, BONE, sp=1.4)
        y += 22

    y += 8
    note = "SPF 25 result: achievable at these filter concentrations. Reaching SPF 50 would require higher concentrations, changing the texture. Octinoxate is EU-permitted; some users prefer zinc-only formulas."
    draw_wrap(draw, note, f_note, MARGIN, y, W - MARGIN*2, LAB_MIST, sp=1.4)

    img.save(os.path.join(OUT_DIR, "slide-03.png"))
    print("slide-03.png saved")

def slide_04():
    img, draw = new_canvas(LAB_MIST)
    slide_label(draw, 4, 8)
    f_head = dmsans(40, bold=True)
    f_name = dmsans(24, bold=True)
    f_desc = dmsans(22)
    f_note = dmsans(20)

    r, g, b = hex_to_rgb(INK)
    y = 90
    draw.text((MARGIN, y), "The ceramide system.", font=f_head, fill=(r, g, b))
    y += th(draw, "X", f_head) + 20
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(r, g, b, 80), width=1)
    y += 24

    ingrs = [
        ("Ceramide NP, AP, EOP", "Three ceramide types. Multi-ceramide approach addresses different aspects of the lipid bilayer."),
        ("Cholesterol", "Critical lipid bilayer co-component. Correctly paired with ceramides."),
        ("Phytosphingosine", "Ceramide precursor. Supports endogenous ceramide synthesis."),
    ]
    for name, desc in ingrs:
        draw.text((MARGIN, y), name, font=f_name, fill=(r, g, b))
        y += th(draw, name, f_name) + 6
        y = draw_wrap(draw, desc, f_desc, MARGIN + 8, y, W - MARGIN*2 - 8, INK, sp=1.4)
        y += 18
    y += 10
    note = "MVE technology encapsulates ceramides in multilayer spheres for gradual release. The '24-hour hydration' claim has clinical support."
    draw_wrap(draw, note, f_note, MARGIN, y, W - MARGIN*2, INK, sp=1.45)

    img.save(os.path.join(OUT_DIR, "slide-04.png"))
    print("slide-04.png saved")

def slide_05():
    img, draw = new_canvas(BONE)
    slide_label(draw, 5, 8)
    f_head = dmsans(40, bold=True)
    f_name = dmsans(24, bold=True)
    f_desc = dmsans(22)

    r, g, b = hex_to_rgb(INK)
    y = 90
    draw.text((MARGIN, y), "The hydrating agents.", font=f_head, fill=(r, g, b))
    y += th(draw, "X", f_head) + 20
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(r, g, b, 80), width=1)
    y += 24

    ingrs = [
        ("Sodium Hyaluronate", "Humectant. Attracts water to the stratum corneum."),
        ("Niacinamide", "Vitamin B3. At ~2% concentration: sebum regulation and barrier support are the primary effects."),
        ("Glycerin", "Humectant. Works synergistically with hyaluronic acid."),
    ]
    for name, desc in ingrs:
        draw.text((MARGIN, y), name, font=f_name, fill=(r, g, b))
        y += th(draw, name, f_name) + 6
        y = draw_wrap(draw, desc, f_desc, MARGIN + 8, y, W - MARGIN*2 - 8, INK, sp=1.4)
        y += 22

    img.save(os.path.join(OUT_DIR, "slide-05.png"))
    print("slide-05.png saved")

def slide_06():
    img, draw = new_canvas(LINEN)
    slide_label(draw, 6, 8)
    f_head = dmsans(40, bold=True)
    f_name = dmsans(24, bold=True)
    f_desc = dmsans(22)

    r, g, b = hex_to_rgb(INK)
    y = 90
    draw.text((MARGIN, y), "The rest of the formula.", font=f_head, fill=(r, g, b))
    y += th(draw, "X", f_head) + 20
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(r, g, b, 80), width=1)
    y += 24

    ingrs = [
        ("Dimethicone", "Silicone emollient. Improves texture, mild occlusive effect."),
        ("Cetearyl Alcohol / Ceteareth-20", "Fatty alcohol emulsifier pair. Stable emulsion system."),
        ("Sodium Lauroyl Lactylate", "Emulsifier with mild skin-conditioning effect."),
        ("Phenoxyethanol", "Preservative. Industry standard."),
    ]
    for name, desc in ingrs:
        draw.text((MARGIN, y), name, font=f_name, fill=(r, g, b))
        y += th(draw, name, f_name) + 6
        y = draw_wrap(draw, desc, f_desc, MARGIN + 8, y, W - MARGIN*2 - 8, INK, sp=1.4)
        y += 18
    y += 10
    note = "No fragrance. No alcohol denat. No known irritants at listed concentrations."
    draw_wrap(draw, note, dmsans(22), MARGIN, y, W - MARGIN*2, INK, sp=1.4)

    img.save(os.path.join(OUT_DIR, "slide-06.png"))
    print("slide-06.png saved")

def slide_07():
    img, draw = new_canvas(LAB_SAGE)
    slide_label(draw, 7, 8)
    f_verdict = dmsans(64, bold=True)
    f_caveat  = dmsans(28)
    f_score   = dmsans(44, bold=True)
    f_body    = dmsans(22)

    r, g, b = hex_to_rgb(INK)
    y = 100
    verdict = "WORTH IT"
    draw.text((cx(draw, verdict, f_verdict), y), verdict, font=f_verdict, fill=(r, g, b))
    y += th(draw, verdict, f_verdict) + 10

    caveat = "WITH ONE CAVEAT"
    draw.text((cx(draw, caveat, f_caveat), y), caveat, font=f_caveat, fill=(r, g, b, 200))
    y += th(draw, caveat, f_caveat) + 16

    score = "8 / 10"
    draw.text((cx(draw, score, f_score), y), score, font=f_score, fill=(r, g, b))
    y += th(draw, score, f_score) + 24

    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(r, g, b, 100), width=1)
    y += 24

    body = (
        "The ceramide system is credible. Multi-ceramide + cholesterol + phytosphingosine with MVE technology is the real product achievement. "
        "No fragrance. Non-comedogenic. Effective humectant stack.\n\n"
        "The caveat: SPF 25 is below the SPF 30-50 range recommended for summer facial use when UV index is above 3. "
        "Best as a year-round daily moisturiser. For active summer days, layer SPF 50 over the top."
    )
    for para in body.split("\n\n"):
        y = draw_wrap(draw, para, f_body, MARGIN, y, W - MARGIN*2, INK, sp=1.5)
        y += 16

    img.save(os.path.join(OUT_DIR, "slide-07.png"))
    print("slide-07.png saved")

def slide_08():
    img, draw = new_canvas(BONE)
    f_head  = dmsans(40, bold=True)
    f_sub   = dmsans(28)
    f_body  = dmsans(24)
    f_small = dmsans(18)

    r, g, b = hex_to_rgb(INK)
    lines = [("The Label.", f_head, 255),
             ("Every formula, decoded.", f_sub, 178),
             ("", None, 0),
             ("We read the INCI so you don't have to.", f_body, 153),
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
