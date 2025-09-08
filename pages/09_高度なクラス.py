import streamlit as st
from lib.ui import section_title, code_showcase
from lib.quiz import mcq

section_title("⑨ 高度なクラス", "__init__ / クラス変数・メソッド / オーバーライド / 多重継承(MRO) / 抽象基底クラス / データ隠蔽（_ / __）でございました。")

code = '''from abc import ABC, abstractmethod

# 1) 代替コンストラクタやユーティリティ
class Ticket:
    tax_rate = 0.1  # クラス変数

    def __init__(self, menu: str, price: int):  # __init__
        self.menu = menu
        self.__price = price  # __ による名前マングリング

    @classmethod
    def from_menu(cls, menu: str) -> "Ticket":
        price = {"醤油": 800, "味噌": 900}.get(menu, 700)
        return cls(menu, price)

    @staticmethod
    def with_tax(amount: int) -> int:
        return int(amount * (1 + Ticket.tax_rate))

    def price(self) -> int:
        return self.__price

# 2) オーバーライド
class BaseRamen:
    def serve(self) -> str:
        return "素ラーメン"

class ShoyuRamen(BaseRamen):
    def serve(self) -> str:  # オーバーライド
        return "醤油ラーメン"

# 3) 多重継承とMRO
class A:
    def who(self):
        return "A"
class B(A):
    def who(self):
        return "B->" + super().who()
class C(A):
    def who(self):
        return "C->" + super().who()
class D(B, C):
    def who(self):
        return "D->" + super().who()
mro_names = [cls.__name__ for cls in D.__mro__]

# 4) 抽象基底クラス（abc）
class RamenBase(ABC):
    @abstractmethod
    def soup(self) -> str:
        ...
    def serve(self) -> str:
        return f"{self.soup()}ラーメンを提供"

class MisoRamen(RamenBase):
    def soup(self) -> str:
        return "味噌"

# 5) データ隠蔽（_ と __）の挙動
secret = Ticket("味噌", 900)
real_price = secret._Ticket__price  # 注意: 参照できてしまう

# 出力例
print(Ticket.with_tax(1000))
print(ShoyuRamen().serve())
print(D().who())
print(mro_names)
print(MisoRamen().serve())
print(real_price)
'''


def run():
    from abc import ABC, abstractmethod

    class Ticket:
        tax_rate = 0.1
        def __init__(self, menu: str, price: int):
            self.menu = menu
            self.__price = price
        @classmethod
        def from_menu(cls, menu: str) -> "Ticket":
            price = {"醤油": 800, "味噌": 900}.get(menu, 700)
            return cls(menu, price)
        @staticmethod
        def with_tax(amount: int) -> int:
            return int(amount * (1 + Ticket.tax_rate))
        def price(self) -> int:
            return self.__price

    class BaseRamen:
        def serve(self) -> str:
            return "素ラーメン"
    class ShoyuRamen(BaseRamen):
        def serve(self) -> str:
            return "醤油ラーメン"

    class A:
        def who(self):
            return "A"
    class B(A):
        def who(self):
            return "B->" + super().who()
    class C(A):
        def who(self):
            return "C->" + super().who()
    class D(B, C):
        def who(self):
            return "D->" + super().who()
    mro_names = [cls.__name__ for cls in D.__mro__]

    class RamenBase(ABC):
        @abstractmethod
        def soup(self) -> str:
            ...
        def serve(self) -> str:
            return f"{self.soup()}ラーメンを提供"
    class MisoRamen(RamenBase):
        def soup(self) -> str:
            return "味噌"

    secret = Ticket("味噌", 900)
    real_price = secret._Ticket__price

    st.write(Ticket.with_tax(1000))
    st.write(ShoyuRamen().serve())
    st.write(D().who())
    st.write("MRO:", mro_names)
    st.write(MisoRamen().serve())
    st.write("name-mangled price:", real_price)


code_showcase("クラス応用テクニック（最小サンプル）", code, runner=run)

st.divider()
st.subheader("小テスト（クラス編）")

mcq(
    "多重継承のメソッド解決順序(MRO)で正しい説明は？",
    [
        "D(B,C)なら D→B→C→A→object の順で探索",
        "常に左から2番目の親だけを探索",
        "BとCのどちらも無視してAに直行",
    ],
    answer_index=0,
    explain="PythonはC3線形化でMROを決定します。",
    key="09_q1",
)

mcq(
    "abc.ABC と @abstractmethod の目的は？",
    [
        "サブクラスに実装を強制するための型的契約を示す",
        "インスタンス生成を高速化する",
        "デストラクタを自動生成する",
    ],
    answer_index=0,
    explain="抽象メソッドを未実装のままではインスタンス化できません。",
    key="09_q2",
)

mcq(
    "__price のようなダブルアンダースコアの挙動は？",
    [
        "_ClassName__price に名前マングリングされる",
        "完全に外部から参照不可能になる",
        "プロパティと同じ意味になる",
    ],
    answer_index=0,
    explain="マングリングにより衝突を避けますが、完全秘匿ではありません。",
    key="09_q3",
)
