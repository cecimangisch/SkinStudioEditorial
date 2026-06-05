"""
Slide generator — 02 · Zinc Oxide, Exactly.
Ingredient School · 9 Slides
Campaign: The Summer Formula · July 2026
"""

from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/tmp/slidefonts"

# Brand palette
BONE      = "#F5F0E8"
INK       = "#1A1A18"
LAB_SAGE  = "#BBD1C6"
LAB_MIST  = "#DAE9DF"
LAB_FROST = "#ECF0EE"
LINEN     = "#F1EAE1"
CLOUD     = "#FAFAFA"
PETAL     = "#E6D2D0"

W, H = 1080, 1080
MARGIN = 80

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def load_font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
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

def new_canvas(bg_hex):
    img = Image.new("RGB", (W, H), hex_to_rgb(bg_hex))
    return img, ImageDraw.Draw(img)

def text_h(draw, text, font):
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[3] - bb[1]

def text_w(draw, text, font):
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0]

def centered_x(draw, text, font):
    return (W - text_w(draw, text, font)) // 2

def wrap_text(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        test = (cur + " " + word).strip()
        if text_w(draw, test, font) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def draw_wrapped(draw, text, font, x, y, max_w, color, spacing=1.5):
    lines = wrap_text(draw, text, font, max_w)
    lh = text_h(draw, "Ag", font)
    for line in lines:
        draw.text((x, y), line, font=font, fill=hex_to_rgb(color))
        y += int(lh * spacing)
    return y

def alpha_text(img, draw, text, font, x, y, color_hex, opacity):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    r, g, b = hex_to_rgb(color_hex)
    d.text((x, y), text, font=font, fill=(r, g, b, opacity))
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    return img.convert("RGB"), ImageDraw.Draw(img.convert("RGB"))

def slide_label(draw, n, total, bg_is_dark=False):
    color = BONE if bg_is_dark else INK
    f = dmsans(16)
    label = f"{n:02d} / {total:02d}"
    tw = text_w(draw, label, f)
    r, g, b = hex_to_rgb(color)
    # Use direct draw at reduced opacity via overlay later
    draw.text((W - MARGIN - tw, 40), label, font=f, fill=(r, g, b, 100))

def rule(draw, y, color=INK, opacity=100):
    r, g, b = hex_to_rgb(color)
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(r, g, b), width=1)
    return y + 1

# ── SLIDE 1 ────────────────────────────────────────────────────────────────────
def slide_01():
    img, draw = new_canvas(BONE)
    f_title = fraunces(80)
    f_sub   = dmsans(26)
    f_small = dmsans(20)

    title1 = "Zinc Oxide,"
    title2 = "Exactly."
    sub    = "The UV filter that works across the entire spectrum—and why that matters more than you think."
    label  = "Ingredient School · @skinlabeditorial"

    h1 = text_h(draw, title1, f_title)
    h2 = text_h(draw, title2, f_title)

    block_start = int(H * 0.28)
    y = block_start
    draw.text((centered_x(draw, title1, f_title), y), title1, font=f_title, fill=hex_to_rgb(INK))
    y += h1 + 8
    draw.text((centered_x(draw, title2, f_title), y), title2, font=f_title, fill=hex_to_rgb(INK))
    y += h2 + 52

    sub_lines = wrap_text(draw, sub, f_sub, 720)
    lh = text_h(draw, "Ag", f_sub)
    for line in sub_lines:
        tx = centered_x(draw, line, f_sub)
        r, g, b = hex_to_rgb(INK)
        draw.text((tx, y), line, font=f_sub, fill=(r, g, b, 191))
        y += int(lh * 1.5)

    y += 50
    lbl_x = centered_x(draw, label, f_small)
    r, g, b = hex_to_rgb(INK)
    draw.text((lbl_x, y), label, font=f_small, fill=(r, g, b, 115))

    img.save(os.path.join(OUT_DIR, "slide-01.png"))
    print("slide-01.png saved")

