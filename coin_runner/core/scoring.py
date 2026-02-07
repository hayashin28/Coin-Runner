# -*- coding: utf-8 -*-
"""core.scoring

Day3〜Day6 用のスコア計算（現行スコア + ベストスコア）。

このリポジトリでは、Day5/Day6 の教材として「ベストスコア」を扱う想定があります。

【責務】
- current: 今回プレイ中のスコア
- best: 今までの最高スコア
- reset(): current を 0 に戻す（best は維持）
- add_for_avoid(): 障害物をよけた等のイベントで加点
- add_points(): 任意の加点（コイン等）
- register_game_over(): ゲーム終了を通知し、ベスト更新なら True

※「保存（永続化）」は core.save_data の責務。
"""

from __future__ import annotations

from dataclasses import dataclass

DEFAULT_AVOID_POINT = 10


@dataclass
class Score:
    """単純なスコア値を 1 個だけ持つデータクラス。"""
    value: int = 0


class ScoringService:
    """スコア計算の中心となるサービスクラス。"""

    def __init__(self, avoid_point: int = DEFAULT_AVOID_POINT, initial_best: int = 0):
        self._score = Score(0)
        self._best = Score(int(initial_best) if int(initial_best) > 0 else 0)
        self._avoid_point = int(avoid_point)

    def reset(self) -> None:
        """今回スコアだけを 0 に戻す（best は維持）。"""
        self._score.value = 0

    def add_for_avoid(self, points: int | None = None) -> None:
        """障害物をよけた等のイベントで加点する。"""
        p = self._avoid_point if points is None else int(points)
        if p < 0:
            p = 0
        self._score.value += p

    def add_points(self, points: int) -> None:
        """任意の加点（コイン等）。"""
        p = int(points)
        if p < 0:
            p = 0
        self._score.value += p

    @property
    def current(self) -> int:
        return int(self._score.value)

    @property
    def best(self) -> int:
        return int(self._best.value)

    def set_best(self, best: int) -> None:
        """ロード結果などで best を上書きする（安全に丸める）。"""
        try:
            b = int(best)
        except Exception:
            b = 0
        if b < 0:
            b = 0
        self._best.value = b

    def register_game_over(self) -> bool:
        """ゲーム終了を通知し、ベスト更新なら True を返す。"""
        if self._score.value > self._best.value:
            self._best.value = int(self._score.value)
            return True
        return False
