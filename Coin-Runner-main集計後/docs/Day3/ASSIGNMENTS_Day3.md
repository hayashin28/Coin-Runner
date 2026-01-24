# Day3 役割分担（7人×3h）— 体裁準拠
**DoD**
- スコア：回避で+10（可変）
- 難易度：`step_sec` 経過ごとに Lv++ と `speed` 上昇
- HUD：Score / Speed / Lv. 表示
- GameOver：Retry/Exit 遷移（Retry時の**初期化順**= Scoring→Difficulty→Scene）

## タイムテーブル
- 0:00–0:10  役割割当・API確認
- 0:10–0:25  設計読合せ（I/O/副作用/例外）
- 0:25–1:15  実装1
- 1:15–1:25  休憩
- 1:25–2:05  実装2（結合）
- 2:05–2:35  検証/修正
- 2:35–2:55  PR→レビュー→マージ
- 2:55–3:00  タグ `day3-2025-10-31`

## 7ロール
1 Scoring / 2 Difficulty / 3 HUD / 4 GameScene統合 / 5 GameOver / 6 Config / 7 QA
