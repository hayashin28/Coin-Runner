# -*- coding: utf-8 -*-
"""game_app.py

【Phase1: 起動の境界を分離する】
- main.py は「起動トリガー」だけにする（SRP）
- GameApp(MDApp) はここに置き、画面構成（ScreenManager）と初期化を担当する

※このフェーズでは、core サービス（Scoring/Difficulty）などの依存注入はまだ接続しない。
  まず「起動が通る」「画面が出る」を最短距離で安定させる。
"""

from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from .config import P
from .scenes.title import Title
from .scenes.play import Play


class GameApp(MDApp):
    """アプリ境界（起動・画面遷移の初期化）"""

    def build(self):
        # ------------------------------------------------------------
        # [Day1] 画面サイズ固定（教材都合で固定が分かりやすい）
        # ------------------------------------------------------------
        Window.size = (P.WINDOW_W, P.WINDOW_H)

        # ------------------------------------------------------------
        # ScreenManager を組み立て、Title / Play を登録
        # ------------------------------------------------------------
        sm = ScreenManager()
        sm.add_widget(Title(name="title"))
        sm.add_widget(Play(name="play"))
        sm.current = "title"
        return sm
