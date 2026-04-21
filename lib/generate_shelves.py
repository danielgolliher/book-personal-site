#!/usr/bin/env python3
"""Generate shelves.svg — a wide bookshelf populated with books.

Books are grouped with a `.book` class plus a shelf-index class so the parent
page can stagger their fade-in animations (mirroring Matt Bateman's pegboard).
"""
import random
import sys

random.seed(20260420)

W, H = 1989, 720
FRAME_COLOR_VAR = "var(--frame, #5a3a24)"
SHELF_COLOR_VAR = "var(--shelf, #6b4a30)"
WALL_COLOR_VAR = "var(--wall, #f4ecd8)"
PAGE_TOP = "#e8d9b0"

# Rich library palette
PALETTE = [
    "#6b2d2d", "#8b3a3a", "#2d4a2d", "#3a5f3a",
    "#1f3a5f", "#2c4a6b", "#d4c4a0", "#9b7a2d",
    "#5f5f2d", "#4a2d4a", "#8b4a2d", "#7a4a2e",
    "#3a3a3a", "#c8a85a", "#6b4a2d", "#a85c3a",
]
LIGHT_COLORS = {"#d4c4a0", "#c8a85a"}  # books where we use dark labels

# Frame
FL, FR = 80, W - 80
FT, FB = 40, H - 30
THK = 16

# Shelf y-positions (top of plank). Book bottom rests at shelf top.
SHELVES = [240, 440, 640]
SHELF_THICK = 10

BOOK_LEFT = FL + THK + 10
BOOK_RIGHT = FR - THK - 10

# Cutout for the name plaque on the bottom shelf (SVG coords).
CUTOUT_SHELF = 2  # index into SHELVES (bottom shelf)
CUTOUT_X1 = 565
CUTOUT_X2 = 1425

out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d">' % (W, H)]

# Internal stylesheet — consumed when loaded via <object>.
out.append('''<style>
  @import url("https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&amp;family=IM+Fell+English:ital@0;1&amp;family=IM+Fell+English+SC&amp;display=swap");
  :root { --wall: #f4ecd8; --frame: #5a3a24; --shelf: #6b4a30; }
  g.book { opacity: 0; }
  @keyframes place_book {
    0%   { opacity: 0; transform: translateY(-40px); }
    65%  { opacity: 1; transform: translateY(4px); }
    100% { opacity: 1; transform: translateY(0); }
  }
  a.menu-book { cursor: pointer; }
  a.menu-book text, g.nameplate text { pointer-events: none; user-select: none; }
  a.menu-book rect.spine { transition: filter 0.15s; }
  a.menu-book:hover rect.spine { filter: brightness(1.2); }
</style>''')

# Back wall
out.append(f'<rect x="{FL}" y="{FT}" width="{FR-FL}" height="{FB-FT}" fill="{WALL_COLOR_VAR}"/>')

# Shelves (planks + shadow)
for y in SHELVES:
    out.append(f'<rect x="{FL+THK}" y="{y}" width="{BOOK_RIGHT-BOOK_LEFT+20}" height="{SHELF_THICK}" fill="{SHELF_COLOR_VAR}"/>')
    out.append(f'<rect x="{FL+THK}" y="{y+SHELF_THICK}" width="{BOOK_RIGHT-BOOK_LEFT+20}" height="3" fill="rgba(0,0,0,0.18)"/>')

