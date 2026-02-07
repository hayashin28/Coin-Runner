# -*- coding: utf-8 -*-
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, BooleanProperty, ListProperty
from kivy.graphics import Color, Rectangle

GRAVITY = -0.5   # 重力（負の値で下方向）
JUMP_V = 10      # ジャンプ初速

class Player(Widget):
    vy = NumericProperty(0.0)
    on_ground = BooleanProperty(True)
    color = ListProperty([0.2, 0.9, 1, 1])

    def __init__(self, **kw):
        super().__init__(**kw)
        with self.canvas:
            self._c = Color(*self.color)
            self._r = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self._sync, size=self._sync, color=self._recolor)

    def _sync(self, *a):
        self._r.pos = self.pos
        self._r.size = self.size

    def _recolor(self, *a):
        self._c.rgba = self.color

    def jump(self):
        """地面にいるときだけジャンプ初速を与える"""
        if self.on_ground:
            self.vy = JUMP_V
            self.on_ground = False
            return True
        return False

    def update(self):
        """毎フレーム呼ぶ更新処理（重力と床判定）"""
        # 重力を加える
        self.vy += GRAVITY

        # Y座標を更新
        self.y += self.vy

        # 地面判定（y=0を地面とする例）
        if self.y <= 0:
            self.y = 0
            self.vy = 0
            self.on_ground = True
