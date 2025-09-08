import streamlit as st
from lib.ui import section_title, code_showcase
from lib.quiz import mcq

section_title("⑧ 関数の高度利用", "高階関数 / ラムダ / map・filter・sorted / ジェネレータ / クロージャ / デコレータ / docstring / データ隠蔽 でございました。")

code = '''from typing import Callable, List, Dict
import time

# 1) ソート: sorted(key=lambda ...)
menu: List[Dict[str,int]] = [
    {"name": "醤油", "price": 800},
    {"name": "味噌", "price": 900},
    {"name": "塩",  "price": 700},
]
sorted_menu = sorted(menu, key=lambda x: x["price"])  # 価格の安い順

# 2) 高階関数 + クロージャ
def make_counter():
    count = 0
    def inc():
        nonlocal count
        count += 1
        return count
    return inc
counter = make_counter()

# 3) map / filter
soups = ["醤油", "味噌", "塩"]
mapped = list(map(lambda s: s+"スープ", soups))
filtered = list(filter(lambda s: "味噌" not in s, mapped))

# 4) ジェネレータ
def gen_bowls():
    yield "一杯目"
    yield "二杯目"
    yield "三杯目"
bowls = list(gen_bowls())

# 5) デコレータ
def log_time(fn):
    """関数の前後で時間を計測するデコレータ"""
    def wrapper(*args, **kwargs):
        t0 = time.time()
        result = fn(*args, **kwargs)
        dt = (time.time() - t0) * 1000
        return f"{fn.__name__} took {dt:.2f} ms -> {result}"
    return wrapper

@log_time
def cook(name: str) -> str:
    """麺を茹でて盛り付ける（ダミー）"""
    return f"{name}完成"

# 6) docstring の確認
doc_of_cook = cook.__doc__  # デコレート後は None になる簡易実装例

# 7) 関数ベースのデータ隠蔽（クロージャで状態保持）
def make_vault(secret: str):
    def get():
        return secret
    def set(value: str):
        nonlocal secret
        secret = value
    return get, set
get_secret, set_secret = make_vault("初期シークレット")
set_secret("更新シークレット")
now_secret = get_secret()

print([m["name"] for m in sorted_menu])
print(counter(), counter())
print(mapped, filtered)
print(bowls)
print(cook("醤油"))
print(doc_of_cook)
print(now_secret)
'''


def run():
    from typing import Callable, List, Dict
    import time

    menu: List[Dict[str, int]] = [
        {"name": "醤油", "price": 800},
        {"name": "味噌", "price": 900},
        {"name": "塩",  "price": 700},
    ]
    sorted_menu = sorted(menu, key=lambda x: x["price"])  # 価格の安い順

    def make_counter():
        count = 0
        def inc():
            nonlocal count
            count += 1
            return count
        return inc
    counter = make_counter()

    soups = ["醤油", "味噌", "塩"]
    mapped = list(map(lambda s: s+"スープ", soups))
    filtered = list(filter(lambda s: "味噌" not in s, mapped))

    def gen_bowls():
        yield "一杯目"
        yield "二杯目"
        yield "三杯目"
    bowls = list(gen_bowls())

    def log_time(fn):
        """関数の前後で時間を計測するデコレータ"""
        def wrapper(*args, **kwargs):
            t0 = time.time()
            result = fn(*args, **kwargs)
            dt = (time.time() - t0) * 1000
            return f"{fn.__name__} took {dt:.2f} ms -> {result}"
        return wrapper

    @log_time
    def cook(name: str) -> str:
        """麺を茹でて盛り付ける（ダミー）"""
        return f"{name}完成"

    doc_of_cook = cook.__doc__

    def make_vault(secret: str):
        def get():
            return secret
        def set(value: str):
            nonlocal secret
            secret = value
        return get, set
    get_secret, set_secret = make_vault("初期シークレット")
    set_secret("更新シークレット")
    now_secret = get_secret()

    st.write([m["name"] for m in sorted_menu])
    st.write(counter(), counter())
    st.write(mapped, filtered)
    st.write(bowls)
    st.write(cook("醤油"))
    st.write("docstring:", doc_of_cook)
    st.write("vault:", now_secret)


code_showcase("関数テク大全（最小サンプル）", code, runner=run)

st.divider()
st.subheader("小テスト（関数編）")

mcq(
    "ジェネレータ関数の正しい説明はどれ？",
    [
        "yieldで値を逐次返し、状態を保持できる",
        "一度に全要素のリストを返す",
        "再帰専用の関数である",
    ],
    answer_index=0,
    explain="ジェネレータはイテレータを返し、再開可能な実行状態を持ちます。",
    key="08_q1",
)

mcq(
    "デコレータ(@decorator)の主目的は？",
    [
        "関数の振る舞いをラップし共通処理を付与する",
        "関数を高速化するためだけの構文",
        "関数を匿名関数(lambda)に変換する",
    ],
    answer_index=0,
    explain="前後処理・認可・キャッシュなど横断的関心事を付与するのに使います。",
    key="08_q2",
)

mcq(
    "sorted(items, key=lambda x: x[\"price\"]) の意味は？",
    [
        "priceキーの値を基準に昇順ソート",
        "priceキーの値を二乗してソート",
        "priceキーの有無でフィルタ",
    ],
    answer_index=0,
    explain="key関数の返り値が比較対象になります。",
    key="08_q3",
)
