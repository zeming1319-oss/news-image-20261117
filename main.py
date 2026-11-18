#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont

# Deterministic, Pillow-based infographic generator for 17 November 2026 world news.
# Outputs only news.png in the current directory.

WIDTH = 1400
HEIGHT = 1900
MARGIN = 60
GUTTER = 30
HEADER_H = 210

BG = (18, 20, 24)
CARD_BG = (30, 33, 39)
CARD_BORDER = (55, 60, 70)
TEXT = (235, 236, 238)
MUTED = (170, 175, 182)
SOURCE = (135, 140, 148)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
FONT_REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")
FONT_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

NEWS_ITEMS = [
    {
        "category": "UKRAINE–RUSSIA",
        "accent": (229, 115, 115),
        "headline": "Ukraine strikes Kerch Bridge for second consecutive night",
        "body": (
            "Ukraine said an \"unprecedented\" operation partly collapsed the bridge linking Russia to occupied Crimea, "
            "suspending road traffic. Russia reported downing a record barrage of over 2,000 drones and retaliated with "
            "strikes on Kyiv's North and South bridges, cutting water and power in parts of the capital."
        ),
        "sources": "BBC, The Guardian, AP, Al Jazeera, RTE",
    },
    {
        "category": "TRUMP IN ASIA",
        "accent": (100, 181, 246),
        "headline": "Trump begins high-stakes Asia trip in Manila",
        "body": (
            "President Trump arrived in the Philippines for ASEAN meetings before heading to APEC in China and a planned "
            "historic trilateral summit with Vladimir Putin and Xi Jinping in Shenzhen. Large protests were held in Manila."
        ),
        "sources": "AP, Reuters, The Guardian, The Washington Post",
    },
    {
        "category": "US–IRAN ESCALATION",
        "accent": (255, 183, 77),
        "headline": "Strikes and ship attacks intensify Gulf tensions",
        "body": (
            "The US struck targets on Iran's Qeshm Island after Iranian mines set at least five ships ablaze in the Strait of Hormuz. "
            "Iran fired drones at a US radar facility in Bahrain as a third US carrier group arrived, disrupting oil shipping."
        ),
        "sources": "NPR, Euronews, AP, Reuters, Le Monde",
    },
    {
        "category": "US AVIATION CRISIS",
        "accent": (129, 199, 132),
        "headline": "Air travel recovery rattled by outage after ground stop",
        "body": (
            "Flights lurched back toward normal after Friday's FAA nationwide ground stop, which caused over 18,000 cancellations. "
            "United Airlines later canceled dozens of flights after a 90-minute system outage as officials faced Senate questioning."
        ),
        "sources": "NPR, Democracy Now!, Euronews",
    },
    {
        "category": "TECH OUTAGES / NSA",
        "accent": (186, 104, 200),
        "headline": "Classified NSA network outage raises alarm",
        "body": (
            "ABC News reported a \"highly classified NSA network went down,\" the latest in a string of US technology and government outages. "
            "A former NSA hacker told CNN \"there's something here\" as lawmakers sought answers on Nvidia chips and Chinese access."
        ),
        "sources": "ABC News, CNN",
    },
    {
        "category": "MEASLES / PUBLIC HEALTH",
        "accent": (77, 208, 225),
        "headline": "US loses measles-elimination status with Bolivia and Mexico",
        "body": (
            "The Pan American Health Organization revoked measles-elimination status after more than 5,700 US infections and over 12 months "
            "of continuing domestic transmission."
        ),
        "sources": "PAHO/AFP, France 24, ABC",
    },
    {
        "category": "MARKETS / AI SLIDE",
        "accent": (255, 241, 118),
        "headline": "Wall Street falls again as AI stocks swing",
        "body": (
            "The S&P 500 sank 0.9%, the Dow dropped 541 points and Nvidia closed down 2.9% after volatile trading. "
            "Jensen Huang said he would be \"honoured\" to return as CEO and is set to testify before Congress on 1 December over chip sales to China."
        ),
        "sources": "AP, Euronews",
    },
    {
        "category": "EU MIGRATION / RWANDA HUBS",
        "accent": (255, 138, 101),
        "headline": "Five EU states plan migrant return hubs in Rwanda",
        "body": (
            "Austria, Denmark, Germany, Greece and the Netherlands announced plans for return hubs, drawing human-rights backlash and criticism from Spain. "
            "The EU also cleared UniCredit's takeover of Germany's Commerzbank."
        ),
        "sources": "The Guardian, Euronews, Christian Science Monitor",
    },
]


def load_fonts():
    return {
        "masthead": ImageFont.truetype(FONT_BOLD, 54),
        "subtitle": ImageFont.truetype(FONT_REG, 28),
        "date": ImageFont.truetype(FONT_BOLD, 22),
        "category": ImageFont.truetype(FONT_BOLD, 20),
        "headline": ImageFont.truetype(FONT_BOLD, 30),
        "body": ImageFont.truetype(FONT_REG, 22),
        "source": ImageFont.truetype(FONT_REG, 17),
    }


