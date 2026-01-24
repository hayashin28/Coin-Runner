# -*- coding: utf-8 -*-
import random
from kivy.core.window import Window
from kivy.metrics import dp

# Day1: 簡易ヘルパー（そのまま）
def initial_x(spread, first):
    return Window.width + (random.uniform(0, Window.width) if first else random.uniform(0, spread))
def pick_kind(rate):
    return 'coin' if random.random() < rate else 'ob'

# Day2: 状態付きスポーナ（TODO）
def _choose_kind(self):
    if self.train_remaining > 0:
        self.train_remaining -= 1
        return self.last_kind

    kind = pick_kind(self.P.COIN_RATE)
    self.last_kind = kind
    self.train_remaining = random.randint(1, self.P.TRAIN_LEN_MAX) if kind == 'coin' else 0
    return kind
class SpawnState:
    def __init__(self, P, ground_y_px, low_jump_h_px):
        self.P=P; self.ground=ground_y_px; self.low_h=low_jump_h_px
        self.next_x = Window.width + random.uniform(0, P.SPAWN_SPREAD_PX)
        self.last_kind=None; self.train_remaining=0
        # TODO: 連結の継続／重み付きサンプリング／train_remaining設定
        pass
    def next_item(self, speed):
        # TODO: gap計算→next_x更新→種類選択→y/size決定→dict返す
        pass
