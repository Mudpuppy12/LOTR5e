#!/usr/bin/env python3
"""Generate a LOTR Roleplaying (5e) bonus actions & reactions cheat sheet PDF."""

from pathlib import Path

from fpdf import FPDF

OUT = Path(__file__).resolve().parent / "LOTR5e_Bonus_Actions_Reactions_Cheat_Sheet.pdf"

PAGE_W, PAGE_H = 595.28, 841.89
MARGIN_X = 28
HALF_GAP = 10
COL_GAP = 18
ICON_W = 28
TITLE_H = 22

BONUS_ACTIONS = [
    (
        "Bonus Action (Rule)",
        "rule",
        "You get a bonus action only if a calling feature, Craft, Virtue, or other rule grants one. One bonus action per turn - choose if you have several options.",
    ),
    (
        "Two-Weapon Fighting",
        "twf",
        "After the Attack action with a light melee weapon in one hand, attack with a different light melee weapon in the other. Do not add your ability modifier to the bonus damage (unless negative).",
    ),
    (
        "Use a Craft",
        "craft",
        "Use a Craft whose timing is a bonus action. No spell slots in Middle-earth - check your calling for which Crafts (if any) use a bonus action.",
    ),
    (
        "Calling or Virtue",
        "calling",
        "Many calling features and Virtues use a bonus action (commands, quick strikes, cunning movement, and the like). Check your sheet for timing.",
    ),
    (
        "Improvise",
        "improvise",
        "Rarely, the Loremaster may allow a quick secondary deed as a bonus action. Only if a rule or ruling grants it - you cannot invent one freely.",
    ),
]

REACTIONS = [
    (
        "Reaction (Rule)",
        "rule",
        "One reaction per round. It can trigger on your turn or another's. After you use it, you regain it at the start of your next turn.",
    ),
    (
        "Opportunity Attack",
        "opportunity",
        "When a hostile creature you can see leaves your reach, use your reaction for one melee attack against it, resolved before it leaves. Disengage prevents this.",
    ),
    (
        "Readied Action",
        "ready",
        "If you took the Ready action, spend your reaction when the trigger occurs to take the chosen action or move up to your speed. You may ignore the trigger.",
    ),
    (
        "Calling or Virtue",
        "calling",
        "Some calling features and Virtues trigger as reactions (parries, warnings, protective deeds). Use only when their listed trigger occurs.",
    ),
    (
        "Use a Craft",
        "craft",
        "Use a Craft whose timing is a reaction, when its trigger occurs. Middle-earth has no Shield or Counterspell - Crafts are subtle and calling-specific.",
    ),
    (
        "Improvise",
        "improvise",
        "The Loremaster may allow an instant response as a reaction. Only with a clear trigger and a ruling - not a free second action.",
    ),
]

