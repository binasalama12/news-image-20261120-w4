#!/usr/bin/env python3
# The One-Day Paper - Friday 20 November 2026.
# A single-page broadsheet: 48 stories, one picture. All art is drawn
# here with PIL primitives; nothing is photographed or copied in.
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

W = 1600
H = 1600
M = 36
CW = W - 2 * M
PAPER = (247, 243, 233)
INK = (26, 24, 20)
PURPLE = (74, 32, 96)
RED = (168, 32, 40)
GOLD = (176, 132, 40)
TEAL = (24, 120, 116)
NAVY = (28, 44, 88)
GREY = (96, 92, 84)

FD = "/usr/share/fonts/truetype/dejavu/"
FL = "/usr/share/fonts/truetype/liberation/"


def F(name, size):
    try:
        return ImageFont.truetype(FD + name, size)
    except OSError:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            return ImageFont.load_default()


def SF(name, size):
    try:
        return ImageFont.truetype(FL + name, size)
    except OSError:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            return ImageFont.load_default()


SANS = "DejaVuSans.ttf"
SANSB = "DejaVuSans-Bold.ttf"
SERIF = "LiberationSerif-Regular.ttf"
SERIFB = "LiberationSerif-Bold.ttf"
SERIFI = "LiberationSerif-Italic.ttf"


def wrap(d, text, font, width):
    words = text.split()
    lines = []
    cur = ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if d.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, font, width, lh, color, max_lines=None):
    lines = wrap(d, text, font, width)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and d.textlength(last + "…", font=font) > width:
            last = last[:-1]
        lines[-1] = last.rstrip() + "…"
    for ln in lines:
        d.text((x, y), ln, font=font, fill=color)
        y += lh
    return y


def one_line(d, x, y, text, font, width, color):
    if d.textlength(text, font=font) > width:
        while text and d.textlength(text + "…", font=font) > width:
            text = text[:-1]
        text = text.rstrip() + "…"
    d.text((x, y), text, font=font, fill=color)
    return y


def rule(d, x, y, w, color=INK, width=2):
    d.line([(x, y), (x + w, y)], fill=color, width=width)