# Populate each shelf with books, tagged with shelf-index and a random group.
book_idx = 0
for shelf_idx, shelf_y in enumerate(SHELVES):
    x = BOOK_LEFT + random.uniform(10, 40)
    while x < BOOK_RIGHT - 40:
        # Occasional gap (bookend, ornament, breathing room).
        if random.random() < 0.07:
            x += random.uniform(25, 70)
            continue

        w = random.randint(22, 54)
        h = random.randint(110, 205)
        if x + w > BOOK_RIGHT - 10:
            break

        # Skip the niche on the bottom shelf — reserved for the name plaque.
        if shelf_idx == CUTOUT_SHELF and x < CUTOUT_X2 and x + w > CUTOUT_X1:
            x = CUTOUT_X2 + random.uniform(5, 15)
            continue

        color = random.choice(PALETTE)
        y_top = shelf_y - h
        group = random.randint(0, 5)
        cls = f"book shelf-{shelf_idx} book-g{group}"

        pieces = [f'<g class="{cls}">']
        pieces.append(f'<rect x="{x:.1f}" y="{y_top}" width="{w}" height="{h}" fill="{color}"/>')
        # top pages
        pieces.append(f'<rect x="{x+1:.1f}" y="{y_top}" width="{w-2}" height="2.5" fill="{PAGE_TOP}"/>')
        # decorative band (title area)
        if random.random() < 0.55:
            band_y = y_top + random.randint(22, 42)
            band_h = random.randint(6, 14)
            band = "#111" if color in LIGHT_COLORS else "#f0e0b8"
            pieces.append(f'<rect x="{x:.1f}" y="{band_y}" width="{w}" height="{band_h}" fill="{band}" opacity="0.55"/>')
        # faint horizontal detail line
        if random.random() < 0.3:
            ly = y_top + h - 20
            pieces.append(f'<line x1="{x+3:.1f}" y1="{ly}" x2="{x+w-3:.1f}" y2="{ly}" stroke="#000" stroke-width="0.5" opacity="0.3"/>')
        # tiny spine band near top for a "gold embossed" look on some books
        if random.random() < 0.18:
            band2_y = y_top + random.randint(8, 14)
            pieces.append(f'<rect x="{x:.1f}" y="{band2_y}" width="{w}" height="2" fill="#c8a85a" opacity="0.8"/>')
        pieces.append('</g>')
        out.append('\n'.join(pieces))

        x += w + random.uniform(0, 3)
        book_idx += 1

# Nameplate (picture frame) sitting on the bottom shelf, left of center.
NAME_BOTTOM = SHELVES[CUTOUT_SHELF]   # 640 — top of bottom shelf plank
NAME_W = 320
NAME_H = 170
NAME_CX = 985
nx1 = NAME_CX - NAME_W / 2
ny1 = NAME_BOTTOM - NAME_H
nx2 = nx1 + NAME_W
ny2 = NAME_BOTTOM

out.append('<g class="book nameplate book-g9">')
# drop shadow behind frame
out.append(f'  <rect x="{nx1+4}" y="{ny1+4}" width="{NAME_W}" height="{NAME_H}" fill="rgba(0,0,0,0.22)"/>')
# outer wood
out.append(f'  <rect x="{nx1}" y="{ny1}" width="{NAME_W}" height="{NAME_H}" fill="#5a3a24"/>')
# gold inner bevel
out.append(f'  <rect x="{nx1+10}" y="{ny1+10}" width="{NAME_W-20}" height="{NAME_H-20}" fill="#c8a85a"/>')
# matt
out.append(f'  <rect x="{nx1+16}" y="{ny1+16}" width="{NAME_W-32}" height="{NAME_H-32}" fill="#f2ead0"/>')
# thin dark inner line
out.append(f'  <rect x="{nx1+16}" y="{ny1+16}" width="{NAME_W-32}" height="{NAME_H-32}" fill="none" stroke="#5a3a24" stroke-width="1"/>')
# name text — two-line or one-line centered
out.append(f'  <text x="{NAME_CX}" y="{ny1 + NAME_H/2 - 2}" text-anchor="middle" '
           f'font-family="IM Fell English, serif" font-size="42" font-weight="400" fill="#2f4a35">Daniel Golliher</text>')
out.append(f'  <text x="{NAME_CX}" y="{ny1 + NAME_H/2 + 30}" text-anchor="middle" '
           f'font-family="IM Fell English, serif" font-style="italic" font-size="15" fill="#5a5040">'
           f'(how to say my last name: &#8220;gol-yer&#8221;)</text>')
out.append('</g>')

# Stack of three flat books with spine titles = menu links.
STACK_CX = 1250
STACK_BOTTOM = NAME_BOTTOM   # 640
BOOK_H = 32
BOOK_GAP = 2
# Listed bottom → top of the pile
menu_stack = [
    ("ABOUT",   "#about",   "#6b2d2d", 180),
    ("WRITING", "#writing", "#2d4a2d", 200),
    ("HOME",    "/",        "#1f3a5f", 170),
]
# Tiny horizontal offset per book so the pile looks slightly uneven.
offsets = [0, 6, -4]

