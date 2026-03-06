# -*- coding: utf-8 -*-
"""core.save_data（Day6: Best保存）

保存先（教材でおすすめの固定）：save/best_score.json
フォーマット：{"best": 350}

重要：
- 壊れていても落ちない
- ファイルが無くても続行
"""

from __future__ import annotations

import json
import os
from typing import Any


def _safe_int(v: Any, default: int = 0) -> int:
    try:
        i = int(v)
    except Exception:
        return default
    return i if i >= 0 else 0


def load_best(path: str) -> int:
    """bestスコアを読み込んで返す。

    仕様：
    - ファイルが存在しない → 0
    - JSONが壊れている → 0
    - {"best": <int>} が取れない → 0
    """
    try:
        if not path or not os.path.exists(path):
            return 0
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return 0
        return _safe_int(data.get("best", 0), 0)
    except Exception:
        return 0


def save_best(path: str, best: int) -> None:
    """bestスコアをJSONに保存する。

    仕様：
    - 保存先フォルダが無い → 作る
    - 失敗しても例外でゲームを止めない
    """
    try:
        if not path:
            return
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        payload = {"best": _safe_int(best, 0)}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False)
    except Exception:
        # 落ちないこと優先。必要なら print 等に差し替える。
        return
