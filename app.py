import streamlit as st

st.set_page_config(
    page_title="川田のラーメン屋さん 🍜",
    page_icon="🍜",
    layout="centered",
)

st.markdown("# 川田のラーメン屋さん 🍜")
st.write("はい、と言う事でございましたけれども。Python基礎を**ラーメン屋の比喩**で腹落ち学習して参ります。")
st.divider()

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

st.info("左のサイドバー（≡ メニュー）から各ページをご覧いただけます。良かったですね！")
