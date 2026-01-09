# -*- coding: utf-8 -*-
"""core.save_data（Day6: 生徒用スタブ）

Day6のテーマ：「bestスコアをアプリを閉じても残す」。

このファイルは “保存/読み込みの責務を分離する” ための置き場所です。
Day6では ScoringService に全部書いてもOKですが、分けると読みやすくなります。

方針（おすすめ）：
- JSONで保存する（読みやすい）
- 壊れていたら 0 に戻して続行（例外で落とさない）

保存フォーマット例：
{"best": 350}

TODO：
- load_best(path) を実装する（ファイルが無い/壊れている場合の扱い）
- save_best(path, best) を実装する（ディレクトリ作成を含む）
"""

from __future__ import annotations

import json
import os
from typing import Any


def load_best(path: str) -> int:
    """bestスコアを読み込んで返す。

    仕様（おすすめ）：
    - ファイルが存在しない → 0 を返す
    - JSONが壊れている → 0 を返す
    - {"best": <int>} が取れない → 0 を返す

    NOTE:
    - “落ちないこと” が一番大事。ゲームは続行できるようにします。
    """
    # Day6:TODO ここを実装する（模範解答は講師用に別途）
    return 0


def save_best(path: str, best: int) -> None:
    """bestスコアをJSONに保存する。

    仕様（おすすめ）：
    - 保存先フォルダが無い → 作る（os.makedirs(..., exist_ok=True)）
    - best は int に丸める
    - 失敗しても例外でゲームを止めない（try/except で握ってログへ）

    NOTE:
    - ここも “落ちないこと” を優先します。
    """
    # Day6:TODO ここを実装する（模範解答は講師用に別途）
    pass
