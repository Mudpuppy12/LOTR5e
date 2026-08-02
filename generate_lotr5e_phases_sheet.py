#!/usr/bin/env python3
"""Generate a LOTR Roleplaying (5e) phases of play cheat sheet PDF."""

from pathlib import Path

from fpdf import FPDF

OUT = Path(__file__).resolve().parent / "LOTR5e_Phases_of_Play_Cheat_Sheet.pdf"

PAGE_W, PAGE_H = 595.28, 841.89
MARGIN_X = 28
HALF_GAP = 14
COL_GAP = 14
ICON_W = 26
TITLE_H = 22

FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/Library/Fonts/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]

ADVENTURING = [
    (
        "Adventuring Phase",
        "phase",
        "Active play resolved day by day and scene by scene. The Company journeys, treats with the Wise, and faces the Shadow. Time passes slowly here.",
    ),
    (
        "Heroic Ventures",
        "venture",
        "Combat, exploration, and deeds of courage. Uses the usual 5E action economy (action, bonus action, reaction, move) tailored to Middle-earth.",
    ),
    (
        "Council",
        "council",
        "A formal gathering with important NPCs - to seek aid, counsel, or offer service. Open with introductions, roleplay the meeting, then resolve with ability checks based on the request and the NPC's attitude.",
    ),
    (
        "Journey",
        "journey",
        "Travel across the wild. Plan a route on the map, assign Journey roles, then resolve events along the way. Travel is part of the adventure, not just downtime between scenes.",
    ),
    (
        "Journey Roles",
        "roles",
        "Guide - leads the Company and sets the path. Hunter - finds food and tracks. Look-out - watches for danger. Scout - surveys the land ahead. Role checks resolve many journey events.",
    ),
]

FELLOWSHIP = [
    (
        "Fellowship Phase",
        "phase",
        "Downtime between Adventuring Phases. Weeks or months may pass 'off-screen' at a Safe Haven while heroes rest, recover, and prepare.",
    ),
    (
        "Safe Haven",
        "haven",
        "A place of rest and refuge (a Patron's hall, a friendly settlement, or a sanctuary). Heroes recover here; the road is no place for a true rest from the Shadow.",
    ),
    (
        "Undertakings",
        "undertaking",
        "Each Player-hero chooses what to do with their free time. Examples: gather rumours, meet your Patron, study lore or maps, raise an heir, heal Shadow scars, or examine magical items and Rewards.",
    ),
    (
        "Yule",
        "yule",
        "A special year-end Fellowship Phase. Time advances on the Tale of Years. Yule phases are typically longer and allow more Undertakings than a short rest between adventures.",
    ),
    (
        "Fellowship & Patron",
        "fellowship",
        "Fellowship Points are a shared Company resource - spend them (by agreement) for aid such as advantage. Your Patron may also grant unique boons when points are spent or when you Meet Patron as an Undertaking.",
    ),
]

FOOTER = (
    "Cycle of play: Adventuring Phase (Journey / Council / Heroic Ventures) -> "
    "Fellowship Phase (rest, Undertakings, recover Shadow) -> next Adventuring Phase.  |  "
    "Shadow is often gained while adventuring and eased during Fellowship.  |  "
    "Loremaster narrates broadly in Fellowship; detail returns when adventure resumes."
)


