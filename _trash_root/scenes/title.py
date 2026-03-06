# -*- coding: utf-8 -*-
from __future__ import annotations

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.core.window import Window


class Title(Screen):
    def __init__(self, scoring, **kwargs):
        super().__init__(**kwargs)
        self.scoring = scoring

    def on_pre_enter(self):
        self.clear_widgets()
        best = getattr(self.scoring, "best", 0)
        self.add_widget(
            Label(
                text=f"[ Coin Runner ]\nBest: {best}\n\nEnter/Space/Touch",
                size_hint=(1, 1),
                font_size=dp(24),
                markup=False,
            )
        )
        Window.bind(on_key_down=self.on_key_down)

    def on_pre_leave(self):
        Window.unbind(on_key_down=self.on_key_down)

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        try:
            key_name = Window._system_keyboard.keycode_to_string(key)
        except AttributeError:
            key_name = ""
        if key_name in ("enter", "numpadenter", "spacebar"):
            self.manager.current = "play"
            return True
        return False

    def on_touch_down(self, *args):
        self.manager.current = "play"
        return True
