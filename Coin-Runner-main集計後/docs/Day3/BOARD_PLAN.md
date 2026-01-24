# 板書案（要点）
- ねらい：記録（Score）×時間成長（Difficulty）×再挑戦（Retry）
- API：Scoring.add_for_avoid() / Difficulty.tick(dt)
- 統合順：tick→回避→HUD→ミス判定→遷移
- Retry初期化順：Scoring→Difficulty→Scene
