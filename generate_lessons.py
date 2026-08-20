#!/usr/bin/env python3
"""
Generate Grade 2 Math Theory – Lessons 1 to 100 (Year 3).
Structure mirrors Year 3: 7 sections + bonus + answer key, with
deterministic SVG diagrams across sections (not LLM placeholders).

Run: python3 generate_lessons.py
"""
import os, math, random
from collections import deque

OUTDIR = os.path.dirname(os.path.abspath(__file__))

# ─── Topics (Grade 2 roadmap, Year-3 style blocks) ───────────────────────────
LESSONS = {
    # 1–10 Place Value
    1:  ("Place Value Foundations", "Tens & Ones | 90-Minute Lesson"),
    2:  ("Comparing & Ordering Numbers", "Compare & Order | 90-Minute Lesson"),
    3:  ("Expanded Form & Digit Values", "Expanded Form | 90-Minute Lesson"),
    4:  ("Skip Counting Patterns", "Skip Counting | 90-Minute Lesson"),
    5:  ("Numbers to 100", "Reading Numbers to 100 | 90-Minute Lesson"),
    6:  ("Number Lines to 100", "Number Lines | 90-Minute Lesson"),
    7:  ("Place Value Mixed Practice", "Place Value Practice | 90-Minute Lesson"),
    8:  ("Comparing 2-Digit Numbers", "Comparing Numbers | 90-Minute Lesson"),
    9:  ("Patterns in Place Value", "Place Value Patterns | 90-Minute Lesson"),
    10: ("Place Value Assessment", "Place Value Assessment | 90-Minute Lesson"),
    # 11–20 Add / Sub
    11: ("Adding Without Regrouping", "Addition Basics | 90-Minute Lesson"),
    12: ("Adding With Regrouping", "Addition With Regrouping | 90-Minute Lesson"),
    13: ("Subtracting Without Regrouping", "Subtraction Basics | 90-Minute Lesson"),
    14: ("Subtracting With Regrouping", "Subtraction With Regrouping | 90-Minute Lesson"),
    15: ("Part–Whole Models", "Part–Whole Thinking | 90-Minute Lesson"),
    16: ("Addition Word Problems", "Addition Stories | 90-Minute Lesson"),
    17: ("Subtraction Word Problems", "Subtraction Stories | 90-Minute Lesson"),
    18: ("Estimation & Reasonableness", "Estimation | 90-Minute Lesson"),
    19: ("Missing-Number Equations", "Missing Numbers | 90-Minute Lesson"),
    20: ("Add & Subtract Review", "Add & Subtract Review | 90-Minute Lesson"),
    # 21–30 Equal Groups / Early ×
    21: ("Equal Groups", "Equal Groups | 90-Minute Lesson"),
    22: ("Arrays & Multiplication", "Arrays | 90-Minute Lesson"),
    23: ("Facts: 2× and 5×", "2× and 5× Facts | 90-Minute Lesson"),
    24: ("Facts: 3× and 4×", "3× and 4× Facts | 90-Minute Lesson"),
    25: ("Facts: 6× and 7×", "6× and 7× Facts | 90-Minute Lesson"),
    26: ("Facts: 8× and 9×", "8× and 9× Facts | 90-Minute Lesson"),
    27: ("Facts: 10×", "10× Facts | 90-Minute Lesson"),
    28: ("Repeated Addition", "Repeated Addition | 90-Minute Lesson"),
    29: ("Multiplication Fluency", "× Fluency | 90-Minute Lesson"),
    30: ("Multiplication Review", "× Review | 90-Minute Lesson"),
    # 31–40 Sharing / Early ÷
    31: ("Sharing Equally", "Sharing | 90-Minute Lesson"),
    32: ("Grouping Models", "Grouping | 90-Minute Lesson"),
    33: ("Division Facts ÷2 ÷5", "÷2 and ÷5 | 90-Minute Lesson"),
    34: ("Division Facts ÷3 ÷4", "÷3 and ÷4 | 90-Minute Lesson"),
    35: ("Division Facts ÷6 ÷10", "÷6 and ÷10 | 90-Minute Lesson"),
    36: ("Relating × and ÷", "× and ÷ Connection | 90-Minute Lesson"),
    37: ("Division Word Problems", "Division Stories | 90-Minute Lesson"),
    38: ("Mixed ×÷ Practice", "Mixed ×÷ | 90-Minute Lesson"),
    39: ("Two-Step ×÷ Stories", "Two-Step Stories | 90-Minute Lesson"),
    40: ("Division Review", "÷ Review | 90-Minute Lesson"),
    # 41–50 Mixed Operations
    41: ("2-Digit × 1-Digit (Easy)", "2-Digit × 1-Digit | 90-Minute Lesson"),
    42: ("Place-Value Strategies", "Place-Value Strategies | 90-Minute Lesson"),
    43: ("Division Within 50", "Division Within 50 | 90-Minute Lesson"),
    44: ("Mixed Operation Stories", "Mixed Stories | 90-Minute Lesson"),
    45: ("Balancing Equations", "Balancing Equations | 90-Minute Lesson"),
    46: ("Order of Operations Intro", "Do ×÷ Before +− | 90-Minute Lesson"),
    47: ("Multi-Step Problems", "Multi-Step Problems | 90-Minute Lesson"),
    48: ("Money & Operations", "Money Problems | 90-Minute Lesson"),
    49: ("Operations Mixed Practice", "Operations Practice | 90-Minute Lesson"),
    50: ("Operations Assessment", "Operations Assessment | 90-Minute Lesson"),
    # 51–60 Fractions
    51: ("Halves & Quarters", "Halves & Quarters | 90-Minute Lesson"),
    52: ("Unit Fractions", "Unit Fractions | 90-Minute Lesson"),
    53: ("Fractions on Number Lines", "Fraction Number Lines | 90-Minute Lesson"),
    54: ("Shading Fractions", "Shading Fractions | 90-Minute Lesson"),
    55: ("Comparing Same Denominator", "Compare Fractions | 90-Minute Lesson"),
    56: ("Fractions of a Set", "Fractions of a Set | 90-Minute Lesson"),
    57: ("Equivalent Halves & Fourths", "Equivalent Fractions | 90-Minute Lesson"),
    58: ("Fraction Word Problems", "Fraction Stories | 90-Minute Lesson"),
    59: ("Mixed Fraction Practice", "Fraction Practice | 90-Minute Lesson"),
    60: ("Fractions Assessment", "Fractions Assessment | 90-Minute Lesson"),
    # 61–70 Measurement & Time
    61: ("Length: cm and m", "Length Units | 90-Minute Lesson"),
    62: ("Mass: g and kg", "Mass Units | 90-Minute Lesson"),
    63: ("Capacity: mL and L", "Capacity Units | 90-Minute Lesson"),
    64: ("Perimeter of Rectangles", "Perimeter | 90-Minute Lesson"),
    65: ("Area by Counting Squares", "Area Squares | 90-Minute Lesson"),
    66: ("Telling Time (Hour & Half)", "Telling Time | 90-Minute Lesson"),
    67: ("Elapsed Time", "Elapsed Time | 90-Minute Lesson"),
    68: ("Calendar Problems", "Calendar | 90-Minute Lesson"),
    69: ("Money: Making Change", "Money & Change | 90-Minute Lesson"),
    70: ("Measurement Review", "Measurement Review | 90-Minute Lesson"),
    # 71–80 Geometry
    71: ("2D Shapes", "2D Shapes | 90-Minute Lesson"),
    72: ("Sides & Vertices", "Sides & Vertices | 90-Minute Lesson"),
    73: ("Quadrilaterals", "Quadrilaterals | 90-Minute Lesson"),
    74: ("Angles: Right / Acute / Obtuse", "Angles | 90-Minute Lesson"),
    75: ("Lines of Symmetry", "Symmetry | 90-Minute Lesson"),
    76: ("3D Shapes Intro", "3D Shapes | 90-Minute Lesson"),
    77: ("Perimeter Applications", "Perimeter Practice | 90-Minute Lesson"),
    78: ("Area Applications", "Area Practice | 90-Minute Lesson"),
    79: ("Shape Patterns", "Shape Patterns | 90-Minute Lesson"),
    80: ("Geometry Review", "Geometry Review | 90-Minute Lesson"),
    # 81–90 Data & Patterns
    81: ("Tally Charts", "Tally Charts | 90-Minute Lesson"),
    82: ("Pictographs", "Pictographs | 90-Minute Lesson"),
    83: ("Bar Graphs", "Bar Graphs | 90-Minute Lesson"),
    84: ("Reading Tables", "Tables | 90-Minute Lesson"),
    85: ("Creating Simple Graphs", "Make a Graph | 90-Minute Lesson"),
    86: ("Number Patterns & Rules", "Number Patterns | 90-Minute Lesson"),
    87: ("Shape & Colour Patterns", "Visual Patterns | 90-Minute Lesson"),
    88: ("Input/Output Tables", "Function Tables | 90-Minute Lesson"),
    89: ("Data Word Problems", "Data Stories | 90-Minute Lesson"),
    90: ("Data & Patterns Review", "Data Review | 90-Minute Lesson"),
    # 91–100 Review
    91: ("Spiral: Numbers & Place Value", "Spiral: Numbers | 90-Minute Lesson"),
    92: ("Spiral: Add & Subtract", "Spiral: + − | 90-Minute Lesson"),
    93: ("Spiral: × and ÷", "Spiral: × ÷ | 90-Minute Lesson"),
    94: ("Spiral: Fractions", "Spiral: Fractions | 90-Minute Lesson"),
    95: ("Spiral: Measurement", "Spiral: Measurement | 90-Minute Lesson"),
    96: ("Spiral: Geometry & Data", "Spiral: Geometry & Data | 90-Minute Lesson"),
    97: ("Real-Life Math", "Real-Life Math | 90-Minute Lesson"),
    98: ("Test-Style Practice A", "Practice Test A | 90-Minute Lesson"),
    99: ("Test-Style Practice B", "Practice Test B | 90-Minute Lesson"),
    100:("End-of-Year Challenge", "End-of-Year Challenge | 90-Minute Lesson"),
}

