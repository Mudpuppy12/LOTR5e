#!/usr/bin/env python3
"""Generate a combined LOTR Roleplaying (5e) combat reference PDF.

Top half: Combat Actions
Bottom half: Bonus Actions & Reactions
One-page complete player combat reference.
"""

from pathlib import Path

from fpdf import FPDF

import generate_lotr5e_bonus_reaction_sheet as bonus_mod
import generate_lotr5e_cheat_sheet as actions_mod

OUT = Path(__file__).resolve().parent / "LOTR5e_Combat_Reference_Combined.pdf"

PAGE_W, PAGE_H = 595.28, 841.89
MARGIN_X = 28
HALF_GAP = 10
COL_GAP = 18
ICON_W = 28
TITLE_H = 22

ACTIONS = actions_mod.ACTIONS
ACTION_REMINDERS = actions_mod.REMINDERS
BONUS_ACTIONS = bonus_mod.BONUS_ACTIONS
REACTIONS = bonus_mod.REACTIONS
ECONOMY_REMINDERS = bonus_mod.REMINDERS

FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/Library/Fonts/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]


class CombinedCheatSheet(FPDF):
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

        if kind == "swords":
            self.set_line_width(2)
            self.line(cx - 7, cy + 7, cx + 7, cy - 7)
            self.line(cx + 7, cy + 7, cx - 7, cy - 7)
            self.set_line_width(1.2)
            self.line(cx - 4, cy + 8, cx - 9, cy + 3)
            self.line(cx + 4, cy + 8, cx + 9, cy + 3)
        elif kind == "craft":
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
        elif kind == "rule":
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
        elif kind == "calling":
            self.line(cx - 6, cy - 9, cx - 6, cy + 9)
            self.set_fill_color(25, 25, 25)
            self.polygon(
                [(cx - 5, cy - 8), (cx + 9, cy - 4), (cx - 5, cy), (cx - 5, cy - 8)],
                style="F",
            )
        elif kind == "opportunity":
            self.ellipse(cx - 8, cy - 6, 12, 12, style="D")
            self.set_line_width(1.8)
            self.line(cx + 2, cy - 2, cx + 10, cy - 8)
            self.line(cx + 10, cy - 8, cx + 5, cy - 8)
            self.line(cx + 10, cy - 8, cx + 10, cy - 3)

    def draw_entry(
        self,
        x: float,
        y: float,
        w: float,
        title: str,
        icon: str,
        body: str,
        title_size: float = 10,
        body_size: float = 7.5,
        title_h: float = 12,
        body_lh: float = 9,
    ) -> None:
        self.draw_icon(icon, x, y + 2, size=ICON_W - 4)
        text_x = x + ICON_W + 4
        text_w = w - ICON_W - 4
        self.set_xy(text_x, y)
        self.set_font(self.font_family, "B", title_size)
        self.set_text_color(20, 20, 20)
        self.cell(text_w, title_h, title, new_x="LMARGIN", new_y="NEXT")
        self.set_x(text_x)
        self.set_font(self.font_family, "", body_size)
        self.set_text_color(40, 40, 40)
        self.multi_cell(text_w, body_lh, body)

    def draw_column_label(self, x: float, y: float, w: float, label: str) -> None:
        self.set_fill_color(235, 230, 220)
        self.rect(x, y, w, 14, style="F")
        self.set_xy(x, y + 1)
        self.set_font(self.font_family, "B", 9)
        self.set_text_color(40, 30, 20)
        self.cell(w, 12, label, align="C")

    def draw_reminder(
        self, bottom: float, reminder_h: float, heading: str, body: str
    ) -> None:
        self.set_fill_color(245, 242, 235)
        self.rect(MARGIN_X, bottom - reminder_h, PAGE_W - 2 * MARGIN_X, reminder_h - 4, style="F")
        self.set_xy(MARGIN_X + 6, bottom - reminder_h + 3)
        self.set_font(self.font_family, "B", 7.5)
        self.set_text_color(50, 40, 30)
        self.cell(PAGE_W - 2 * MARGIN_X - 12, 9, heading)
        self.set_xy(MARGIN_X + 6, bottom - reminder_h + 12)
        self.set_font(self.font_family, "", 6.8)
        self.set_text_color(55, 45, 35)
        self.multi_cell(PAGE_W - 2 * MARGIN_X - 12, 8, body)

    def draw_actions_half(self, top: float, bottom: float) -> None:
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
        row_h = (grid_bottom - grid_top) / 6
        col_w = (PAGE_W - 2 * MARGIN_X - COL_GAP) / 2
        left_x = MARGIN_X
        right_x = MARGIN_X + col_w + COL_GAP

        for i, (title, icon, body) in enumerate(ACTIONS[:5]):
            self.draw_entry(
                left_x,
                grid_top + i * row_h,
                col_w,
                title,
                icon,
                body,
                title_size=11,
                body_size=8,
                title_h=13,
                body_lh=9.5,
            )
        for i, (title, icon, body) in enumerate(ACTIONS[5:]):
            self.draw_entry(
                right_x,
                grid_top + i * row_h,
                col_w,
                title,
                icon,
                body,
                title_size=11,
                body_size=8,
                title_h=13,
                body_lh=9.5,
            )

        self.draw_reminder(bottom, reminder_h, "Middle-earth reminders", ACTION_REMINDERS)

    def draw_bonus_reaction_half(self, top: float, bottom: float) -> None:
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
            self.draw_entry(left_x, entries_top + i * left_row_h, col_w, title, icon, body)
        for i, (title, icon, body) in enumerate(REACTIONS):
            self.draw_entry(right_x, entries_top + i * right_row_h, col_w, title, icon, body)

        self.draw_reminder(
            bottom, reminder_h, "Action economy reminders", ECONOMY_REMINDERS
        )

    def build(self) -> None:
        self.add_page()
        mid = PAGE_H / 2
        self.draw_actions_half(top=12, bottom=mid - HALF_GAP)
        self.draw_bonus_reaction_half(top=mid + HALF_GAP + 4, bottom=PAGE_H - 12)


def main() -> None:
    pdf = CombinedCheatSheet()
    pdf.build()
    pdf.output(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
