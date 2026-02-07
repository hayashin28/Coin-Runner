# -*- coding: utf-8 -*-
from __future__ import annotations

from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.clock import Clock

from coin_runner.config import Pfrom coin_runner.ui.hud import build_hud, HUDfrom coin_runner.game.player import Playerfrom coin_runner.game.obstacle import Objfrom coin_runner.game.spawner import SpawnStatefrom coin_runner.ui.parallax import ParallaxLayerfrom coin_runner.core.save_data import save_best

def aabb(ax, ay, aw, ah, bx, by, bw, bh):
    return (ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by)


GROUND_Y = dp(P.GROUND_Y_PX)
LOW_JUMP_H = dp(P.JUMP_TIER_PX)


class Play(Screen):
    def __init__(self, scoring, difficulty, save_path: str, **kwargs):
        super().__init__(**kwargs)
        self.scoring = scoring
        self.difficulty = difficulty
        self.save_path = save_path

    def on_pre_enter(self):
        self.root = FloatLayout()
        self.clear_widgets()
        self.add_widget(self.root)

        # HUD
        self.lbl = build_hud()
        self.root.add_widget(self.lbl)

        self.hud = HUD(self.scoring, self.difficulty)

        # Player
        self.player = Player(size=(dp(52), dp(52)))
        self.player.pos = (dp(80), GROUND_Y)
        self.root.add_widget(self.player)

        # Parallax (3 bands)
        self.bg_layers = []
        try:
            band_hs = getattr(P, "BG_BAND_HEIGHTS_PX", (140, 110, 80))
            colors = getattr(P, "BG_COLORS", ((0.10, 0.10, 0.18, 1), (0.16, 0.18, 0.28, 1), (0.22, 0.26, 0.38, 1)))
            ratios = getattr(P, "BG_SPEED_RATIOS", (0.25, 0.5, 0.8))
            y = 0
            for h, c, r in zip(band_hs, colors, ratios):
                layer = ParallaxLayer(band_h_px=h, color=c, size_hint=(1, None), height=dp(h), pos=(0, dp(y)))
                self.root.add_widget(layer)
                self.bg_layers.append((layer, float(r)))
                y += h
        except Exception:
            self.bg_layers = []

        # Spawn state
        self.spawn = SpawnState(P, ground_y_px=GROUND_Y, low_jump_h_px=LOW_JUMP_H)

        # Objects pool
        self.objects = []
        for _ in range(6):
            o = Obj(size=(dp(42), dp(42)))
            self._place_object(o, first=True)
            self.objects.append(o)
            self.root.add_widget(o)

        # State
        self.t = 0.0
        self.energy = 100
        self.game_over = False
        self.new_record = False
        self.debug = False

        # Reset services
        self.scoring.reset()
        self.difficulty.reset()

        Window.bind(on_key_down=self._on_key)
        self._ev = Clock.schedule_interval(self.update, 1 / 60)

    def on_pre_leave(self):
        try:
            Window.unbind(on_key_down=self._on_key)
            if self._ev:
                self._ev.cancel()
        except Exception:
            pass

    def _on_key(self, _w, key, scancode, codepoint, keycode, *_):
        name = keycode[1]
        if self.game_over and name in ("enter", "numpadenter", "spacebar"):
            return self._restart()
        if name in ("up", "spacebar"):
            self.player.try_jump(P)
            return True
        if name == "f1":
            self.debug = not self.debug
            return True
        return False

    def _speed(self) -> float:
        return float(P.BASE_SPEED) * float(self.difficulty.current.speed)

    def _place_object(self, o: Obj, first: bool = False):
        info = self.spawn.next_item(self._speed())
        o.kind = info["kind"]
        o.size = (info["w"], info["h"])
        o.pos = (info["x"], info["y"])

        # color by kind
        if o.kind == "coin":
            o.color = [0.35, 1, 0.35, 1]
        elif o.kind == "ob_low":
            o.color = [1, 0.35, 0.4, 1]
        elif o.kind == "ob_high":
            o.color = [1, 0.2, 0.2, 1]
        else:  # ob_train
            o.color = [0.6, 0.3, 0.1, 1]

    def update(self, dt):
        if self.game_over:
            return

        self.t += dt
        self.difficulty.tick(dt)
        speed = self._speed()

        # Player physics
        self.player.vy += P.GRAVITY * dt
        self.player.y += self.player.vy * dt
        if self.player.y <= GROUND_Y:
            self.player.y = GROUND_Y
            self.player.vy = 0
            self.player.on_ground = True

        # Parallax tick
        for layer, ratio in self.bg_layers:
            try:
                layer.tick(dt, speed * ratio)
            except Exception:
                pass

        # Move objects & recycle
        for o in self.objects:
            o.x -= speed * dt

            if o.right < 0:
                # obstacle passed -> avoid score (coin is excluded)
                if o.kind != "coin":
                    self.scoring.add_for_avoid()
                self._place_object(o, first=False)

        # Collisions
        for o in self.objects:
            if aabb(
                self.player.x,
                self.player.y,
                self.player.width,
                self.player.height,
                o.x,
                o.y,
                o.width,
                o.height,
            ):
                if o.kind == "coin":
                    self.scoring.add_points(P.SCORE_RATE)
                    # collect coin -> move it away immediately
                    self._place_object(o, first=False)
                else:
                    self.energy -= 20
                    if self.energy <= 0:
                        self.energy = 0
                        self._on_game_over()
                        break

        debug_info = None
        if self.debug:
            debug_info = {"t": self.t, "next_x": self.spawn.next_x, "last_kind": self.spawn.last_kind}

        self.lbl.text = self.hud.build_text(
            energy=self.energy,
            debug=debug_info,
            game_over=self.game_over,
            new_record=self.new_record,
        )

    def _on_game_over(self):
        self.game_over = True
        self.new_record = self.scoring.register_game_over()
        if self.new_record:
            save_best(self.save_path, self.scoring.best)
        # HUD final update
        debug_info = None
        if self.debug:
            debug_info = {"t": self.t, "next_x": self.spawn.next_x, "last_kind": self.spawn.last_kind}
        self.lbl.text = self.hud.build_text(
            energy=self.energy,
            debug=debug_info,
            game_over=True,
            new_record=self.new_record,
        )

    def _restart(self):
        # Save best even if not new (optional) – safe
        save_best(self.save_path, self.scoring.best)

        self.t = 0.0
        self.energy = 100
        self.game_over = False
        self.new_record = False

        self.player.pos = (dp(80), GROUND_Y)
        self.player.vy = 0
        self.player.on_ground = True

        self.scoring.reset()
        self.difficulty.reset()

        for o in self.objects:
            self._place_object(o, first=True)

        return True