# ── SLIDE 2 ────────────────────────────────────────────────────────────────────
def slide_02():
    img, draw = new_canvas(LAB_MIST)
    f_head = dmsans(40, bold=True)
    f_body = dmsans(24)
    f_tag  = dmsans(20, bold=True)
    f_lbl  = dmsans(16)

    # section label
    label = "02 / 09"
    r, g, b = hex_to_rgb(INK)
    draw.text((W - MARGIN - text_w(draw, label, f_lbl), 40), label, font=f_lbl, fill=(r, g, b, 102))

    y = 90
    draw.text((MARGIN, y), "What it is.", font=f_head, fill=hex_to_rgb(INK))
    y += text_h(draw, "What it is.", f_head) + 20
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(*hex_to_rgb(INK), 102), width=1)
    y += 28

    body = (
        "Zinc oxide (ZnO) is an inorganic mineral compound. In sunscreen formulations, "
        "it functions as a UV filter — a substance that attenuates UV radiation before it "
        "reaches viable skin cells.\n\n"
        "It appears as a white powder in raw form. In modern sunscreens, it is micronised "
        "or nano-sized to reduce visible whitening on skin. Both particle sizes provide "
        "equivalent UV protection."
    )
    for para in body.split("\n\n"):
        y = draw_wrapped(draw, para, f_body, MARGIN, y, W - MARGIN*2, INK, spacing=1.5)
        y += 20

    # INCI pill
    inci = "INCI: Zinc Oxide"
    pw = text_w(draw, inci, f_tag) + 32
    ph = text_h(draw, inci, f_tag) + 20
    draw.rounded_rectangle([MARGIN, y, MARGIN + pw, y + ph], radius=8, fill=hex_to_rgb(INK))
    draw.text((MARGIN + 16, y + 10), inci, font=f_tag, fill=hex_to_rgb(BONE))

    img.save(os.path.join(OUT_DIR, "slide-02.png"))
    print("slide-02.png saved")

# ── SLIDE 3 ────────────────────────────────────────────────────────────────────
def slide_03():
    img, draw = new_canvas(BONE)
    f_head = dmsans(40, bold=True)
    f_body = dmsans(24)
    f_lbl  = dmsans(16)

    label = "03 / 09"
    r, g, b = hex_to_rgb(INK)
    draw.text((W - MARGIN - text_w(draw, label, f_lbl), 40), label, font=f_lbl, fill=(r, g, b, 102))

    y = 90
    draw.text((MARGIN, y), "How it works.", font=f_head, fill=hex_to_rgb(INK))
    y += text_h(draw, "How it works.", f_head) + 20
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(*hex_to_rgb(INK), 102), width=1)
    y += 28

    paras = [
        "Zinc oxide works via two mechanisms simultaneously: it reflects UV radiation and it absorbs it.",
        "The absorption mechanism is dominant. ZnO absorbs photons of UV energy and converts them into small amounts of heat — a process that occurs at the particle surface.",
        "This conversion does not generate the reactive intermediates that some organic filters produce. The molecule does not degrade in the process.",
        "This is what photostability means in practice: the filter works at hour one and hour six at the same efficacy.",
    ]
    for para in paras:
        y = draw_wrapped(draw, para, f_body, MARGIN, y, W - MARGIN*2, INK, spacing=1.5)
        y += 22

    img.save(os.path.join(OUT_DIR, "slide-03.png"))
    print("slide-03.png saved")

# ── SLIDE 4 ────────────────────────────────────────────────────────────────────
def slide_04():
    img, draw = new_canvas(INK)
    f_head = dmsans(40, bold=True)
    f_row  = dmsans(26)
    f_note = dmsans(22)
    f_lbl  = dmsans(16)

    label = "04 / 09"
    r, g, b = hex_to_rgb(BONE)
    draw.text((W - MARGIN - text_w(draw, label, f_lbl), 40), label, font=f_lbl, fill=(r, g, b, 102))

    y = 90
    draw.text((MARGIN, y), "What it covers.", font=f_head, fill=hex_to_rgb(BONE))
    y += text_h(draw, "What it covers.", f_head) + 20
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(*hex_to_rgb(LAB_SAGE), 200), width=1)
    y += 36

    rows = [
        ("UVB  (290–320 nm)", "effective attenuation"),
        ("UVA2 (320–340 nm)", "effective attenuation"),
        ("UVA1 (340–400 nm)", "effective attenuation"),
    ]
    for r_label, r_val in rows:
        row = f"{r_label}   ·   {r_val}"
        draw.text((MARGIN, y), row, font=f_row, fill=hex_to_rgb(BONE))
        y += text_h(draw, row, f_row) + 18
    y += 20

    note = "Zinc oxide is the only single UV filter approved in the EU and US that covers the full UV spectrum on its own without additional stabilisers."
    y = draw_wrapped(draw, note, f_note, MARGIN, y, W - MARGIN*2, BONE, spacing=1.5)

    img.save(os.path.join(OUT_DIR, "slide-04.png"))
    print("slide-04.png saved")

