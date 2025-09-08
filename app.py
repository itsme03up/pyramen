import streamlit as st

st.set_page_config(
    page_title="川田のラーメン屋さん 🍜",
    page_icon="🍜",
    layout="centered",
)

st.markdown("# 川田のラーメン屋さん 🍜")
st.write("はい、と言う事でございましたけれども。Python基礎を**ラーメン屋の比喩**で腹落ち学習して参ります。")
st.divider()

# 進捗（小テストの合算表示 + Reset）
st.subheader("進捗（小テスト 合計）")
qs = st.session_state.get('quiz_state', {'correct': 0, 'total': 0, 'graded': {}})
correct = qs.get('correct', 0)
total = qs.get('total', 0)
rate = (correct / total * 100) if total else 0.0
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("正解", correct)
with col2:
    st.metric("受験数", total)
with col3:
    st.metric("正答率", f"{rate:.0f}%")

if st.button("Reset（スコア初期化）"):
    # graded情報を消去。必要があれば個別の選択状態もユーザー側で変更可。
    st.session_state['quiz_state'] = {'correct': 0, 'total': 0, 'graded': {}}
    st.success("スコアを初期化しました。お疲れ様でございました！")

st.subheader("学習メニュー")
st.markdown("""
- ① データ型（材料の種類）
- ② モジュール（道具箱）
- ③ クラスとオブジェクト（レシピと一杯）
- ④ リスト編
- ⑤ 文字列編
- ⑥ 例外処理編
- ⑦ 変数スコープ
- ⑧ 関数の高度利用
- ⑨ 高度なクラス
""")

st.info("左のサイドバー（≡ メニュー）から各ページをご覧いただけます。お疲れ様でございました！")
