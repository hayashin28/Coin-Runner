# -*- coding: utf-8 -*-
"""ui.hud

HUD（スコアやスピードなどの表示）を担当する小さな部品。

Phase2 では、core のサービス（ScoringService / DifficultyService）を受け取り、
表示文字列を組み立てる形を“正”にする。

ただし、Play は教材として Label 直書きでも回せるため、
build_hud() は Label を返すファクトリとして残す。
"""

from __future__ import annotations


class HUD:
    def __init__(self, scoring_service, difficulty_service):
        self.svc_s = scoring_service
        self.svc_d = difficulty_service

    def build_text(self, energy: int, debug: dict | None = None, game_over: bool = False, new_record: bool = False) -> str:
        s = self.svc_s.current
        b = self.svc_s.best
        d = self.svc_d.current
        lines = [
            f"Score: {s}   Best: {b}",
            f"Speed: x{d.speed:.2f} (Lv.{d.stage})   Energy: {int(energy)}",
        ]
        if debug:
            lines.append(f"t:{debug.get('t',0):.2f}  next_x:{debug.get('next_x',0):.1f}  last:{debug.get('last_kind','-')}")
        if game_over:
            lines.append("Game Over! Press Enter/Space to restart.")
            if new_record:
                lines.append("NEW RECORD! ✨")
        return "\n".join(lines)


def build_hud():
    """HUD表示用の Label を作って返す（Widget）。"""
    from kivy.uix.label import Label
    from kivy.metrics import dp

    lbl = Label(
        text="Score: 0   Best: 0\nSpeed: x1.00 (Lv.1)   Energy: 100",
        size_hint=(None, None),
        size=(dp(420), dp(120)),
        pos=(dp(10), dp(10)),
        halign="left",
        valign="bottom",
        font_size=dp(16),
        markup=False,
    )
    lbl.text_size = lbl.size
    return lbl
