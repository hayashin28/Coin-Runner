# -*- coding: utf-8 -*-
"""
optional_assets.py

任意アセット（背景/スプライト/BGM）を「無くても落ちない」で扱うための薄い層。

設計意図（成果発表直前の安全設計）
- 取得できなければ None を返す（例外で落とさない）
- ロード失敗も None（try/exceptで握る）
- 利用側は「if tex: / if snd:」でフォールバックへ
- パス解決だけはユーザー側で実装（ここだけ差し替え対象）

このファイルは “真似させる型” として、厚めにコメントを付けてあります。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict

from kivy.core.audio import SoundLoader
from kivy.core.image import Image as CoreImage
from kivy.graphics.texture import Texture


@dataclass
class OptionalAssets:
    """
    OptionalAssets は「アセットがあれば使う、無ければ無視する」を保証する。

    なぜこの形？
    - 成果発表直前は、音や画像の欠落で例外落ちするのが最悪
    - なので、ここで“失敗を飲み込む”責務を一箇所に集約する
    """
    debug: bool = True

    # キャッシュ：同じキーを何度もロードしても重くならないように（任意）
    _tex_cache: Dict[str, Optional[Texture]] = None  # type: ignore[assignment]
    _snd_cache: Dict[str, object] = None             # type: ignore[assignment]

    def __post_init__(self):
        self._tex_cache = {}
        self._snd_cache = {}

    # ------------------------------------------------------------
    # ここだけ “実装”
    # ------------------------------------------------------------
    def _assets_dir(self) -> Path:
        # coin_runner/optional_assets.py の場所から assets/ を指す
        return Path(__file__).resolve().parent / "assets"

    def get_image_path(self, key: str) -> Optional[Path]:
        m = {
            "bg_tile": "img/bg_tile.png",
            "player": "img/player.png",
            "coin": "img/coin.png",
            "hazard_red": "img/hazard.png",
        }
        rel = m.get(key)
        if not rel:
            return None
        p = self._assets_dir() / rel
        return p if p.exists() else None

    def get_sound_path(self, key: str) -> Optional[Path]:
        m = {
            "bgm": "bgm/bgm.ogg",
            "se_coin": "se/coin.wav",
        }
        rel = m.get(key)
        if not rel:
            return None
        p = self._assets_dir() / rel
        return p if p.exists() else None

    # ------------------------------------------------------------
    # ここから下は “完成品”：例外を表に出さない
    # ------------------------------------------------------------
    def _log(self, msg: str) -> None:
        if self.debug:
            print(msg)

    def load_texture(self, key: str, use_cache: bool = True) -> Optional[Texture]:
        """
        画像を Texture としてロードして返す。
        - 入力: key（論理名）
        - 出力: Texture または None
        - 例外: ここでは投げない（すべて None）
        """
        if use_cache and key in self._tex_cache:
            return self._tex_cache[key]

        p = self.get_image_path(key)
        if not p:
            self._log(f"[ASSET] texture not set: {key}")
            if use_cache:
                self._tex_cache[key] = None
            return None

        try:
            p = Path(p)
            if not p.exists():
                self._log(f"[ASSET] texture missing: {key} -> {p}")
                if use_cache:
                    self._tex_cache[key] = None
                return None

            tex = CoreImage(str(p)).texture
            if use_cache:
                self._tex_cache[key] = tex
            return tex
        except Exception as e:
            self._log(f"[ASSET] texture load failed: {key} ({e})")
            if use_cache:
                self._tex_cache[key] = None
            return None

    def load_sound(self, key: str, loop: bool = True, volume: float = 0.7, use_cache: bool = True):
        """
        音を Sound としてロードして返す。
        - 入力: key（論理名）
        - 出力: Sound または None
        - 副作用: loop/volume をここで設定
        - 例外: ここでは投げない（すべて None）
        """
        if use_cache and key in self._snd_cache:
            return self._snd_cache[key]

        p = self.get_sound_path(key)
        if not p:
            self._log(f"[ASSET] sound not set: {key}")
            if use_cache:
                self._snd_cache[key] = None
            return None

        try:
            p = Path(p)
            if not p.exists():
                self._log(f"[ASSET] sound missing: {key} -> {p}")
                if use_cache:
                    self._snd_cache[key] = None
                return None

            snd = SoundLoader.load(str(p))
            if not snd:
                self._log(f"[ASSET] sound loader returned None: {key} -> {p}")
                if use_cache:
                    self._snd_cache[key] = None
                return None

            snd.loop = bool(loop)
            snd.volume = float(volume)

            if use_cache:
                self._snd_cache[key] = snd
            return snd
        except Exception as e:
            self._log(f"[ASSET] sound load failed: {key} ({e})")
            if use_cache:
                self._snd_cache[key] = None
            return None