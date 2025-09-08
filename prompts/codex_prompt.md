# Project: 川田のラーメン屋さん（Streamlit）

## Goals
- 裏メニュー 07〜09 を追加し、各ページ: 解説 / コード / 実行 / クイズ を提供
- クイズ正答をセッションに蓄積し、トップで総合点を可視化（Reset 可能）

## Deliverables
- pages/07_変数スコープ.py
- pages/08_関数の高度利用.py
- pages/09_高度なクラス.py
- lib/quiz.py（採点・集計の対応）
- app.py（総合スコアの表示とResetボタン）

## Constraints
- Python 3.10+, Streamlit 1.36+
- 既存の lib/ui.py（section_title, code_showcase）と lib/quiz.py（mcq）を再利用
- 川田語の正誤メッセージ：「良かったですね！」/「惜しかったです」
- サンプルコードは最小限で実行可能、コメントは日本語

## Acceptance Criteria
- `streamlit run app.py` で 07〜09 の各ページがサイドバーに表示され、実行タブが動作する
- 各ページに2問以上のミニクイズがあり、採点で正誤メッセージが表示される
- クイズ正答が `st.session_state` に蓄積され、トップページで合算スコア（正解数・受験数・正答率）が見える
- Reset ボタンでスコアが初期化できる
