# Day2 生徒用タスク（日本語ヒント）

## 目標
1) 背景3帯のパララックス
2) 障害3種＋コインのフェア・スポーン
3) F1デバッグ（t/speed/next_x/last）

## 手順
- `ui/parallax.py` のTODOを埋める（矩形2枚でラップ）
- `game/spawner.py` の `SpawnState` を完成（_choose_kind / next_item）
- `scenes/play.py` の D2 コメントに従って、背景tickと再配置処理を追加

## ヒント
- ラップ: 左に1枚分出たら x += 2*width
- 間隔: MIN_GAP + U(0, spread) ／ 高の直後は +EXTRA
- 連結: train_remaining を使って 'ob_train' を継続
