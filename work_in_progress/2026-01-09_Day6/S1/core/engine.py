# -*- coding: utf-8 -*-
# ScreenManagerで Title→Play の画面切り替えを行います。
# 毎フレームの更新は各Screen側でClockを使って行います。

from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock

class GameSM(ScreenManager):
    pass

def wire_fps_update(screen, update_fn, fps=60):
    # Screenに60FPSの更新をひもづけるヘルパー（必要になったら使用）。
    state = {"ev": None}
    def on_enter(*_):
        if state["ev"] is None:
            state["ev"] = Clock.schedule_interval(lambda dt: update_fn(dt), 1.0/fps)
    def on_leave(*_):
        if state["ev"] is not None:
            state["ev"].cancel(); state["ev"] = None
    screen.bind(on_pre_enter=on_enter, on_pre_leave=on_leave)
    return screen