# ─── CSS (Year-3 aligned) ────────────────────────────────────────────────────
CSS = """
    body {
      font-family: 'Segoe UI', Arial, sans-serif;
      max-width: 880px; margin: 0 auto;
      padding: 32px 24px; color: #1a1a2e;
      font-size: 15px; line-height: 1.75;
    }
    h1 { text-align:center; font-size:1.55em; color:#14532d; margin-bottom:4px; }
    .meta { text-align:center; color:#555; margin-bottom:28px; font-size:.97em; }
    .section-header {
      background:#e8f5e9; border-left:5px solid #14532d;
      padding:7px 14px; margin:28px 0 14px 0;
      font-weight:bold; font-size:1.05em; color:#14532d;
      border-radius:0 6px 6px 0;
    }
    .bonus {
      background:#fff8e1; border-left:5px solid #f9a825;
      padding:7px 14px; margin:28px 0 14px 0;
      font-weight:bold; font-size:1.05em; color:#7a5c00;
      border-radius:0 6px 6px 0;
    }
    .answer-header {
      background:#e6f4ea; border-left:5px solid #2e7d32;
      padding:7px 14px; margin:28px 0 14px 0;
      font-weight:bold; font-size:1.05em; color:#2e7d32;
      border-radius:0 6px 6px 0;
    }
    .question { margin:10px 0 10px 18px; }
    .blank {
      display:inline-block; min-width:54px;
      border-bottom:2px solid #333; margin:0 5px; vertical-align:bottom;
    }
    .wide-blank {
      display:inline-block; min-width:160px;
      border-bottom:2px solid #333; margin:0 5px; vertical-align:bottom;
    }
    .mc-options { display:flex; gap:18px; flex-wrap:wrap; margin:5px 0 3px 0; }
    .mc-opt { padding:3px 14px; border:1.5px solid #a5d6a7; border-radius:4px; background:#f1f8f2; }
    .tf-row { display:inline-flex; gap:18px; margin-left:10px; }
    .tf-opt { padding:2px 12px; border:1.5px solid #a5d6a7; border-radius:4px; background:#f1f8f2; }
    .match-instructions { margin:2px 0 8px 18px; color:#555; font-size:.93em; }
    .matching { display:flex; gap:50px; margin:8px 0 10px 18px; flex-wrap:wrap; }
    .match-col { display:flex; flex-direction:column; gap:8px; }
    .match-item {
      padding:5px 14px; border:1.5px solid #a5d6a7; border-radius:6px;
      background:#f1f8f2; min-width:110px; text-align:center;
    }
    .match-blank {
      display:inline-block; min-width:26px;
      border-bottom:2px solid #333; margin-right:6px; vertical-align:bottom;
    }
    table.answer-key {
      border-collapse:collapse; width:100%;
      margin-top:12px; font-size:.93em;
    }
    table.answer-key th {
      background:#14532d; color:#fff;
      padding:7px 12px; text-align:center;
    }
    table.answer-key td {
      border:1px solid #a5d6a7; padding:6px 12px; text-align:center;
    }
    table.answer-key tr:nth-child(even) td { background:#f0faf2; }
    hr { border:none; border-top:1px solid #c8e6c9; margin:32px 0; }
    .name-line { display:flex; gap:32px; margin-bottom:20px; font-size:.97em; }
    .name-line span { white-space:nowrap; }
    .name-line .line { flex:1; border-bottom:1.5px solid #333; min-width:100px; }
    ol.q-list { padding-left:22px; margin:0; }
    ol.q-list li { margin:10px 0; }
    .answer-section { break-before:page; page-break-before:always; }
    .diagram-wrap { margin: 14px 0 4px 18px; }
    .diagram-caption { font-size:.87em; color:#666; font-style:italic; margin: 2px 0 10px 18px; }
    @media print { hr.before-answer { display:none; } }
"""

PALETTES = [
    ("#e8f5e9", "#14532d"),
    ("#e3f2fd", "#0d47a1"),
    ("#fff3e0", "#e65100"),
    ("#fce4ec", "#880e4f"),
    ("#f3e5f5", "#4a148c"),
    ("#fffde7", "#f57f17"),
]
NAMES = ["Hoa", "Linh", "Nam", "Tuan", "Bao", "Mai", "Lan", "Minh", "Thu", "Phong"]
THINGS = ["pencils", "stickers", "toys", "books", "candies", "marbles", "coins", "apples", "cards", "flowers"]

# Cross-lesson diversity trackers
_RECENT_DIAGRAMS = deque(maxlen=3)
_RECENT_TOPIC_Q = deque(maxlen=2)

def lesson_rng(n):
    return random.Random(n * 7919 + 31337)

def tier(n):
    if n <= 33:
        return 1
    if n <= 51:
        return 2
    return 3  # lessons 52–100: harder band

def hard_lesson(n):
    return n >= 52

def max_num(n):
    t = tier(n)
    if t == 1:
        return min(50 + n, 99)
    if t == 2:
        return min(180 + n * 4, 500)
    return min(450 + n * 5, 999)

def mul_max(n):
    t = tier(n)
    return {1: 5, 2: 10, 3: 12}[t]

def lesson_slot(n, which=1, count=5):
    """Rotate question templates within a unit so neighbouring lessons differ."""
    return ((n - 1) + (which - 1) * 2) % count

def _pick_avoid(rng, options, recent):
    opts = list(options)
    fresh = [o for o in opts if o not in recent]
    return rng.choice(fresh if fresh else opts)

# Per-lesson trackers (reset each build_lesson)
_RECENT_MUL = deque(maxlen=2)
_RECENT_WORD = deque(maxlen=2)
_RECENT_MEAS = deque(maxlen=2)
_RECENT_GEO = deque(maxlen=2)
_RECENT_FRAC = deque(maxlen=2)

def reset_lesson_trackers():
    _RECENT_MUL.clear()
    _RECENT_WORD.clear()
    _RECENT_MEAS.clear()
    _RECENT_GEO.clear()
    _RECENT_FRAC.clear()

def _pal(rng):
    return rng.choice(PALETTES)

def diagram(svg, caption):
    return (f'<div class="diagram-wrap">{svg}</div>'
            f'<div class="diagram-caption">{caption}</div>')

# ─── SVG helpers (deterministic, Year-3 style) ───────────────────────────────
def svg_clock(hour, minute=0, size=130):
    cx = cy = size / 2
    r = cx - 5
    def pt(deg, rad):
        a = math.radians(deg - 90)
        return cx + rad * math.cos(a), cy + rad * math.sin(a)
    ticks = []
    for i in range(60):
        ox, oy = pt(i * 6, r - 2)
        ix, iy = pt(i * 6, r - (12 if i % 5 == 0 else 7))
        ticks.append(f'<line x1="{ox:.1f}" y1="{oy:.1f}" x2="{ix:.1f}" y2="{iy:.1f}" '
                     f'stroke="#333" stroke-width="{"2.5" if i%5==0 else "1"}"/>')
    nums = []
    for n in range(1, 13):
        tx, ty = pt(n * 30, r - 18)
        nums.append(f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="middle" '
                    f'dominant-baseline="central" font-size="11" font-weight="bold" fill="#333">{n}</text>')
    mx, my = pt(minute * 6, r - 18)
    hx, hy = pt((hour % 12 + minute / 60) * 30, r - 30)
    svg = (f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" '
           f'font-family="\'Segoe UI\',Arial,sans-serif">'
           f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="white" stroke="#333" stroke-width="2.5"/>'
           f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="#333"/>'
           + "".join(ticks) + "".join(nums) +
           f'<line x1="{cx}" y1="{cy}" x2="{mx:.1f}" y2="{my:.1f}" stroke="#555" stroke-width="2.5" stroke-linecap="round"/>'
           f'<line x1="{cx}" y1="{cy}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="#333" stroke-width="4" stroke-linecap="round"/>'
           f'</svg>')
    return svg, f"{hour}:{minute:02d}"