# ── SLIDE 5 ────────────────────────────────────────────────────────────────────
def slide_05():
    img, draw = new_canvas(LAB_FROST)
    f_head = dmsans(40, bold=True)
    f_body = dmsans(24)
    f_lbl  = dmsans(16)

    label = "05 / 09"
    r, g, b = hex_to_rgb(INK)
    draw.text((W - MARGIN - text_w(draw, label, f_lbl), 40), label, font=f_lbl, fill=(r, g, b, 102))

    y = 90
    draw.text((MARGIN, y), "Why stability matters.", font=f_head, fill=hex_to_rgb(INK))
    y += text_h(draw, "Why stability matters.", f_head) + 20
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(*hex_to_rgb(INK), 80), width=1)
    y += 28

    paras = [
        "A UV filter that degrades under sunlight provides less protection over time — even without reapplication.",
        "Zinc oxide does not meaningfully degrade under UV exposure. Its crystal structure absorbs and dissipates energy without breaking down.",
        "By contrast: avobenzone degrades by approximately 50% after one hour of UV exposure without photostabilisers. Many formulations pair avobenzone with octocrylene or Tinosorb S specifically to address this.",
        "Zinc oxide requires no stabiliser partner.",
    ]
    for para in paras:
        y = draw_wrapped(draw, para, f_body, MARGIN, y, W - MARGIN*2, INK, spacing=1.5)
        y += 22

    img.save(os.path.join(OUT_DIR, "slide-05.png"))
    print("slide-05.png saved")

# ── SLIDE 6 ────────────────────────────────────────────────────────────────────
def slide_06():
    img, draw = new_canvas(LINEN)
    f_head = dmsans(38, bold=True)
    f_body = dmsans(24)
    f_lbl  = dmsans(16)

    label = "06 / 09"
    r, g, b = hex_to_rgb(INK)
    draw.text((W - MARGIN - text_w(draw, label, f_lbl), 40), label, font=f_lbl, fill=(r, g, b, 102))

    y = 90
    draw.text((MARGIN, y), "Why sensitive skin tolerates it.", font=f_head, fill=hex_to_rgb(INK))
    y += text_h(draw, "Why sensitive skin tolerates it.", f_head) + 20
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(*hex_to_rgb(INK), 80), width=1)
    y += 28

    paras = [
        "Zinc oxide has a secondary anti-inflammatory effect. It moderates the activity of mast cells and inhibits certain pro-inflammatory cytokines.",
        "This is not incidental — it is why zinc oxide appears in wound-care formulations and why dermatologists recommend mineral sunscreens for rosacea, post-procedure skin, and acne-prone presentations.",
        "In standard particle sizes, zinc oxide does not penetrate beyond the stratum corneum. No systemic absorption has been demonstrated at routine use concentrations.",
    ]
    for para in paras:
        y = draw_wrapped(draw, para, f_body, MARGIN, y, W - MARGIN*2, INK, spacing=1.5)
        y += 22

    img.save(os.path.join(OUT_DIR, "slide-06.png"))
    print("slide-06.png saved")

