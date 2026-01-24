# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.core.window import Window

class Title(Screen):
    def on_pre_enter(self):
        # 画面表示前にラベルをセット
        self.clear_widgets()
        self.add_widget(Label(
            text='[ Neon Runner A / Day1 ]\nEnter/Space/Touch',
            size_hint=(1, 1),
            font_size=dp(24),
            markup=True
        ))
        # キーボード入力を受け取るようにバインド
        Window.bind(on_key_down=self.on_key_down)

    def on_pre_leave(self):
        # 画面離脱時にキーボードバインドを解除
        Window.unbind(on_key_down=self.on_key_down)

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        # keycode を文字列に変換して判定
        try:
            key_name = Window._system_keyboard.keycode_to_string(key)
        except AttributeError:
            key_name = ''
        # Enter, NumpadEnter, Space で play に移動
        if key_name in ('enter', 'numpadenter', 'spacebar'):
            self.manager.current = 'play'
            return True  # 他に伝播させない
        return False

    def on_touch_down(self, *args):
        # タッチでも play に移動
        self.manager.current = 'play'
        return True
