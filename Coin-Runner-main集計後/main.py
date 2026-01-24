# -*- coding: utf-8 -*-
from kivymd.app import MDApp
from kivy.core.window import Window
from .config import P
from .scenes.title import Title
from .scenes.play import Play
from kivy.uix.screenmanager import ScreenManager

class GameApp(MDApp):
    def build(self):
        Window.size=(P.WINDOW_W,P.WINDOW_H)
        sm=ScreenManager(); sm.add_widget(Title(name="title")); sm.add_widget(Play(name="play")); sm.current="title"
        return sm

if __name__=="__main__":
    GameApp().run()

# -*- coding: utf-8 -*-
"""
=============================

このファイルで“埋める”もの（全体解答ではない）
-----------------------------------------------
- [Day4-A] Title → Play 導線（Enter/Space/Touch）
- [Day5-D] GameOver 検知 → （可能なら）ScoringService通知 → GameOver画面へ遷移
  ※ ここでは「main.pyだけで橋渡し」する。Play.py 側は触らない。

なぜ main.py で橋渡しできる？
----------------------------
- Play(Screen) は update() 内で energy<=0 のとき self.game_over=True にする。
- main.py が「play_screen.game_over を定期監視」すれば、
  “ゲーム終了の瞬間”を捕まえられる。

このZipの注意（超重要）
----------------------
- scenes/game_over_scene.py は雛形の途中（未完成）なので、
  それを import すると落ちる可能性がある。
- よって「動けば尚よし」を優先し、GameOver用Screenを main.py 内に最小実装する。

用語（3つまで）
--------------
- ポーリング：一定間隔で状態を見に行って変化を検知する方式。
- 橋渡し：A（Play）で起きた出来事をB（Scoring/画面遷移）へ伝える役。
- ScreenManager：複数の画面（Screen）を切り替えるコンテナ。
"""

Exception
from config import P
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.clock import Clock

# ------------------------------------------------------------
# 起動方法の差に強くする（動けば尚よし）
# - python -m パッケージ起動 → 相対import OK
# - python main.py 直実行     → 相対importが落ちることがある
# ------------------------------------------------------------
try:
    from .config import P
    from .scenes.title import Title
    from .scenes.play import Play
    from .core.scoring import ScoringService
except Exception:
    from config import P
    from scenes.title import Title
    from scenes.play import Play
    from core.scoring import ScoringService


