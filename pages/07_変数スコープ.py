import streamlit as st
from lib.ui import section_title, code_showcase
from lib.quiz import mcq

section_title("⑦ 変数スコープ", "local / enclosing / global / builtins でした。")

# デモ用のグローバル変数
x = "global"

# サンプルコード（最小で実行可能）
code = '''x = "global"
def outer():
    x = "enclosing"
    def inner():
        nonlocal x
        x = x + "->inner"
        return x
    inner()
    return x

def use_global():
    global x
    x = x + "->G"
    return x

print(outer())      # enclosing->inner
print(use_global()) # global->G
'''


def run():
    def outer():
        x = "enclosing"
        def inner():
            nonlocal x
            x = x + "->inner"
            return x
        inner()
        return x

    def use_global():
        global x
        x = x + "->G"
        return x

    st.write(outer())
    st.write(use_global())


code_showcase("スコープの流れを可視化", code, runner=run)

st.divider()
st.subheader("小テスト（スコープ編）")

mcq(
    "nonlocal はどのスコープを参照？",
    ["グローバル", "直近の外側（enclosing）", "ビルトイン"],
    answer_index=1,
    explain="nonlocal は『直近の外側関数スコープ』を参照します。",
    key="scope_q1",
)

mcq(
    "global を使うと何が起きますか？",
    ["関数外の同名変数を書き換える", "関数内だけのコピーを作る", "ビルトインを書き換える"],
    answer_index=0,
    explain="global はモジュールレベルの同名変数を指す宣言です。",
    key="scope_q2",
)