REMINDERS = (
    "Turn economy: Move + Action + (optional) Bonus Action. One Reaction per round.  |  "
    "Free object interaction: draw a weapon, open a door, or similar once on your turn without spending an action.  |  "
    "You cannot trade an action for a bonus action (or vice versa)."
)

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
                bold_alt = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
                if bold_alt.exists():
                    self.add_font("Sheet", "B", str(bold_alt))
                else:
                    self.add_font("Sheet", "B", str(p))
                self.font_family = "Sheet"
                break

    def draw_icon(self, kind: str, x: float, y: float, size: float = 22) -> None:
        self.set_fill_color(25, 25, 25)
        self.set_draw_color(25, 25, 25)
        self.set_line_width(1.2)
        cx, cy = x + size / 2, y + size / 2
        r = size * 0.38

        if kind == "rule":
            self.rect(cx - 8, cy - 8, 16, 16, style="D")
            self.set_font(self.font_family, "B", 11)
            self.set_text_color(25, 25, 25)
            self.set_xy(cx - 4, cy - 5)
            self.cell(8, 10, "!", align="C")
        elif kind == "twf":
            self.set_line_width(2)
            self.line(cx - 8, cy + 6, cx - 2, cy - 8)
            self.line(cx + 8, cy + 6, cx + 2, cy - 8)
            self.set_line_width(1.2)
            self.line(cx - 9, cy + 2, cx - 4, cy + 7)
            self.line(cx + 9, cy + 2, cx + 4, cy + 7)
        elif kind == "craft":
            self.rect(cx - 8, cy - 7, 16, 14, style="D")
            self.line(cx, cy - 7, cx, cy + 7)
            self.line(cx - 5, cy - 2, cx - 2, cy - 2)
            self.line(cx - 5, cy + 1, cx - 1, cy + 1)
            self.line(cx + 2, cy - 2, cx + 5, cy - 2)
            self.line(cx + 2, cy + 1, cx + 5, cy + 1)
        elif kind == "calling":
            # banner / pennant
            self.line(cx - 6, cy - 9, cx - 6, cy + 9)
            self.set_fill_color(25, 25, 25)
            self.polygon(
                [(cx - 5, cy - 8), (cx + 9, cy - 4), (cx - 5, cy), (cx - 5, cy - 8)],
                style="F",
            )
        elif kind == "opportunity":
            # curved arrow leaving reach
            self.ellipse(cx - 8, cy - 6, 12, 12, style="D")
            self.set_line_width(1.8)
            self.line(cx + 2, cy - 2, cx + 10, cy - 8)
            self.line(cx + 10, cy - 8, cx + 5, cy - 8)
            self.line(cx + 10, cy - 8, cx + 10, cy - 3)
        elif kind == "ready":
            self.ellipse(cx - r, cy - r, 2 * r, 2 * r, style="D")
            self.line(cx, cy, cx, cy - 6)
            self.line(cx, cy, cx + 5, cy + 3)
        elif kind == "improvise":
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

    def draw_entry(
        self,
        x: float,
        y: float,
        w: float,
        title: str,
        icon: str,
        body: str,
    ) -> None:
        self.draw_icon(icon, x, y + 2, size=ICON_W - 4)
        text_x = x + ICON_W + 4
        text_w = w - ICON_W - 4
        self.set_xy(text_x, y)
        self.set_font(self.font_family, "B", 10)
        self.set_text_color(20, 20, 20)
        self.cell(text_w, 12, title, new_x="LMARGIN", new_y="NEXT")
        self.set_x(text_x)
        self.set_font(self.font_family, "", 7.5)
        self.set_text_color(40, 40, 40)
        self.multi_cell(text_w, 9, body)

    def draw_column_label(self, x: float, y: float, w: float, label: str) -> None:
        self.set_fill_color(235, 230, 220)
        self.rect(x, y, w, 14, style="F")
        self.set_xy(x, y + 1)
        self.set_font(self.font_family, "B", 9)
        self.set_text_color(40, 30, 20)
        self.cell(w, 12, label, align="C")

    def draw_half(self, top: float, bottom: float) -> None:
        content_top = top + 8
        self.set_xy(MARGIN_X, content_top)
        self.set_font(self.font_family, "B", 13)
        self.set_text_color(20, 20, 20)
        self.cell(PAGE_W - 2 * MARGIN_X, TITLE_H - 4, "The Lord of the Rings Roleplaying", align="C")
        self.set_xy(MARGIN_X, content_top + 14)
        self.set_font(self.font_family, "", 9)
        self.set_text_color(70, 70, 70)
        self.cell(
            PAGE_W - 2 * MARGIN_X,
            11,
            "Bonus Actions & Reactions (5E) - Player-hero reference",
            align="C",
        )

        reminder_h = 36
        label_h = 16
        grid_top = content_top + TITLE_H + 6
        grid_bottom = bottom - reminder_h - 6
        col_w = (PAGE_W - 2 * MARGIN_X - COL_GAP) / 2
        left_x = MARGIN_X
        right_x = MARGIN_X + col_w + COL_GAP

        self.draw_column_label(left_x, grid_top, col_w, "BONUS ACTIONS")
        self.draw_column_label(right_x, grid_top, col_w, "REACTIONS")

        entries_top = grid_top + label_h + 4
        left_row_h = (grid_bottom - entries_top) / len(BONUS_ACTIONS)
        right_row_h = (grid_bottom - entries_top) / len(REACTIONS)

        for i, (title, icon, body) in enumerate(BONUS_ACTIONS):
            y = entries_top + i * left_row_h
            self.draw_entry(left_x, y, col_w, title, icon, body)

        for i, (title, icon, body) in enumerate(REACTIONS):
            y = entries_top + i * right_row_h
            self.draw_entry(right_x, y, col_w, title, icon, body)

        self.set_fill_color(245, 242, 235)
        self.rect(MARGIN_X, bottom - reminder_h, PAGE_W - 2 * MARGIN_X, reminder_h - 4, style="F")
        self.set_xy(MARGIN_X + 6, bottom - reminder_h + 3)
        self.set_font(self.font_family, "B", 7.5)
        self.set_text_color(50, 40, 30)
        self.cell(PAGE_W - 2 * MARGIN_X - 12, 9, "Action economy reminders")
        self.set_xy(MARGIN_X + 6, bottom - reminder_h + 12)
        self.set_font(self.font_family, "", 6.8)
        self.set_text_color(55, 45, 35)
        self.multi_cell(PAGE_W - 2 * MARGIN_X - 12, 8, REMINDERS)

    def draw_cut_line(self) -> None:
        mid = PAGE_H / 2
        self.set_draw_color(120, 120, 120)
        self.set_line_width(0.6)
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
