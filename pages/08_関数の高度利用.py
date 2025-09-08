import streamlit as st
from lib.ui import section_title, code_showcase
from lib.quiz import mcq

section_title("⑧ 関数の高度利用", "高階関数 / クロージャ / ラムダでございました。")

code = '''from typing import Callable, List

def make_seasoner(salt_gram: int) -> Callable[[str], str]:
    # 外側の値（salt_gram）を覚えた関数（クロージャ）を返す
    def season(soup: str) -> str:
        return f"{soup} + 塩{salt_gram}g"
    return season

bowls: List[str] = ["醤油", "味噌", "塩"]
add5 = make_seasoner(5)

# map: 各要素に関数を適用
seasoned = list(map(add5, bowls))

# filter: 条件に合う要素だけ残す（ここでは「味噌」を除外）
spicy = list(filter(lambda s: "味噌" not in s, seasoned))

print(seasoned)
print(spicy)
'''


def run():
    from typing import Callable, List

    def make_seasoner(salt_gram: int) -> Callable[[str], str]:
        def season(soup: str) -> str:
            return f"{soup} + 塩{salt_gram}g"
        return season

    bowls: List[str] = ["醤油", "味噌", "塩"]
    add5 = make_seasoner(5)
    seasoned = list(map(add5, bowls))
    spicy = list(filter(lambda s: "味噌" not in s, seasoned))
    st.write(seasoned)
    st.write(spicy)


code_showcase("高階関数とクロージャの実例", code, runner=run)

st.divider()
st.subheader("小テスト（関数編）")

mcq(
    "クロージャ（closure）が保持しているのはどれですか？",
    [
        "外側の関数スコープの変数の状態",
        "関数名だけを保持する",
        "戻り値だけを保持する",
    ],
    answer_index=0,
    explain="クロージャは自由変数（外側のスコープの変数）に束縛し、その状態を保ちます。",
    key="08_q1",
)

mcq(
    "map と filter の組み合わせの説明として正しいものは？",
    [
        "mapは各要素に関数を適用し、filterは条件で要素を絞り込む",
        "mapは要素を削除し、filterは要素を複製する",
        "どちらもリストをソートする",
    ],
    answer_index=0,
    explain="mapで形を変え、filterで条件抽出するのが基本パターンです。",
    key="08_q2",
)

mcq(
    "ラムダ関数の主な利点は？",
    [
        "無名の小さな関数をインラインで簡潔に書ける",
        "実行速度が常に通常の関数より速い",
        "デコレータを必ず付けて使える",
    ],
    answer_index=0,
    explain="可読性を保てる範囲で、短い処理をその場で書けるのが利点です。",
    key="08_q3",
)