for i, (label, href, color, bw) in enumerate(menu_stack):
    cx = STACK_CX + offsets[i]
    bx1 = cx - bw / 2
    bx2 = cx + bw / 2
    y_bot = STACK_BOTTOM - i * (BOOK_H + BOOK_GAP)
    y_top = y_bot - BOOK_H

    out.append(f'<a href="{href}" class="menu-book">')
    out.append(f'  <g class="book menu book-g{10+i}">')
    # spine main
    out.append(f'    <rect class="spine" x="{bx1:.1f}" y="{y_top:.1f}" width="{bw}" height="{BOOK_H}" fill="{color}"/>')
    # page edge peeks (both ends)
    out.append(f'    <rect x="{bx1:.1f}" y="{y_top+2:.1f}" width="3" height="{BOOK_H-4}" fill="#e8d9b0" opacity="0.8"/>')
    out.append(f'    <rect x="{bx2-3:.1f}" y="{y_top+2:.1f}" width="3" height="{BOOK_H-4}" fill="#e8d9b0" opacity="0.8"/>')
    # gold rules top and bottom on the spine
    out.append(f'    <rect x="{bx1+7:.1f}" y="{y_top+5:.1f}" width="{bw-14}" height="1.5" fill="#c8a85a" opacity="0.85"/>')
    out.append(f'    <rect x="{bx1+7:.1f}" y="{y_bot-6.5:.1f}" width="{bw-14}" height="1.5" fill="#c8a85a" opacity="0.85"/>')
    # title — centered along the spine
    out.append(f'    <text x="{cx:.1f}" y="{y_top + BOOK_H/2 + 5.5:.1f}" text-anchor="middle" '
               f'font-family="IM Fell English SC, IM Fell English, serif" font-size="16" font-weight="400" '
               f'letter-spacing="4" fill="#f0e0b8">{label}</text>')
    out.append('  </g>')
    out.append('</a>')

# Photo of Daniel — right edge just abuts the nameplate, left edge tucks behind
# the boroughs frame (drawn first so boroughs overlays it).
PHOTO_CX = 725
PHOTO_W = 180
PHOTO_H = 135
PHOTO_BOTTOM = SHELVES[CUTOUT_SHELF]  # 640
px1 = PHOTO_CX - PHOTO_W / 2
py1 = PHOTO_BOTTOM - PHOTO_H

out.append('<g class="book photo book-g17">')
# shadow
out.append(f'  <rect x="{px1+4}" y="{py1+4}" width="{PHOTO_W}" height="{PHOTO_H}" fill="rgba(0,0,0,0.25)"/>')
# wood frame
out.append(f'  <rect x="{px1}" y="{py1}" width="{PHOTO_W}" height="{PHOTO_H}" fill="#5a3a24"/>')
# gold inner bevel
out.append(f'  <rect x="{px1+5}" y="{py1+5}" width="{PHOTO_W-10}" height="{PHOTO_H-10}" fill="#c8a85a"/>')
# cream matt
out.append(f'  <rect x="{px1+9}" y="{py1+9}" width="{PHOTO_W-18}" height="{PHOTO_H-18}" fill="#f2ead0"/>')
# image (3:2 — width-limited, centered vertically)
img_w = PHOTO_W - 20
img_h = img_w * 2 / 3
img_x = px1 + (PHOTO_W - img_w) / 2
img_y = py1 + (PHOTO_H - img_h) / 2
out.append(f'  <image href="daniel.jpg" x="{img_x:.1f}" y="{img_y:.1f}" width="{img_w}" height="{img_h:.1f}" preserveAspectRatio="xMidYMid slice"/>')
out.append('</g>')

# NYC five-boroughs picture — sits in front of the photo, on the bottom shelf.
BORO_CX = 625
BORO_SIZE = 100
BORO_BOTTOM = SHELVES[CUTOUT_SHELF]  # 640
bx = BORO_CX - BORO_SIZE / 2
by = BORO_BOTTOM - BORO_SIZE

out.append('<g class="book boroughs book-g15">')
# shadow
out.append(f'  <rect x="{bx+3}" y="{by+3}" width="{BORO_SIZE}" height="{BORO_SIZE}" fill="rgba(0,0,0,0.22)"/>')
# wood frame
out.append(f'  <rect x="{bx}" y="{by}" width="{BORO_SIZE}" height="{BORO_SIZE}" fill="#5a3a24"/>')
# cream matt
out.append(f'  <rect x="{bx+6}" y="{by+6}" width="{BORO_SIZE-12}" height="{BORO_SIZE-12}" fill="#f4ecd8"/>')
# the boroughs image
out.append(f'  <image href="nyc-boroughs.png" x="{bx+10}" y="{by+10}" width="{BORO_SIZE-20}" height="{BORO_SIZE-20}" preserveAspectRatio="xMidYMid meet"/>')
out.append('</g>')

