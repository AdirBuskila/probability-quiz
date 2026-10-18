# -*- coding: utf-8 -*-
"""Draw the circuit diagrams of the "circ" course as clean SVG, generated from defs.py (never cropped).
    PYTHONUTF8=1 py tools/verify/needhelp/circ/diagrams.py        -> images/courses/circ/*.svg
Series = units side by side, parallel = stacked branches between two rails, bridge = the classic five-unit bridge.
Every picture has its own light background so it reads the same in the light and the dark theme."""
import pathlib, sys
from xml.sax.saxutils import escape

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from defs import CIRCUITS, DIAGRAMS  # noqa: E402

ROOT = HERE.parents[3]
OUT = ROOT / "images" / "courses" / "circ"

BW, BH = 56, 40        # unit box
GAP = 28               # wire between series items
VG = 18                # vertical gap between parallel branches
RAIL = 24              # rail wire length
INK, BOX, FILL, SOFT = "#1f2937", "#0f766e", "#ecfdf5", "#475569"


def fmt_p(p):
    s = ("%.4f" % float(p)).rstrip("0").rstrip(".")
    return s


def layout(node, probs, show):
    """Returns (w, h, cy, draw) with draw(x, y) -> list of svg strings; cy = y of the wire through the block."""
    k, v = node
    if k == "C":
        def draw(x, y):
            out = ['<rect x="%g" y="%g" width="%d" height="%d" rx="7" fill="%s" stroke="%s" stroke-width="2.4"/>' % (x, y, BW, BH, FILL, BOX)]
            if show:
                out.append('<text stroke="none" x="%g" y="%g" text-anchor="middle" font-size="16" font-weight="700" fill="%s">%s</text>' % (x + BW / 2, y + 17, INK, escape(v)))
                out.append('<text stroke="none" x="%g" y="%g" text-anchor="middle" font-size="11.5" fill="%s">%s</text>' % (x + BW / 2, y + 32, SOFT, fmt_p(probs[v])))
            else:
                out.append('<text stroke="none" x="%g" y="%g" text-anchor="middle" font-size="17" font-weight="700" fill="%s">%s</text>' % (x + BW / 2, y + BH / 2 + 6, INK, escape(v)))
            return out
        return BW, BH, BH / 2, draw
    if k == "S":
        subs = [layout(ch, probs, show) for ch in v]
        top = max(s[2] for s in subs)
        bot = max(s[1] - s[2] for s in subs)
        w = sum(s[0] for s in subs) + GAP * (len(subs) - 1)

        def draw(x, y):
            out, cx = [], x
            for i, (sw, sh, scy, sd) in enumerate(subs):
                out += sd(cx, y + top - scy)
                if i < len(subs) - 1:
                    out.append('<line x1="%g" y1="%g" x2="%g" y2="%g"/>' % (cx + sw, y + top, cx + sw + GAP, y + top))
                cx += sw + GAP
            return out
        return w, top + bot, top, draw
    if k == "P":
        subs = [layout(ch, probs, show) for ch in v]
        mw = max(s[0] for s in subs)
        w = mw + 2 * RAIL
        ys, y0 = [], 0
        for s in subs:
            ys.append(y0)
            y0 += s[1] + VG
        h = y0 - VG
        c0, c1 = ys[0] + subs[0][2], ys[-1] + subs[-1][2]
        cy = (c0 + c1) / 2

        def draw(x, y):
            out = ['<line x1="%g" y1="%g" x2="%g" y2="%g"/>' % (x, y + c0, x, y + c1),
                   '<line x1="%g" y1="%g" x2="%g" y2="%g"/>' % (x + w, y + c0, x + w, y + c1)]
            for (sw, sh, scy, sd), sy in zip(subs, ys):
                bx = x + RAIL + (mw - sw) / 2
                out += sd(bx, y + sy)
                out.append('<line x1="%g" y1="%g" x2="%g" y2="%g"/>' % (x, y + sy + scy, bx, y + sy + scy))
                out.append('<line x1="%g" y1="%g" x2="%g" y2="%g"/>' % (bx + sw, y + sy + scy, x + w, y + sy + scy))
            return out
        return w, h, cy, draw
    if k == "BR":
        a, b, c, d, e = v
        arm = 40                      # wire from the node to a unit
        w = 2 * RAIL + 2 * BW + 2 * arm + 2 * 14
        row = 112                     # distance between the two row wires
        h = row + BH
        cy = h / 2
        ty, by = BH / 2, BH / 2 + row
        tx = w / 2                    # x of the two middle nodes

        def unit(letter):
            return layout(("C", letter), probs, show)[3]

        def draw(x, y):
            out = []
            ax = x + RAIL + 14
            bx = x + w - RAIL - 14 - BW
            # rails
            out.append('<line x1="%g" y1="%g" x2="%g" y2="%g"/>' % (x, y + ty, x, y + by))
            out.append('<line x1="%g" y1="%g" x2="%g" y2="%g"/>' % (x + w, y + ty, x + w, y + by))
            for yy in (ty, by):
                out.append('<line x1="%g" y1="%g" x2="%g" y2="%g"/>' % (x, y + yy, ax, y + yy))
                out.append('<line x1="%g" y1="%g" x2="%g" y2="%g"/>' % (ax + BW, y + yy, x + tx, y + yy))
                out.append('<line x1="%g" y1="%g" x2="%g" y2="%g"/>' % (x + tx, y + yy, bx, y + yy))
                out.append('<line x1="%g" y1="%g" x2="%g" y2="%g"/>' % (bx + BW, y + yy, x + w, y + yy))
            out += unit(a)(ax, y); out += unit(b)(bx, y)
            out += unit(c)(ax, y + row); out += unit(d)(bx, y + row)
            # middle unit E between the two middle nodes
            ey = y + (ty + by) / 2 - BH / 2
            out.append('<line x1="%g" y1="%g" x2="%g" y2="%g"/>' % (x + tx, y + ty, x + tx, ey))
            out.append('<line x1="%g" y1="%g" x2="%g" y2="%g"/>' % (x + tx, ey + BH, x + tx, y + by))
            out += unit(e)(x + tx - BW / 2, ey)
            for yy in (ty, by):
                out.append('<circle cx="%g" cy="%g" r="3.5" fill="%s" stroke="none"/>' % (x + tx, y + yy, INK))
            return out
        return w, h, cy, draw
    raise ValueError(k)


