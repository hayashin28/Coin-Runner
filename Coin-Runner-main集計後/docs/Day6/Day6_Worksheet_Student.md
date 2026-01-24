# Day6：セーブデータ（Best保存）＆“遊び続けたくなる”仕上げの日（7人×3時間用シナリオ）

## 0. 今日のゴール（先生が最初に読む用）

3時間で、次を「クラス全体」として完成させます。

1. **ベストスコア（Best）がアプリ再起動後も残る**（JSON保存）
2. Title / Play / GameOver のどこかで **Bestが見える**（表示）
3. Best更新時に **NEW RECORD! のように分かる**（メッセージ or 色 or 1行テキスト）
4. セーブが壊れていても **ゲームが落ちない**（0に戻して続行）

> ポイント：  
> Day5までで「ベスト更新の判定」までは作れている前提です。  
> Day6は “**続けて遊びたくなる体験**” を作る日。  
> 技術的には「**永続化（ファイル保存）**」と「**落ちない設計**」がテーマです。

---

## 1. 今日の7人の役割（先に割り当てる）

| 役割 | 担当 | 触る場所（主） | 今日の責務 |
|---:|---|---|---|
| A | セーブ/ロード担当 | `core/save_data.py`（新規）/ `core/scoring.py` | Bestを読み書きできるAPIを作る |
| B | Scoring統合担当 | `core/scoring.py` | Best更新→保存の呼び出し順を決める |
| C | Title表示担当 | `scenes/title.py` | TitleでBest表示（or 表示用ラベル追加） |
| D | GameOver表示担当 | `scenes/game_over_scene.py`（＋画面側） | NEW RECORD表示（更新時だけ） |
| E | Play呼び出し担当 | `scenes/play.py` | 起動時load / GameOver時save の接続（設計だけでもOK） |
| F | 安全設計・例外担当 | A〜Eのどこか | “壊れても落ちない”のルールを守る |
| G | QA/バグログ担当 | `docs/Day6_buglog.md` | テスト手順を書き、見つけた不具合を記録 |

---

## 2. 今日の時間割（板書用）

- 0:00〜0:10　Day5までの状況確認（Bestはある？更新判定はある？）
- 0:10〜0:20　役割分担＆「保存仕様」の確認
- 0:20〜1:10　実装タイム1（A/Bが先行、他は表示準備）
- 1:10〜1:20　休憩
- 1:20〜2:10　実装タイム2（結合：load→表示→更新→save）
- 2:10〜2:35　テストプレイ＆バグログ記入
- 2:35〜3:00　“遊び続けたくなる演出” 1個だけ追加して締め

---

## 3. 仕様（齟齬防止のための固定ルール）

### 3-1. セーブファイルの場所

- 保存先（おすすめ固定）：`save/best_score.json`  
  （プロジェクト直下に `save/` フォルダを作る）

### 3-2. JSONフォーマット

```json
{"best": 350}
```

### 3-3. “落ちない設計” のルール（超重要）

- ファイルが無い → **best=0** で続行
- JSONが壊れている → **best=0** で続行
- 保存に失敗した → **ゲームは続行**（例外で止めない）
- best が変な値 → **intに丸めて 0以上にクリップ**

---

## 4. 役割ごとの詳細タスク（チェックリスト）

### 4-1. A：セーブ/ロード担当（`core/save_data.py`）

- [ ] `load_best(path)` を実装した
- [ ] `save_best(path, best)` を実装した
- [ ] フォルダが無ければ `os.makedirs(..., exist_ok=True)` で作る
- [ ] 例外が起きてもゲームが落ちない（try/except）
- [ ] JSONが壊れていても 0 に戻る

**実装ヒント（これくらい書いてOK）**
- 読み込み：
  - `open(path, "r", encoding="utf-8")`
  - `json.load(f)` → dict
  - `best = int(data.get("best", 0))`
  - `best = max(0, best)`
- 保存：
  - `os.makedirs(os.path.dirname(path), exist_ok=True)`
  - `json.dump({"best": best}, f, ensure_ascii=False, indent=2)`

---

### 4-2. B：Scoring統合担当（`core/scoring.py`）

- [ ] Day5で作った `best` の仕組みを確認した
- [ ] GameOver時に `register_game_over()` を呼ぶ設計ができた
- [ ] `register_game_over()` が True のときだけ “更新演出フラグ” を立てる案を作った
- [ ] Day6として `load_best()` / `save_best()` の呼び出し順を決めた

**齟齬ポイント（ここを守る）**
- `reset()` は「今回スコア」だけ0に戻す（bestは保持）
- “更新判定 → best更新 → 保存” の順で呼ぶ

---

### 4-3. C：Title表示担当（`scenes/title.py`）

- [ ] Titleに Best 表示を追加した（ラベル1行でOK）
- [ ] キーボード入力（Enter/Space）でPlayへ進める（Day1 TODOが残っていたらここでやる）
- [ ] 文字が見えない問題があれば `markup` / `color` / `font_size` を調整した

**表示ヒント**
- 表示文字例：  
  `Best: 350\nEnter/Space/Touch`
- 「読み込みはTitleがやる」か「PlayがやってTitleに渡す」かは自由  
  ただし “落ちない” を優先。

---

### 4-4. D：GameOver表示担当（`scenes/game_over_scene.py` + 画面側）

- [ ] GameOverで「今回スコア」と「Best」が見える（どちらかでもOK）
- [ ] Best更新なら `NEW RECORD!` を1行出す
- [ ] 更新判定は **ScoringService.register_game_over() の戻り値** を使う想定にする

---

### 4-5. E：Play呼び出し担当（`scenes/play.py`）

- [ ] 起動時（Play生成時 or on_pre_enter）に `load_best()` を呼ぶ設計にした
- [ ] GameOver確定時に `save_best()` を呼ぶ設計にした
- [ ] 例外で止まらないように “try/except” の方針を入れた

> ※ Playは既にタスクが多いので、  
> **設計だけ**（どこで呼ぶか決めてコメントで残す）でも合格にしてOK。

---

### 4-6. F：安全設計・例外担当（全体）

- [ ] 「ファイルが壊れても落ちない」ことを最優先にレビューした
- [ ] try/except の範囲が広すぎないか（必要な箇所だけ）見直した
- [ ] best が負になる・文字になるケースを0に丸める設計を確認した

---

### 4-7. G：QA/バグログ担当（`docs/Day6_buglog.md`）

- [ ] “保存あり/なし/壊れたJSON” の3パターンでテストした
- [ ] バグログに再現手順を必ず書いた
- [ ] 直ったものには `[fixed]` を付けた

---

## 5. テスト手順（最短でOK）

1) 初回起動：saveファイルが無い状態で起動 → **落ちずに Best=0**  
2) 1回プレイしてベスト更新 → GameOver後に **save/best_score.json が作られる**  
3) アプリを閉じて再起動 → Title/Play/GameOver のどこかで **Bestが残る**  
4) `best_score.json` をわざと壊す（例：`{` だけ）→ 起動しても **落ちない**（Best=0）

---

## 6. よくある迷子ポイント（先に潰す）

- 「bestはどこで持つ？」  
  → ScoringService が持つのが一番わかりやすい
- 「保存をどこで呼ぶ？」  
  → GameOver確定の瞬間（“更新判定した直後”）が安全
- 「JSONが壊れて落ちる」  
  → load_best で try/except して 0 に戻す

---

## 7. 今日のDoD（定義：ここまでできたら合格）

- [ ] Bestが **次回起動でも残る**
- [ ] Best更新時に **NEW RECORD! が分かる**
- [ ] 壊れたJSONでも **落ちない**

