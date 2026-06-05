"""
Slide generator — 08 · Ceramides, Exactly.
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

def body_slide(bg, n, headline, paras, txt=INK, rule_col=INK, lbl_col=None):
    if lbl_col is None: lbl_col = txt
    img, draw = new_canvas(bg)
    slide_label(draw, n, 9, color=lbl_col)
    f_head = dmsans(40, bold=True)
    f_body = dmsans(24)
    y = 90
    r, g, b = hex_to_rgb(txt)
    draw.text((MARGIN, y), headline, font=f_head, fill=(r, g, b))
    y += th(draw, headline, f_head) + 20
    rr, rg, rb = hex_to_rgb(rule_col)
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(rr, rg, rb, 110), width=1)
    y += 28
    for para in paras:
        y = draw_wrap(draw, para, f_body, MARGIN, y, W - MARGIN*2, txt, sp=1.5)
        y += 20
    return img

def slide_01():
    img, draw = new_canvas(LINEN)
    f_title = fraunces(80)
    f_sub   = dmsans(26)
    f_small = dmsans(20)

    y = int(H * 0.26)
    r, g, b = hex_to_rgb(INK)
    for title in ["Ceramides,", "Exactly."]:
        draw.text((cx(draw, title, f_title), y), title, font=f_title, fill=(r, g, b))
        y += th(draw, title, f_title) + 8
    y += 52

    sub = "They are not a moisturising ingredient. They are a structural one."
    for line in wrap(draw, sub, f_sub, 720):
        draw.text((cx(draw, line, f_sub), y), line, font=f_sub, fill=(r, g, b, 191))
        y += th(draw, line, f_sub) + 10
    y += 50

    label = "Ingredient School · @skinlabeditorial"
    draw.text((cx(draw, label, f_small), y), label, font=f_small, fill=(r, g, b, 115))

    img.save(os.path.join(OUT_DIR, "slide-01.png"))
    print("slide-01.png saved")

def slide_02():
    paras = [
        "Ceramides are a family of lipid molecules composed of a sphingosine base linked to a fatty acid chain. They are the dominant lipid class in the stratum corneum — approximately 50% of the lipid content by weight.",
        "They are produced by keratinocytes and secreted into the intercellular space, where they form the lamellar structures that create the skin's lipid bilayer.",
        "INCI names include: Ceramide NP, Ceramide AP, Ceramide EOP, Ceramide NS — among others. Different types have different structural roles.",
    ]
    img = body_slide(BONE, 2, "What they are.", paras)
    img.save(os.path.join(OUT_DIR, "slide-02.png"))
    print("slide-02.png saved")

def slide_03():
    img, draw = new_canvas(LAB_FROST)
    slide_label(draw, 3, 9)
    f_head = dmsans(40, bold=True)
    f_body = dmsans(24)

    y = 90
    r, g, b = hex_to_rgb(INK)
    draw.text((MARGIN, y), "How they function.", font=f_head, fill=(r, g, b))
    y += th(draw, "X", f_head) + 20
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(r, g, b, 110), width=1)
    y += 28

    intro = "The stratum corneum follows the 'brick and mortar' model: corneocytes are the bricks; ceramides, cholesterol, and fatty acids are the mortar. Ceramides provide structural cohesion, controlling:"
    y = draw_wrap(draw, intro, f_body, MARGIN, y, W - MARGIN*2, INK, sp=1.5)
    y += 16

    bullets = [
        "Water retention (preventing TEWL)",
        "Permeability to external agents",
        "Mechanical integrity of the surface barrier",
    ]
    for b_text in bullets:
        draw.rectangle([MARGIN, y + 7, MARGIN + 10, y + 17], fill=hex_to_rgb(LAB_SAGE))
        draw.text((MARGIN + 22, y), b_text, font=f_body, fill=(r, g, b))
        y += th(draw, b_text, f_body) + 14
    y += 16

    final = "Without adequate ceramide content, the lipid bilayer becomes disordered — more permeable to both water loss and irritants."
    draw_wrap(draw, final, f_body, MARGIN, y, W - MARGIN*2, INK, sp=1.5)

    img.save(os.path.join(OUT_DIR, "slide-03.png"))
    print("slide-03.png saved")

def slide_04():
    img, draw = new_canvas(INK)
    slide_label(draw, 4, 9, color=BONE)
    f_head = dmsans(38, bold=True)
    f_name = dmsans(24, bold=True)
    f_desc = dmsans(22)

    y = 90
    r, g, b = hex_to_rgb(BONE)
    draw.text((MARGIN, y), "What summer does to ceramide levels.", font=f_head, fill=(r, g, b))
    y += th(draw, "X", f_head) + 20
    rr, rg, rb = hex_to_rgb(LAB_SAGE)
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(rr, rg, rb, 180), width=1)
    y += 28

    factors = [
        ("UV radiation:", "UV exposure induces ceramidase activity — an enzyme that degrades ceramides. Cumulative UV exposure measurably reduces ceramide levels over time."),
        ("Surfactant exposure:", "Increased sweating leads to more cleansing. Surfactants in cleansers extract ceramides from the lipid bilayer directly."),
        ("Heat:", "Elevated temperature increases enzymatic ceramide degradation rate. High humidity does not compensate."),
    ]
    for name, desc in factors:
        draw.text((MARGIN, y), name, font=f_name, fill=(r, g, b))
        y += th(draw, name, f_name) + 6
        y = draw_wrap(draw, desc, f_desc, MARGIN + 8, y, W - MARGIN*2 - 8, BONE, sp=1.4)
        y += 20

    img.save(os.path.join(OUT_DIR, "slide-04.png"))
    print("slide-04.png saved")

def slide_05():
    img, draw = new_canvas(LAB_MIST)
    slide_label(draw, 5, 9)
    f_head = dmsans(40, bold=True)
    f_name = dmsans(24, bold=True)
    f_desc = dmsans(22)

    y = 90
    r, g, b = hex_to_rgb(INK)
    draw.text((MARGIN, y), "The ceramide family.", font=f_head, fill=(r, g, b))
    y += th(draw, "X", f_head) + 20
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(r, g, b, 110), width=1)
    y += 28

    intro = "At least 12 ceramide subtypes exist in human skin. Most commonly used in formulations:"
    y = draw_wrap(draw, intro, f_desc, MARGIN, y, W - MARGIN*2, INK, sp=1.5)
    y += 16

    types = [
        ("Ceramide NP (2)", "One of the most abundant in skin. Important for barrier integrity."),
        ("Ceramide AP (6-II)", "Involved in lamellar body structure."),
        ("Ceramide EOP (1)", "Long-chain. Critical for lipid bilayer arrangement."),
        ("Ceramide NS (3)", "Water-binding properties in intercellular space."),
    ]
    for name, desc in types:
        draw.text((MARGIN, y), name, font=f_name, fill=(r, g, b))
        y += th(draw, name, f_name) + 4
        y = draw_wrap(draw, desc, f_desc, MARGIN + 8, y, W - MARGIN*2 - 8, INK, sp=1.35)
        y += 16

    img.save(os.path.join(OUT_DIR, "slide-05.png"))
    print("slide-05.png saved")

def slide_06():
    paras = [
        "Topical ceramides do not integrate into the lipid bilayer identically to endogenous ceramides.",
        "What they do: act as a reservoir in the upper stratum corneum from which ceramides can be incorporated into intercellular lipid spaces over time. They also reduce TEWL through occlusive and semi-occlusive effects.",
        "Clinical evidence shows measurable improvement in barrier function (TEWL reduction) and stratum corneum ceramide content after consistent use of ceramide-containing formulations over 2–4 weeks.",
        "The effect is real. The mechanism is partly indirect.",
    ]
    img = body_slide(BONE, 6, "What topical ceramides actually do.", paras)
    img.save(os.path.join(OUT_DIR, "slide-06.png"))
    print("slide-06.png saved")

def slide_07():
    paras = [
        "Effective ceramide formulations combine ceramides with cholesterol and fatty acids — the three critical components of the intercellular lipid bilayer. Ratio matters: 1:1:1 to 3:1:1 (ceramide:cholesterol:fatty acid) is most effective for barrier restoration.",
        "Look for: multiple ceramide types (NP, AP, EOP), with cholesterol and fatty acids (stearic acid, linoleic acid) in the same formula.",
        "CeraVe is the best-known example of the multi-ceramide + cholesterol approach. The patented MVE technology provides sustained ceramide release rather than single-dose application.",
    ]
    img = body_slide(LAB_FROST, 7, "What to look for.", paras)
    img.save(os.path.join(OUT_DIR, "slide-07.png"))
    print("slide-07.png saved")

def slide_08():
    paras = [
        "Ceramides are not a moisturising ingredient in the traditional sense. They restore the architectural integrity of the stratum corneum — and that structural restoration is what reduces TEWL and improves hydration.",
        "In summer, when UV exposure and increased cleansing actively degrade ceramide levels, topical ceramides are among the most evidence-backed interventions available.",
        "Not because they are trending. Because the mechanism is clear and the clinical data supports it.",
    ]
    img = body_slide(INK, 8, "The takeaway.", paras, txt=BONE, rule_col=LAB_SAGE, lbl_col=BONE)
    f_head = dmsans(44, bold=True)
    _, draw = new_canvas(INK)  # just for size calc
    img.save(os.path.join(OUT_DIR, "slide-08.png"))
    print("slide-08.png saved")

def slide_09():
    img, draw = new_canvas(LINEN)
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
