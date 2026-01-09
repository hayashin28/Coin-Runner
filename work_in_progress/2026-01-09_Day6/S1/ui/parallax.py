# -*- coding: utf-8 -*-
# Day2: パララックス（TODOを埋める）
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
class ParallaxLayer(Widget):
    def __init__(self, band_h_px, color, **kw):
        super().__init__(**kw)
        self.band_h = dp(band_h_px); self.color_rgba = color
        # TODO: canvasにColor/Rectangleを2枚作る→bindで同期→_syncで横並びに
        pass
    def _sync(self,*a):
        # TODO: Rectangleのsize/posを自分に合わせる
        pass
    def tick(self, dt, speed_px_s):
        # TODO: 左へ流し、x<=-widthなら+2*widthでワープ
        pass