class GameOver(Screen):
    """
    [Day4-B / Day5-C] 本来は別ファイルでUIを作るのが自然だが、
    このZipでは雛形が未完成の可能性があるため、main.py内で最小実装する。

    できること（最小）
    - スコア表示（今回 / Best / NEW RECORD）
    - Enter/Space で Retry、Esc で Title
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._label = Label(
            text="GAME OVER",
            size_hint=(1, 1),
            halign="center",
            valign="middle",
            font_size=dp(22),
        )
        # Labelのhalign/valignを効かせるには text_size が必要
        self._label.bind(size=lambda *_: setattr(self._label, "text_size", self._label.size))
        self.add_widget(self._label)

    def set_message(self, last_score: int, best_score: int, is_new_record: bool):
        # [Day5-C] NEW RECORD 表示条件：今回 > best(前回まで)
        new_txt = "\n[ NEW RECORD! ]" if is_new_record else ""
        self._label.text = (
            f"[ Coin-Runner / GameOver ]\n\n"
            f"Score: {last_score}\n"
            f"Best : {best_score}"
            f"{new_txt}\n\n"
            f"Enter/Space : Retry\n"
            f"Esc         : Title"
        )


class GameApp(MDApp):
    def build(self):
        # ============================================================
        # [Day1] 画面サイズ固定
        # ============================================================
        Window.size = (P.WINDOW_W, P.WINDOW_H)

        # ============================================================
        # ScreenManager 構築（Title / Play / GameOver）
        # ============================================================
        self.sm = ScreenManager()
        self.sm.add_widget(Title(name="title"))
        self.sm.add_widget(Play(name="play"))

        # [Day4-B] 本来の GameOver 画面は別担当だが、main.py内の最小Screenで代替
        self.sm.add_widget(GameOver(name="game_over"))

        self.sm.current = "title"

        # ============================================================
        # [Day5-A] スコアサービス（Best管理はDay5で発展）
        # ============================================================
        self.scoring = ScoringService()
        # main.pyだけでBestを見せたいので、ここでは最小のbest保持を自前で用意
        self.best_score = 0

        # ============================================================
        # [Day4-A] 入力：Title→Play 導線（Enter/Space）
        # [Day5-D] 入力：GameOver→Retry/Title
        # ============================================================
        Window.bind(on_key_down=self._on_key_down_router)

        # ============================================================
        # [Day5-D] GameOver検知の“橋渡し”（ポーリング監視）
        # ============================================================
        # Playは on_pre_enter で player/objects を組み立て、updateを回す。
        # その結果として game_over=True が立つ。
        # → main.py側で play.game_over を監視して検知する。
        self._handled_game_over = False
        self._watch_ev = Clock.schedule_interval(self._watch_game_over, 1/30)

        # ============================================================
        # [Day5-D 追加保険] Playの再入場でUIが二重に積まれないようにパッチ
        # ============================================================
        # 何が起きる？
        # - ScreenManagerで play→game_over→play と戻ると、
        #   Play.on_pre_enter が毎回 root を add_widget してしまい重なる可能性がある。
        #
        # 対策（main.pyだけで出来る最小）
        # - Play.on_pre_enter を“初回だけ実行”し、2回目以降は _restart() だけ呼ぶ
        self._patch_play_reenter()

        return self.sm

    # ------------------------------------------------------------
    # [Day5-D] Play 再入場パッチ（main.pyだけで動作安定）
    # ------------------------------------------------------------
    def _patch_play_reenter(self):
        play = self.sm.get_screen("play")

        if getattr(play, "_nia_patched", False):
            return

        original_on_pre_enter = getattr(play, "on_pre_enter", None)
        original_on_pre_leave = getattr(play, "on_pre_leave", None)

        def patched_on_pre_enter(*args, **kwargs):
            # 2回目以降：UIを積まずに “再開” だけ
            if getattr(play, "_nia_built_once", False):
                # ここは「動けば尚よし」最優先の保険
                try:
                    # Playのupdateが止まっているので、復帰させる
                    if hasattr(play, "_restart"):
                        play._restart()
                    # Playは on_pre_enter 内で Window.bind / Clock.schedule をしているので
                    # それと同等の復帰を最小で行う
                    try:
                        Window.bind(on_key_down=play._on_key)
                    except Exception:
                        pass
                    try:
                        # すでに _ev があれば再作成
                        play._ev = Clock.schedule_interval(play.update, 1/60)
                    except Exception:
                        pass
                except Exception:
                    pass
                return

            # 初回：元の実装をそのまま実行
            play._nia_built_once = True
            if callable(original_on_pre_enter):
                return original_on_pre_enter(*args, **kwargs)

        def patched_on_pre_leave(*args, **kwargs):
            # 元の挙動（unbind/cancel）は尊重
            if callable(original_on_pre_leave):
                return original_on_pre_leave(*args, **kwargs)

        play.on_pre_enter = patched_on_pre_enter
        play.on_pre_leave = patched_on_pre_leave
        play._nia_patched = True

    # ------------------------------------------------------------
    # [Day4-A / Day5-D] キー入力ルータ（main.pyで導線を保証）
    # ------------------------------------------------------------
    def _on_key_down_router(self, window, key, scancode, codepoint, modifiers):
        current = self.sm.current

        # Title → Play（Day4-A）
        if current == "title":
            # Enter(13) / NumpadEnter(271) / Space(32)
            if key in (13, 271, 32) or codepoint in (" ", "\r", "\n"):
                self.sm.current = "play"
                # GameOver監視の状態を戻す（新しいプレイが始まるため）
                self._handled_game_over = False
                return True
            return False

        # GameOver → Retry / Title（Day5-D）
        if current == "game_over":
            # Retry
            if key in (13, 271, 32) or codepoint in (" ", "\r", "\n"):
                self._retry_from_game_over()
                return True
            # Esc(27)
            if key == 27:
                self.sm.current = "title"
                return True
            return False

        # Play中のキーは Play自身（ジャンプ等）に任せる
        return False

    # ------------------------------------------------------------
    # [Day5-D] GameOver監視：Play.game_over を検知して遷移する
    # ------------------------------------------------------------
    def _watch_game_over(self, dt):
        # Play画面が存在しない/まだ入ってない間は何もしない
        try:
            play = self.sm.get_screen("play")
        except Exception:
            return

        # play.game_over がまだ生えていない（未入場）なら待つ
        if not hasattr(play, "game_over"):
            return

        # すでに処理済みなら二重発火を防ぐ
        if self._handled_game_over:
            return

        # ここが“橋渡し”の核心：Playがgame_over=Trueにした瞬間を捕まえる
        if getattr(play, "game_over", False):
            self._handled_game_over = True

            # スコア回収（Playは self.score を持つ）
            last_score = int(getattr(play, "score", 0))

            # [Day5-D] ScoringService へ通知（もし Day5でAPIが実装されていれば呼ぶ）
            # ただし現在のScoringServiceには register_game_over が未実装の可能性がある。
            # → “あれば呼ぶ / 無ければ best を自前で更新”で安全にする。
            is_new_record = False
            try:
                # ScoringService.current は読み取り専用なので、
                # ここでは「通知の概念」を見せるための最小手当として内部に反映する。
                # （※授業では Day5-A で正しいAPIを作るのが本筋）
                if hasattr(self.scoring, "_score"):
                    self.scoring._score.value = last_score  # 教材のための最小ブリッジ（privateアクセス）
                if hasattr(self.scoring, "register_game_over"):
                    is_new_record = bool(self.scoring.register_game_over())
            except Exception:
                pass

            # best管理（main.py側の最小）
            if last_score > self.best_score:
                is_new_record = True
                self.best_score = last_score

            # GameOver画面にメッセージをセット
            go = self.sm.get_screen("game_over")
            go.set_message(last_score=last_score, best_score=self.best_score, is_new_record=is_new_record)

            # 画面遷移（Title→Play→GameOver が成立）
            self.sm.current = "game_over"

    # ------------------------------------------------------------
    # [Day5-D] Retry：Playをリセットして戻る
    # ------------------------------------------------------------
    def _retry_from_game_over(self):
        play = self.sm.get_screen("play")

        # Playに _restart があるので、それを使う（UIを積み増ししない）
        try:
            if hasattr(play, "_restart"):
                play._restart()
        except Exception:
            pass

        # Playへ戻す
        self.sm.current = "play"
        self._handled_game_over = False


if __name__ == "__main__":
    GameApp().run()