def text_width(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def line_height(font):
    bbox = font.getbbox("Ay")
    return bbox[3] - bbox[1]


def wrap_text(draw, text, font, max_width):
    words = text.split()
    if not words:
        return [""]
    lines = []
    current = words[0]
    for word in words[1:]:
        trial = current + " " + word
        if text_width(draw, trial, font) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def draw_wrapped(draw, text, font, x, y, max_width, fill, spacing=6):
    lines = wrap_text(draw, text, font, max_width)
    lh = line_height(font)
    cy = y
    for line in lines:
        draw.text((x, cy), line, font=font, fill=fill)
        cy += lh + spacing
    # return bottom y after last line (without extra trailing spacing beyond drawn)
    total_h = len(lines) * lh + (len(lines) - 1) * spacing if lines else 0
    return y + total_h


def measure_wrapped(draw, text, font, max_width, spacing=6):
    lines = wrap_text(draw, text, font, max_width)
    lh = line_height(font)
    total_h = len(lines) * lh + (len(lines) - 1) * spacing if lines else 0
    return total_h, len(lines)


def draw_card(draw, fonts, item, x, y, w, h):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=18, fill=CARD_BG, outline=CARD_BORDER, width=2)

    pad_x = 24
    pad_y = 22
    inner_w = w - 2 * pad_x
    cursor_y = y + pad_y

    # Category tag pill
    cat = item["category"]
    cat_font = fonts["category"]
    cat_pad_x = 10
    cat_pad_y = 6
    cat_tw = text_width(draw, cat, cat_font)
    cat_th = line_height(cat_font)
    pill_w = cat_tw + 2 * cat_pad_x
    pill_h = cat_th + 2 * cat_pad_y
    draw.rounded_rectangle([x + pad_x, cursor_y, x + pad_x + pill_w, cursor_y + pill_h], radius=8, fill=item["accent"])
    # choose dark text on bright accents for readability
    draw.text((x + pad_x + cat_pad_x, cursor_y + cat_pad_y - 1), cat, font=cat_font, fill=(20, 20, 20))
    cursor_y += pill_h + 16

    # Headline
    headline_font = fonts["headline"]
    cursor_y = draw_wrapped(draw, item["headline"], headline_font, x + pad_x, cursor_y, inner_w, TEXT, spacing=4)
    cursor_y += 12

    # Body
    body_font = fonts["body"]
    cursor_y = draw_wrapped(draw, item["body"], body_font, x + pad_x, cursor_y, inner_w, MUTED, spacing=5)
    cursor_y += 14

    # Source line
    src_text = "Sources: " + item["sources"]
    draw_wrapped(draw, src_text, fonts["source"], x + pad_x, cursor_y, inner_w, SOURCE, spacing=4)

    return cursor_y


def compute_card_height(draw, fonts, item, w):
    pad_x = 24
    pad_y = 22
    inner_w = w - 2 * pad_x
    h = pad_y
    cat_th = line_height(fonts["category"])
    h += (cat_th + 12) + 16
    hh, _ = measure_wrapped(draw, item["headline"], fonts["headline"], inner_w, spacing=4)
    h += hh + 12
    bh, _ = measure_wrapped(draw, item["body"], fonts["body"], inner_w, spacing=5)
    h += bh + 14
    sh, _ = measure_wrapped(draw, "Sources: " + item["sources"], fonts["source"], inner_w, spacing=4)
    h += sh + pad_y
    return h


def main():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    fonts = load_fonts()

    # Masthead
    title = "WORLD NEWS — 17 NOVEMBER 2026"
    subtitle = "Eight stories that shaped the day"
    draw.text((MARGIN, 48), title, font=fonts["masthead"], fill=TEXT)
    draw.text((MARGIN, 118), subtitle, font=fonts["subtitle"], fill=MUTED)
    # accent rule
    draw.line([(MARGIN, 165), (WIDTH - MARGIN, 165)], fill=(70, 76, 86), width=2)
    draw.line([(MARGIN, 165), (MARGIN + 360, 165)], fill=(100, 181, 246), width=4)

    # Cards grid: 2 columns x 4 rows
    cols = 2
    rows = 4
    card_w = (WIDTH - 2 * MARGIN - GUTTER) // 2
    grid_top = HEADER_H
    available_h = HEIGHT - grid_top - MARGIN
    card_h = (available_h - (rows - 1) * GUTTER) // rows

    # Verify fit; if overflow, warn via print (but keep deterministic output)
    max_needed = 0
    for item in NEWS_ITEMS:
        needed = compute_card_height(draw, fonts, item, card_w)
        if needed > max_needed:
            max_needed = needed

    for idx, item in enumerate(NEWS_ITEMS):
        r = idx // cols
        c = idx % cols
        x = MARGIN + c * (card_w + GUTTER)
        y = grid_top + r * (card_h + GUTTER)
        actual_h = card_h
        # ensure card is tall enough for content if small margin exists
        needed = compute_card_height(draw, fonts, item, card_w)
        if needed > actual_h:
            actual_h = needed
        draw_card(draw, fonts, item, x, y, card_w, actual_h)

    # Footer note/date line for completeness
    footer = "Tuesday, 17 November 2026"
    fw = text_width(draw, footer, fonts["date"])
    draw.text((WIDTH - MARGIN - fw, 122), footer, font=fonts["date"], fill=(120, 126, 134))

    img.save("news.png", format="PNG")


if __name__ == "__main__":
    main()
