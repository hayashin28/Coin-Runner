# CONFIG_PATCH.md — Day3 追記箇所
`config.py` に下記定数を**追加**してください（単位明記）。

```python
# 難易度カーブ（秒/倍率）
DIFFICULTY_STEP_SEC = 20.0
DIFFICULTY_INCREMENT = 0.15
DIFFICULTY_MAX_STAGE = 10

# スコア
AVOID_POINT = 10
```
