import streamlit as st
from lib.ui import section_title, code_showcase
from lib.quiz import mcq

section_title("⑨ 高度なクラス", "@property / @classmethod / 特殊メソッド でございました。")

code = '''class Ticket:
    tax_rate = 0.1  # クラス変数（全体に共通）

    def __init__(self, menu: str, price: int):
        self.menu = menu
        self._price = price

    @property
    def price(self) -> int:
        # 読み書きの間に検証や加工を挟める
        return self._price

    @price.setter
    def price(self, value: int) -> None:
        if value < 0:
            raise ValueError("価格は0以上でございました")
        self._price = value

    @classmethod
    def from_menu(cls, menu: str) -> "Ticket":
        base = {"醤油": 800, "味噌": 900}.get(menu, 700)
        return cls(menu, base)

    @staticmethod
    def with_tax(amount: int) -> int:
        return int(amount * (1 + Ticket.tax_rate))

    def __str__(self) -> str:
        return f"{self.menu}({self.price}円)"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Ticket) and (self.menu, self.price) == (other.menu, other.price)

# 利用例
t = Ticket.from_menu("味噌")
print(t)
print(Ticket.with_tax(t.price))
t.price = 950
print(t == Ticket("味噌", 950))
'''


def run():
    class Ticket:
        tax_rate = 0.1

        def __init__(self, menu: str, price: int):
            self.menu = menu
            self._price = price

        @property
        def price(self) -> int:
            return self._price

        @price.setter
        def price(self, value: int) -> None:
            if value < 0:
                raise ValueError("価格は0以上でございました")
            self._price = value

        @classmethod
        def from_menu(cls, menu: str) -> "Ticket":
            base = {"醤油": 800, "味噌": 900}.get(menu, 700)
            return cls(menu, base)

        @staticmethod
        def with_tax(amount: int) -> int:
            return int(amount * (1 + Ticket.tax_rate))

        def __str__(self) -> str:
            return f"{self.menu}({self.price}円)"

        def __eq__(self, other: object) -> bool:
            return isinstance(other, Ticket) and (self.menu, self.price) == (other.menu, other.price)

    t = Ticket.from_menu("味噌")
    st.write(str(t))
    st.write(Ticket.with_tax(t.price))
    t.price = 950
    st.write(t == Ticket("味噌", 950))


code_showcase("プロパティ / クラスメソッド / 特殊メソッド", code, runner=run)

st.divider()
st.subheader("小テスト（クラス編）")

mcq(
    "@property を使う主な利点はどれですか？",
    [
        "属性アクセスの形で検証や変換を挟める",
        "常に速度が上がる",
        "クラス変数だけを参照できる",
    ],
    answer_index=0,
    explain="外部APIはattrアクセスのまま、中で検証/カプセル化できる点が利点です。",
    key="09_q1",
)

mcq(
    "@classmethod の典型的な使い方は？",
    [
        "代替コンストラクタとして、与えられた情報からインスタンスを生成",
        "インスタンスの状態だけを変更するイベントハンドラ",
        "GC（ガーベジコレクタ）を直接操作する",
    ],
    answer_index=0,
    explain="clsを受け取るため、クラス全体の文脈でインスタンス生成に向きます。",
    key="09_q2",
)

