"""
Slide generator — 01 · SPF Math
Open/Provocation · 2 Slides
Campaign: The Summer Formula · July 2026
"""

from PIL import Image, ImageDraw, ImageFont
import os

# ── Output directory ──────────────────────────────────────────────────────────
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Brand palette ─────────────────────────────────────────────────────────────
BONE     = "#F5F0E8"
INK      = "#1A1A18"
LAB_SAGE = "#BBD1C6"
LAB_MIST = "#DAE9DF"

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# ── Font paths ─────────────────────────────────────────────────────────────────
FONT_DIR = "/tmp/slidefonts"

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
    name = "DMSans-Bold.ttf" if bold else "DMSans-Regular.ttf"
    return load_font(name, size)

# ── Helpers ────────────────────────────────────────────────────────────────────
W, H = 1080, 1080

def new_canvas(bg_hex):
    img = Image.new("RGB", (W, H), hex_to_rgb(bg_hex))
    draw = ImageDraw.Draw(img)
    return img, draw

def centered_text(draw, text, font, y, color, max_width=None):
    """Draw text centered horizontally at y."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    draw.text((x, y), text, font=font, fill=hex_to_rgb(color))
    return bbox[3] - bbox[1]  # return height

def text_height(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[3] - bbox[1]

def wrap_text(text, font, draw, max_width):
    """Wrap text to fit within max_width pixels."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def draw_wrapped(draw, text, font, x, y, max_width, color, line_spacing=1.4):
    lines = wrap_text(text, font, draw, max_width)
    for line in lines:
        draw.text((x, y), line, font=font, fill=hex_to_rgb(color))
        bbox = draw.textbbox((0, 0), line, font=font)
        lh = bbox[3] - bbox[1]
        y += int(lh * line_spacing)
    return y

# ── Slide 1 ────────────────────────────────────────────────────────────────────
def slide_01():
    img, draw = new_canvas(BONE)

    f_dmsans_48 = dmsans(48)
    f_fraunces_72 = fraunces(72)
    f_dmsans_28 = dmsans(28)
    f_dmsans_20 = dmsans(20)

    # Measure total block height
    line1 = "SPF 50 doesn't mean"
    line2 = "twice the protection"
    line3 = "of SPF 25."
    line4 = "Here is what the number actually measures."

    h1 = text_height(draw, line1, f_dmsans_48)
    h2 = text_height(draw, line2, f_fraunces_72)
    h3 = text_height(draw, line3, f_dmsans_48)
    h4 = text_height(draw, line4, f_dmsans_28)

    gap_lines = 16
    gap_after = 60

    total = h1 + gap_lines + h2 + gap_lines + h3 + gap_after + h4
    start_y = int((H - total) * 0.45)

    y = start_y
    centered_text(draw, line1, f_dmsans_48, y, INK)
    y += h1 + gap_lines

    centered_text(draw, line2, f_fraunces_72, y, INK)
    y += h2 + gap_lines

    centered_text(draw, line3, f_dmsans_48, y, INK)
    y += h3 + gap_after

    # Sub-line at reduced opacity — draw with alpha via paste
    sub_color = (*hex_to_rgb(INK), 178)  # ~70% opacity
    img_sub = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d_sub = ImageDraw.Draw(img_sub)
    bbox = d_sub.textbbox((0, 0), line4, font=f_dmsans_28)
    tw = bbox[2] - bbox[0]
    d_sub.text(((W - tw) // 2, y), line4, font=f_dmsans_28, fill=sub_color)
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, img_sub)
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    # Handle
    handle = "@skinlabeditorial"
    handle_color = (*hex_to_rgb(INK), 128)
    img2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(img2)
    bbox_h = d2.textbbox((0, 0), handle, font=f_dmsans_20)
    tw_h = bbox_h[2] - bbox_h[0]
    d2.text((W - tw_h - 40, H - 50), handle, font=f_dmsans_20, fill=handle_color)
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, img2)
    img = img.convert("RGB")

    path = os.path.join(OUT_DIR, "slide-01.png")
    img.save(path)
    print(f"Saved {path}")

# ── Slide 2 ────────────────────────────────────────────────────────────────────
def slide_02():
    img, draw = new_canvas(INK)

    f_head = dmsans(38, bold=True)
    f_data = dmsans(26)
    f_formula = dmsans(22)
    f_body = dmsans(22)
    f_footer = dmsans(18)

    margin = 80
    body_width = 920

    y = 90

    # Headline
    draw.text((margin, y), "The SPF scale is not linear.", font=f_head, fill=hex_to_rgb(BONE))
    y += text_height(draw, "The SPF scale is not linear.", f_head) + 28

    # Rule
    draw.line([(margin, y), (W - margin, y)], fill=hex_to_rgb(LAB_SAGE), width=1)
    y += 28

    # Data rows
    data = [
        ("SPF 25", "96% UVB blocked"),
        ("SPF 50", "98% UVB blocked"),
        ("SPF 100", "99% UVB blocked"),
    ]
    for label, val in data:
        row_text = f"{label}  ·  {val}"
        draw.text((margin, y), row_text, font=f_data, fill=hex_to_rgb(BONE))
        y += text_height(draw, row_text, f_data) + 14
    y += 20

    # Formula box
    formula = "protection = 1 − (1 ÷ SPF)"
    f_bbox = draw.textbbox((0, 0), formula, font=f_formula)
    fw = f_bbox[2] - f_bbox[0]
    fh = f_bbox[3] - f_bbox[1]
    box_pad = 16
    box_color = (*hex_to_rgb(LAB_MIST), 26)  # ~10% opacity
    # Draw tinted box via RGBA overlay
    img_box = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d_box = ImageDraw.Draw(img_box)
    d_box.rectangle(
        [margin, y - box_pad, margin + fw + box_pad * 2, y + fh + box_pad],
        fill=(*hex_to_rgb(LAB_MIST), 40)
    )
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, img_box)
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)
    draw.text((margin + box_pad, y), formula, font=f_formula, fill=hex_to_rgb(LAB_MIST))
    y += fh + box_pad * 2 + 32

    # Body text
    body_paragraphs = [
        "What SPF measures: how much longer UV takes to cause erythema on protected skin versus unprotected. A time ratio, not a linear percentage.",
        "The variable that matters more than the number: application quantity. The test standard is 2mg per cm². Most people apply 20-40% of that.",
        "A correctly applied SPF 25 outperforms an under-applied SPF 50.",
    ]
    for para in body_paragraphs:
        y = draw_wrapped(draw, para, f_body, margin, y, body_width, BONE, line_spacing=1.5)
        y += 18

    # Footer
    footer = "Ingredients, decoded.  ·  @skinlabeditorial"
    footer_color = (*hex_to_rgb(BONE), 102)  # ~40% opacity
    img_f = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d_f = ImageDraw.Draw(img_f)
    d_f.text((margin, H - 52), footer, font=f_footer, fill=footer_color)
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, img_f)
    img = img.convert("RGB")

    path = os.path.join(OUT_DIR, "slide-02.png")
    img.save(path)
    print(f"Saved {path}")

# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    slide_01()
    slide_02()
    print("Done — 2 slides generated.")
