import streamlit as st
from lib.ui import section_title, code_showcase

section_title("③ クラスとオブジェクト", "レシピ＝設計図（クラス）と一杯＝実物（インスタンス）でございました。")

code = '''class Ramen:
    shop_stock = 3

    def __init__(self, soup: str, noodle: str):
        self.soup = soup
        self.noodle = noodle

    def serve(self):
        if Ramen.shop_stock <= 0:
            return "売り切れでございました"
        Ramen.shop_stock -= 1
        return f"{self.soup}（{self.noodle}）をお出ししました。残り{Ramen.shop_stock}"

class SpicyRamen(Ramen):
    def add_spice(self, level: int):
        return f"辛さレベル{level}を追加しました"
'''

def run():
    class Ramen:
        shop_stock = 3
        def __init__(self, soup, noodle):
            self.soup = soup
            self.noodle = noodle
        def serve(self):
            if Ramen.shop_stock <= 0:
                return "売り切れでございました"
            Ramen.shop_stock -= 1
            return f"{self.soup}（{self.noodle}）をお出ししました。残り{Ramen.shop_stock}"

    class SpicyRamen(Ramen):
        def add_spice(self, level: int):
            return f"辛さレベル{level}を追加しました"

    r1 = Ramen("醤油", "細麺")
    st.write(r1.serve())
    r2 = SpicyRamen("味噌", "中太")
    st.write(r2.add_spice(5))
    st.write(r2.serve())
    r3 = Ramen("塩", "極細")
    st.write(r3.serve())
    r4 = Ramen("豚骨", "極太")
    st.write(r4.serve())

code_showcase("在庫と提供の流れ", code, runner=run)