class PhasesSheet(FPDF):
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

    def draw_icon(self, kind: str, x: float, y: float, size: float = 20) -> None:
        self.set_fill_color(25, 25, 25)
        self.set_draw_color(25, 25, 25)
        self.set_line_width(1.2)
        cx, cy = x + size / 2, y + size / 2

        if kind == "phase":
            self.ellipse(cx - 8, cy - 8, 16, 16, style="D")
            self.line(cx, cy - 5, cx, cy + 5)
            self.line(cx - 5, cy, cx + 5, cy)
        elif kind == "venture":
            self.set_line_width(2)
            self.line(cx - 6, cy + 6, cx + 6, cy - 6)
            self.line(cx + 6, cy + 6, cx - 6, cy - 6)
        elif kind == "council":
            self.ellipse(cx - 3, cy - 8, 6, 6, style="F")
            self.ellipse(cx - 9, cy - 4, 5, 5, style="F")
            self.ellipse(cx + 4, cy - 4, 5, 5, style="F")
            self.rect(cx - 4, cy - 2, 8, 8, style="F")
        elif kind == "journey":
            self.line(cx - 8, cy + 6, cx - 2, cy - 2)
            self.line(cx - 2, cy - 2, cx + 3, cy + 2)
            self.line(cx + 3, cy + 2, cx + 8, cy - 6)
            self.ellipse(cx + 6, cy - 8, 4, 4, style="F")
        elif kind == "roles":
            for dx in (-7, 0, 7):
                self.ellipse(cx + dx - 2.5, cy - 6, 5, 5, style="D")
                self.line(cx + dx, cy - 1, cx + dx, cy + 6)
        elif kind == "haven":
            self.line(cx - 9, cy + 2, cx, cy - 8)
            self.line(cx, cy - 8, cx + 9, cy + 2)
            self.rect(cx - 7, cy + 2, 14, 7, style="D")
            self.rect(cx - 2, cy + 4, 4, 5, style="D")
        elif kind == "undertaking":
            self.rect(cx - 7, cy - 8, 14, 16, style="D")
            self.line(cx - 4, cy - 4, cx + 4, cy - 4)
            self.line(cx - 4, cy, cx + 4, cy)
            self.line(cx - 4, cy + 4, cx + 2, cy + 4)
        elif kind == "yule":
            # simple tree
            self.line(cx, cy + 8, cx, cy + 2)
            self.line(cx, cy - 8, cx - 7, cy + 2)
            self.line(cx, cy - 8, cx + 7, cy + 2)
            self.line(cx - 7, cy + 2, cx + 7, cy + 2)
        elif kind == "fellowship":
            self.ellipse(cx - 9, cy - 5, 10, 10, style="D")
            self.ellipse(cx - 1, cy - 5, 10, 10, style="D")

    def draw_entry(
        self,
        x: float,
        y: float,
        w: float,
        title: str,
        icon: str,
        body: str,
    ) -> None:
        self.draw_icon(icon, x, y + 1, size=ICON_W - 4)
        text_x = x + ICON_W + 2
        text_w = w - ICON_W - 2
        self.set_xy(text_x, y)
        self.set_font(self.font_family, "B", 10)
        self.set_text_color(20, 20, 20)
        self.cell(text_w, 12, title, new_x="LMARGIN", new_y="NEXT")
        self.set_x(text_x)
        self.set_font(self.font_family, "", 7.5)
        self.set_text_color(40, 40, 40)
        self.multi_cell(text_w, 9, body)

    def draw_section_banner(self, x: float, y: float, w: float, label: str) -> None:
        self.set_fill_color(235, 230, 220)
        self.rect(x, y, w, 16, style="F")
        self.set_xy(x, y + 2)
        self.set_font(self.font_family, "B", 10)
        self.set_text_color(40, 30, 20)
        self.cell(w, 12, label, align="C")

    def draw_header(self, top: float) -> float:
        self.set_xy(MARGIN_X, top)
        self.set_font(self.font_family, "B", 14)
        self.set_text_color(20, 20, 20)
        self.cell(PAGE_W - 2 * MARGIN_X, 16, "The Lord of the Rings Roleplaying", align="C")
        self.set_xy(MARGIN_X, top + 16)
        self.set_font(self.font_family, "", 9)
        self.set_text_color(70, 70, 70)
        self.cell(PAGE_W - 2 * MARGIN_X, 12, "Phases of Play (5E) - Player-hero & Loremaster reference", align="C")

        # Intro strip
        intro_y = top + 32
        intro_h = 28
        self.set_fill_color(245, 242, 235)
        self.rect(MARGIN_X, intro_y, PAGE_W - 2 * MARGIN_X, intro_h, style="F")
        self.set_xy(MARGIN_X + 8, intro_y + 4)
        self.set_font(self.font_family, "", 7.5)
        self.set_text_color(50, 40, 30)
        self.multi_cell(
            PAGE_W - 2 * MARGIN_X - 16,
            9,
            "Play alternates between two phases. Adventuring Phases cover the deeds of the Company "
            "in detail. Fellowship Phases cover rest and preparation, often spanning weeks or months "
            "before the next adventure begins.",
        )
        return intro_y + intro_h + 8

    def draw_column(
        self,
        x: float,
        top: float,
        bottom: float,
        w: float,
        banner: str,
        entries: list,
    ) -> None:
        self.draw_section_banner(x, top, w, banner)
        entries_top = top + 20
        row_h = (bottom - entries_top) / len(entries)
        for i, (title, icon, body) in enumerate(entries):
            self.draw_entry(x, entries_top + i * row_h, w, title, icon, body)

    def draw_footer(self, bottom: float, footer_h: float) -> None:
        self.set_fill_color(245, 242, 235)
        self.rect(MARGIN_X, bottom - footer_h, PAGE_W - 2 * MARGIN_X, footer_h - 4, style="F")
        self.set_xy(MARGIN_X + 6, bottom - footer_h + 3)
        self.set_font(self.font_family, "B", 7.5)
        self.set_text_color(50, 40, 30)
        self.cell(PAGE_W - 2 * MARGIN_X - 12, 9, "Phase cycle reminders")
        self.set_xy(MARGIN_X + 6, bottom - footer_h + 12)
        self.set_font(self.font_family, "", 6.8)
        self.set_text_color(55, 45, 35)
        self.multi_cell(PAGE_W - 2 * MARGIN_X - 12, 8, FOOTER)

    def build(self) -> None:
        self.add_page()
        content_top = self.draw_header(top=16)
        footer_h = 40
        grid_bottom = PAGE_H - 12 - footer_h
        col_w = (PAGE_W - 2 * MARGIN_X - COL_GAP) / 2
        left_x = MARGIN_X
        right_x = MARGIN_X + col_w + COL_GAP

        self.draw_column(
            left_x, content_top, grid_bottom, col_w, "ADVENTURING PHASE", ADVENTURING
        )
        self.draw_column(
            right_x, content_top, grid_bottom, col_w, "FELLOWSHIP PHASE", FELLOWSHIP
        )
        self.draw_footer(PAGE_H - 12, footer_h)


def main() -> None:
    pdf = PhasesSheet()
    pdf.build()
    pdf.output(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
