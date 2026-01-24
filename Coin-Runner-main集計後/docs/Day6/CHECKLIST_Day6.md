# CHECKLIST Day6（Coin-Runner）

## 最低ライン（合格条件）
- [ ] saveファイルが無くても起動できる（Best=0）
- [ ] Best更新で save/best_score.json が作られる
- [ ] 再起動しても Best が残る
- [ ] best_score.json が壊れていても落ちない（Best=0で続行）
- [ ] NEW RECORD! が分かる（1行でもOK）

## 目視テスト（3分）
- [ ] Title/Play/GameOver のどこかで Best が見える
- [ ] Best が増えたときだけ NEW RECORD! が出る
- [ ] 連続リトライしても current と best が混ざらない

## ありがち事故チェック
- [ ] reset() が best まで消していない
- [ ] 保存先フォルダが無い時に例外で落ちない
- [ ] best が負にならない（max(0, best)）
