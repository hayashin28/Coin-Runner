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
    def __init__(self, navigator, scoring_service, last_score):
        # 画面遷移の制御を行うオブジェクト。
        # Day1〜Day3 時点では「タイトルへ戻る or ゲームをリトライする」だけを担当する。
        self.nav = navigator

        # Day5: スコア管理用サービス
        self.scoring = scoring_service

        # Day5: 直前のプレイスコア
        self.last_score = last_score

        # Day5: NEW RECORD 判定フラグ
        # register_game_over は
        #   True  → ベスト更新
        #   False → 更新なし
        self.is_new_record = self.scoring.register_game_over(last_score)

        # Day6:TODO （発展）GameOver で “NEW RECORD!” を出す + 保存する
        # -----------------------------------------------------------------
        # ねらい：
        # - Day5 で best を作ったら、GameOver で “更新した！” を見せたい
        # - Day6 では “更新した best をファイルへ保存” までやる
        #
        # 設計例：
        # - ScoringService.register_game_over() -> bool を呼ぶ（True=更新）
        # - True のとき self.is_new_record=True にして、画面側が演出する
        # - その直後に scoring.save_best("save/best_score.json") を呼ぶ
        #
        # 注意：
        # - 画面（UI）とロジック（保存）は役割分担すると読みやすくなる
        # - 例外で落ちない設計にする（保存失敗してもゲームは動く）
        # -----------------------------------------------------------------

        # 例:
        # self.last_score = 0
        # self.is_new_record = False

    def on_retry(self):
        """Retry（もう一度遊ぶ）が押されたときに呼ばれる想定のハンドラ。"""
        self.nav.goto_game(reset=True)

    def on_exit(self):
        """Exit（タイトルへ戻る）が押されたときに呼ばれる想定のハンドラ。"""
        self.nav.goto_title()
