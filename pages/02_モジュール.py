import streamlit as st
from lib.ui import section_title, code_showcase

section_title("② モジュール（道具箱）", "import / from / as の使い分けでございました。")

code = '''# ramen_tools.py（と仮定）
def make_soup(base: str) -> str:
    return f"{base}スープ完成です"

# 利用例
# import ramen_tools
# print(ramen_tools.make_soup("醤油"))

# from ramen_tools import make_soup
# print(make_soup("味噌"))

# import ramen_tools as rt
# print(rt.make_soup("塩"))
'''

def run():
    def make_soup(base: str) -> str:
        return f"{base}スープ完成です"
    st.write(make_soup("醤油"))
    st.write(make_soup("味噌"))
    st.write(make_soup("塩"))

code_showcase("道具箱を呼んで使う", code, runner=run)