def sky_band(d, x, y, w, h, top, bottom):
    steps = max(1, h // 6)
    for i in range(steps):
        t = i / max(1, steps - 1)
        col = tuple(int(top[c] + (bottom[c] - top[c]) * t) for c in range(3))
        yy = y + i * 6
        d.rectangle([x, yy, x + w, min(y + h, yy + 6)], fill=col)


def sun(d, cx, cy, r, col=(232, 176, 60)):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    for k in range(8):
        a = math.pi * k / 4
        x1 = cx + int(math.cos(a) * (r + 4))
        y1 = cy + int(math.sin(a) * (r + 4))
        x2 = cx + int(math.cos(a) * (r + 14))
        y2 = cy + int(math.sin(a) * (r + 14))
        d.line([(x1, y1), (x2, y2)], fill=col, width=3)


def skyline(d, x, y, w, h, col, seed=3, base=None):
    rnd = random.Random(seed)
    base = base if base is not None else y + h
    cx = x
    while cx < x + w:
        bw = rnd.randint(18, 46)
        bh = rnd.randint(int(h * 0.25), h)
        d.rectangle([cx, base - bh, cx + bw, base], fill=col)
        if rnd.random() < 0.5:
            d.rectangle([cx + bw // 3, base - bh - 8, cx + bw // 3 + 6, base - bh],
                        fill=col)
        cx += bw + rnd.randint(2, 8)


def flag(d, x, y, w, h, stripes):
    n = len(stripes)
    for i, col in enumerate(stripes):
        d.rectangle([x, y + i * h // n, x + w, y + (i + 1) * h // n], fill=col)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def scene(d, x, y, w, h, kind):
    """Flat illustration for one panel, drawn from scratch."""
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    if kind == "cyclone":
        sky_band(d, x, y, w, h, (52, 62, 92), (160, 178, 200))
        d.ellipse([x + w // 2 - 52, y + h // 2 - 40, x + w // 2 + 52,
                   y + h // 2 + 40], outline=(240, 240, 240), width=6)
        d.ellipse([x + w // 2 - 34, y + h // 2 - 26, x + w // 2 + 34,
                   y + h // 2 + 26], outline=(240, 240, 240), width=5)
        d.ellipse([x + w // 2 - 16, y + h // 2 - 12, x + w // 2 + 16,
                   y + h // 2 + 12], outline=(240, 240, 240), width=4)
        for i in range(14):
            rx = x + (i * 37) % w
            d.line([(rx, y + 8), (rx - 6, y + 26)], fill=(200, 210, 225), width=2)
        d.rectangle([x, y + h - 26, x + w, y + h], fill=(30, 44, 66))
        for i in range(5):
            d.rectangle([x + 12 + i * 30, y + h - 40, x + 28 + i * 30, y + h - 26],
                        fill=(200, 190, 160))
    elif kind == "missile":
        sky_band(d, x, y, w, h, (20, 26, 58), (58, 74, 110))
        skyline(d, x, y + h - 60, w, 60, (12, 16, 34), seed=7)
        for i in range(26):
            t = i / 25
            px = x + int(t * w * 0.8)
            py = y + int(h * 0.62 - t * t * h * 0.5)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 190, 60))
        d.ellipse([x + int(w * 0.82) - 16, y + int(h * 0.12) - 16,
                   x + int(w * 0.82) + 16, y + int(h * 0.12) + 16],
                  fill=(255, 120, 40))
        for k in range(8):
            a = math.pi * k / 4
            d.line([(x + int(w * 0.82) + int(math.cos(a) * 20),
                     y + int(h * 0.12) + int(math.sin(a) * 20)),
                    (x + int(w * 0.82) + int(math.cos(a) * 30),
                     y + int(h * 0.12) + int(math.sin(a) * 30))],
                   fill=(255, 120, 40), width=3)
    elif kind == "flags":
        sky_band(d, x, y, w, h, (150, 180, 208), (220, 214, 196))
        skyline(d, x, y + h - 44, w, 44, (52, 58, 72), seed=11)
        for i, stripes in enumerate([
                [(178, 34, 52), (255, 255, 255), (30, 60, 140)],
                [(222, 0, 0), (255, 222, 0)],
                [(255, 255, 255), (0, 60, 160), (222, 0, 0)]]):
            fx = x + 26 + i * (w // 3)
            flag(d, fx, y + 16, w // 4, 26, stripes)
            d.line([(fx + w // 8, y + 16), (fx + w // 8, y + h - 44)],
                   fill=INK, width=2)
    elif kind == "bridge":
        sky_band(d, x, y, w, h, (70, 96, 130), (190, 200, 210))
        d.rectangle([x, y + h - 30, x + w, y + h], fill=(40, 48, 60))
        d.line([(x, y + h - 30), (x + w, y + h - 30)], fill=(220, 220, 220), width=3)
        for i in range(5):
            px = x + (i + 1) * w // 6
            d.line([(px, y + 14), (px, y + h - 30)], fill=(200, 200, 200), width=2)
        d.line([(x, y + 14), (x + w // 2, y + h - 30)], fill=(220, 120, 60), width=3)
        d.line([(x + w, y + 14), (x + w // 2, y + h - 30)], fill=(220, 120, 60), width=3)
        d.ellipse([x + w // 2 - 10, y + h // 2 - 10, x + w // 2 + 10, y + h // 2 + 10],
                  fill=(255, 150, 40))
    elif kind == "summit":
        sky_band(d, x, y, w, h, (140, 170, 200), (226, 220, 200))
        skyline(d, x, y + h - 52, w, 52, (40, 52, 80), seed=5)
        d.rectangle([x + w // 2 - 34, y + h - 96, x + w // 2 + 34, y + h - 52],
                    fill=(120, 40, 50))
        d.polygon([(x + w // 2 - 34, y + h - 96), (x + w // 2 + 34, y + h - 96),
                   (x + w // 2, y + h - 118)], fill=(150, 50, 60))
        sun(d, x + w - 26, y + 22, 12)
    elif kind == "climate":
        sky_band(d, x, y, w, h, (120, 170, 150), (220, 228, 210))
        d.ellipse([x + w // 2 - 30, y + 10, x + w // 2 + 30, y + 70],
                  fill=(60, 140, 90))
        d.ellipse([x + w // 2 - 18, y + 18, x + w // 2 - 2, y + 34],
                  fill=(120, 190, 130))
        d.ellipse([x + w // 2 + 4, y + 40, x + w // 2 + 20, y + 58],
                  fill=(120, 190, 130))
        for i in range(4):
            d.rectangle([x + 10 + i * 16, y + h - 18, x + 22 + i * 16, y + h - 6],
                        fill=(90, 90, 90))
    elif kind == "court":
        sky_band(d, x, y, w, h, (200, 198, 188), (240, 236, 224))
        d.rectangle([x + 12, y + h - 42, x + w - 12, y + h - 34], fill=(120, 110, 96))
        for i in range(4):
            cx = x + 24 + i * (w - 48) // 3
            d.rectangle([cx - 6, y + 18, cx + 6, y + h - 42], fill=(230, 226, 214))
        d.polygon([(x + 8, y + 18), (x + w - 8, y + 18), (x + w // 2, y + 2)],
                  fill=(140, 30, 40))
        d.rectangle([x + w // 2 - 8, y + h - 30, x + w // 2 + 8, y + h - 22],
                    fill=(60, 50, 40))
    elif kind == "market":
        d.rectangle([x, y, x + w, y + h], fill=(240, 238, 230))
        for i in range(6):
            bx = x + 8 + i * (w - 16) // 6
            bh = [18, 34, 26, 44, 30, 48][i]
            d.rectangle([bx, y + h - 10 - bh, bx + (w - 16) // 7, y + h - 10],
                        fill=(150, 160, 170))
        d.line([(x + 6, y + h - 46), (x + w // 3, y + h - 30),
                (x + 2 * w // 3, y + h - 58), (x + w - 6, y + 12)],
               fill=(178, 32, 40), width=4)
    elif kind == "game":
        sky_band(d, x, y, w, h, (58, 40, 96), (200, 120, 160))
        sun(d, x + w // 2, y + h // 2 - 6, 20, col=(255, 200, 80))
        d.rectangle([x, y + h - 22, x + w, y + h], fill=(30, 24, 44))
        skyline(d, x, y + h - 44, w, 22, (20, 16, 34), seed=9)
        d.rectangle([x + 10, y + 10, x + 34, y + 22], fill=(255, 255, 255))
    elif kind == "orbit":
        d.rectangle([x, y, x + w, y + h], fill=(10, 14, 34))
        for i in range(40):
            rnd = random.Random(100 + i)
            sx = x + rnd.randint(2, max(3, w - 4))
            sy = y + rnd.randint(2, max(3, h - 4))
            d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
        d.ellipse([x + w // 2 - 34, y + h // 2 - 12, x + w // 2 + 34, y + h // 2 + 12],
                  outline=(200, 200, 220), width=2)
        d.ellipse([x + w // 2 - 5, y + h // 2 - 5, x + w // 2 + 5, y + h // 2 + 5],
                  fill=(255, 190, 60))
        d.ellipse([x + w - 22, y + 12, x + w - 12, y + 22], fill=(200, 200, 210))
    elif kind == "gavel":
        sky_band(d, x, y, w, h, (210, 205, 190), (244, 240, 228))
        d.rectangle([x + w // 2 - 26, y + h - 20, x + w // 2 + 26, y + h - 12],
                    fill=(120, 90, 60))
        d.rectangle([x + w // 2 - 34, y + h // 2 - 8, x + w // 2 + 34,
                     y + h // 2 + 8], fill=(90, 60, 40))
        d.line([(x + w // 2, y + h // 2 + 8), (x + w // 2 + 26, y + h - 20)],
               fill=(90, 60, 40), width=6)
    elif kind == "drought":
        sky_band(d, x, y, w, h, (240, 200, 120), (250, 230, 170))
        sun(d, x + w - 24, y + 20, 16, col=(240, 120, 40))
        d.rectangle([x, y + h - 26, x + w, y + h], fill=(170, 130, 80))
        for i in range(5):
            px = x + 14 + i * (w - 28) // 4
            d.line([(px, y + h - 26), (px, y + h - 48)], fill=(120, 90, 50), width=3)
            d.line([(px, y + h - 48), (px - 8, y + h - 40)], fill=(120, 90, 50), width=2)
            d.line([(px, y + h - 48), (px + 8, y + h - 40)], fill=(120, 90, 50), width=2)
    elif kind == "reactor":
        sky_band(d, x, y, w, h, (150, 165, 185), (220, 222, 216))
        for i in range(3):
            cx = x + 26 + i * (w - 52) // 2
            d.polygon([(cx - 16, y + h - 16), (cx - 10, y + 22),
                       (cx + 10, y + 22), (cx + 16, y + h - 16)],
                      fill=(150, 150, 150))
        d.rectangle([x, y + h - 16, x + w, y + h], fill=(90, 90, 90))
    elif kind == "handshake":
        sky_band(d, x, y, w, h, (170, 190, 210), (232, 228, 216))
        d.ellipse([x + w // 2 - 30, y + h // 2 - 8, x + w // 2 + 30, y + h // 2 + 8],
                  fill=(210, 180, 140))
        d.line([(x + 10, y + h // 2), (x + w // 2 - 28, y + h // 2)],
               fill=(120, 90, 60), width=8)
        d.line([(x + w - 10, y + h // 2), (x + w // 2 + 28, y + h // 2)],
               fill=(90, 110, 130), width=8)
    elif kind == "tanker":
        sky_band(d, x, y, w, h, (140, 170, 200), (210, 220, 228))
        d.rectangle([x, y + h - 22, x + w, y + h], fill=(40, 90, 120))
        d.rectangle([x + 12, y + h - 44, x + w - 12, y + h - 22], fill=(140, 50, 40))
        d.rectangle([x + w - 40, y + h - 62, x + w - 18, y + h - 44],
                    fill=(220, 220, 220))
        d.ellipse([x + w // 2 - 8, y + 14, x + w // 2 + 8, y + 30], fill=(255, 140, 40))
    elif kind == "cricket":
        d.rectangle([x, y, x + w, y + h], fill=(120, 170, 100))
        d.rectangle([x + w // 2 - 4, y + 8, x + w // 2 + 4, y + h - 8],
                    fill=(230, 220, 190))
        d.rectangle([x + 12, y + h - 26, x + w - 12, y + h - 18], fill=(200, 185, 150))
        d.ellipse([x + w - 26, y + 12, x + w - 16, y + 22], fill=(178, 32, 40))
        d.rectangle([x + 14, y + 14, x + 20, y + 44], fill=(150, 110, 70))
    else:
        sky_band(d, x, y, w, h, (150, 170, 200), (225, 222, 210))
        sun(d, x + w // 2, y + h // 2, 14)


HEROES = [
    dict(num="1", kick="ODISHA · STORM", scene="cyclone",
         head="Akvan comes ashore on the Odisha coast",
         dek="Cyclone Akvan crossed the coast near Gopalpur at noon, winds "
             "90-100 km/h gusting to 110. Three hundred thousand people are "
             "out of harm's way, 423 rescue teams deployed, red alerts in "
             "11 districts.",
         src="IMD · THE HINDU"),
    dict(num="2", kick="RIYADH · ATTACK", scene="missile",
         head="Houthi missile hits Riyadh's KAFD financial district",
         dek="A Houthi missile damaged a wealth-fund tower in the financial "
             "district, one of Riyadh's tallest. No casualties are reported, "
             "as air defences answered the strike.",
         src="ARAB NEWS · REUTERS"),
    dict(num="3", kick="SHENZHEN · DIPLOMACY", scene="flags",
         head="Trump, Xi and Putin issue a joint declaration",
         dek="No big peace deal from the trilateral's second day. Trump says "
             "the Iran war call waits until 2027, rates the summit '12 out "
             "of 10', and Putin may attend December's G20 in Miami.",
         src="REUTERS · AP"),
]

PICTURED = [
    dict(num="4", kick="KERCH STRAIT · WAR", scene="bridge",
         head="Crimean Bridge hit a third time this week; rail halted",
         dek="A Ukrainian naval drone strike disrupted rail traffic on the "
             "bridge. Rail partly resumes; Putin vows retaliation, and Kyiv "
             "was hit by drones.",
         src="CLAIM · KYIV"),
    dict(num="5", kick="SHENZHEN · SUMMIT", scene="summit",
         head="APEC leaders meet in Shenzhen",
         dek="Leaders gather in China for the APEC summit. Xi urges APEC "
             "economies to back open trade and new technology.",
         src="AP"),
    dict(num="6", kick="ANTALYA · CLIMATE", scene="climate",
         head="COP31's final day: fossil fuels cut from the text",
         dek="A revised draft strips out every fossil-fuel phase-out pledge. "
             "Delegates push back as the final plenary meets today.",
         src="UNFCCC · AFP"),
    dict(num="7", kick="THE HAGUE · LAW", scene="court",
         head="The world answers the genocide verdict",
         dek="Britain expels Myanmar's defence attache and seeks an urgent "
             "Security Council meeting. The Gambia hails a 'historic' verdict.",
         src="AP · BBC"),
    dict(num="8", kick="NEW YORK · MARKETS", scene="market",
         head="Anthropic's debut can't stop the slide",
         dek="The Dow fell 1,084 points, the S&P 2.02% and the Nasdaq 2.25%, "
             "as the AI selloff bit a day after Anthropic's record debut.",
         src="BLOOMBERG"),
    dict(num="9", kick="VICE CITY · GAMES", scene="game",
         head="GTA VI passes The Odyssey's $1.84bn",
         dek="Launch-day sales top The Odyssey's $1.80bn global run, Sensor "
             "Tower estimates. Reviews land; Rockstar calls it the "
             "highest-rated game ever.",
         src="SENSOR TOWER"),
    dict(num="10", kick="SPACE · SCIENCE", scene="orbit",
         head="NASA confirms Voyager 1's light-day milestone",
         dek="The probe is now a full light-day from Earth - 16 billion miles "
             "out, the farthest any human-made object has ever travelled.",
         src="NASA · JPL"),
    dict(num="11", kick="SEOUL · LAW", scene="gavel",
         head="South Korea clears ex-PM Han",
         dek="The Supreme Court overturns former prime minister Han Duck-soo's "
             "conviction, in the case tied to the 2024 martial-law declaration.",
         src="KOREA TIMES"),
    dict(num="12", kick="SUVA · CLIMATE", scene="drought",
         head="Fiji declares a national disaster over drought",
         dek="Fiji declares a national disaster over drought and water "
             "shortages. El Nino leaves water short across the islands.",
         src="AFP"),
    dict(num="13", kick="VIENNA · SECURITY", scene="reactor",
         head="North Korea expands uranium enrichment at Yongbyon",
         dek="The UN watchdog reports growth at the nuclear site, in its "
             "latest assessment of the Yongbyon complex.",
         src="IAEA"),
    dict(num="14", kick="CARACAS · DIPLOMACY", scene="handshake",
         head="US and Venezuela restore military cooperation",
         dek="The two countries sign an agreement to work together again, "
             "restoring a military channel closed for years.",
         src="REUTERS"),
    dict(num="15", kick="HORMUZ · CONFLICT", scene="tanker",
         head="ADNOC vessel attacked in the Strait of Hormuz",
         dek="One crew member is missing after the strike on the ADNOC vessel "
             "in the strait.",
         src="REUTERS"),
    dict(num="16", kick="WELLINGTON · CRICKET", scene="cricket",
         head="Day two at the Basin: Nicholls' 113 anchors New Zealand",
         dek="New Zealand build on Henry Nicholls' unbeaten 113 as India hunt "
             "early wickets, in the first Test at the Basin Reserve.",
         src="AP"),
]

BRIEFS = [
    (17, "BRUSSELS", "EU-UK summit opens"),
    (18, "NEW DELHI", "Modi meets William and Kate"),
    (19, "DHAKA", "Fire at the Yunus home; arson feared"),
    (20, "MUMBAI", "Sensex +1.21%, Nifty +1.14% on the day"),
    (21, "TOKYO", "Hayabusa2 gives up landing; mission rewritten"),
    (22, "BERLIN", "Coalition of the Willing meets in Berlin"),
    (23, "BERLIN", "Merz hosts Qatar's emir in Berlin"),
    (24, "NEW DELHI", "Pakistan minister leads delegation to Delhi for SCO"),
    (25, "MANILA", "Philippines-Chile trade deal signed"),
    (26, "MANILA", "Musk plans Philippines projects"),
    (27, "HONG KONG", "India beats Malaysia, Asian Hockey Trophy opens"),
    (28, "IPOH", "Harimau Shakti exercise opens in Ipoh"),
    (29, "NEW DELHI", "India's electronics exports jump 44%"),
    (30, "NEW DELHI", "ICMR completes 100 tech transfers"),
    (31, "NEW DELHI", "India unveils its first bird-flu vaccine"),
    (32, "GENEVA", "World Children's Day marked worldwide"),
    (33, "EUROPE", "Youth anti-war protests across Europe"),
    (34, "BRUSSELS", "EU delays its methane rules by 24 months"),
    (35, "COLOGNE", "Bayern Munich beat Koln 3-0"),
    (36, "U17 CUP", "Argentina 0-2 Australia at the U17 Cup"),
    (37, "WASHINGTON", "Jobless claims come in at 203,000"),
    (38, "STRASBOURG", "NATO's assembly opens its 72nd session"),
    (39, "HANOI", "Azerbaijan's Aliyev visits Vietnam"),
    (40, "MARKETS", "Crude futures fall over 3%"),
    (41, "KHARTOUM", "Sudan army: two-year El Obeid siege broken"),
    (42, "MOGADISHU", "Somalia gives UAE ambassador 72 hours to leave"),
    (43, "SAN SALVADOR", "Migrant boat capsizes off El Salvador; dozens missing"),
    (44, "PORT-AU-PRINCE", "Haiti approves Salvadoran troop deal vs gangs"),
    (45, "ARABIAN SEA", "Amur falcons cross the Arabian Sea"),
    (46, "NEW YORK", "Al-Saadi appears in a New York court over a UK plot"),
    (47, "KYIV", "Witkoff and Kushner brief Zelenskyy"),
    (48, "BEIJING", "Xi urges APEC to back open trade, new tech"),
]

TIMELINE = [
    ("Overnight", "Crimean Bridge hit a third time"),
    ("~06:00 UTC", "APEC leaders meet in Shenzhen"),
    ("~10:00 UTC", "Trilateral declaration issued"),
    ("~12:00 UTC", "Akvan makes landfall in Odisha"),
    ("~14:00 UTC", "Houthi missile hits Riyadh KAFD"),
    ("Late", "Wall Street slides; Dow -1,084"),
]

REGIONS = [
    ("EUROPE", 11, (28, 44, 88)),
    ("THE AMERICAS", 7, (24, 120, 116)),
    ("ASIA-PACIFIC", 19, (168, 32, 40)),
    ("MIDEAST", 4, (176, 132, 40)),
    ("AFRICA", 2, (74, 32, 96)),
    ("OCEANIA", 1, (90, 110, 60)),
    ("WORLD", 4, (96, 92, 84)),
]

CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 70), (-85, 66),
     (-80, 73), (-70, 62), (-55, 52), (-60, 46), (-75, 35), (-80, 25),
     (-90, 20), (-97, 16), (-105, 20), (-110, 23), (-117, 32), (-125, 40),
     (-125, 48), (-140, 60), (-155, 58)],
    [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-40, -20), (-48, -28),
     (-58, -35), (-65, -40), (-70, -50), (-73, -40), (-72, -20), (-78, -5)],
    [(-10, 36), (-9, 43), (0, 44), (-2, 48), (2, 51), (8, 57), (10, 59),
     (18, 56), (21, 55), (28, 59), (30, 60), (23, 65), (18, 69), (12, 70),
     (5, 62), (5, 58), (-2, 50), (-5, 43), (-9, 37)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (30, -30),
     (20, -35), (15, -30), (12, -18), (9, -5), (9, 4), (-8, 4), (-13, 8)],
    [(30, 60), (40, 68), (60, 70), (80, 73), (100, 77), (120, 73),
     (140, 72), (160, 70), (178, 66), (162, 60), (158, 52), (142, 45),
     (135, 43), (127, 40), (122, 32), (120, 25), (110, 20), (105, 10),
     (100, 8), (95, 15), (90, 22), (85, 20), (80, 8), (77, 8), (72, 20),
     (66, 25), (60, 25), (55, 26), (50, 29), (48, 30), (42, 35), (36, 36),
     (30, 36), (30, 42), (35, 45), (30, 55)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35),
     (140, -38), (147, -39), (150, -37), (153, -27), (146, -19), (142, -11),
     (136, -12), (132, -11), (126, -14), (122, -17), (114, -21)],
]

PINS = {
    4: (36, 45), 5: (114, 22), 6: (30, 36), 7: (4, 52), 8: (-74, 40),
    9: (-80, 25), 10: (-118, 34), 11: (127, 37), 12: (178, -18),
    13: (16, 48), 14: (-67, 10), 15: (56, 26), 16: (175, -41),
}


def inside_poly(lon, lat, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > lat) != (yj > lat):
            xin = (xj - xi) * (lat - yi) / (yj - yi) + xi
            if lon < xin:
                inside = not inside
        j = i
    return inside


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    step_lon, step_lat = 4.5, 4.5
    lon = -172.0
    while lon < 188:
        lat = -56.0
        while lat < 82:
            if any(inside_poly(lon, lat, poly) for poly in CONTINENTS):
                px = x + int((lon + 180) / 360 * w)
                py = y + int((80 - lat) / 136 * h)
                d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(200, 205, 215))
            lat += step_lat
        lon += step_lon
    for num, (lon, lat) in PINS.items():
        px = x + int((lon + 180) / 360 * w)
        py = y + int((80 - lat) / 136 * h)
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((px - 3, py - 6), str(num), font=F(SANSB, 9), fill=(255, 255, 255))


def kicker_row(d, x, y, num, kick, src, width):
    d.text((x, y), num, font=F(SANSB, 13), fill=PURPLE)
    d.text((x + 22, y), "· " + kick, font=F(SANSB, 13), fill=PURPLE)
    if src:
        sw = d.textlength(src, font=F(SANS, 10))
        d.text((x + width - sw, y + 2), src, font=F(SANS, 10), fill=GREY)
    return y + 20


def hero_panel(d, x, y, w, h, story):
    scene(d, x, y, w, 200, story["scene"])
    ty = y + 210
    kicker_row(d, x, ty, story["num"], story["kick"], story["src"], w)
    ty += 24
    ty = text_block(d, x, ty, story["head"], SF(SERIFB, 30), w, 34, INK,
                    max_lines=2)
    text_block(d, x, ty + 4, story["dek"], F(SANS, 14), w, 18, (52, 48, 42),
               max_lines=3)


def hero_wide(d, x, y, w, h, story):
    sw = 620
    scene(d, x, y, sw, h, story["scene"])
    tx = x + sw + 22
    tw = w - sw - 22
    ty = y + 14
    kicker_row(d, tx, ty, story["num"], story["kick"], story["src"], tw)
    ty += 26
    ty = text_block(d, tx, ty, story["head"], SF(SERIFB, 34), tw, 38, INK,
                    max_lines=2)
    text_block(d, tx, ty + 6, story["dek"], F(SANS, 15), tw, 19, (52, 48, 42),
               max_lines=3)


def pic_panel(d, x, y, w, h, story):
    scene(d, x, y, w, 62, story["scene"])
    ty = y + 68
    d.text((x, ty), story["num"], font=F(SANSB, 11), fill=PURPLE)
    d.text((x + 18, ty), "· " + story["kick"], font=F(SANSB, 11), fill=PURPLE)
    ty += 17
    ty = text_block(d, x, ty, story["head"], SF(SERIFB, 15), w, 17, INK,
                    max_lines=2)
    text_block(d, x, ty + 2, story["dek"], F(SANS, 10), w, 12, (52, 48, 42),
               max_lines=2)


def paper(im):
    d = ImageDraw.Draw(im, "RGBA")
    rnd = random.Random(20261120)
    for _ in range(9000):
        px = rnd.randint(0, W - 1)
        py = rnd.randint(0, H - 1)
        v = rnd.randint(-7, 7)
        d.point((px, py), fill=(247 + v, 243 + v, 233 + v))
    return d


def main():
    im = Image.new("RGB", (W, H), PAPER)
    d = paper(im)

    # --- top bar -------------------------------------------------------
    d.text((M, 18), "ONE DAY OF WORLD NEWS, ONE PICTURE",
           font=F(SANSB, 15), fill=PURPLE)
    right = "48 STORIES - 7 REGIONS - EVERY ONE FROM THIS FRIDAY"
    rw = d.textlength(right, font=F(SANSB, 15))
    d.text((W - M - rw, 18), right, font=F(SANSB, 15), fill=INK)
    rule(d, M, 44, CW, INK, 3)

    # --- masthead: small name left, big date right --------------------
    d.text((M, 62), "THE ONE-DAY PAPER", font=SF(SERIFB, 40), fill=INK)
    d.text((M, 108), "Atlas Fidelity · an edition drawn from the wires",
           font=SF(SERIFI, 17), fill=GREY)
    date = "Friday 20 November 2026"
    dw = d.textlength(date, font=SF(SERIFB, 58))
    d.text((W - M - dw, 58), date, font=SF(SERIFB, 58), fill=INK)
    d.text((W - M - d.textlength("FRIDAY EDITION", font=F(SANSB, 13)), 122),
           "FRIDAY EDITION", font=F(SANSB, 13), fill=RED)
    rule(d, M, 140, CW, PURPLE, 2)

    # --- timeline ------------------------------------------------------
    y = 152
    d.rectangle([M, y, M + 96, y + 44], fill=RED)
    d.text((M + 8, y + 4), "THE DAY", font=F(SANSB, 13), fill=(255, 255, 255))
    d.text((M + 8, y + 22), "IN UTC", font=F(SANSB, 13), fill=(255, 255, 255))
    cw = (CW - 96) // len(TIMELINE)
    for i, (when, what) in enumerate(TIMELINE):
        cx = M + 96 + i * cw + 10
        d.text((cx, y + 2), when, font=F(SANSB, 12), fill=RED)
        text_block(d, cx, y + 18, what, F(SANS, 11), cw - 20, 13, INK,
                   max_lines=2)
    rule(d, M, 204, CW, INK, 1)

    # --- region strip: equal-width blocks so every label is readable --
    y = 212
    rw = CW // len(REGIONS)
    for i, (name, count, col) in enumerate(REGIONS):
        d.rectangle([M + i * rw, y, M + (i + 1) * rw, y + 26], fill=col)
        label = "%s %d" % (name, count)
        lw = d.textlength(label, font=F(SANSB, 12))
        d.text((M + i * rw + (rw - lw) // 2, y + 6), label,
               font=F(SANSB, 12), fill=(255, 255, 255))

    # --- heroes: two columns, then one wide --------------------------
    hy = 250
    hw = (CW - 16) // 2
    hero_panel(d, M, hy, hw, 370, HEROES[0])
    hero_panel(d, M + hw + 16, hy, hw, 370, HEROES[1])
    rule(d, M, hy + 378, CW, INK, 1)
    hero_wide(d, M, hy + 390, CW, 190, HEROES[2])

    # --- pictured rows: 6 / 4 / 3 --------------------------------------
    rows = [PICTURED[0:6], PICTURED[6:10], PICTURED[10:13]]
    py = hy + 592
    for row in rows:
        gap = 12
        pw = (CW - gap * (len(row) - 1)) // len(row)
        for i, story in enumerate(row):
            pic_panel(d, M + i * (pw + gap), py, pw, 140, story)
        py += 152

    # --- bottom: map + briefs -----------------------------------------
    by = py + 4
    rule(d, M, by, CW, PURPLE, 2)
    by += 10
    d.text((M, by), "WHERE IT HAPPENED", font=F(SANSB, 16), fill=PURPLE)
    d.text((M + 600, by), "ALSO ON FRIDAY 20 NOVEMBER - 32 MORE STORIES",
           font=F(SANSB, 16), fill=RED)
    by += 26
    draw_map(d, M, by, 560, 148)
    bx = M + 600
    bw = CW - 600
    col_w = (bw - 20) // 2
    for ci in range(2):
        cx = bx + ci * (col_w + 20)
        for ri in range(16):
            n, place, txt = BRIEFS[ci * 16 + ri]
            yy = by + ri * 9 + 1
            d.ellipse([cx, yy + 2, cx + 5, yy + 7], fill=RED)
            line = "%d %s - %s" % (n, place, txt)
            one_line(d, cx + 9, yy, line, F(SANS, 9), col_w - 9, INK)

    # --- date check ----------------------------------------------------
    dy = 1478
    d.rectangle([M, dy, M + 150, dy + 66], fill=RED)
    d.text((M + 10, dy + 12), "DATE", font=F(SANSB, 18), fill=(255, 255, 255))
    d.text((M + 10, dy + 34), "CHECK", font=F(SANSB, 18), fill=(255, 255, 255))
    d.rectangle([M + 150, dy, M + CW, dy + 66], outline=RED, width=2)
    dc = ("Left out - they broke before Friday: the ICJ genocide ruling on "
          "Myanmar itself (Thursday 19 Nov) - Friday's news is the world's "
          "answer to it - Denmark's Greenland-US pact (19 Nov) - Anthropic's "
          "$81.34bn IPO (19 Nov); its first trading day was Thursday - "
          "Germany's electricity-tax cut (18 Nov) - the Crimean Bridge span "
          "collapse (17-18 Nov). Not yet: the trilateral's first meeting was "
          "19 Nov; the joint declaration is Friday's.")
    text_block(d, M + 162, dy + 6, dc, F(SANS, 11), CW - 174, 14, INK,
               max_lines=4)

    # --- footer --------------------------------------------------------
    fy = 1556
    d.text((M, fy), "Every story here happened, or was first reported, on "
                    "Friday 20 November 2026, in some time zone. Disputed "
                    "claims are attributed, not stated as fact.",
           font=SF(SERIFI, 13), fill=INK)
    d.text((M, fy + 20), "Sources: Reuters - AP - AFP - BBC - Bloomberg - "
                         "IMD - NASA - IAEA - The Hindu - Arab News - "
                         "Sensor Tower. Original drawings, drawn for this page.",
           font=F(SANS, 12), fill=GREY)

    out = im.resize((1024, 1024), Image.LANCZOS)
    candidates = []
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        candidates.append(out_dir)
    candidates.append(".")
    candidates.append(os.path.dirname(os.path.abspath(__file__)))
    last_err = None
    saved = None
    for cand in candidates:
        try:
            path = os.path.join(cand, "entry.png")
            out.save(path)
            saved = path
            break
        except OSError as err:
            last_err = err
    if saved is None:
        raise last_err
    print("wrote %s 1024x1024" % saved)


if __name__ == "__main__":
    main()
