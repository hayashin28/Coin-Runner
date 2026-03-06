# pyright: ignore
# -*- coding: utf-8 -*-
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty, ListProperty, BooleanProperty
from kivy.graphics import Color, Rectangle, Ellipse, Line


class Obj(Widget):
    kind = StringProperty("ob")
    vx = NumericProperty(200.0)
    color = ListProperty([1, 1, 1, 1])
    alive = BooleanProperty(True)

    def __init__(self, **kw):
        super().__init__(**kw)

        with self.canvas:
            # --- default (rectangle) ---
            self._c_rect = Color(1, 1, 1, 1)
            self._r_rect = Rectangle(size=self.size, pos=self.pos)

            # --- coin (platformer-like, original) ---
            self._c_coin_out = Color(1.0, 0.86, 0.18, 0.0)
            self._e_coin_out = Ellipse(size=self.size, pos=self.pos)

            self._c_coin_in = Color(1.0, 0.74, 0.12, 0.0)
            self._e_coin_in = Ellipse(size=self.size, pos=self.pos)

            self._c_coin_hi = Color(1.0, 1.0, 1.0, 0.0)
            self._e_coin_hi = Ellipse(size=self.size, pos=self.pos)

            self._c_coin_edge = Color(0.45, 0.27, 0.05, 0.0)
            self._l_coin = Line(ellipse=(0, 0, 0, 0), width=1.1)

        self.bind(pos=self._sync, size=self._sync, color=self._apply_style, kind=self._apply_style)
        self._sync()
        self._apply_style()

    def _sync(self, *a):
        # rect
        self._r_rect.pos = self.pos
        self._r_rect.size = self.size

        # coin (縦長の楕円にして“コイン感”)
        x, y = self.pos
        w, h = self.size
        cx = x + w * 0.20
        cy = y + h * 0.10
        cw = w * 0.60
        ch = h * 0.80

        # 外周
        self._e_coin_out.pos = (cx, cy)
        self._e_coin_out.size = (cw, ch)

        # 内側（少し小さく）
        ix = cx + cw * 0.10
        iy = cy + ch * 0.12
        iw = cw * 0.80
        ih = ch * 0.76
        self._e_coin_in.pos = (ix, iy)
        self._e_coin_in.size = (iw, ih)

        # ハイライト（左上に小さく）
        hx = cx + cw * 0.18
        hy = cy + ch * 0.55
        hw = cw * 0.22
        hh = ch * 0.28
        self._e_coin_hi.pos = (hx, hy)
        self._e_coin_hi.size = (hw, hh)

        # 縁取り
        self._l_coin.ellipse = (cx, cy, cw, ch)

    def _apply_style(self, *a):
        if self.kind == "coin":
            # hide rect
            r, g, b, a0 = self.color if len(self.color) >= 4 else (1, 1, 1, 1)
            self._c_rect.rgba = (r, g, b, 0.0)

            # show coin
            self._c_coin_out.rgba = (1.0, 0.86, 0.18, 1.0)
            self._c_coin_in.rgba = (1.0, 0.74, 0.12, 1.0)
            self._c_coin_hi.rgba = (1.0, 1.0, 1.0, 0.35)
            self._c_coin_edge.rgba = (0.45, 0.27, 0.05, 1.0)
        else:
            # show rect
            r, g, b, a0 = self.color if len(self.color) >= 4 else (1, 1, 1, 1)
            self._c_rect.rgba = (r, g, b, a0)

            # hide coin
            self._c_coin_out.rgba = (1, 1, 1, 0.0)
            self._c_coin_in.rgba = (1, 1, 1, 0.0)
            self._c_coin_hi.rgba = (1, 1, 1, 0.0)
            self._c_coin_edge.rgba = (1, 1, 1, 0.0)

    # 左へ流す＆画面外でalive=False
    def update(self, dt):
        self.x -= self.vx * dt
        if self.x + self.width < 0:
            self.alive = False

    def tick(self, dt):
        pass

    def recycle_to_right(self, x, y, speed, kind):
        pass