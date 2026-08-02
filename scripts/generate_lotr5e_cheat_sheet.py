#!/usr/bin/env python3
"""Generate a LOTR Roleplaying (5e) combat actions cheat sheet PDF."""

from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "LOTR5e_Combat_Actions_Cheat_Sheet.pdf"

# A4 points
PAGE_W, PAGE_H = 595.28, 841.89
MARGIN_X = 28
HALF_GAP = 10  # space around dashed cut line
COL_GAP = 18
ICON_W = 28
TITLE_H = 22

ACTIONS = [
    (
        "Attack",
        "swords",
        "Make an attack with a melee weapon, ranged weapon, improvised weapon, or unarmed. Some calling features allow Extra Attack.",
    ),
    (
        "Use a Craft",
        "craft",
        "Use a Craft or calling feature that takes an action. Middle-earth has no spell slots - subtle Crafts replace overt spellcasting.",
    ),
    (
        "Dash",
        "dash",
        "Double your speed for this turn. The increase equals your speed after applying modifiers.",
    ),
    (
        "Disengage",
        "disengage",
        "Your movement does not provoke opportunity attacks for the rest of your turn.",
    ),
    (
        "Dodge",
        "dodge",
        "Attackers you can see have disadvantage against you, and you have advantage on Dexterity saves. Ends if you are incapacitated or your speed is 0.",
    ),
    (
        "Help",
        "help",
        "Within 5 feet, give a creature advantage on its next ability check, or give an ally advantage on its first attack against a target within 5 feet of you.",
    ),
    (
        "Hide",
        "hide",
        "Make a Dexterity (Stealth) check to hide, following the usual rules for hiding.",
    ),
    (
        "Ready",
        "ready",
        "Choose a perceivable trigger and an action (or move up to your speed). When it occurs, use your reaction. Readying a concentrating Craft requires concentration.",
    ),
    (
        "Search",
        "search",
        "Devote your attention to finding something. The Loremaster may call for Perception, Investigation, Explore, Hunting, or another skill.",
    ),
    (
        "Use an Object",
        "object",
        "Use an object that needs your action - including magical items, Rewards on your gear, or interacting with more than one object.",
    ),
    (
        "Improvise",
        "improvise",
        "Attempt anything fitting a tale of Middle-earth. The Loremaster decides if it is possible and what roll, if any, is required.",
    ),
]

REMINDERS = (
    "Shadow: Miserable (Shadow >= half Wisdom) - auto-fail on a natural 1-2. "
    "Anguished (Shadow >= Wisdom) - disadvantage on checks, attacks, and saves.  |  "
    "Fellowship: Spend points to aid the Company (often advantage).  |  "
    "Optional: 3 Success Dice (d6) may replace a d20."
)

# Prefer a Unicode TTF so we can use en-dashes etc. if desired.
FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/Library/Fonts/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]


