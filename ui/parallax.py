# -*- coding: utf-8 -*-
# Day2: パララックス（TODOを埋める）
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp


class ParallaxLayer(Widget):
    def __init__(self, band_h_px, color, **kw):
        super().__init__(**kw)
        self.band_h = dp(band_h_px)
        self.color_rgba = color

        # TODO: canvasにColor/Rectangleを2枚作る→bindで同期→_syncで横並びに　完了
        with self.canvas:
            Color(*self.color_rgba)
            self.rect1 = Rectangle()
            self.rect2 = Rectangle()

        # サイズ・位置が変わったら同期
        self.bind(pos=self._sync, size=self._sync)

    def _sync(self, *a):
        # TODO: Rectangleのsize/posを自分に合わせる　完了
        w = self.width
        h = self.band_h
        x, y = self.x, self.y

        self.rect1.size = (w, h)
        self.rect2.size = (w, h)

        self.rect1.pos = (x, y)
        self.rect2.pos = (x + w, y)

    def tick(self, dt, speed_px_s):
        # TODO: 左へ流し、x<=-widthなら+2*widthでワープ　完了
        dx = speed_px_s * dt

        self.rect1.pos = (self.rect1.pos[0] - dx, self.rect1.pos[1])
        self.rect2.pos = (self.rect2.pos[0] - dx, self.rect2.pos[1])

        w = self.width

        if self.rect1.pos[0] <= -w:
            self.rect1.pos = (self.rect1.pos[0] + 2 * w, self.rect1.pos[1])

        if self.rect2.pos[0] <= -w:
            self.rect2.pos = (self.rect2.pos[0] + 2 * w, self.rect2.pos[1])