# Little American flag — stands on the bottom shelf right of the menu books.
FLAG_BASE_CX = 1390
FLAG_BASE_Y = SHELVES[CUTOUT_SHELF]  # 640
FLAG_POLE_X = FLAG_BASE_CX - 1
FLAG_POLE_TOP = 510
FLAG_W = 70
FLAG_H = 42
flx1 = FLAG_POLE_X + 3
fly1 = FLAG_POLE_TOP + 8
flx2 = flx1 + FLAG_W
fly2 = fly1 + FLAG_H

out.append('<g class="book flag book-g16">')
# shadow at base
out.append(f'  <ellipse cx="{FLAG_BASE_CX}" cy="{FLAG_BASE_Y}" rx="18" ry="2" fill="rgba(0,0,0,0.25)"/>')
# wooden stand
out.append(f'  <rect x="{FLAG_BASE_CX-14}" y="{FLAG_BASE_Y-7}" width="28" height="7" fill="#5a3a24" rx="1.5"/>')
out.append(f'  <rect x="{FLAG_BASE_CX-14}" y="{FLAG_BASE_Y-7}" width="28" height="2" fill="#6b4a2e"/>')
# pole
out.append(f'  <rect x="{FLAG_POLE_X}" y="{FLAG_POLE_TOP}" width="2.5" height="{FLAG_BASE_Y-FLAG_POLE_TOP-7}" fill="#8a6a3a"/>')
# gold finial
out.append(f'  <circle cx="{FLAG_POLE_X+1.25}" cy="{FLAG_POLE_TOP-2}" r="2.8" fill="#c8a85a"/>')
# flag base (white)
out.append(f'  <rect x="{flx1}" y="{fly1}" width="{FLAG_W}" height="{FLAG_H}" fill="#ffffff"/>')
# 7 red stripes (13 total stripes, rows 0/2/4/6/8/10/12)
stripe_h = FLAG_H / 13
for i in (0, 2, 4, 6, 8, 10, 12):
    out.append(f'  <rect x="{flx1}" y="{fly1 + i*stripe_h:.2f}" width="{FLAG_W}" height="{stripe_h:.2f}" fill="#b22234"/>')
# blue canton (top-left, 7 stripes tall, ~2/5 of flag width)
canton_w = FLAG_W * 0.4
canton_h = 7 * stripe_h
out.append(f'  <rect x="{flx1}" y="{fly1}" width="{canton_w:.2f}" height="{canton_h:.2f}" fill="#3c3b6e"/>')
# simplified stars on canton (3 rows x 3 cols = 9)
for row in range(3):
    for col in range(3):
        sx = flx1 + 5 + col * 8
        sy = fly1 + 5 + row * 6.5
        out.append(f'  <circle cx="{sx:.2f}" cy="{sy:.2f}" r="1.1" fill="white"/>')
# thin border
out.append(f'  <rect x="{flx1}" y="{fly1}" width="{FLAG_W}" height="{FLAG_H}" fill="none" stroke="rgba(0,0,0,0.25)" stroke-width="0.5"/>')
out.append('</g>')

# Pigeon figurine — perched on top of the menu-book stack, facing left toward
# the nameplate.
TOP_BOOK_CX = STACK_CX + offsets[-1]                       # center x of top book
TOP_BOOK_Y  = STACK_BOTTOM - (len(menu_stack) - 1) * (BOOK_H + BOOK_GAP) - BOOK_H  # top surface of top book
PG_CX = TOP_BOOK_CX
PG_FEET_Y = TOP_BOOK_Y
PG_BODY_CY = PG_FEET_Y - 25
PG_HEAD_CX = PG_CX - 28
PG_HEAD_CY = PG_FEET_Y - 50