def render(items):
    """items: [(caption|None, name)] -> svg text."""
    PAD, TERM, CAP = 20, 26, 22
    blocks = []
    for cap, name in items:
        tree, probs, show = CIRCUITS[name]
        blocks.append((cap,) + layout(tree, probs, show))
    inner = max(b[1] for b in blocks)
    W = inner + 2 * (PAD + TERM)
    y, parts = PAD, []
    for cap, bw, bh, bcy, bd in blocks:
        if cap:
            parts.append('<text stroke="none" x="%g" y="%g" font-size="15" font-weight="700" fill="%s">%s</text>' % (PAD, y + 12, INK, escape(cap)))
            y += CAP
        x0 = PAD + TERM + (inner - bw) / 2
        cyy = y + bcy
        parts.append('<g stroke="%s" stroke-width="2.4" stroke-linecap="round" fill="none">' % INK)
        parts.append('<line x1="%g" y1="%g" x2="%g" y2="%g"/>' % (PAD + 6, cyy, x0, cyy))
        parts.append('<line x1="%g" y1="%g" x2="%g" y2="%g"/>' % (x0 + bw, cyy, W - PAD - 6, cyy))
        parts.append("</g>")
        parts.append('<g stroke="%s" stroke-width="2.4" stroke-linecap="round" fill="none">' % INK)
        parts += bd(x0, y)
        parts.append("</g>")
        parts.append('<circle cx="%g" cy="%g" r="5" fill="%s"/><circle cx="%g" cy="%g" r="5" fill="%s"/>' % (PAD + 6, cyy, INK, W - PAD - 6, cyy, INK))
        y += bh + (18 if cap else 0)
    H = y + PAD - (18 if blocks[-1][0] else 0)
    body = "".join(parts)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
            'font-family="Arial, Helvetica, sans-serif" role="img">'
            '<rect x="1" y="1" width="%d" height="%d" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>%s</svg>'
            % (W, H, W, H, W - 2, H - 2, body))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, items in DIAGRAMS.items():
        (OUT / (name + ".svg")).write_text(render(items), encoding="utf-8", newline="\n")
    print("wrote %d diagrams to %s" % (len(DIAGRAMS), OUT))


if __name__ == "__main__":
    main()
