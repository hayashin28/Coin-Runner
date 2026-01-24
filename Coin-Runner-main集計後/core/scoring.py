# -*- coding: utf-8 -*-
"""core.scoring

Day3〜Day5 用のスコア計算クラス。

【Day3 までの前提】
- 「障害物をよけた回数」に応じてスコアを加算する。
- 1回あたりの加算量は avoid_point で決める。

【Day5 の拡張目標（生徒用TODOのイメージ）】
- 「今回のスコア」と「ベストスコア（ハイスコア）」を同時に扱えるようにする。
- GameOver 時に「今回のスコアがベストを更新したか？」を判定する。
- HUD や GameOver 画面から現在スコアとベストスコアを参照できる API を用意する。

ここでは生徒が読みやすいように、最小限の実装 + コメントだけを置いている。
実際の Day5 の作業では、このクラスを拡張してもよい。
    今回のスコアを 0 に戻す
    ハイスコア（best）は残る

障害物をよけた瞬間
    scoring.add_for_avoid()
    スコアが +10（DEFAULT_AVOID_POINT）

GameOver 時
    is_new_record = scoring.register_game_over()

    True  -> ハイスコア更新
    False -> 更新なし

表示（HUD / GameOver 画面）
    scoring.current  # 今回のスコア
    scoring.best     # ハイスコア

【用語解説】

class
    設計図。
    「スコアをどう扱うか」をまとめたもの。

dataclass
    数字を入れる箱を簡単に作る仕組み。
    例: Score(value=10)

property
    「変数みたいに使える関数」。
    実際は関数だが、scoring.current のように書ける。
    読み取り専用の値として使わせたいときに便利。

reset()
    「今回のプレイを最初からやり直す」。

register_game_over()
    「ゲームが終わったことをスコアに知らせる」。
    ベスト更新チェックを行い、True / False を返す。

best（ハイスコア）
    今までで一番良かったスコア。
    リトライしても消えない。"""

from dataclasses import dataclass

DEFAULT_AVOID_POINT = 10

@dataclass
class Score:
    """単純なスコア値を 1個だけ持つデータクラス。

    attributes:
        value: 現在のスコア値（整数）
    """
    value: int = 0


class ScoringService:
    """スコア計算の中心となるサービスクラス。

    【責務】
    - 「現在のスコア」を 1か所で管理する。
    - 「障害物をよけたとき」の加点処理を提供する。

    【Day5 で拡張したい案】（生徒用のヒント）
    - best というフィールドを追加し、「今までの最高スコア」を記録する。
    - ゲーム開始時に reset() で現在スコアだけ 0 に戻し、best は維持する。
    - add_for_avoid() のほかに、ゲーム終了時に呼び出す register_game_over() を用意し、
      そこで「best の更新チェック」を行う。

    ここではクラス自体の形だけを提示し、具体的な Day5 実装は TODO として残してある。
    """
    def __init__(self, avoid_point: int = DEFAULT_AVOID_POINT):
        # 現在スコア用の Score インスタンス
        self._score = Score()
        # Day5:TODO ベストスコア用の変数を追加したい場合はここにフィールドを足す
        # 例: self._best = Score()
        self._best = Score()
        # 1回よけるごとの加点幅
        self._avoid_point = int(avoid_point)
       

    def reset(self) -> None:
        """現在スコアだけを 0 に戻す。

        Day1〜Day3 では「ゲーム開始時・Retry 時に呼ばれる」想定。
        Day5 でハイスコアを扱う場合は、ここでは best はリセットしないのが自然。
        """
        self._score.value = 0
        # Day5:TODO ベストスコアの扱いを変えたい場合はここに処理を追加する

    def add_for_avoid(self, points: int | None = None) -> None:
        """障害物を 1つよけたときにスコアを加算する。

        args:
            points: 加点したい量。None の場合は avoid_point を使う。

        注意:
            - 負の値が渡ってきた場合は 0 点として扱う（減点しない仕様）。
        """
        p = self._avoid_point if points is None else int(points)
        if p < 0:
            p = 0
        self._score.value += p

    @property
    def current(self) -> int:
        """現在のスコア値を整数で返す。"""
        return self._score.value

    # Day5:TODO ここに「best（ハイスコア）」関連の API を追加するアイデア
    # 例:
    @property
    def best(self) -> int:
    #     """今までのプレイで到達した最高スコアを返す。"""
         return self._best.value
    #
    def register_game_over(self) -> bool:
    #"""
    # ゲーム終了時に呼び出し
    # 今回のスコアがベスト更新なら True を返す。
    # """
       if self._score.value > self._best.value:
             self._best.value = self._score.value
             return True
       return False