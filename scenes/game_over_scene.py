# -*- coding: utf-8 -*-
"""scenes.game_over_scene

GameOver 画面用のロジック雛形。

【Day3 まで】
- Retry ボタンでゲームに戻る。
- Exit ボタンでタイトルに戻る。
- 画面の見た目やラベル表示は、別の Kivy Screen 側で定義する想定。

【Day5 の拡張案（生徒用TODOのイメージ）】
- 「今回のスコア」と「ベストスコア」を受け取り、
  NEW RECORD! メッセージを出すかどうか判定する。
- 例えば、GameOverScene.__init__ に scoring_service を渡し、
  register_game_over() の戻り値に応じてフラグを立てる設計にしてもよい。
"""


class GameOverScene:
    def __init__(self, navigator):
        # 画面遷移の制御を行うオブジェクト。
        # Day1〜Day3 時点では「タイトルへ戻る or ゲームをリトライする」だけを担当する。
        self.nav = navigator
        # Day5:TODO 必要ならここに「直前スコア」「ベスト更新フラグ」などのフィールドを追加してよい。
        # 例:
        # self.last_score = 0
        # self.is_new_record = False

    def on_retry(self):
        """Retry（もう一度遊ぶ）が押されたときに呼ばれる想定のハンドラ。"""
        self.nav.goto_game(reset=True)

    def on_exit(self):
        """Exit（タイトルへ戻る）が押されたときに呼ばれる想定のハンドラ。"""
        self.nav.goto_title()
