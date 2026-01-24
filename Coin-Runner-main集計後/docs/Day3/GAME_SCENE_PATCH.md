# GAME_SCENE_PATCH.md — Day3 追記箇所
`scenes/game_scene.py` の `update(self, dt)` へ以下を**追記**してください（既存は保持）。

1) 難易度の時間更新
```python
self.difficulty.tick(dt)  # dtはフレーム時間（秒）
```

2) 回避イベント時のスコア加算（例：障害物を避けた瞬間）
```python
self.scoring.add_for_avoid()
```

3) HUD の更新と反映
```python
labels = self.hud.update()
self.label_score.text = labels["score"]
self.label_speed.text = labels["speed"]
```

4) ミス判定で GameOver へ
```python
if self.player.hp <= 0:
    self.navigator.goto_game_over()
```
