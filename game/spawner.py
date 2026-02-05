# -*- coding: utf-8 -*-
"""game.spawner

Day2 のスポーンロジック（フェアな間隔 + 種類選択 + 連結(train)）。

- next_x: 次に出すオブジェクトの x 位置（px）
- last_kind: 直前の kind（デバッグ用）
- train_remaining: train継続の残り回数（ob_train の連結）

kind:
- coin
- ob_low
- ob_high
- ob_train
"""

from __future__ import annotations

import random
from kivy.core.window import Window
from kivy.metrics import dp


def initial_x(spread, first):
    return Window.width + (random.uniform(0, Window.width) if first else random.uniform(0, spread))


def pick_kind(rate):
    return "coin" if random.random() < rate else "ob"


class SpawnState:
    def __init__(self, P, ground_y_px, low_jump_h_px):
        self.P = P
        self.ground = float(ground_y_px)
        self.low_h = float(low_jump_h_px)

        self.next_x = Window.width + random.uniform(0, dp(P.SPAWN_SPREAD_PX))
        self.last_kind: str | None = None

        # train（ob_train）連結用
        self.train_remaining = 0

    def _weighted_choice(self) -> str:
        P = self.P
        items = [
            ("ob_low",  float(getattr(P, "WEIGHT_OB_LOW", 0.50))),
            ("ob_high", float(getattr(P, "WEIGHT_OB_HIGH", 0.25))),
            ("ob_train",float(getattr(P, "WEIGHT_OB_TRAIN", 0.15))),
            ("coin",    float(getattr(P, "WEIGHT_COIN", 0.10))),
        ]
        total = sum(w for _, w in items if w > 0)
        if total <= 0:
            return "coin"
        r = random.random() * total
        acc = 0.0
        for k, w in items:
            if w <= 0:
                continue
            acc += w
            if r <= acc:
                return k
        return items[-1][0]

    def _choose_kind(self) -> str:
        """train 継続ロジック込みで kind を決める。"""
        P = self.P

        # train継続
        if self.train_remaining > 0:
            self.train_remaining -= 1
            self.last_kind = "ob_train"
            return "ob_train"

        kind = self._weighted_choice()

        # ob_train が選ばれたら、連結数を決める
        if kind == "ob_train":
            seg_min = int(getattr(P, "TRAIN_SEGMENTS_MIN", 2))
            seg_max = int(getattr(P, "TRAIN_SEGMENTS_MAX", 3))
            if seg_max < seg_min:
                seg_max = seg_min
            segments = random.randint(seg_min, seg_max)
            # 今回分は今返すので、残りは segments-1
            self.train_remaining = max(0, segments - 1)

        self.last_kind = kind
        return kind

    def next_item(self, speed_px_s: float) -> dict:
        """次の出現情報を dict で返す。

        return:
            {"kind": str, "x": float, "y": float, "w": float, "h": float}
        """
        P = self.P

        # gap: MIN_GAP + U(0, spread) + (高い障害物の直後なら EXTRA)
        spread = dp(getattr(P, "SPAWN_SPREAD_PX", 240))
        gap = dp(getattr(P, "MIN_GAP_PX", 140)) + random.uniform(0, spread)

        if self.last_kind == "ob_high":
            gap += dp(getattr(P, "EXTRA_GAP_AFTER_HIGH", 40))

        # 次の x を更新（速度が速いほどgapはそのまま px）
        self.next_x = max(self.next_x + gap, Window.width + gap)

        kind = self._choose_kind()

        # サイズ・高さ
        if kind == "coin":
            w = h = dp(42)
            y = self.ground + self.low_h * 0.5
        elif kind == "ob_low":
            w = dp(getattr(P, "OB_LOW_W", 42))
            h = dp(getattr(P, "OB_LOW_H", 42))
            y = self.ground
        elif kind == "ob_high":
            w = dp(getattr(P, "OB_HIGH_W", 42))
            h = dp(getattr(P, "OB_HIGH_H", 72))
            y = self.ground + self.low_h
        else:  # ob_train
            w = dp(60)
            h = dp(42)
            y = self.ground

        return {"kind": kind, "x": float(self.next_x), "y": float(y), "w": float(w), "h": float(h)}
