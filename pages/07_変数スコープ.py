import streamlit as st
from lib.ui import section_title, code_showcase
from lib.quiz import mcq

section_title("⑦ 変数スコープ", "ローカル / グローバル / ノンローカル（入れ子関数）でございました。")

# サンプルコード（最小で実行可能）
code = '''shop_name = "川田"
orders = 0

def take_order(menu: str) -> str:
    # 関数内の変数はローカル（外からは見えない）
    local_note = "一時メモ"
    return f"{menu} を承りました（{local_note}）"

def make_counter():
    # 入れ子関数でノンローカル変数を使う
    count = 0
    def inc():
        nonlocal count  # 1つ外側のスコープの変数を書き換える
        count += 1
        return count
    return inc

def rename_shop(new_name: str) -> None:
    # グローバルを書き換えるときは global を明示
    global shop_name
    shop_name = new_name

# 利用例
counter = make_counter()
print(take_order("醤油"))
print(counter())
print(counter())
rename_shop("新・川田")
print(shop_name)
'''


def run():
    # 実行用：上のコードを関数内で再現
    shop_name = "川田"
    orders = 0

    def take_order(menu: str) -> str:
        local_note = "一時メモ"
        return f"{menu} を承りました（{local_note}）"

    def make_counter():
        count = 0
        def inc():
            nonlocal count
            count += 1
            return count
        return inc

    def rename_shop(new_name: str) -> str:
        # この関数ではグローバルは使わず、結果だけ返す（デモ用）
        return new_name

    counter = make_counter()
    st.write(take_order("醤油"))
    st.write(counter())
    st.write(counter())
    st.write(rename_shop("新・川田"))


code_showcase("スコープの基本（local / nonlocal / global）", code, runner=run)

st.divider()
st.subheader("小テスト（スコープ編）")

mcq(
    "global を使うと何が起きますか？",
    [
        "関数外の同名変数を書き換える",
        "関数内だけのコピーを作る",
        "エラーになるだけで実際は変化しない",
    ],
    answer_index=0,
    explain="global はモジュールレベルの同名変数を指す宣言。書き換えは破壊的です。",
    key="07_q1",
)

mcq(
    "nonlocal はどのスコープの変数を対象にしますか？",
    [
        "1つ外側の関数スコープの変数を書き換える",
        "グローバル変数を書き換える",
        "ローカル変数を新規作成する",
    ],
    answer_index=0,
    explain="nonlocal はネストした関数で、直近の外側の関数スコープ変数に束縛します。",
    key="07_q2",
)

