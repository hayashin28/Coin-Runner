# -*- coding: utf-8 -*-
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty, ListProperty, BooleanProperty
from kivy.graphics import Color, Rectangle

class Obj(Widget):
    kind = StringProperty("ob")
    vx   = NumericProperty(200.0)
    color= ListProperty([1,1,1,1])
    alive= BooleanProperty(True)
    def __init__(self, **kw):
        super().__init__(**kw)
        with self.canvas:
            self._c=Color(*self.color); self._r=Rectangle(size=self.size,pos=self.pos)
        self.bind(pos=self._sync,size=self._sync,color=self._clr)
    def _sync(self,*a): self._r.pos=self.pos; self._r.size=self.size
    def _clr(self,*a): self._c.rgba=self.color
    # Day1: 左へ流す＆画面外でalive=False（答えは書かない）
    def update(self, dt):
        self.x -= self.vx * dt
        if self.x + self.width < 0:
            self.alive = False

    def tick(self, dt):
        pass
    # Day1: 右端へ再配置（答えは書かない）
    def recycle_to_right(self, x, y, speed, kind):
        pass
