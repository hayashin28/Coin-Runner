# -*- coding: utf-8 -*-
"""main.py

【Phase1: SRP（単一責任）】
- このファイルの責務は「起動トリガー」だけ。
- 実際のアプリ境界（GameApp）は game_app.py に置く。

実行例:
    python -m <package_name>.main
"""

from .game_app import GameApp


def main() -> None:
    GameApp().run()


if __name__ == "__main__":
    main()
