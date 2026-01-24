# -*- coding: utf-8 -*-
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, BooleanProperty, ListProperty
from kivy.graphics import Color, Rectangle

class Player(Widget):
    vy = NumericProperty(0.0)
    on_ground = BooleanProperty(True)
    color = ListProperty([0.2,0.9,1,1])
    def __init__(self, **kw):
        super().__init__(**kw)
        with self.canvas:
            self._c=Color(*self.color)
            self._r=Rectangle(size=self.size,pos=self.pos)
        self.bind(pos=self._sync,size=self._sync,color=self._recolor)
    def _sync(self,*a): self._r.pos=self.pos; self._r.size=self.size
    def _recolor(self,*a): self._c.rgba=self.color
    # Day1:TODO 地面でのみジャンプ初速を与える（答えは書かない）
    def jump(self):
    # 地面にいるときだけジャンプ可能
        # if self.on_ground: self.vy=P.JUMP_V; self.on_ground=False; return True
        # return False
        pass