# ── SLIDE 7 ────────────────────────────────────────────────────────────────────
def slide_07():
    img, draw = new_canvas(BONE)
    f_head    = dmsans(38, bold=True)
    f_body    = dmsans(24)
    f_big_num = dmsans(72, bold=True)
    f_sub_num = dmsans(22)
    f_lbl     = dmsans(16)

    label = "07 / 09"
    r, g, b = hex_to_rgb(INK)
    draw.text((W - MARGIN - text_w(draw, label, f_lbl), 40), label, font=f_lbl, fill=(r, g, b, 102))

    y = 90
    draw.text((MARGIN, y), "Concentration in formulations.", font=f_head, fill=hex_to_rgb(INK))
    y += text_h(draw, "Concentration in formulations.", f_head) + 20
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(*hex_to_rgb(INK), 80), width=1)
    y += 28

    # Callout box
    num = "15–22%"
    sub = "typical concentration range"
    bw = 400
    bh = text_h(draw, num, f_big_num) + text_h(draw, sub, f_sub_num) + 52
    draw.rounded_rectangle([MARGIN, y, MARGIN + bw, y + bh], radius=8, fill=hex_to_rgb(LAB_MIST))
    draw.text((MARGIN + 20, y + 16), num, font=f_big_num, fill=hex_to_rgb(INK))
    draw.text((MARGIN + 20, y + 16 + text_h(draw, num, f_big_num) + 8), sub, font=f_sub_num, fill=(*hex_to_rgb(INK), 153))
    y += bh + 28

    paras = [
        "EU regulation permits zinc oxide as a UV filter at concentrations up to 25%.",
        "Higher concentrations increase SPF but also increase whitening and texture weight. Particle size reduction (micronised/nano ZnO) improves aesthetics without reducing efficacy.",
    ]
    for para in paras:
        y = draw_wrapped(draw, para, f_body, MARGIN, y, W - MARGIN*2, INK, spacing=1.5)
        y += 20

    img.save(os.path.join(OUT_DIR, "slide-07.png"))
    print("slide-07.png saved")

# ── SLIDE 8 ────────────────────────────────────────────────────────────────────
def slide_08():
    img, draw = new_canvas(INK)
    f_head = dmsans(44, bold=True)
    f_body = dmsans(24)
    f_lbl  = dmsans(16)

    label = "08 / 09"
    r, g, b = hex_to_rgb(BONE)
    draw.text((W - MARGIN - text_w(draw, label, f_lbl), 40), label, font=f_lbl, fill=(r, g, b, 102))

    y = 90
    draw.text((MARGIN, y), "The takeaway.", font=f_head, fill=hex_to_rgb(BONE))
    y += text_h(draw, "The takeaway.", f_head) + 20
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(*hex_to_rgb(LAB_SAGE), 180), width=1)
    y += 28

    paras = [
        "Zinc oxide is not simply 'safer' than chemical filters. That framing misses the point.",
        "It is a photostable, broad-spectrum UV filter with a secondary anti-inflammatory effect and a strong safety record at standard concentrations. It is the only single filter that covers the full UV spectrum without additional stabilisers.",
        "Its drawbacks are aesthetic, not functional: whitening, texture, difficulty blending on dark skin tones. Those are formulation problems. Not safety trade-offs.",
        "Understanding the difference matters.",
    ]
    for para in paras:
        y = draw_wrapped(draw, para, f_body, MARGIN, y, W - MARGIN*2, BONE, spacing=1.5)
        y += 22

    img.save(os.path.join(OUT_DIR, "slide-08.png"))
    print("slide-08.png saved")

# ── SLIDE 9 ────────────────────────────────────────────────────────────────────
def slide_09():
    img, draw = new_canvas(LAB_MIST)
    f_head  = dmsans(36, bold=True)
    f_sub   = dmsans(28)
    f_body  = dmsans(24)
    f_small = dmsans(22)

    texts = [
        ("Ingredient School.", f_head, INK, 255),
        ("One ingredient. The complete picture.", f_sub, INK, 204),
        ("", None, None, 0),
        ("Every week at @skinlabeditorial", f_body, INK, 255),
        ("", None, None, 0),
        ("Ingredients, decoded.", f_small, INK, 153),
    ]

    total_h = 0
    line_heights = []
    for text, font, color, _ in texts:
        if text and font:
            lh = text_h(draw, text, font)
        else:
            lh = 32
        line_heights.append(lh)
        total_h += lh + 18

    y = (H - total_h) // 2
    for i, (text, font, color, opacity) in enumerate(texts):
        if text and font:
            tx = centered_x(draw, text, font)
            r2, g2, b2 = hex_to_rgb(color)
            draw.text((tx, y), text, font=font, fill=(r2, g2, b2, opacity))
        y += line_heights[i] + 18

    img.save(os.path.join(OUT_DIR, "slide-09.png"))
    print("slide-09.png saved")

# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    slide_01()
    slide_02()
    slide_03()
    slide_04()
    slide_05()
    slide_06()
    slide_07()
    slide_08()
    slide_09()
    print("Done — 9 slides generated.")
