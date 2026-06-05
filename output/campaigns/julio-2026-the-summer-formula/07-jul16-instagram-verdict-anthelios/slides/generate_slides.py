"""
Slide generator — 07 · The Verdict: La Roche-Posay Anthelios Invisible Fluid SPF 50+
The Verdict · 10 Slides
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

def body_slide(bg, n, headline, paras, txt=INK, rule_col=INK, lbl_col=None):
    if lbl_col is None: lbl_col = txt
    img, draw = new_canvas(bg)
    slide_label(draw, n, 10, color=lbl_col)
    f_head = dmsans(38, bold=True)
    f_body = dmsans(23)
    y = 90
    r, g, b = hex_to_rgb(txt)
    draw.text((MARGIN, y), headline, font=f_head, fill=(r, g, b))
    y += th(draw, headline, f_head) + 20
    y = hr(draw, y, rule_col, 100)
    for para in paras:
        y = draw_wrap(draw, para, f_body, MARGIN, y, W - MARGIN*2, txt, sp=1.5)
        y += 18
    return img

def ingr_slide(bg, n, headline, ingredients, txt=INK, rule_col=INK, lbl_col=None):
    if lbl_col is None: lbl_col = txt
    img, draw = new_canvas(bg)
    slide_label(draw, n, 10, color=lbl_col)
    f_head = dmsans(38, bold=True)
    f_name = dmsans(24, bold=True)
    f_desc = dmsans(22)

    y = 90
    r, g, b = hex_to_rgb(txt)
    draw.text((MARGIN, y), headline, font=f_head, fill=(r, g, b))
    y += th(draw, headline, f_head) + 20
    rr, rg, rb = hex_to_rgb(rule_col)
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(rr, rg, rb, 150), width=1)
    y += 24

    for name, desc in ingredients:
        draw.text((MARGIN, y), name, font=f_name, fill=(r, g, b))
        y += th(draw, name, f_name) + 6
        y = draw_wrap(draw, desc, f_desc, MARGIN + 8, y, W - MARGIN*2 - 8, txt, sp=1.35)
        y += 18

    return img

def slide_01():
    img, draw = new_canvas(INK)
    f_fr   = fraunces(52)
    f_big  = dmsans(44, bold=True)
    f_sub  = dmsans(22)
    f_sm   = dmsans(18)

    r, g, b = hex_to_rgb(BONE)
    y = 110
    verdict = "The Verdict:"
    draw.text((cx(draw, verdict, f_fr), y), verdict, font=f_fr, fill=(r, g, b))
    y += th(draw, verdict, f_fr) + 28

    for line in ["La Roche-Posay", "Anthelios Invisible", "Fluid SPF 50+"]:
        draw.text((cx(draw, line, f_big), y), line, font=f_big, fill=(r, g, b))
        y += th(draw, line, f_big) + 8
    y += 48

    sub = "The most recommended sunscreen in dermatology circles. Here is why—and where it falls short."
    for wl in wrap(draw, sub, f_sub, 740):
        draw.text((cx(draw, wl, f_sub), y), wl, font=f_sub, fill=(r, g, b, 165))
        y += th(draw, wl, f_sub) + 10

    handle = "@skinlabeditorial"
    draw.text((W - MARGIN - tw(draw, handle, f_sm), H - 50),
              handle, font=f_sm, fill=(r, g, b, 115))

    img.save(os.path.join(OUT_DIR, "slide-01.png"))
    print("slide-01.png saved")

def slide_02():
    paras = [
        "Texture: fluid, low-viscosity. Applies like water with slight slip. No drag. No white cast. No perceptible scent.",
        "Finish: skin-identical. Disappears within 30 seconds of application. Suitable under makeup without pilling.",
        "Application: the 2mg/cm² standard is achievable without the effort required by most mineral SPFs. Proper dosing is more likely — which directly improves real-world SPF performance.",
        "Assessment: the texture does what dermatologists mean when they say 'a sunscreen you will actually use.'",
    ]
    img = body_slide(BONE, 2, "First impression.", paras)
    img.save(os.path.join(OUT_DIR, "slide-02.png"))
    print("slide-02.png saved")

def slide_03():
    paras = [
        "On normal-to-dry skin: adds slight luminosity. No tightening. No film.",
        "On oily skin: mild oil-control effect. Some users report slight greasiness in high-humidity conditions.",
        "On dark skin tones: invisible. No ash, no cast. This is the primary aesthetic advantage over mineral formulas.",
        "On acne-prone skin: non-comedogenic per clinical testing. Octocrylene is present — a low-level sensitiser for some. Patch test recommended.",
    ]
    img = body_slide(LAB_FROST, 3, "On skin.", paras)
    img.save(os.path.join(OUT_DIR, "slide-03.png"))
    print("slide-03.png saved")

def slide_04():
    paras = [
        "The formula's fluid consistency makes first application easy. Reapplication over makeup is the harder problem — applicable to all SPFs, not specific to Anthelios.",
        "At 50ml for €45: at proper outdoor use (face + décolletage, 2mg/cm², twice daily), a 50ml bottle lasts approximately 10 days of heavy use.",
        "This is not a criticism of the product. It is a real cost consideration that changes the value calculation for high-use summer scenarios.",
    ]
    img = body_slide(LINEN, 4, "The reapplication problem.", paras)
    img.save(os.path.join(OUT_DIR, "slide-04.png"))
    print("slide-04.png saved")

def slide_05():
    ingr = [
        ("Mexoryl SX (ecamsule)", "L'Oréal-patented. Photostable. Covers UVA1 and UVA2. One of the most effective single UVA filters available."),
        ("Mexoryl XL (drometrizole trisiloxane)", "Hybrid filter: covers both UVA and UVB. Oil-soluble. Photostable."),
        ("Tinosorb S", "Broad-spectrum, photostable. Stabilises avobenzone in the same formulation."),
        ("Avobenzone", "UVA1 filter. Photounstable alone — stabilised here by Tinosorb S."),
    ]
    img = ingr_slide(INK, 5, "The UV filters.", ingr, txt=BONE, rule_col=LAB_SAGE, lbl_col=BONE)
    img.save(os.path.join(OUT_DIR, "slide-05.png"))
    print("slide-05.png saved")

def slide_06():
    ingr = [
        ("Glycerin", "Humectant. Standard and effective."),
        ("Dimethicone / Cyclopentasiloxane", "Silicone emollients providing the invisible texture. Non-comedogenic."),
        ("Tocopherol", "Vitamin E. Antioxidant. Minor protective benefit against UV-induced oxidative stress."),
        ("Phenoxyethanol / Methylparaben", "Preservative system. Methylparaben within EU safe concentration limits."),
    ]
    img = ingr_slide(LAB_MIST, 6, "The base.", ingr)
    img.save(os.path.join(OUT_DIR, "slide-06.png"))
    print("slide-06.png saved")

def slide_07():
    paras = [
        "The Mexoryl SX + XL + Tinosorb S combination achieves comprehensive, photostable UVA1 coverage without aesthetic trade-offs.",
        "Most SPFs that adequately cover UVA1 use mineral filters (zinc oxide) — with whitening and texture as the trade-off. Anthelios achieves equivalent UVA1 coverage with a texture that disappears on skin.",
        "This is the formulation achievement. It is real, it is patented, and it is why this product appears repeatedly in dermatologist recommendations.",
    ]
    img = body_slide(BONE, 7, "What the formula does well.", paras)
    img.save(os.path.join(OUT_DIR, "slide-07.png"))
    print("slide-07.png saved")

def slide_08():
    img, draw = new_canvas(LAB_FROST)
    slide_label(draw, 8, 10)
    f_head  = dmsans(38, bold=True)
    f_label = dmsans(24, bold=True)
    f_item  = dmsans(23)

    y = 90
    r, g, b = hex_to_rgb(INK)
    draw.text((MARGIN, y), "Who it is for.", font=f_head, fill=(r, g, b))
    y += th(draw, "X", f_head) + 20
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(r, g, b, 100), width=1)
    y += 24

    draw.text((MARGIN, y), "Suited for:", font=f_label, fill=(r, g, b))
    y += th(draw, "X", f_label) + 12
    for item in ["Daily facial SPF for all skin tones",
                 "Under makeup (fluid, no pilling)",
                 "Oily skin in moderate conditions",
                 "Anyone who under-applies due to texture"]:
        draw.rectangle([MARGIN, y + 6, MARGIN + 12, y + 18], fill=hex_to_rgb(LAB_SAGE))
        draw.text((MARGIN + 22, y), item, font=f_item, fill=(r, g, b))
        y += th(draw, item, f_item) + 14
    y += 16

    draw.text((MARGIN, y), "Not ideal for:", font=f_label, fill=(r, g, b))
    y += th(draw, "X", f_label) + 12
    for item in ["Budget-restricted daily users (cost per application is significant)",
                 "Anyone with octocrylene sensitivity",
                 "Full-body summer application (volume cost)",
                 "Individuals who prefer paraben-free formulations"]:
        draw.rectangle([MARGIN, y + 6, MARGIN + 12, y + 18], fill=hex_to_rgb(PETAL))
        draw.text((MARGIN + 22, y), item, font=f_item, fill=(r, g, b))
        y += th(draw, item, f_item) + 14

    img.save(os.path.join(OUT_DIR, "slide-08.png"))
    print("slide-08.png saved")

def slide_09():
    img, draw = new_canvas(INK)
    slide_label(draw, 9, 10, color=BONE)
    f_head  = dmsans(36, bold=True)
    f_score = dmsans(96, bold=True)
    f_row   = dmsans(20)

    r, g, b = hex_to_rgb(BONE)
    y = 70
    draw.text((MARGIN, y), "Lab Score.", font=f_head, fill=(r, g, b))
    y += th(draw, "Lab Score.", f_head) + 20
    rr, rg, rb = hex_to_rgb(LAB_SAGE)
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(rr, rg, rb, 200), width=1)
    y += 28

    score = "9.2 / 10"
    draw.text((cx(draw, score, f_score), y), score, font=f_score, fill=(r, g, b))
    y += th(draw, score, f_score) + 36

    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(rr, rg, rb, 100), width=1)
    y += 24

    rows = [
        ("UV filter system", "10 / 10"),
        ("Photostability", "10 / 10"),
        ("Texture / aesthetics", "9 / 10"),
        ("Ingredient quality", "8.5 / 10"),
        ("Value for money", "7.5 / 10"),
        ("Accessibility", "7 / 10"),
    ]
    for label, val in rows:
        draw.text((MARGIN, y), label, font=f_row, fill=(r, g, b, 178))
        draw.text((W - MARGIN - tw(draw, val, f_row), y), val, font=f_row, fill=(r, g, b, 178))
        y += th(draw, label, f_row) + 14

    img.save(os.path.join(OUT_DIR, "slide-09.png"))
    print("slide-09.png saved")

def slide_10():
    img, draw = new_canvas(BONE)
    f_head  = dmsans(40, bold=True)
    f_sub   = dmsans(28)
    f_body  = dmsans(24)
    f_small = dmsans(18)

    lines = [
        ("The Verdict.", f_head, INK, 255),
        ("Every formula, evidence-based.", f_sub, INK, 178),
        ("", None, None, 0),
        ("Questions about the formulation?", f_body, INK, 153),
        ("Leave them below.", f_body, INK, 153),
        ("", None, None, 0),
        ("@skinlabeditorial", f_body, INK, 200),
        ("Ingredients, decoded.", f_small, INK, 115),
    ]
    lhs = [th(draw, t or "X", fn or f_small) for t, fn, _, _ in lines]
    total = sum(lhs) + 14 * len(lines)
    y = (H - total) // 2

    for i, (text, font, color, opacity) in enumerate(lines):
        if text and font:
            r2, g2, b2 = hex_to_rgb(color)
            draw.text((cx(draw, text, font), y), text, font=font, fill=(r2, g2, b2, opacity))
        y += lhs[i] + 14

    img.save(os.path.join(OUT_DIR, "slide-10.png"))
    print("slide-10.png saved")

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    for fn in [slide_01,slide_02,slide_03,slide_04,slide_05,slide_06,
               slide_07,slide_08,slide_09,slide_10]:
        fn()
    print("Done — 10 slides generated.")
