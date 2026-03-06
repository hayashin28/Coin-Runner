# -*- coding: utf-8 -*-
from __future__ import annotations

from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.clock import Clock

from ..config import P
from ..ui.hud import build_hud
from ..game.player import Player
from ..game.obstacle import Obj
from ..game.spawner import SpawnState
from ..ui.parallax import ParallaxLayer
from ..core.save_data import save_best


def aabb(ax, ay, aw, ah, bx, by, bw, bh):
    return (ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by)


GROUND_Y = dp(P.GROUND_Y_PX)
LOW_JUMP_H = dp(P.JUMP_TIER_PX)


class Play(Screen):
    """
    成果発表直前の最小ループ版（Coin-Runner）

    目的：
        - 30秒生き残ると GOAL が右から流れてくる
        - SPACE でジャンプして Hole(=障害物) を回避
        - Coin を取って加点
        - GOAL に触れたら WIN → スコア確定 → 再スタート可

    スコア（確定：A案）：
        - WIN: score = coin*100 + max(0, 3000 - clear_seconds*100) + 1000
        - LOSE: score = coin*50
    """

    def __init__(self, scoring, difficulty, save_path: str, **kwargs):
        super().__init__(**kwargs)
        self.scoring = scoring
        self.difficulty = difficulty
        self.save_path = save_path

    def on_pre_enter(self):
        self.root = FloatLayout()
        self.clear_widgets()
        self.add_widget(self.root)

        # ----------------------------
        # 背景（パララックス）
        # ----------------------------
        self.bg_layers: list[tuple[ParallaxLayer, float]] = []
        try:
            band_hs = getattr(P, "BG_BAND_HEIGHTS_PX", (140, 110, 80))
            colors = getattr(
                P,
                "BG_COLORS",
                (
                    (0.10, 0.10, 0.18, 1),
                    (0.16, 0.18, 0.28, 1),
                    (0.22, 0.26, 0.38, 1),
                ),
            )
            ratios = getattr(P, "BG_SPEED_RATIOS", (0.25, 0.5, 0.8))
            y = 0
            for h, c, r in zip(band_hs, colors, ratios):
                layer = ParallaxLayer(
                    band_h_px=h,
                    color=c,
                    size_hint=(1, None),
                    height=dp(h),
                    pos=(0, dp(y)),
                )
                self.root.add_widget(layer)
                self.bg_layers.append((layer, float(r)))
                y += h
        except Exception:
            self.bg_layers = []

        # ----------------------------
        # スポーン（Coin / Hole）
        # ----------------------------
        self.spawn = SpawnState(P, ground_y_px=GROUND_Y, low_jump_h_px=LOW_JUMP_H)

        # 重要：Widgetは size_hint が (1,1) のままだと巨大化するので None に固定
        self.objects: list[Obj] = []
        for _ in range(6):
            o = Obj(size_hint=(None, None), size=(dp(42), dp(42)))
            self._place_object(o, first=True)
            self.objects.append(o)
            self.root.add_widget(o)

        # ----------------------------
        # GOAL（30秒後に有効化）
        # ----------------------------
        self.goal = Obj(size_hint=(None, None), size=(dp(84), dp(84)))
        # --- BONUS COIN（常時流す） ---
        self.goal.kind = "coin"
        self.goal.color = [1.0, 0.9, 0.2, 1]   # 黄（コイン色）
        self.goal.opacity = 1.0
        self.goal_active = True
        self.goal.size = (dp(96), dp(96))      # 目立たせる
        self.goal.pos = (Window.width + dp(60), GROUND_Y + dp(20))
        self.root.add_widget(self.goal)

        # ----------------------------
        # プレイヤー
        # ----------------------------
        self.player = Player(size_hint=(None, None), size=(dp(52), dp(52)))
        self.player.pos = (dp(80), GROUND_Y)
        self.root.add_widget(self.player)

        # ----------------------------
        # HUD（最上面）
        # ----------------------------
        self.lbl = build_hud()
        # 表示が切れやすいので少し広げる（安全策）
        self.lbl.size = (dp(520), dp(160))
        self.lbl.text_size = self.lbl.size
        self.root.add_widget(self.lbl)

        # ----------------------------
        # 状態
        # ----------------------------
        self.t = 0.0
        self.coin_count = 0
        self.game_over = False
        self.win = False
        self.new_record = False
        self.debug = False

        # reset
        self.scoring.reset()
        self.difficulty.reset()

        Window.bind(on_key_down=self._on_key)
        self._ev = Clock.schedule_interval(self.update, 1 / 60)

    def on_pre_leave(self):
        try:
            Window.unbind(on_key_down=self._on_key)
            if getattr(self, "_ev", None):
                self._ev.cancel()
        except Exception:
            pass


    def _on_key(self, _w, key, scancode, codepoint, modifiers):
        # まずKivyの変換を試す（環境によって空が返る）
        try:
            name = Window.keycode_to_string(key) or ""
        except Exception:
            name = ""

        # フォールバック：今回のログ（key=32, scancode=44, codepoint=' '）に合わせて確実に拾う
        if not name:
            if codepoint == " " or key == 32 or scancode == 44:
                name = "spacebar"
            elif key == 273:  # Up（環境で違う可能性はあるが、spaceが取れれば十分）
                name = "up"
            elif codepoint in ("\r", "\n") or key in (13, 271):
                name = "enter"

        # ここから通常分岐
        if self.game_over and name in ("enter", "numpadenter", "spacebar"):
            return self._restart()

        # プレイ中：ジャンプ
        if name in ("up", "spacebar"):
            if getattr(self.player, "on_ground", True):
                self.player.vy = float(getattr(P, "JUMP_V", 460.0))
                self.player.on_ground = False
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
        o.size_hint = (None, None)
        o.size = (info["w"], info["h"])
        o.pos = (info["x"], info["y"])

        # 見た目：Coin / Hole を明確に
        if o.kind == "coin":
            o.color = [1.0, 0.9, 0.2, 1]   # 黄
        else:
            # ここでは ob_* を Hole として扱う（触れたら即LOSE）
            o.color = [1.0, 0.2, 0.2, 1]   # 赤

    def _ensure_goal(self):
        """30秒経過でGOALを有効化する（視認性を最優先で固定）。"""
        if self.goal_active:
            return
        if self.t < 30.0:
            return

        self.goal_active = True
        self.goal.opacity = 1.0
        self.goal.kind = "goal"
        self.goal.color = [0.2, 1.0, 0.4, 1]   # 緑（目立つ）
        self.goal.size_hint = (None, None)
        self.goal.size = (dp(120), dp(120))    # 大きくして視認性を担保
        self.goal.pos = (Window.width + dp(60), GROUND_Y + dp(20))  # 地面より少し上

    print("[GOAL] spawned at t>=30")
    def update(self, dt):
        # --- TIME LIMIT（30秒で終了 → 結果表示へ） ---
        if self.t >= 30.0:
            self._finish(win=True)  # ここを必ず通す（HUDのResult表示もここでやる）
            return

        self.t += dt
        self.difficulty.tick(dt)
        speed = self._speed()

        # Player physics（Playが責務を持つ：dtベース）
        # 重力は「下向き」が正解なので、常に負に正規化する
        g = float(getattr(P, "GRAVITY", -1200))
        g = -abs(g)
        self.player.vy += g * dt
        self.player.y += self.player.vy * dt
        if self.player.y <= GROUND_Y:
            self.player.y = GROUND_Y
            self.player.vy = 0
            self.player.on_ground = True

        # Parallax
        for layer, ratio in self.bg_layers:
            try:
                layer.tick(dt, speed * ratio)
            except Exception:
                pass

        # Move objects & recycle
        for o in self.objects:
            o.x -= speed * dt
            if o.right < 0:
                self._place_object(o, first=False)

        # GOAL
        self._ensure_goal()
        if self.goal_active:
            self.goal.x -= speed * dt
            if self.goal.right < 0:
                # 見逃しても詰まないように再出現
                self.goal.x = Window.width + dp(60)

        # Collisions: Coin / Hole
        for o in self.objects:
            if self.player.collide_widget(o):
                if o.kind == "coin":
                    self.coin_count += 1
                    self._place_object(o, first=False)
                else:
                    # Hole 接触で即LOSE
                    self._finish(win=False)
                    return

        # Collision: GOAL
        if self.goal_active and aabb(
            self.player.x, self.player.y, self.player.width, self.player.height,
            self.goal.x, self.goal.y, self.goal.width, self.goal.height,
        ):
            # Collision: BONUS COIN（取ったら加点して再出現）
            if self.goal_active and aabb(
                self.player.x, self.player.y, self.player.width, self.player.height,
                self.goal.x, self.goal.y, self.goal.width, self.goal.height,
            ):
                self.coin_count += 3  # ボーナス感（1でもOK）
                self.goal.x = Window.width + dp(60)
                return

        # HUD（目的が伝わる最小表示）
        left = max(0.0, 30.0 - self.t)
        if left > 0:
            goal_txt = f"GOAL in: {left:4.1f}s"
        else:
            goal_txt = "GOAL: ON"

        d = self.difficulty.current
        lines = [
            f"Coin: {self.coin_count}   {goal_txt}",
            f"Speed: x{d.speed:.2f} (Lv.{d.stage})",
            "SPACE: Jump",
        ]
        if self.debug:
            lines.append(f"t:{self.t:.2f}  last:{self.spawn.last_kind}  next_x:{self.spawn.next_x:.1f}")
        self.lbl.text = "\n".join(lines)

    def _finish(self, win: bool):
        """WIN/LOSE確定→スコア確定→HUD表示更新"""
        self.game_over = True
        self.win = bool(win)

        clear_seconds = float(self.t)

        if self.win:
            time_bonus = max(0, int(3000 - clear_seconds * 100))
            score = int(self.coin_count * 100 + time_bonus + 1000)
            status = "WIN"
        else:
            score = int(self.coin_count * 50)
            status = "LOSE"

        # ScoringServiceに「確定スコア」を反映（直前フェーズなので直接代入で止血）
        try:
            self.scoring._score.value = int(score)  # type: ignore[attr-defined]
        except Exception:
            self.scoring.reset()
            self.scoring.add_points(int(score))

        self.new_record = self.scoring.register_game_over()
        if self.new_record:
            save_best(self.save_path, self.scoring.best)

        extra = "\nNEW RECORD! ✨" if self.new_record else ""
        self.lbl.text = (
            f"{status}!   Coin: {self.coin_count}   Time: {clear_seconds:4.1f}s\n"
            f"Score: {score}   Best: {self.scoring.best}\n"
            f"Press Enter/Space to restart."
            f"{extra}"
        )

    def _restart(self):
        # bestは安全のため保存（上書きはscoring.best）
        save_best(self.save_path, self.scoring.best)

        self.t = 0.0
        self.coin_count = 0
        self.game_over = False
        self.win = False
        self.new_record = False

        self.player.pos = (dp(80), GROUND_Y)
        self.player.vy = 0
        self.player.on_ground = True

        self.scoring.reset()
        self.difficulty.reset()

        for o in self.objects:
            self._place_object(o, first=True)

        self.goal_active = False
        self.goal.opacity = 0.0
        self.goal.pos = (Window.width + dp(9999), GROUND_Y)

        return True