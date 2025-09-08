import streamlit as st
from lib.explains import EXPLAINS

st.title("📖 お店シミュレーション：解説集")
st.caption("穴埋めドリル（Q1〜Q8）の“腹落ち”解説・正解例・落とし穴・追加練習です。")

qs = [f"Q{i}" for i in range(1, 9)]
pick = st.selectbox("問題を選択", qs, index=0)

st.markdown(EXPLAINS[pick])

st.divider()
st.info("ドリル本編はサイドバーの『10_お店シミュレーション_穴埋め』から実施できます。お疲れ様でございました！")