class CheatSheet(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="pt", format="A4")
        self.set_auto_page_break(auto=False)
        self.set_margins(0, 0, 0)
        self.font_family = "Helvetica"
        for path in FONT_CANDIDATES:
            p = Path(path)
            if p.exists():
                self.add_font("Sheet", "", str(p))
                # Bold fallback: try Arial Bold
                bold = p.with_name(p.name.replace("Arial", "Arial Bold").replace(".ttf", " Bold.ttf"))
                bold_alt = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
                if bold_alt.exists():
                    self.add_font("Sheet", "B", str(bold_alt))
                elif bold.exists():
                    self.add_font("Sheet", "B", str(bold))
                else:
                    self.add_font("Sheet", "B", str(p))
                self.font_family = "Sheet"
                break

    def draw_icon(self, kind: str, x: float, y: float, size: float = 22) -> None:
        """Simple silhouette-style icons."""
        self.set_fill_color(25, 25, 25)
        self.set_draw_color(25, 25, 25)
        self.set_line_width(1.2)
        cx, cy = x + size / 2, y + size / 2
        r = size * 0.38

        if kind == "swords":
            self.set_line_width(2)
            self.line(cx - 7, cy + 7, cx + 7, cy - 7)
            self.line(cx + 7, cy + 7, cx - 7, cy - 7)
            self.set_line_width(1.2)
            self.line(cx - 4, cy + 8, cx - 9, cy + 3)
            self.line(cx + 4, cy + 8, cx + 9, cy + 3)
        elif kind == "craft":
            # open book / rune tablet
            self.rect(cx - 8, cy - 7, 16, 14, style="D")
            self.line(cx, cy - 7, cx, cy + 7)
            self.line(cx - 5, cy - 2, cx - 2, cy - 2)
            self.line(cx - 5, cy + 1, cx - 1, cy + 1)
            self.line(cx + 2, cy - 2, cx + 5, cy - 2)
            self.line(cx + 2, cy + 1, cx + 5, cy + 1)
        elif kind == "dash":
            self.ellipse(cx - 5, cy - 9, 10, 8, style="F")
            self.rect(cx - 4, cy - 2, 8, 10, style="F")
            self.set_line_width(2)
            self.line(cx - 10, cy + 2, cx - 14, cy - 2)
            self.line(cx - 10, cy + 5, cx - 15, cy + 5)
            self.line(cx - 10, cy + 8, cx - 14, cy + 12)
        elif kind == "disengage":
            self.ellipse(cx - r, cy - r + 1, 2 * r, 2 * r, style="D")
            self.line(cx - 5, cy - 1, cx + 5, cy - 1)
            self.line(cx, cy - 6, cx, cy + 5)
        elif kind == "dodge":
            self.ellipse(cx - 4, cy - 9, 8, 7, style="F")
            self.rect(cx - 3.5, cy - 3, 7, 9, style="F")
            self.set_line_width(1.5)
            self.line(cx + 6, cy - 4, cx + 11, cy - 8)
            self.line(cx + 6, cy, cx + 12, cy - 1)
        elif kind == "help":
            # two overlapping circles (fellowship)
            self.ellipse(cx - 9, cy - 5, 10, 10, style="D")
            self.ellipse(cx - 1, cy - 5, 10, 10, style="D")
        elif kind == "hide":
            self.ellipse(cx - 4, cy - 8, 8, 7, style="F")
            self.rect(cx - 5, cy - 2, 10, 8, style="F")
            self.set_fill_color(255, 255, 255)
            self.ellipse(cx - 10, cy + 2, 20, 10, style="F")
            self.set_fill_color(25, 25, 25)
        elif kind == "ready":
            self.ellipse(cx - r, cy - r, 2 * r, 2 * r, style="D")
            self.line(cx, cy, cx, cy - 6)
            self.line(cx, cy, cx + 5, cy + 3)
        elif kind == "search":
            self.ellipse(cx - 7, cy - 7, 12, 12, style="D")
            self.set_line_width(2.2)
            self.line(cx + 3, cy + 3, cx + 9, cy + 9)
        elif kind == "object":
            self.rect(cx - 7, cy - 4, 14, 10, style="D")
            self.line(cx - 7, cy - 1, cx + 7, cy - 1)
            self.ellipse(cx - 2, cy - 7, 4, 4, style="D")
        elif kind == "improvise":
            # star / hope
            pts = [
                (cx, cy - 9),
                (cx + 2.5, cy - 2.5),
                (cx + 9, cy - 2.5),
                (cx + 4, cy + 2),
                (cx + 5.5, cy + 9),
                (cx, cy + 4.5),
                (cx - 5.5, cy + 9),
                (cx - 4, cy + 2),
                (cx - 9, cy - 2.5),
                (cx - 2.5, cy - 2.5),
            ]
            for i in range(len(pts)):
                x1, y1 = pts[i]
                x2, y2 = pts[(i + 1) % len(pts)]
                self.line(x1, y1, x2, y2)

    def draw_action(
        self,
        x: float,
        y: float,
        w: float,
        title: str,
        icon: str,
        body: str,
        row_h: float,
    ) -> None:
        self.draw_icon(icon, x, y + 2, size=ICON_W - 4)
        text_x = x + ICON_W + 4
        text_w = w - ICON_W - 4
        self.set_xy(text_x, y)
        self.set_font(self.font_family, "B", 11)
        self.set_text_color(20, 20, 20)
        self.cell(text_w, 13, title, new_x="LMARGIN", new_y="NEXT")
        self.set_x(text_x)
        self.set_font(self.font_family, "", 8)
        self.set_text_color(40, 40, 40)
        self.multi_cell(text_w, 9.5, body)

    def draw_half(self, top: float, bottom: float) -> None:
        usable_h = bottom - top
        content_top = top + 8
        self.set_xy(MARGIN_X, content_top)
        self.set_font(self.font_family, "B", 13)
        self.set_text_color(20, 20, 20)
        self.cell(PAGE_W - 2 * MARGIN_X, TITLE_H - 4, "The Lord of the Rings Roleplaying", align="C")
        self.set_xy(MARGIN_X, content_top + 14)
        self.set_font(self.font_family, "", 9)
        self.set_text_color(70, 70, 70)
        self.cell(PAGE_W - 2 * MARGIN_X, 11, "Combat Actions (5E) - Player-hero reference", align="C")

        reminder_h = 34
        grid_top = content_top + TITLE_H + 6
        grid_bottom = bottom - reminder_h - 6
        grid_h = grid_bottom - grid_top
        row_h = grid_h / 6  # 5 rows of pairs + leftover for last item spanning conceptually

        col_w = (PAGE_W - 2 * MARGIN_X - COL_GAP) / 2
        left_x = MARGIN_X
        right_x = MARGIN_X + col_w + COL_GAP

        # Layout: left column 0-4, right column 5-9, then Improvise under left or centered bottom of grid
        left_actions = ACTIONS[:5]
        right_actions = ACTIONS[5:]  # Help through Improvise

        for i, (title, icon, body) in enumerate(left_actions):
            y = grid_top + i * row_h
            self.draw_action(left_x, y, col_w, title, icon, body, row_h)

        for i, (title, icon, body) in enumerate(right_actions):
            y = grid_top + i * row_h
            self.draw_action(right_x, y, col_w, title, icon, body, row_h)

        # Reminders strip
        self.set_fill_color(245, 242, 235)
        self.rect(MARGIN_X, bottom - reminder_h, PAGE_W - 2 * MARGIN_X, reminder_h - 4, style="F")
        self.set_xy(MARGIN_X + 6, bottom - reminder_h + 3)
        self.set_font(self.font_family, "B", 7.5)
        self.set_text_color(50, 40, 30)
        self.cell(PAGE_W - 2 * MARGIN_X - 12, 9, "Middle-earth reminders")
        self.set_xy(MARGIN_X + 6, bottom - reminder_h + 12)
        self.set_font(self.font_family, "", 6.8)
        self.set_text_color(55, 45, 35)
        self.multi_cell(PAGE_W - 2 * MARGIN_X - 12, 8, REMINDERS)

    def draw_cut_line(self) -> None:
        mid = PAGE_H / 2
        self.set_draw_color(120, 120, 120)
        self.set_line_width(0.6)
        # dashed line
        x = MARGIN_X
        dash, gap = 6, 4
        while x < PAGE_W - MARGIN_X:
            x2 = min(x + dash, PAGE_W - MARGIN_X)
            self.line(x, mid, x2, mid)
            x = x2 + gap
        self.set_font(self.font_family, "", 7)
        self.set_text_color(140, 140, 140)
        self.set_xy(0, mid - 9)
        self.cell(PAGE_W, 8, "[ cut here ]", align="C")

    def build(self) -> None:
        self.add_page()
        mid = PAGE_H / 2
        self.draw_half(top=12, bottom=mid - HALF_GAP)
        self.draw_cut_line()
        self.draw_half(top=mid + HALF_GAP + 4, bottom=PAGE_H - 12)


def main() -> None:
    pdf = CheatSheet()
    pdf.build()
    pdf.output(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
