# -*- coding: utf-8 -*-
"""ui.hud

HUD（スコアやスピードなどのラベル文言）を組み立てるための小さなクラス。

【Day3 までの前提】
- ScoringService / DifficultyService から現在値をもらい、
  「Score: xxx」「Speed: x1.00 (Lv.1)」のような文字列を返す。

【Day5 の拡張案（生徒用TODOのイメージ）】
- ベストスコア（ハイスコア）を追加で表示する。
  例: "Score: 120  Best: 350" のような形式。
- 必要であればコンボ数や残りエネルギーなどもここで整形してよい。
"""


class HUD:
    def __init__(self, scoring_service, difficulty_service):
        """HUD に必要なサービスを受け取って保持する。

        args:
            scoring_service: 現在スコアやベストスコアを管理するサービス。
            difficulty_service: 現在の難易度レベル・速度倍率を管理するサービス。
        """
        self.svc_s = scoring_service
        self.svc_d = difficulty_service

    def get_labels(self) -> dict:
        """画面に表示したいラベル文字列を dict で返す。

        return の例:
            {
                "score": "Score: 120",
                "speed": "Speed: x1.20 (Lv.3)",
                # Day5:TODO 実装次第で "best": "Best: 350" などを追加してもよい
            }
        """
        s = self.svc_s.current
        d = self.svc_d.current
        labels = {
            "score": f"Score: {s}",
            "speed": f"Speed: x{d.speed:.2f} (Lv.{d.stage})",
        }
        # Day5:TODO ハイスコア best を表示したい場合のヒント
        # if hasattr(self.svc_s, "best"):
        #     labels["best"] = f"Best: {self.svc_s.best}"
        return labels
