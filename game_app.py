# -*- coding: utf-8 -*-
"""game_app.py

【Phase2: TODO 実装（Day2〜Day6）】
- main.py は起動トリガー
- GameApp はアプリ境界として、依存（coreサービス）を生成して Scene に注入する（DI）
- Best は save/best_score.json に永続化する（壊れていても落ちない）

このフェーズでは「教材の TODO（生徒用スタブ）」を “講師用の完成形” として埋める。
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


class GameApp(MDApp):
    def build(self):
        Window.size = (P.WINDOW_W, P.WINDOW_H)

        # --- save path（教材仕様：プロジェクト直下 save/best_score.json） ---
        base_dir = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(base_dir, "save", "best_score.json")

        # --- core services ---
        best = load_best(save_path)
        scoring = ScoringService(avoid_point=getattr(P, "SCORE_RATE", 10), initial_best=best)
        difficulty = DifficultyService()

        # --- screens (DI) ---
        sm = ScreenManager()
        sm.add_widget(Title(scoring=scoring, name="title"))
        sm.add_widget(Play(scoring=scoring, difficulty=difficulty, save_path=save_path, name="play"))
        sm.current = "title"
        return sm