def svg_number_line(lo, hi, mark, width=420):
    pad = 24
    span = hi - lo
    def x(v):
        return pad + (v - lo) / span * (width - 2 * pad)
    ticks = []
    step = max(1, span // 10)
    for v in range(lo, hi + 1, step):
        xx = x(v)
        ticks.append(f'<line x1="{xx:.0f}" y1="18" x2="{xx:.0f}" y2="32" stroke="#333" stroke-width="2"/>')
        ticks.append(f'<text x="{xx:.0f}" y="48" text-anchor="middle" font-size="11" fill="#333">{v}</text>')
    mx = x(mark)
    return (f'<svg width="{width}" height="58" viewBox="0 0 {width} 58" '
            f'font-family="\'Segoe UI\',Arial,sans-serif">'
            f'<line x1="{pad}" y1="25" x2="{width-pad}" y2="25" stroke="#333" stroke-width="2"/>'
            + "".join(ticks) +
            f'<circle cx="{mx:.0f}" cy="25" r="6" fill="#c0392b"/>'
            f'</svg>')

def svg_place_value(num):
    h, t, o = num // 100, (num % 100) // 10, num % 10
    leaves = []
    if num >= 100:
        parts = [("Hundreds", h, h * 100), ("Tens", t, t * 10), ("Ones", o, o)]
        xs = [40, 200, 360]
        W = 480
    else:
        parts = [("Tens", t if num >= 10 else 0, (t if num >= 10 else 0) * 10), ("Ones", o, o)]
        if num < 10:
            parts = [("Ones", o, o)]
            xs = [180]
            W = 360
        else:
            xs = [80, 280]
            W = 440
    leaf_svg = ""
    for (label, d, val), x in zip(parts, xs):
        leaf_svg += (f'<rect x="{x}" y="78" width="120" height="40" rx="6" fill="#e8f5e9" stroke="#14532d"/>'
                     f'<text x="{x+60}" y="96" text-anchor="middle" font-size="12" font-weight="bold" fill="#14532d">{d} {label}</text>'
                     f'<text x="{x+60}" y="111" text-anchor="middle" font-size="11" fill="#555">= {val}</text>'
                     f'<line x1="{W//2}" y1="44" x2="{x+60}" y2="78" stroke="#14532d" stroke-width="1.8"/>')
    return (f'<svg width="{W}" height="130" viewBox="0 0 {W} 130" font-family="\'Segoe UI\',Arial,sans-serif">'
            f'<rect x="{(W-160)//2}" y="6" width="160" height="38" rx="7" fill="#14532d"/>'
            f'<text x="{W//2}" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#fff">{num}</text>'
            + leaf_svg + '</svg>')

def svg_ten_frame(filled, total=10):
    fill, stroke = "#e8f5e9", "#14532d"
    cells = ""
    for i in range(total):
        r, c = divmod(i, 5)
        x, y = 8 + c * 36, 8 + r * 36
        cells += f'<rect x="{x}" y="{y}" width="32" height="32" fill="white" stroke="{stroke}" stroke-width="2"/>'
        if i < filled:
            cells += f'<circle cx="{x+16}" cy="{y+16}" r="10" fill="{stroke}"/>'
    return (f'<svg width="190" height="84" viewBox="0 0 190 84" font-family="\'Segoe UI\',Arial,sans-serif">'
            f'{cells}</svg>')

def svg_array(rows, cols, rng):
    fill, stroke = _pal(rng)
    cs = 22
    cells = ""
    for r in range(rows):
        for c in range(cols):
            cells += (f'<rect x="{6+c*cs}" y="{6+r*cs}" width="{cs-4}" height="{cs-4}" rx="3" '
                      f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
    W, H = cols * cs + 8, rows * cs + 8
    return (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="\'Segoe UI\',Arial,sans-serif">'
            f'{cells}</svg>')

def svg_equal_groups(groups, per, rng):
    fill, stroke = _pal(rng)
    boxes = ""
    for g in range(groups):
        x0 = 8 + g * 70
        dots = "".join(
            f'<circle cx="{x0+18+(i%3)*16}" cy="{28+(i//3)*16}" r="6" fill="{stroke}"/>'
            for i in range(per)
        )
        boxes += (f'<rect x="{x0}" y="8" width="62" height="{20+((per-1)//3+1)*16}" rx="6" '
                  f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>{dots}')
    W = groups * 70 + 10
    H = 28 + ((per - 1) // 3 + 1) * 16
    return (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="\'Segoe UI\',Arial,sans-serif">'
            f'{boxes}</svg>')

def svg_part_whole(whole, part_a, part_b, rng, hide="b"):
    fill, stroke = _pal(rng)
    a_lbl = str(part_a) if hide != "a" else "?"
    b_lbl = str(part_b) if hide != "b" else "?"
    w_lbl = str(whole) if hide != "w" else "?"
    return (f'<svg width="280" height="110" viewBox="0 0 280 110" font-family="\'Segoe UI\',Arial,sans-serif">'
            f'<rect x="60" y="8" width="160" height="40" rx="6" fill="#14532d"/>'
            f'<text x="140" y="34" text-anchor="middle" fill="#fff" font-size="16" font-weight="bold">{w_lbl}</text>'
            f'<rect x="20" y="62" width="110" height="38" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
            f'<text x="75" y="87" text-anchor="middle" fill="{stroke}" font-size="15" font-weight="bold">{a_lbl}</text>'
            f'<rect x="150" y="62" width="110" height="38" rx="6" fill="#fff8e1" stroke="#f9a825" stroke-width="2"/>'
            f'<text x="205" y="87" text-anchor="middle" fill="#7a5c00" font-size="15" font-weight="bold">{b_lbl}</text>'
            f'</svg>')

def svg_rect(w_u, h_u, rng):
    fill, stroke = _pal(rng)
    s = 12
    W, H = w_u * s + 24, h_u * s + 28
    return (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="\'Segoe UI\',Arial,sans-serif">'
            f'<rect x="12" y="8" width="{w_u*s}" height="{h_u*s}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
            f'<text x="{12+w_u*s//2}" y="{H-4}" text-anchor="middle" font-size="11" fill="{stroke}">{w_u} cm</text>'
            f'<text x="8" y="{8+h_u*s//2}" text-anchor="middle" font-size="11" fill="{stroke}" '
            f'transform="rotate(-90,8,{8+h_u*s//2})">{h_u} cm</text></svg>')

def svg_grid_area(cols, rows, shaded, rng):
    fill, stroke = _pal(rng)
    cs = 22
    cells = ""
    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c
            col = stroke if idx in shaded else fill
            cells += (f'<rect x="{2+c*cs}" y="{2+r*cs}" width="{cs-2}" height="{cs-2}" '
                      f'fill="{col}" stroke="{stroke}" stroke-width="1"/>')
    return f'<svg width="{cols*cs+4}" height="{rows*cs+4}" viewBox="0 0 {cols*cs+4} {rows*cs+4}">{cells}</svg>'

def svg_frac_bar(numer, denom, rng):
    fill, stroke = _pal(rng)
    W, H = 200, 32
    seg = W // denom
    rects = "".join(
        f'<rect x="{i*seg}" y="0" width="{seg}" height="{H}" '
        f'fill="{stroke if i < numer else fill}" stroke="white" stroke-width="1"/>'
        for i in range(denom)
    )
    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">{rects}</svg>'

def svg_frac_pie(numer, denom, rng):
    fill, stroke = _pal(rng)
    cx, cy, r = 50, 50, 40
    slices = ""
    for i in range(denom):
        a1 = math.radians(i * 360 / denom - 90)
        a2 = math.radians((i + 1) * 360 / denom - 90)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        x2, y2 = cx + r * math.cos(a2), cy + r * math.sin(a2)
        col = stroke if i < numer else fill
        large = 1 if 360 / denom > 180 else 0
        slices += (f'<path d="M{cx},{cy} L{x1:.1f},{y1:.1f} A{r},{r} 0 {large},1 {x2:.1f},{y2:.1f} Z" '
                   f'fill="{col}" stroke="white" stroke-width="1"/>')
    return f'<svg width="100" height="100" viewBox="0 0 100 100">{slices}</svg>'

def svg_frac_numberline(numer, denom):
    W = 280
    ticks = ""
    for i in range(denom + 1):
        x = 20 + i * (W - 40) / denom
        ticks += f'<line x1="{x:.0f}" y1="22" x2="{x:.0f}" y2="34" stroke="#333" stroke-width="1.5"/>'
        ticks += f'<text x="{x:.0f}" y="50" text-anchor="middle" font-size="10" fill="#333">{i}/{denom}</text>'
    tx = 20 + numer * (W - 40) / denom
    return (f'<svg width="{W}" height="58" viewBox="0 0 {W} 58" font-family="\'Segoe UI\',Arial,sans-serif">'
            f'<line x1="16" y1="28" x2="{W-16}" y2="28" stroke="#333" stroke-width="2"/>'
            f'{ticks}<circle cx="{tx:.0f}" cy="28" r="6" fill="#c0392b"/></svg>')

SHAPE_META = {
    "Circle": (0, 0), "Square": (4, 4), "Triangle": (3, 0),
    "Rectangle": (4, 2), "Pentagon": (5, 5), "Hexagon": (6, 6), "Diamond": (4, 2),
}

def svg_shape(name, rng, symmetry=False):
    fill, stroke = _pal(rng)
    bodies = {
        "Circle": f'<circle cx="40" cy="40" r="32" fill="{fill}" stroke="{stroke}" stroke-width="3"/>',
        "Square": f'<rect x="10" y="10" width="60" height="60" fill="{fill}" stroke="{stroke}" stroke-width="3"/>',
        "Triangle": f'<polygon points="40,6 74,72 6,72" fill="{fill}" stroke="{stroke}" stroke-width="3"/>',
        "Rectangle": f'<rect x="6" y="14" width="98" height="48" fill="{fill}" stroke="{stroke}" stroke-width="3"/>',
        "Pentagon": f'<polygon points="40,5 75,28 62,70 18,70 5,28" fill="{fill}" stroke="{stroke}" stroke-width="3"/>',
        "Hexagon": f'<polygon points="40,4 72,22 72,58 40,76 8,58 8,22" fill="{fill}" stroke="{stroke}" stroke-width="3"/>',
        "Diamond": f'<polygon points="40,4 76,40 40,76 4,40" fill="{fill}" stroke="{stroke}" stroke-width="3"/>',
    }
    overlay = ""
    if symmetry and name == "Square":
        overlay = (f'<line x1="10" y1="40" x2="70" y2="40" stroke="#c0392b" stroke-width="1.5" stroke-dasharray="4,3"/>'
                   f'<line x1="40" y1="10" x2="40" y2="70" stroke="#c0392b" stroke-width="1.5" stroke-dasharray="4,3"/>')
    elif symmetry and name == "Rectangle":
        overlay = (f'<line x1="6" y1="38" x2="104" y2="38" stroke="#c0392b" stroke-width="1.5" stroke-dasharray="4,3"/>'
                   f'<line x1="55" y1="14" x2="55" y2="62" stroke="#c0392b" stroke-width="1.5" stroke-dasharray="4,3"/>')
    w, h = ("110", "70") if name == "Rectangle" else ("80", "80")
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{bodies[name]}{overlay}</svg>'

def svg_angle(kind, rng):
    fill, stroke = _pal(rng)
    deg = {"right": 90, "acute": 45, "obtuse": 125}[kind]
    rad = math.radians(deg)
    x2 = 80 + 50 * math.cos(math.pi - rad)
    y2 = 80 - 50 * math.sin(math.pi - rad)
    return (f'<svg width="110" height="95" viewBox="0 0 110 95" font-family="\'Segoe UI\',Arial,sans-serif">'
            f'<line x1="20" y1="80" x2="80" y2="80" stroke="{stroke}" stroke-width="3"/>'
            f'<line x1="80" y1="80" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{stroke}" stroke-width="3"/>'
            f'<path d="M60,80 A20,20 0 0,0 {80+20*math.cos(math.pi-rad):.0f},{80-20*math.sin(math.pi-rad):.0f}" '
            f'fill="none" stroke="#c0392b" stroke-width="2"/>'
            f'</svg>')

def svg_bar_graph(items, rng):
    """items: list of (label, value)"""
    fill, stroke = _pal(rng)
    max_v = max(v for _, v in items) or 1
    bar_w, gap, base_y, max_h = 36, 18, 120, 90
    bars = ""
    for i, (lab, val) in enumerate(items):
        h = int(val / max_v * max_h)
        x = 40 + i * (bar_w + gap)
        bars += (f'<rect x="{x}" y="{base_y-h}" width="{bar_w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
                 f'<text x="{x+bar_w/2}" y="{base_y-h-6}" text-anchor="middle" font-size="11" fill="{stroke}">{val}</text>'
                 f'<text x="{x+bar_w/2}" y="{base_y+16}" text-anchor="middle" font-size="11" fill="#333">{lab}</text>')
    W = 40 + len(items) * (bar_w + gap) + 20
    return (f'<svg width="{W}" height="150" viewBox="0 0 {W} 150" font-family="\'Segoe UI\',Arial,sans-serif">'
            f'<line x1="30" y1="20" x2="30" y2="{base_y}" stroke="#333" stroke-width="2"/>'
            f'<line x1="30" y1="{base_y}" x2="{W-10}" y2="{base_y}" stroke="#333" stroke-width="2"/>'
            f'{bars}</svg>')

def svg_pictograph(items, rng):
    fill, stroke = _pal(rng)
    rows = ""
    for i, (lab, count) in enumerate(items):
        icons = "".join(
            f'<circle cx="{70+j*20}" cy="{18+i*30}" r="7" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
            for j in range(count)
        )
        rows += f'<text x="4" y="{22+i*30}" font-size="12" fill="#333">{lab}</text>{icons}'
    W = max(70 + max(c for _, c in items) * 20 + 20, 160)
    return f'<svg width="{W}" height="{len(items)*30+10}" viewBox="0 0 {W} {len(items)*30+10}">{rows}</svg>'

def svg_ruler(length_cm, rng):
    fill, stroke = _pal(rng)
    px = 16
    W = length_cm * px + 30
    marks = ""
    for i in range(length_cm + 1):
        x = 15 + i * px
        h = 12 if i % 5 == 0 else 7
        marks += f'<line x1="{x}" y1="18" x2="{x}" y2="{18+h}" stroke="{stroke}" stroke-width="1.5"/>'
        if i % 5 == 0:
            marks += f'<text x="{x}" y="46" text-anchor="middle" font-size="10" fill="{stroke}">{i}</text>'
    return (f'<svg width="{W}" height="52" viewBox="0 0 {W} 52">'
            f'<rect x="10" y="16" width="{length_cm*px+10}" height="14" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
            f'{marks}</svg>')

def svg_thermometer(temp, rng):
    fill, stroke = _pal(rng)
    y = 90 - min(temp, 40) * 1.4
    return (f'<svg width="55" height="110" viewBox="0 0 55 110">'
            f'<rect x="22" y="12" width="10" height="70" rx="5" fill="#eee" stroke="{stroke}" stroke-width="2"/>'
            f'<circle cx="27" cy="90" r="12" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
            f'<rect x="24" y="{y:.0f}" width="6" height="{90-y:.0f}" fill="#c0392b"/>'
            f'<text x="42" y="55" font-size="11" fill="{stroke}">{temp}°C</text></svg>')

# ─── MC / TF helpers ─────────────────────────────────────────────────────────
def mc_html(rng, correct, lo=0, spread=10, text_options=None):
    labels = ['A', 'B', 'C', 'D']
    if text_options:
        pool = list(text_options)
        rng.shuffle(pool)
        correct_label = None
        html = '<div class="mc-options">'
        for i, (val, is_cor) in enumerate(pool[:4]):
            lbl = labels[i]
            if is_cor:
                correct_label = lbl
            html += f'<span class="mc-opt">{lbl}) {val}</span>'
        html += '</div>'
        return html, correct_label
    wrongs, tried = set(), {correct}
    for _ in range(80):
        if len(wrongs) >= 3:
            break
        d = rng.randint(1, max(1, spread))
        for cand in (correct + d, correct - d):
            if cand not in tried and cand >= lo:
                wrongs.add(cand)
                tried.add(cand)
    extra = 1
    while len(wrongs) < 3:
        cand = correct + extra
        if cand not in tried:
            wrongs.add(cand)
        extra += 1
    pool = [(correct, True)] + [(w, False) for w in list(wrongs)[:3]]
    rng.shuffle(pool)
    correct_label = None
    html = '<div class="mc-options">'
    for i, (val, is_cor) in enumerate(pool[:4]):
        lbl = labels[i]
        if is_cor:
            correct_label = lbl
        html += f'<span class="mc-opt">{lbl}) {val}</span>'
    html += '</div>'
    return html, correct_label

def tf_html(statement, is_true):
    opts = '<span class="tf-row"><span class="tf-opt">True</span><span class="tf-opt">False</span></span>'
    return f'{statement} &nbsp;{opts}', "True" if is_true else "False"

def q_li(text):
    return f'<li class="question">{text}</li>'

# ─── Topic block helpers ─────────────────────────────────────────────────────
def topic_block(n):
    if n <= 10: return "place"
    if n <= 20: return "addsub"
    if n <= 30: return "mul"
    if n <= 40: return "div"
    if n <= 50: return "ops"
    if n <= 60: return "frac"
    if n <= 70: return "measure"
    if n <= 80: return "geo"
    if n <= 90: return "data"
    return "review"

# ─── Section builders ────────────────────────────────────────────────────────
def sec_topic(n, rng, which):
    """Sections 1–2: topic-focused with diagrams."""
    block = topic_block(n)
    topic, _ = LESSONS[n]
    html = '<ol class="q-list">'
    answers = []
    t = tier(n)
    hi = max_num(n)
    slot = lesson_slot(n, which, 5)
    hard = hard_lesson(n)
    used_diag = []

    def add(q, ans, diag=None, caption=None):
        nonlocal html
        answers.append((str(len(answers) + 1), ans))
        body = q
        if diag:
            body += "<br>" + diagram(diag, caption or "")
            used_diag.append(caption or "diag")
        html += q_li(body)

    # Build 5 questions based on block
    if block == "place":
        if slot == 0:
            num = rng.randint(10, hi)
            add(f'What is the value of the digit <strong>{(num//10)%10}</strong> in <strong>{num}</strong>? '
                f'<span class="blank"></span>',
                str(((num // 10) % 10) * 10),
                svg_place_value(num), f"Place value of {num}")
            add(f'Expanded form: {num} = <span class="blank"></span> tens + <span class="blank"></span> ones',
                f"{num//10} tens, {num%10} ones", svg_place_value(num), f"{num}")
        elif slot == 1:
            num = rng.randint(10, hi)
            add(f'How many tens in <strong>{num}</strong>? <span class="blank"></span>', str(num // 10))
            add(f'How many ones in <strong>{num}</strong>? <span class="blank"></span>', str(num % 10),
                svg_place_value(num), f"{num}")
        else:
            num = rng.randint(10, hi)
            add(f'What is the value of the tens digit in <strong>{num}</strong>? <span class="blank"></span>',
                str((num // 10) * 10), svg_place_value(num), f"Place value of {num}")
        a, b = rng.randint(10, hi), rng.randint(10, hi)
        sym = ">" if a > b else ("<" if a < b else "=")
        add(f'Fill in &gt;, &lt;, or =: {a} <span class="blank"></span> {b}', sym)
        lo, hi_nl = 0, min(100, ((hi // 10) + 1) * 10)
        mark = rng.randint(lo + 5, hi_nl - 5)
        add(f'What number is marked on the number line? <span class="blank"></span>',
            str(mark), svg_number_line(lo, hi_nl, mark), f"Number line {lo}–{hi_nl}")
        if slot % 2 == 0:
            filled = rng.randint(3, 9)
            add(f'How many counters are in the ten-frame? <span class="blank"></span>',
                str(filled), svg_ten_frame(filled), "Ten-frame")
        else:
            skip = rng.choice([2, 5, 10])
            start = rng.randint(1, 5) * skip
            seq = [start + i * skip for i in range(5)]
            add(f'What comes next? {", ".join(map(str, seq[:4]))}, <span class="blank"></span>',
                str(seq[4]))

    elif block == "addsub":
        a = rng.randint(15, hi // 2 if hi > 40 else 40)
        b = rng.randint(10, min(a - 1, 40))
        whole = a + b
        hide = rng.choice(["b", "a", "w"])
        ans = {"a": a, "b": b, "w": whole}[hide]
        add(f'Find the missing number in the part–whole model. <span class="blank"></span>',
            str(ans), svg_part_whole(whole, a, b, rng, hide=hide), "Part–whole model")
        x, y = rng.randint(20, min(hi, 80)), rng.randint(15, 40)
        add(f'{x} + {y} = <span class="blank"></span>', str(x + y))
        x, y = rng.randint(40, min(hi, 99)), rng.randint(10, 35)
        if x <= y:
            x = y + 10
        add(f'{x} − {y} = <span class="blank"></span>', str(x - y))
        x, y = rng.randint(12, 40), rng.randint(12, 40)
        opt, lbl = mc_html(rng, x + y, lo=1, spread=8)
        add(f'{x} + {y} = ?{opt}', f"{lbl}) {x+y}")
        stmt_ok = rng.random() < 0.5
        x, y = rng.randint(20, 50), rng.randint(10, 20)
        shown = x + y if stmt_ok else x + y + rng.choice([-2, 2])
        qh, ans = tf_html(f"<strong>{x} + {y} = {shown}</strong>", shown == x + y)
        add(qh, ans)

    elif block in ("mul", "div", "ops"):
        rows, cols = rng.randint(2, 4), rng.randint(3, 6)
        product = rows * cols
        add(f'How many squares are in this array? <span class="blank"></span>',
            str(product), svg_array(rows, cols, rng), f"{rows} × {cols} array")
        g, p = rng.randint(2, 5), rng.randint(2, 6)
        add(f'There are <strong>{g}</strong> equal groups with <strong>{p}</strong> in each. Total? '
            f'<span class="blank"></span>',
            str(g * p), svg_equal_groups(g, p, rng), f"{g} groups of {p}")
        a, b = rng.randint(2, mul_max(n)), rng.randint(2, mul_max(n))
        if block == "div":
            add(f'{a*b} ÷ {a} = <span class="blank"></span>', str(b))
            add(f'{a*b} ÷ {b} = <span class="blank"></span>', str(a))
        else:
            add(f'{a} × {b} = <span class="blank"></span>', str(a * b))
            c, d = rng.randint(2, mul_max(n)), rng.randint(2, mul_max(n))
            opt, lbl = mc_html(rng, c * d, lo=1, spread=max(5, c * d // 4))
            add(f'{c} × {d} = ?{opt}', f"{lbl}) {c*d}")
        if block == "ops":
            a, b, c = rng.randint(2, 6), rng.randint(2, 6), rng.randint(5, 20)
            add(f'{a} × {b} + {c} = <span class="blank"></span>', str(a * b + c))
        else:
            a, b = rng.randint(2, mul_max(n)), rng.randint(2, mul_max(n))
            add(f'{a} × {b} = <span class="blank"></span>', str(a * b))

    elif block == "frac":
        denom = rng.choice([2, 3, 4, 6, 8] if hard else [2, 3, 4])
        numer = rng.randint(1, denom - 1)
        if slot in (0, 2):
            style = "pie" if slot == 0 else "bar"
            svg = svg_frac_pie(numer, denom, rng) if style == "pie" else svg_frac_bar(numer, denom, rng)
            add(f'What fraction is shaded? <span class="blank"></span>',
                f"{numer}/{denom}", svg, "Shaded fraction")
        else:
            numer2 = rng.randint(1, denom - 1)
            add(f'What fraction is marked? <span class="blank"></span>',
                f"{numer2}/{denom}", svg_frac_numberline(numer2, denom), "Fraction number line")
        if slot == 1:
            whole = denom * rng.randint(2, 6 if hard else 4)
            add(f'{numer}/{denom} of {whole} = <span class="blank"></span>', str(numer * whole // denom))
        elif slot == 3:
            add(f'Equivalent to 1/2: <span class="blank"></span>/4', "2")
        else:
            add(f'Which is larger: <strong>1/2</strong> or <strong>1/4</strong>? <span class="blank"></span>', "1/2")
        if slot == 4:
            add(f'How many quarters make one whole? <span class="blank"></span>', "4")
        else:
            add(f'Shade shows 1 out of 4 equal parts. Fraction: <span class="blank"></span>',
                "1/4", svg_frac_pie(1, 4, rng), "One quarter")
        if hard:
            add(f'Compare: {numer}/{denom} vs 1/{denom}. Larger? <span class="blank"></span>',
                f"{numer}/{denom}" if numer > 1 else f"1/{denom}")
        else:
            add(f'How many halves make one whole? <span class="blank"></span>', "2")

    elif block == "measure":
        if slot == 0:
            length = rng.randint(4, 12 if hard else 10)
            add(f'How long is the object? <span class="blank"></span> cm',
                f"{length} cm", svg_ruler(length, rng), "Ruler")
        elif slot == 1:
            mv, cm = rng.randint(1, 5), rng.randint(100, 450 if hard else 350)
            longer = f"{mv} m" if mv * 100 > cm else (f"{cm} cm" if cm > mv * 100 else "equal")
            add(f'Which is longer: <strong>{mv} m</strong> or <strong>{cm} cm</strong>? <span class="blank"></span>', longer)
        else:
            temp = rng.randint(12, 38 if hard else 32)
            add(f'What temperature is shown? <span class="blank"></span> °C',
                f"{temp} °C", svg_thermometer(temp, rng), "Thermometer")
        h, m = rng.randint(1, 12), rng.choice([0, 15, 30, 45] if hard else [0, 30])
        clock, ts = svg_clock(h, m)
        add(f'What time does the clock show? <span class="blank"></span>',
            ts, clock, f"Clock showing {ts}")
        if slot >= 2 and hard:
            w, h_u = rng.randint(4, 12), rng.randint(3, 9)
            add(f'Perimeter of {w}×{h_u} cm rectangle? <span class="blank"></span> cm',
                f"{2*(w+h_u)} cm", svg_rect(w, h_u, rng), "Rectangle")
        else:
            add(f'How many minutes are in <strong>2</strong> hours? <span class="blank"></span>', "120")
        if hard:
            add(f'How many cm in <strong>3</strong> metres? <span class="blank"></span>', "300")
        else:
            mv, cm = rng.randint(1, 4), rng.randint(80, 350)
            longer = f"{mv} m" if mv * 100 > cm else (f"{cm} cm" if cm > mv * 100 else "equal")
            add(f'Longer: <strong>{mv} m</strong> or <strong>{cm} cm</strong>? <span class="blank"></span>', longer)

    elif block == "geo":
        sname = rng.choice(list(SHAPE_META))
        sides = SHAPE_META[sname][0]
        add(f'Name this shape: <span class="blank"></span>',
            sname, svg_shape(sname, rng), sname)
        s2 = rng.choice([s for s in SHAPE_META if s != "Circle"])
        add(f'How many sides does a <strong>{s2}</strong> have? <span class="blank"></span>',
            str(SHAPE_META[s2][0]), svg_shape(s2, rng), s2)
        kind = rng.choice(["right", "acute", "obtuse"])
        label = {"right": "Right angle", "acute": "Acute angle", "obtuse": "Obtuse angle"}[kind]
        add(f'What type of angle is shown? <span class="blank"></span>',
            label, svg_angle(kind, rng), "Angle")
        sq = rng.choice(["Square", "Rectangle"])
        add(f'Count the dashed symmetry lines on the <strong>{sq}</strong>: <span class="blank"></span>',
            str(SHAPE_META[sq][1]), svg_shape(sq, rng, symmetry=True), f"{sq} with symmetry lines")
        w, h = rng.randint(3, 8), rng.randint(2, 6)
        add(f'Perimeter of this rectangle? <span class="blank"></span> cm',
            f"{2*(w+h)} cm", svg_rect(w, h, rng), "Rectangle")

    elif block == "data":
        items = [("Mon", rng.randint(2, 10 if hard else 8)), ("Tue", rng.randint(2, 10 if hard else 8)),
                 ("Wed", rng.randint(2, 10 if hard else 8)), ("Thu", rng.randint(2, 10 if hard else 8))]
        if slot % 2 == 0:
            target = items[(n + which) % len(items)]
            add(f'How many on <strong>{target[0]}</strong>? <span class="blank"></span>',
                str(target[1]), svg_bar_graph(items[:3], rng), "Bar graph")
            add(f'Which day has the most? <span class="blank"></span>',
                max(items, key=lambda x: x[1])[0])
        else:
            fruits = [("Apples", rng.randint(2, 6)), ("Pears", rng.randint(2, 6)),
                      ("Bananas", rng.randint(2, 6))]
            fi = rng.randint(0, 2)
            add(f'Each ● = 1 fruit. How many <strong>{fruits[fi][0]}</strong>? <span class="blank"></span>',
                str(fruits[fi][1]), svg_pictograph(fruits, rng), "Pictograph (● = 1)")
            add(f'Total fruit shown? <span class="blank"></span>',
                str(sum(f for _, f in fruits)))
        skip = rng.choice([2, 3, 5, 6 if hard else 5, 10])
        start = skip
        seq = [start + i * skip for i in range(5)]
        add(f'Rule: add {skip}. Missing: {seq[0]}, {seq[1]}, ___, {seq[3]}, {seq[4]} → '
            f'<span class="blank"></span>', str(seq[2]))
        add(f'Total for Mon + Tue? <span class="blank"></span>', str(items[0][1] + items[1][1]))
        if hard:
            add(f'Mean of Mon–Wed? <span class="blank"></span>',
                str((items[0][1] + items[1][1] + items[2][1]) // 3))
        else:
            add(f'Difference Wed − Mon? <span class="blank"></span>',
                str(items[2][1] - items[0][1]))

    else:  # review — mix rotates by slot
        order = list(range(5))
        start = (slot + which - 1) % 5
        order = order[start:] + order[:start]
        for idx in order:
            if len(answers) >= 5:
                break
            if idx == 0:
                num = rng.randint(20, hi)
                add(f'Expanded form of <strong>{num}</strong>: '
                    f'<span class="blank"></span> tens, <span class="blank"></span> ones',
                    f"{num//10} tens, {num%10} ones", svg_place_value(num), f"{num}")
            elif idx == 1:
                rows, cols = 3, rng.randint(3, 6 if hard else 5)
                add(f'Array total: <span class="blank"></span>',
                    str(rows * cols), svg_array(rows, cols, rng), f"{rows}×{cols}")
            elif idx == 2:
                numer, denom = rng.randint(1, 3), 4
                add(f'Shaded fraction: <span class="blank"></span>',
                    f"{numer}/{denom}", svg_frac_pie(numer, denom, rng), "Fraction")
            elif idx == 3:
                h, m = rng.randint(1, 12), rng.choice([0, 15, 30, 45] if hard else [0, 30])
                clock, ts = svg_clock(h, m)
                add(f'Time shown: <span class="blank"></span>', ts, clock, "Clock")
            else:
                items = [("A", rng.randint(3, 9)), ("B", rng.randint(3, 9)), ("C", rng.randint(3, 9))]
                add(f'Who has the most? <span class="blank"></span>',
                    max(items, key=lambda x: x[1])[0], svg_bar_graph(items, rng), "Bar graph")
        if hard and len(answers) < 5:
            a, b, c = rng.randint(2, 6), rng.randint(2, 6), rng.randint(10, 30)
            add(f'{a} × {b} + {c} = <span class="blank"></span> <small>(× first)</small>', str(a * b + c))

    # Ensure exactly 5
    while len(answers) < 5:
        a, b = rng.randint(5, 20), rng.randint(2, 9)
        add(f'{a} + {b} = <span class="blank"></span>', str(a + b))
    html += '</ol>'
    title = f"Section {which}: {topic} (15 mins)"
    _RECENT_DIAGRAMS.extend(used_diag[-2:])
    return title, html, answers

def sec_muldiv(n, rng):
    t = tier(n)
    hard = hard_lesson(n)
    tmax = mul_max(n)
    slot = lesson_slot(n, 1, 5)
    html = '<ol class="q-list">'
    answers = []

    q_specs = []

    if slot == 0:
        rows, cols = rng.randint(2, 4), rng.randint(3, 5)
        q_specs.append((f'Write a multiplication for this array. '
                        f'<span class="blank"></span> × <span class="blank"></span> = <span class="blank"></span><br>'
                        + diagram(svg_array(rows, cols, rng), f"{rows} rows of {cols}"),
                        f"{rows} × {cols} = {rows*cols}"))
        a, b = rng.randint(2, tmax), rng.randint(2, tmax)
        q_specs.append((f'{a} × {b} = <span class="blank"></span>', str(a * b)))
        b2 = rng.randint(2, tmax)
        q_specs.append((f'{a*b} ÷ {a} = <span class="blank"></span>', str(b)))
        g, p = rng.randint(2, 5), rng.randint(2, 6)
        q_specs.append((f'{g} groups of {p} = <span class="blank"></span><br>'
                        + diagram(svg_equal_groups(g, p, rng), f"{g} groups of {p}"),
                        str(g * p)))
        c, d = rng.randint(2, tmax), rng.randint(2, tmax)
        opt, lbl = mc_html(rng, c * d, lo=1, spread=max(4, c * d // 3))
        q_specs.append((f'{c} × {d} = ?{opt}', f"{lbl}) {c*d}"))

    elif slot == 1:
        g, p = rng.randint(3, 6), rng.randint(3, 7)
        q_specs.append((f'Draw meaning: {g} × {p}. Total squares?<br>'
                        + diagram(svg_array(min(g, 4), min(p, 6), rng), "Array model"),
                        str(g * p)))
        for a, b in [(rng.randint(2, tmax), rng.randint(2, tmax)) for _ in range(2)]:
            q_specs.append((f'{a} × {b} = <span class="blank"></span>', str(a * b)))
        total = rng.randint(3, tmax) * rng.randint(2, tmax)
        div = rng.randint(2, tmax)
        while total % div:
            div = rng.randint(2, 5)
            total = div * rng.randint(3, 8)
        q_specs.append((f'{total} ÷ {div} = <span class="blank"></span>', str(total // div)))
        if hard:
            x, y = rng.randint(12, 45), rng.randint(2, 9)
            q_specs.append((f'{x} × {y} = <span class="blank"></span>', str(x * y)))
        else:
            skip = rng.choice([2, 5, 10])
            seq = [skip * i for i in range(1, 6)]
            q_specs.append((f'Skip count by {skip}: {seq[0]}, {seq[1]}, ___, {seq[3]}, {seq[4]} → '
                            f'<span class="blank"></span>', str(seq[2])))

    elif slot == 2:
        a, b = rng.randint(2, tmax), rng.randint(2, tmax)
        prod = a * b
        q_specs.append((f'Missing factor: <span class="blank"></span> × {b} = {prod}', str(a)))
        q_specs.append((f'Fact family: {a} × {b} = {prod}, so {prod} ÷ {a} = <span class="blank"></span>', str(b)))
        q_specs.append((f'Also {prod} ÷ {b} = <span class="blank"></span>', str(a)))
        rows, cols = rng.randint(2, 3), rng.randint(4, 6)
        q_specs.append((f'Repeated addition: {cols} + {cols} + … ({rows} times) = <span class="blank"></span><br>'
                        + diagram(svg_array(rows, cols, rng), f"{rows} rows of {cols}"),
                        str(rows * cols)))
        if hard:
            extra = ((n * 3) % 15) + 5
            q_specs.append((f'Order: {a} × {b} + {extra} = <span class="blank"></span> '
                            f'<br><small>(× first)</small>', str(a * b + extra)))
        else:
            x, y = rng.randint(2, tmax), rng.randint(2, tmax)
            q_specs.append((f'{x} × {y} = <span class="blank"></span>', str(x * y)))

    elif slot == 3:
        pairs = [(rng.randint(2, tmax), rng.randint(2, tmax)) for _ in range(3)]
        for a, b in pairs:
            q_specs.append((f'{a} × {b} = <span class="blank"></span>', str(a * b)))
        a, b = pairs[0]
        q_specs.append((f'Which is greater: {a}×{b} or {(a-1)*b if a > 2 else a*(b+1)}? '
                        f'<span class="blank"></span>', f"{a}×{b}"))
        total, groups = rng.randint(4, 8) * rng.randint(3, 6), rng.randint(3, 6)
        while total % groups:
            groups = rng.randint(3, 5)
            total = groups * rng.randint(4, 7)
        q_specs.append((f'{total} shared into {groups} equal groups. Each group? <span class="blank"></span>',
                        str(total // groups)))

    else:  # slot 4
        if hard:
            x, m = rng.randint(11, 35), rng.randint(2, 9)
            q_specs.append((f'2-digit × 1-digit: {x} × {m} = <span class="blank"></span>', str(x * m)))
        a, b = rng.randint(2, tmax), rng.randint(2, tmax)
        q_specs.append((f'{a} × {b} = <span class="blank"></span>', str(a * b)))
        q_specs.append((f'{a*b} ÷ {b} = <span class="blank"></span>', str(a)))
        g, p = rng.randint(2, 5), rng.randint(2, 6)
        q_specs.append((f'Equal groups diagram total?<br>'
                        + diagram(svg_equal_groups(g, p, rng), f"{g} groups of {p}"),
                        str(g * p)))
        c, d, e = rng.randint(2, 5), rng.randint(2, 5), rng.randint(8, 25)
        q_specs.append((f'{c} × {d} + {e} = <span class="blank"></span>', str(c * d + e)))
        if len(q_specs) < 5:
            q_specs.append((f'{b} × {a} = <span class="blank"></span>', str(a * b)))

    for q, ans in q_specs[:5]:
        html += q_li(q)
        answers.append((str(len(answers) + 1), ans))
    html += '</ol>'
    _RECENT_MUL.append(slot)
    return "Section 3: Multiplication &amp; Division (15 mins)", html, answers


def sec_word(n, rng):
    hi = max_num(n)
    hard = hard_lesson(n)
    thing = rng.choice(THINGS)
    name = rng.choice(NAMES)
    slot = lesson_slot(n, 2, 5)
    html = '<ol class="q-list">'
    answers = []

    templates = []

    if slot == 0:
        a, b = rng.randint(12, min(40, hi // 2 + 10)), rng.randint(8, 25)
        templates.append((f'<strong>{name}</strong> has <strong>{a} {thing}</strong> and gets '
                          f'<strong>{b} more</strong>. Total?<br>'
                          + diagram(svg_part_whole(a + b, a, b, rng, hide="w"), "Part–whole")
                          + f'Answer: <span class="blank"></span>', str(a + b)))
        have, give = rng.randint(25, min(60, hi)), rng.randint(5, 20)
        templates.append((f'<strong>{rng.choice(NAMES)}</strong> has {have} {thing} and gives away {give}. '
                          f'Left? <span class="blank"></span>', str(have - give)))
        g, p = rng.randint(3, 6), rng.randint(3, 8)
        templates.append((f'{g} boxes × {p} {thing}. Total?<br>'
                          + diagram(svg_equal_groups(min(g, 5), min(p, 6), rng), "Equal groups")
                          + f'Answer: <span class="blank"></span>', str(g * p)))
        total, groups = rng.randint(4, 9) * rng.randint(3, 6), rng.randint(3, 6)
        while total % groups:
            groups = rng.randint(3, 5)
            total = groups * rng.randint(4, 8)
        templates.append((f'{total} {thing} shared equally into {groups} groups. Each? <span class="blank"></span>',
                          str(total // groups)))
        price, qty = rng.choice([2000, 5000, 10000]), rng.randint(2, 5)
        templates.append((f'Each costs {price:,} VND. Buy {qty}. Total? <span class="blank"></span> VND'.replace(",", "."),
                          str(price * qty)))

    elif slot == 1:
        red, blue = rng.randint(8, 25), rng.randint(8, 25)
        while red == blue:
            blue = rng.randint(8, 25)
        more = "red" if red > blue else "blue"
        templates.append((f'{red} red and {blue} blue {thing}. Which colour has more? <span class="blank"></span>',
                          more))
        a, b = rng.randint(20, min(70, hi)), rng.randint(10, 35)
        templates.append((f'{a} − {b} = ?  (story: {name} had {a}, used {b}) <span class="blank"></span>', str(a - b)))
        g, p = rng.randint(3, 7), rng.randint(3, 9)
        templates.append((f'{name} packs {g} bags with {p} {thing} each. Total? <span class="blank"></span>', str(g * p)))
        trays, per_t = rng.randint(3, 6), rng.randint(4, 8)
        templates.append((f'{trays} trays with {per_t} each. How many {thing}? <span class="blank"></span>',
                          str(trays * per_t)))
        if hard:
            a, b, c = rng.randint(30, 80), rng.randint(2, 6), rng.randint(2, 6)
            templates.append((f'{a} {thing}, then {b} groups of {c} more arrive. Total? <span class="blank"></span>',
                              str(a + b * c)))
        else:
            templates.append((f'How many more: {red} or {blue}? Difference? <span class="blank"></span>',
                              str(abs(red - blue))))

    elif slot == 2:
        start = rng.randint(15, 40)
        more = rng.randint(5, 20)
        templates.append((f'{name} collects {start} {thing}, then {more} more. Total? <span class="blank"></span>',
                          str(start + more)))
        total = rng.randint(5, 9) * rng.randint(4, 8)
        groups = rng.randint(3, 6)
        while total % groups:
            groups = rng.randint(3, 5)
            total = groups * rng.randint(5, 8)
        templates.append((f'{total} {thing} ÷ {groups} groups = <span class="blank"></span> each', str(total // groups)))
        price = rng.choice([3000, 7000, 12000, 15000])
        paid = price * rng.randint(2, 4)
        templates.append((f'Paid {paid:,} VND for {price:,} VND items. How many bought? <span class="blank"></span>'.replace(",", "."),
                          str(paid // price)))
        w, h = rng.randint(3, 8), rng.randint(2, 6)
        templates.append((f'A rectangle sticker is {w} cm by {h} cm. Perimeter? <span class="blank"></span> cm',
                          str(2 * (w + h))))
        if hard:
            trays, per_t, give = rng.randint(4, 7), rng.randint(5, 9), rng.randint(8, 20)
            templates.append((f'{trays}×{per_t} {thing}, then {give} given away. Left? <span class="blank"></span>',
                              str(trays * per_t - give)))
        else:
            a, b = rng.randint(10, 30), rng.randint(2, 9)
            templates.append((f'{a} × {b} stickers on a page. Total? <span class="blank"></span>', str(a * b)))

    elif slot == 3:
        d1, d2 = rng.randint(10, 30), rng.randint(10, 30)
        templates.append((f'Monday {d1}, Tuesday {d2}. Total for two days? <span class="blank"></span>', str(d1 + d2)))
        templates.append((f'Difference between {max(d1,d2)} and {min(d1,d2)}? <span class="blank"></span>',
                          str(abs(d1 - d2))))
        g, p = rng.randint(4, 8), rng.randint(3, 7)
        templates.append((f'{g} rows of {p} {thing}. Total?<br>'
                          + diagram(svg_array(min(g, 4), min(p, 6), rng), "Array")
                          + f'Answer: <span class="blank"></span>', str(g * p)))
        if hard:
            a, b, c = rng.randint(2, 6), rng.randint(2, 6), rng.randint(10, 30)
            templates.append((f'{a} × {b} + {c} = ? <span class="blank"></span> <small>(× first)</small>',
                              str(a * b + c)))
            templates.append((f'{a} × {b} − {c} = ? <span class="blank"></span> <small>(× first)</small>',
                              str(a * b - c)))
        else:
            have, need = rng.randint(20, 50), rng.randint(30, 70)
            templates.append((f'Has {have}, needs {need}. How many more? <span class="blank"></span>', str(need - have)))
            templates.append((f'{have} + {need - have} = <span class="blank"></span>', str(need)))

    else:  # slot 4 — mixed / challenge stories
        if hard:
            a, b, c = rng.randint(40, 120), rng.randint(3, 8), rng.randint(3, 8)
            templates.append((f'Store has {a} {thing}. Sells {b} bags of {c}. Left? <span class="blank"></span>',
                              str(a - b * c)))
            x, m = rng.randint(12, 35), rng.randint(3, 9)
            templates.append((f'{x} packs × {m} {thing} each = <span class="blank"></span>', str(x * m)))
        else:
            a, b = rng.randint(15, 45), rng.randint(8, 25)
            templates.append((f'{a} + {b} = ? <span class="blank"></span>', str(a + b)))
            templates.append((f'{a + b} − {b} = <span class="blank"></span>', str(a)))
        total, r1, r2 = rng.choice([24, 36, 48]), 2, 3
        templates.append((f'Share {total} in ratio {r1}:{r2} (smaller share)? <span class="blank"></span>',
                          str(total * r1 // (r1 + r2))))
        sh, sm, ah, am = rng.randint(7, 14), rng.choice([0, 15, 30]), rng.randint(1, 3), rng.choice([0, 15, 30])
        em = (sm + am) % 60
        eh = (sh + ah + (sm + am) // 60) % 24
        templates.append((f'Start {sh}:{sm:02d}, wait {ah}h {am}min. Time? <span class="blank"></span>',
                          f"{eh}:{em:02d}"))

    while len(templates) < 5:
        a, b = rng.randint(3, 9), rng.randint(3, 9)
        templates.append((f'{a} × {b} = <span class="blank"></span>', str(a * b)))

    html = '<ol class="q-list">' + "".join(q_li(q) for q, _ in templates[:5]) + '</ol>'
    answers = [(str(i + 1), a) for i, (_, a) in enumerate(templates[:5])]
    _RECENT_WORD.append(slot)
    return "Section 4: Word Problems (20 mins)", html, answers


def sec_measure(n, rng):
    t = tier(n)
    hard = hard_lesson(n)
    slot = lesson_slot(n, 3, 5)
    html = '<ol class="q-list">'
    answers = []

    def add(q, ans, diag=None, cap=None):
        answers.append((str(len(answers) + 1), ans))
        body = q + (("<br>" + diagram(diag, cap)) if diag else "")
        nonlocal html
        html += q_li(body)

    facts = [
        ("minutes in {a} hour(s)", lambda a: a * 60, (2, 5 if not hard else 6)),
        ("cm in {a} metre(s)", lambda a: a * 100, (2, 6)),
        ("g in {a} kg", lambda a: a * 1000, (2, 4)),
        ("days in {a} week(s)", lambda a: a * 7, (2, 6)),
        ("months in {a} year(s)", lambda a: a * 12, (1, 2)),
    ]
    fact = facts[(n + slot) % len(facts)]
    a_val = rng.randint(*fact[2])
    add(f'How many {fact[0].format(a=a_val)}? <span class="blank"></span>', str(fact[1](a_val)))

    if slot % 2 == 0:
        sh, sm = rng.randint(7, 16), rng.choice([0, 15, 30, 45] if hard else [0, 30])
        add_h, add_m = rng.randint(1, 4 if hard else 3), rng.choice([0, 15, 30, 45])
        tot = sm + add_m
        eh = (sh + add_h + tot // 60) % 24
        em = tot % 60
        add(f'Start <strong>{sh}:{sm:02d}</strong>. After <strong>{add_h}h {add_m}min</strong>, time? '
            f'<span class="blank"></span>', f"{eh}:{em:02d}")
    else:
        h1, m1 = rng.randint(8, 14), rng.choice([0, 15, 30, 45])
        h2, m2 = rng.randint(1, 5), rng.choice([0, 15, 30, 45])
        start_m = h1 * 60 + m1
        end_m = h2 * 60 + m2
        diff = end_m - start_m if end_m > start_m else (12 * 60 + end_m) - start_m
        add(f'From {h1}:{m1:02d} to {h2}:{m2:02d} (same morning) is how many minutes? '
            f'<span class="blank"></span>', str(diff))

    mv, cm = rng.randint(1, 5 if hard else 4), rng.randint(80, 450 if hard else 350)
    longer = f"{mv} m" if mv * 100 > cm else (f"{cm} cm" if cm > mv * 100 else "equal")
    add(f'Longer: <strong>{mv} m</strong> or <strong>{cm} cm</strong>? <span class="blank"></span>', longer)

    choice = _pick_avoid(rng, ["clock", "ruler", "thermo"], _RECENT_MEAS)
    _RECENT_MEAS.append(choice)
    if choice == "clock":
        h, m = rng.randint(1, 12), rng.choice([0, 15, 30, 45] if t >= 2 else [0, 30])
        clock, ts = svg_clock(h, m)
        add(f'What time does the clock show?', ts, clock, f"Clock {ts}")
    elif choice == "ruler":
        length = rng.randint(4, 14 if hard else 12)
        add(f'Read the ruler length: <span class="blank"></span> cm', f"{length} cm",
            svg_ruler(length, rng), "Ruler")
    else:
        temp = rng.randint(10, 38 if hard else 32)
        add(f'Read the thermometer: <span class="blank"></span> °C', f"{temp} °C",
            svg_thermometer(temp, rng), "Thermometer")

    if hard and slot >= 2:
        w, h = rng.randint(4, 12), rng.randint(3, 9)
        add(f'Perimeter AND area: rectangle {w} cm × {h} cm. Perimeter = <span class="blank"></span> cm, '
            f'Area = <span class="blank"></span> cm²', f"P={2*(w+h)} cm, A={w*h} cm²",
            svg_rect(w, h, rng), "Rectangle")
    else:
        w, h = rng.randint(3, 9), rng.randint(2, 7)
        add(f'Perimeter of this rectangle? <span class="blank"></span> cm', f"{2*(w+h)} cm",
            svg_rect(w, h, rng), "Rectangle")

    html += '</ol>'
    return "Section 5: Measurement &amp; Time (10 mins)", html, answers


def sec_geo_data(n, rng):
    t = tier(n)
    hard = hard_lesson(n)
    slot = lesson_slot(n, 4, 5)
    html = '<ol class="q-list">'
    answers = []

    def add(q, ans, diag=None, cap=None):
        answers.append((str(len(answers) + 1), ans))
        body = q + (("<br>" + diagram(diag, cap)) if diag else "")
        nonlocal html
        html += q_li(body)

    modes = ["shape", "sym", "angle", "area", "bar", "picto", "tf"]
    order = modes[slot:] + modes[:slot]
    used = 0

    if "shape" in order[:3]:
        sname = rng.choice(list(SHAPE_META))
        add(f'Name this shape: <span class="blank"></span>', sname, svg_shape(sname, rng), sname)
        used += 1
    if used < 5 and "sym" in order:
        sq = rng.choice(["Square", "Rectangle", "Diamond"])
        add(f'Lines of symmetry on this {sq}? <span class="blank"></span>',
            str(SHAPE_META[sq][1]), svg_shape(sq, rng, symmetry=(sq in ("Square", "Rectangle"))), sq)
        used += 1
    if used < 5 and "angle" in order and t >= 2:
        kind = rng.choice(["right", "acute", "obtuse"])
        label = {"right": "Right angle", "acute": "Acute angle", "obtuse": "Obtuse angle"}[kind]
        add(f'Angle type? <span class="blank"></span>', label, svg_angle(kind, rng), "Angle")
        used += 1
    if used < 5 and "area" in order:
        cols, rows = rng.randint(3, 6 if hard else 5), rng.randint(2, 5)
        shaded = set(rng.sample(range(cols * rows), rng.randint(3, cols * rows - 1)))
        add(f'Each square = 1 cm². Shaded area? <span class="blank"></span>',
            f"{len(shaded)} cm²", svg_grid_area(cols, rows, shaded, rng), "Area grid")
        used += 1
    if used < 5 and "bar" in order:
        labs = ["Red", "Blue", "Green", "Yellow"][:3 + (1 if hard else 0)]
        items = [(lab, rng.randint(2, 10 if hard else 8)) for lab in labs[:3]]
        add(f'Which colour has the most? <span class="blank"></span>',
            max(items, key=lambda x: x[1])[0], svg_bar_graph(items, rng), "Bar graph")
        used += 1
    if used < 5 and "picto" in order:
        fruits = [("Apples", rng.randint(2, 6)), ("Pears", rng.randint(2, 6)), ("Bananas", rng.randint(2, 6))]
        fi = rng.randint(0, 2)
        add(f'Each ● = 1. How many {fruits[fi][0]}? <span class="blank"></span>',
            str(fruits[fi][1]), svg_pictograph(fruits, rng), "Pictograph")
        used += 1
    while used < 5:
        facts = [
            ("A triangle has 3 sides.", True),
            ("A square has 5 sides.", False),
            ("A hexagon has 6 sides.", True),
            ("A circle has 4 vertices.", False),
            ("A right angle is 90°.", True),
        ]
        stmt, ok = facts[(n + used) % len(facts)]
        qh, ans = tf_html(stmt, ok)
        add(qh, ans)
        used += 1

    html += '</ol>'
    _RECENT_GEO.append(slot)
    return "Section 6: Geometry &amp; Data (10 mins)", html, answers


def sec_fractions(n, rng):
    t = tier(n)
    hard = hard_lesson(n)
    slot = lesson_slot(n, 5, 5)
    html = '<ol class="q-list">'
    answers = []
    denoms = [2, 3, 4] if t == 1 else ([2, 3, 4, 5, 6, 8] if hard else [2, 3, 4, 5, 6])

    styles = ["pie", "bar", "numberline", "set", "compare"]
    rot = styles[slot:] + styles[:slot]

    def add(q, ans, diag=None, cap=None):
        answers.append((str(len(answers) + 1), ans))
        body = q + (("<br>" + diagram(diag, cap)) if diag else "")
        nonlocal html
        html += q_li(body)

    for style in rot:
        if len(answers) >= 5:
            break
        d = rng.choice(denoms)
        num = rng.randint(1, d - 1)
        if style == "pie":
            add(f'Fraction of the circle shaded? <span class="blank"></span>',
                f"{num}/{d}", svg_frac_pie(num, d, rng), "Fraction circle")
        elif style == "bar":
            add(f'Fraction of the bar shaded? <span class="blank"></span>',
                f"{num}/{d}", svg_frac_bar(num, d, rng), "Fraction bar")
        elif style == "numberline":
            d2 = rng.choice([2, 4, 5, 8] if hard else [2, 4])
            n2 = rng.randint(1, d2 - 1)
            add(f'Fraction on the number line? <span class="blank"></span>',
                f"{n2}/{d2}", svg_frac_numberline(n2, d2), "Fraction number line")
        elif style == "set":
            whole = d * rng.randint(2, 6 if hard else 4)
            add(f'{num}/{d} of {whole} = <span class="blank"></span>', str(num * whole // d))
        elif style == "compare":
            add(f'Which is greater: <strong>{num}/{d}</strong> or <strong>1/{d}</strong>? '
                f'<span class="blank"></span>', f"{num}/{d}" if num > 1 else "1/{d}")

    while len(answers) < 5:
        d4 = rng.choice(denoms)
        n4 = rng.randint(1, d4 - 1)
        add(f'Fraction NOT shaded? <span class="blank"></span>',
            f"{d4-n4}/{d4}", svg_frac_bar(n4, d4, rng), "Fraction bar")

    html += '</ol>'
    _RECENT_FRAC.append(slot)
    title = "Section 7: Fractions &amp; Proportion (15 mins)" if hard else "Section 7: Fractions (15 mins)"
    return title, html, answers


def sec_bonus(n, rng):
    t = tier(n)
    hard = hard_lesson(n)
    html = '<ol class="q-list">'
    answers = []
    slot = n % 5

    if hard:
        if slot == 0:
            a, b, c, d = rng.randint(60, 200), rng.randint(2, 9), rng.randint(2, 9), rng.randint(15, 50)
            html += q_li(f'({a} + {d}) − {b} × {c} = <span class="blank"></span> <small>(× first)</small>')
            answers.append(("B1", str((a + d) - b * c)))
        elif slot == 1:
            w, h = rng.randint(4, 12), rng.randint(3, 9)
            html += q_li(f'Perimeter {w}×{h} rectangle? <span class="blank"></span> cm; '
                           f'Area? <span class="blank"></span> cm²')
            answers.append(("B1", f"P={2*(w+h)}, A={w*h}"))
        elif slot == 2:
            num, den = rng.randint(1, 5), rng.choice([4, 6, 8])
            whole = den * rng.randint(3, 8)
            html += q_li(f'{num}/{den} of {whole} = <span class="blank"></span>')
            answers.append(("B1", str(num * whole // den)))
        elif slot == 3:
            x, m = rng.randint(11, 40), rng.randint(3, 9)
            html += q_li(f'Challenge: {x} × {m} = <span class="blank"></span>')
            answers.append(("B1", str(x * m)))
        else:
            sh, sm, ah, am = 9, 15, 2, 45
            em = (sm + am) % 60
            eh = (sh + ah + (sm + am) // 60) % 24
            html += q_li(f'Start {sh}:{sm:02d}, add {ah}h {am}min. Time? <span class="blank"></span>')
            answers.append(("B1", f"{eh}:{em:02d}"))
    elif t == 1:
        a, b, c = rng.randint(20, 60), rng.randint(10, 30), rng.randint(5, 20)
        html += q_li(f'{a} + {b} − {c} = <span class="blank"></span>')
        answers.append(("B1", str(a + b - c)))
    else:
        a, b, c, d = rng.randint(50, 150), rng.randint(2, 9), rng.randint(2, 9), rng.randint(10, 35)
        html += q_li(f'({a} + {d}) − {b} × {c} = <span class="blank"></span> <small>(× first)</small>')
        answers.append(("B1", str((a + d) - b * c)))

    skip = rng.choice([3, 4, 5, 6 if hard else 5, 10])
    seq = [skip * i for i in range(1, 6)]
    html += q_li(f'Missing term: {seq[0]}, {seq[1]}, {seq[2]}, ___, {seq[4]} → <span class="blank"></span>')
    answers.append(("B2", str(seq[3])))

    if slot % 2 == 0:
        rows, cols = rng.randint(2, 4), rng.randint(3, 6)
        html += q_li(f'Array total?<br>' + diagram(svg_array(rows, cols, rng), f"{rows}×{cols}")
                     + '<span class="blank"></span>')
        answers.append(("B3", str(rows * cols)))
    else:
        d, num = rng.choice([2, 4, 8]), rng.randint(1, 3)
        html += q_li(f'Quick fraction:<br>' + diagram(svg_frac_pie(num, d, rng), f"{num}/{d}")
                     + '<span class="blank"></span>')
        answers.append(("B3", f"{num}/{d}"))

    html += '</ol>'
    return "Bonus Challenge (5 mins)", html, answers

# ─── Page builder ────────────────────────────────────────────────────────────
def build_lesson(n, rng):
    reset_lesson_trackers()
    topic, subtitle = LESSONS[n]
    sections = []
    all_answers = []

    for which in (1, 2):
        title, html, ans = sec_topic(n, rng, which)
        # differentiate sec2 slightly by re-seeding offset
        if which == 2:
            rng2 = random.Random(n * 7919 + 31337 + 777)
            title, html, ans = sec_topic(n, rng2, which)
            title = f"Section 2: {topic} — Practice (15 mins)"
        sections.append((title, html))
        all_answers.append((title, ans))

    for fn in (sec_muldiv, sec_word, sec_measure, sec_geo_data, sec_fractions, sec_bonus):
        title, html, ans = fn(n, rng)
        sections.append((title, html))
        all_answers.append((title, ans))

    body = ""
    for title, html in sections:
        cls = "bonus" if title.startswith("Bonus") else "section-header"
        icon = "⭐ " if cls == "bonus" else "⏱ "
        body += f'<div class="{cls}">{icon}{title}</div>\n{html}\n'

    ak_rows = ""
    for sec_title, sec_ans in all_answers:
        short = sec_title.split(":")[0].replace("Section ", "S").replace("Bonus Challenge (5 mins)", "Bonus")
        if "—" in sec_title:
            short = "S2"
        for q, a in sec_ans:
            ak_rows += f'<tr><td>{short}</td><td>{q}</td><td style="text-align:left">{a}</td></tr>\n'

    answer_section = f"""
<hr class="before-answer">
<div class="answer-section">
  <div class="answer-header">✅ Answer Key — Lesson {n}</div>
  <table class="answer-key">
    <thead><tr><th>Section</th><th>Q#</th><th>Answer</th></tr></thead>
    <tbody>{ak_rows}</tbody>
  </table>
</div>
"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Lesson {n} – Grade 2 Math Theory</title>
  <style>{CSS}</style>
</head>
<body>
  <h1>🧠 Grade 2 Math Theory – Lesson {n}</h1>
  <div class="meta">{subtitle} &nbsp;|&nbsp; Level: Year 3</div>
  <div class="name-line">
    <span>Name:</span><span class="line"></span>
    <span>Date:</span><span class="line"></span>
  </div>
  <hr>
{body}
{answer_section}
</body>
</html>"""

def main():
    for n in range(1, 101):
        rng = lesson_rng(n)
        html = build_lesson(n, rng)
        path = os.path.join(OUTDIR, f"Lesson {n} - Grade 2 Math Theory.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  ✓ Lesson {n}: {LESSONS[n][0]}")
    print(f"\nDone. 100 Year-2 lessons saved to:\n  {OUTDIR}")

if __name__ == "__main__":
    main()
