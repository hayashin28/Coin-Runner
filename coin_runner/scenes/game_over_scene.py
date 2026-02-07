# -*- coding: utf-8 -*-
"""scenes.game_over_scene

Day5/Day6 の拡張用。
Phase2 では Play 内で Game Over 表示まで完結させているため、
このファイルは将来の拡張（画面遷移）用に“動く雛形”として整備しておく。
"""

from __future__ import annotations

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.core.window import Window


class GameOverScene(Screen):
    def __init__(self, scoring, on_restart=None, **kwargs):
        super().__init__(**kwargs)
        self.scoring = scoring
        self.on_restart = on_restart
        self._new_record = False

    def set_new_record(self, flag: bool):
        self._new_record = bool(flag)

    def on_pre_enter(self):
        self.clear_widgets()
        msg = f"Game Over\nScore: {self.scoring.current}\nBest: {self.scoring.best}"
        if self._new_record:
            msg += "\nNEW RECORD! ✨"
        msg += "\n\nPress Enter/Space"
        self.add_widget(Label(text=msg, font_size=dp(28)))
        Window.bind(on_key_down=self._on_key)

    def on_pre_leave(self):
        Window.unbind(on_key_down=self._on_key)

    def _on_key(self, _w, key, scancode, codepoint, modifiers):
        try:
            key_name = Window._system_keyboard.keycode_to_string(key)
        except AttributeError:
            key_name = ""
        if key_name in ("enter", "numpadenter", "spacebar"):
            if callable(self.on_restart):
                self.on_restart()
            return True
        return False
