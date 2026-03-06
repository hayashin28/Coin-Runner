# -*- coding: utf-8 -*-
"""game_app.py

アプリ境界（DIの起点）。

- main.py は起動トリガー
- GameApp は依存（coreサービス）を生成して Scene に注入する（DI）
- Best は save/best_score.json に永続化する（壊れていても落ちない）

- Window.clearcolor を指定して「白背景で白文字が見えない」問題を確実に回避
- どの game_app が実行されているかを print で固定（ズレ検知用）
"""

from __future__ import annotations

import os

from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from .config import P
from .core.scoring import ScoringService
from .core.difficulty import DifficultyService
from .core.save_data import load_best
from .scenes.title import Title
from .scenes.play import Play
from .optional_assets import OptionalAssets


class GameApp(MDApp):
    def build(self):
        Window.size = (P.WINDOW_W, P.WINDOW_H)
        self.theme_cls.theme_style = "Dark"
        
        # --- patch: 視認性のため背景を暗く固定 ---
        Window.clearcolor = (0.08, 0.08, 0.10, 1)

        # --- Optional assets entrypoint（無くても落ちない）---
        self.assets = OptionalAssets(debug=True)

        # --- Optional BGM（無ければ無音で続行）---
        self._bgm = self.assets.load_sound("bgm", loop=True, volume=0.7)
        if self._bgm is not None:
            self._bgm.play() # pyright: ignore[reportAttributeAccessIssue]

        # --- patch: 実行されているモジュールを事実で固定 ---
        print("[BOOT] coin_runner.game_app build()")

        # --- save path（coin_runner 配下に save/best_score.json） ---
        base_dir = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(base_dir, "save", "best_score.json")

        # --- core services ---
        best = load_best(save_path)
        scoring = ScoringService(
            avoid_point=getattr(P, "SCORE_RATE", 10),
            initial_best=best,
        )
        difficulty = DifficultyService()

        # --- screens (DI) ---
        sm = ScreenManager()
        sm.add_widget(Title(scoring=scoring, name="title"))
        sm.add_widget(Play(scoring=scoring, difficulty=difficulty, save_path=save_path, name="play"))
        sm.current = "title"
        return sm