out.append('<g class="book pigeon book-g13">')
# shadow on the shelf
out.append(f'  <ellipse cx="{PG_CX}" cy="{PG_FEET_Y}" rx="34" ry="2.5" fill="rgba(0,0,0,0.22)"/>')
# feet (two little legs)
out.append(f'  <line x1="{PG_CX-10}" y1="{PG_FEET_Y-8}" x2="{PG_CX-12}" y2="{PG_FEET_Y}" stroke="#b97a56" stroke-width="2.2" stroke-linecap="round"/>')
out.append(f'  <line x1="{PG_CX+10}" y1="{PG_FEET_Y-8}" x2="{PG_CX+12}" y2="{PG_FEET_Y}" stroke="#b97a56" stroke-width="2.2" stroke-linecap="round"/>')
# tail (back-right)
out.append(f'  <path d="M {PG_CX+26} {PG_BODY_CY-10} L {PG_CX+50} {PG_BODY_CY-2} L {PG_CX+50} {PG_BODY_CY+10} L {PG_CX+26} {PG_BODY_CY+6} Z" fill="#556069"/>')
# body (plump oval)
out.append(f'  <ellipse cx="{PG_CX}" cy="{PG_BODY_CY}" rx="32" ry="22" fill="#7c8b96"/>')
# belly highlight
out.append(f'  <ellipse cx="{PG_CX-10}" cy="{PG_BODY_CY+6}" rx="17" ry="14" fill="#b2bec8" opacity="0.75"/>')
# wing
out.append(f'  <path d="M {PG_CX-14} {PG_BODY_CY-16} Q {PG_CX+4} {PG_BODY_CY-20} {PG_CX+22} {PG_BODY_CY-8} Q {PG_CX+18} {PG_BODY_CY+10} {PG_CX-4} {PG_BODY_CY+8} Q {PG_CX-20} {PG_BODY_CY-2} {PG_CX-14} {PG_BODY_CY-16} Z" fill="#6b7a85"/>')
# wing bar (faint)
out.append(f'  <path d="M {PG_CX-8} {PG_BODY_CY-2} L {PG_CX+16} {PG_BODY_CY-1}" stroke="#4a5560" stroke-width="0.8" opacity="0.7"/>')
# neck (iridescent dark)
out.append(f'  <ellipse cx="{PG_CX-18}" cy="{PG_BODY_CY-16}" rx="12" ry="11" fill="#4a5862"/>')
out.append(f'  <ellipse cx="{PG_CX-20}" cy="{PG_BODY_CY-18}" rx="8" ry="4" fill="#5a6975" opacity="0.7"/>')
# head
out.append(f'  <circle cx="{PG_HEAD_CX}" cy="{PG_HEAD_CY}" r="11" fill="#5d6a76"/>')
# beak
out.append(f'  <path d="M {PG_HEAD_CX-11} {PG_HEAD_CY+1} L {PG_HEAD_CX-21} {PG_HEAD_CY+3} L {PG_HEAD_CX-20} {PG_HEAD_CY-1} L {PG_HEAD_CX-11} {PG_HEAD_CY-2} Z" fill="#2e2620"/>')
# cere (the little bump at base of beak)
out.append(f'  <ellipse cx="{PG_HEAD_CX-12}" cy="{PG_HEAD_CY-3}" rx="3.5" ry="1.8" fill="#d6cec4"/>')
# eye (orange with pupil)
out.append(f'  <circle cx="{PG_HEAD_CX-3}" cy="{PG_HEAD_CY-2}" r="2.2" fill="#ff9d2a"/>')
out.append(f'  <circle cx="{PG_HEAD_CX-3}" cy="{PG_HEAD_CY-2}" r="1.1" fill="#141414"/>')
out.append('</g>')

# Frame (drawn last so it overlaps shelf edges cleanly).
out.append(f'<rect x="{FL}" y="{FT}" width="{THK}" height="{FB-FT}" fill="{FRAME_COLOR_VAR}"/>')
out.append(f'<rect x="{FR-THK}" y="{FT}" width="{THK}" height="{FB-FT}" fill="{FRAME_COLOR_VAR}"/>')
out.append(f'<rect x="{FL}" y="{FT}" width="{FR-FL}" height="{THK}" fill="{FRAME_COLOR_VAR}"/>')
out.append(f'<rect x="{FL}" y="{FB-THK}" width="{FR-FL}" height="{THK}" fill="{FRAME_COLOR_VAR}"/>')

# Subtle wood grain on frame
for side_x in (FL, FR - THK):
    for gy in range(FT + 20, FB - 20, 40):
        out.append(f'<line x1="{side_x+3}" y1="{gy}" x2="{side_x+THK-3}" y2="{gy+random.randint(5,15)}" stroke="rgba(0,0,0,0.12)" stroke-width="0.6"/>')

out.append('</svg>')

with open(sys.argv[1] if len(sys.argv) > 1 else "shelves.svg", "w") as f:
    f.write("\n".join(out))

print(f"wrote {sys.argv[1] if len(sys.argv) > 1 else 'shelves.svg'} ({book_idx} books)")
