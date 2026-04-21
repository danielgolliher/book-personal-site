---
title: Your Book Title
slug: your-book-slug
shelf: bottom
color: "#6b2d2d"
width: 44
height: 180
---

# Your Book Title

Write your content here using Markdown.

You can have multiple paragraphs, **bold** or *italic* text, and
[links](https://example.com).

## A subsection

- Bullet
- Lists
- Work

More paragraphs flow naturally.

---

## Reference — frontmatter fields

- **title**: shown on the page heading AND (truncated if needed) on the book
  spine in vertical small caps.
- **slug**: the URL segment. Will become `/books/<slug>/` on the site. Use
  lowercase-with-dashes.
- **shelf**: `middle` recommended. (`bottom` is technically allowed, but the
  mobile-visible portion of the bottom shelf is occupied by the nameplate
  niche, so a `bottom` book is only visible on desktop. `top` is reserved
  for filler books and is not allowed.)
- **color**: any CSS hex color. Library-palette options:
    - `#6b2d2d` burgundy
    - `#8b3a3a` oxblood
    - `#2d4a2d` forest
    - `#3a5f3a` moss
    - `#1f3a5f` navy
    - `#2c4a6b` steel
    - `#d4c4a0` cream
    - `#9b7a2d` ochre
    - `#5f5f2d` olive
    - `#4a2d4a` plum
    - `#8b4a2d` rust
    - `#3a3a3a` charcoal
    - `#c8a85a` gold
- **width**: book spine width in px, 22–54. Narrower = slimmer book.
- **height**: book spine height in px, 110–205. Taller = more room for the
  title but stands out more.
