import streamlit as st
from lib.ui import section_title, code_showcase

section_title("① データ型（材料の種類）", "list / tuple / dict / set などの基礎でございました。")

code = '''length = 15
ratio = 3.14
note = "旨味"
is_hot = True
toppings = ["ネギ","チャーシュー"]
menu = {"醤油":800, "味噌":900}
unique = {"限定","背脂"}

print(type(toppings), toppings[0])
print(menu.get("塩", "未定"))
'''

def run():
    length = 15
    ratio = 3.14
    note = "旨味"
    is_hot = True
    toppings = ["ネギ","チャーシュー"]
    menu = {"醤油":800, "味噌":900}
    unique = {"限定","背脂"}
    st.write(type(toppings), toppings[0])
    st.write(menu.get("塩", "未定"))

code_showcase("材料の種類の確認", code, runner=run)
