import streamlit as st
from lib.ui import section_title, code_showcase
from lib.quiz import mcq

st.set_page_config(page_title="⑧ 関数の高度利用（Lambda & 高階関数）", page_icon="🍜")
section_title("⑧ 関数の高度利用（Lambda & 高階関数）",
              "関数＝道具。渡す・返す・並べる。lambda で“即席の小道具”を作って厨房を回します。")

# ──────────────────────────────────────────────────────────
# #1 関数は“値”として扱える（＋原文の誤りを修正）
# ──────────────────────────────────────────────────────────
code1 = '''# 原文の誤り修正：
#  - funct → func
#  - fs / fas のタイポを tools に統一

def func():
    print(1)

# 関数を変数に代入（= 道具を指すラベル）
f = func
f()  # => 1

print(f)        # <function func at 0x...>
print(type(f))  # <class 'function'>

# コレクションにも入れられる
tools = [func, func, func]
tools[0]()      # => 1
'''

def run1():
    def func():
        st.write(1)
    f = func
    f()
    st.write("関数オブジェクト名:", f.__name__)
    st.write("型:", type(f).__name__)
    tools = [func, func, func]
    tools[0]()

code_showcase("#1 関数は“値”（代入・参照・コレクション）", code1, runner=run1)

st.markdown("""
**解説**  
- 関数はオブジェクト（値）なので **代入／引数／戻り値／リスト格納** ができます。  
- `func` は**関数そのもの**、`func()` は**実行**でした。
""")
st.divider()

# ──────────────────────────────────────────────────────────
# #2 高階関数：関数を受け取る／返す（＋原文の誤り修正）
# ──────────────────────────────────────────────────────────
code2 = '''# 原文の誤り修正：
#  - hi_func1/hi_func2 はそのまま。挙動を説明用に整理。

def func1(num):
    return [(i+1)*num for i in range(num)]  # 例: num=5 → [5,10,15,20,25]

def func2(num):
    return num**num                          # 例: num=5 → 3125

def hi_func1(func):
    # 関数を“受け取って”実行（= 高階関数）
    return func(5)

def hi_func2(text):
    # 条件で“関数を返す”（= 高階関数）
    if len(text) % 2 == 0:
        return func1
    else:
        return func2

result1 = hi_func1(func1)   # => [5,10,15,20,25]
result2 = hi_func1(func2)   # => 3125
print(result1)
print(result2)

result3 = hi_func2("hoge")  # len=4 偶数 → func1 を返す
result4 = hi_func2("abc")   # len=3 奇数 → func2 を返す
print(result3(7))           # => [7,14,21,28,35,42,49]
print(result4(7))           # => 7**7
'''

def run2():
    def func1(num): return [(i+1)*num for i in range(num)]
    def func2(num): return num**num
    def hi_func1(func): return func(5)
    def hi_func2(text): return func1 if (len(text)%2==0) else func2
    st.write(hi_func1(func1))
    st.write(hi_func1(func2))
    f3 = hi_func2("hoge")
    f4 = hi_func2("abc")
    st.write(f3(7))
    st.write(f4(7))

code_showcase("#2 高階関数（受け取る／返す）", code2, runner=run2)

st.markdown("""
**解説**  
- **高階関数**＝関数を **引数に** 取る or **戻り値に** 返す関数。  
- 厨房比喩：**レシピ（関数）を差し替える**ことでフローを切り替える。
""")
st.divider()

# ──────────────────────────────────────────────────────────
# #3 命令型フィルタ（Before）→ ラーメン版に置き換え
# ──────────────────────────────────────────────────────────
code3 = '''# 似た処理をコピペしている“Before”パターン（ラーメン価格に置換）
def pick_odd(prices):
    ret = []
    for p in prices:
        if p % 2 == 1:
            ret.append(p)
    return ret

def pick_even(prices):
    ret = []
    for p in prices:
        if p % 2 == 0:
            ret.append(p)
    return ret

def pick_over900(prices):
    ret = []
    for p in prices:
        if p >= 900:
            ret.append(p)
    return ret

prices = [800, 930, 740, 1000, 880, 1200, 950, 700, 900]
print(pick_odd(prices))
print(pick_even(prices))
print(pick_over900(prices))
'''

def run3():
    def pick_odd(prices):
        ret=[]
        for p in prices:
            if p%2==1: ret.append(p)
        return ret
    def pick_even(prices):
        ret=[]
        for p in prices:
            if p%2==0: ret.append(p)
        return ret
    def pick_over900(prices):
        ret=[]
        for p in prices:
            if p>=900: ret.append(p)
        return ret
    prices = [800, 930, 740, 1000, 880, 1200, 950, 700, 900]
    st.write("奇数価格:", pick_odd(prices))
    st.write("偶数価格:", pick_even(prices))
    st.write("900円以上:", pick_over900(prices))

code_showcase("#3 フィルタのコピペ（Before）", code3, runner=run3)

st.markdown("""
**解説（Before）**  
- 中身はほぼ同じで **条件だけが違う**。  
- 条件＝関数（述語）として外へ出せば、**1つに共通化**できます → 次へ。
""")
st.divider()

# ──────────────────────────────────────────────────────────
# #4 述語関数＋lambda / filter / map（After）
# ──────────────────────────────────────────────────────────
code4 = '''# 述語（True/False を返す）を外だしして共通化
def is_odd(n):  return n % 2 == 1
def is_even(n): return n % 2 == 0
def is_over900(p): return p >= 900

def pick_by(pred, nums):
    return [n for n in nums if pred(n)]

prices = [800, 930, 740, 1000, 880, 1200, 950, 700, 900]

print(pick_by(is_odd, prices))
print(pick_by(is_even, prices))
print(pick_by(is_over900, prices))

# lambda + 組み込み高階関数
names = ["醤油", "味噌", "塩", "豚骨"]
lengths = list(map(lambda s: (s, len(s)), names))
expensive = list(filter(lambda p: p >= 900, prices))
# もちろん sorted(prices) で十分だが、例として key に lambda を渡す
sorted_by_price = sorted(prices, key=lambda p: p)

print(lengths)
print(expensive)
print(sorted_by_price)
'''

def run4():
    def is_odd(n):  return n%2==1
    def is_even(n): return n%2==0
    def is_over900(p): return p>=900
    def pick_by(pred, nums): return [n for n in nums if pred(n)]
    prices=[800, 930, 740, 1000, 880, 1200, 950, 700, 900]
    st.write("奇数:", pick_by(is_odd, prices))
    st.write("偶数:", pick_by(is_even, prices))
    st.write("900円以上:", pick_by(is_over900, prices))
    names=["醤油","味噌","塩","豚骨"]
    lengths=list(map(lambda s:(s,len(s)), names))
    expensive=list(filter(lambda p:p>=900, prices))
    sorted_by_price=sorted(prices, key=lambda p:p)
    st.write("名前と文字数:", lengths)
    st.write("高価格のみ:", expensive)
    st.write("価格でソート:", sorted_by_price)

code_showcase("#4 高階関数（After）と lambda / map / filter / sorted", code4, runner=run4)

st.markdown("""
**要点**  
- **高階関数**＝関数を **受け取り**／**返す**。  
- **lambda**＝その場限りの小関数（`key=` や `map`/`filter` に最適）。  
- `filter(pred, it)` は述語が True の要素だけを通し、`map(f, it)` は各要素に f を適用。  
- 読みやすさ次第では **内包表記**の方が良い場面も多いです。
""")

# ──────────────────────────────────────────────────────────
# #5 sorted(key=lambda ...)：メニューを価格で並べ替え
# ──────────────────────────────────────────────────────────
code5 = '''menu = [
    {"name": "醤油", "price": 800},
    {"name": "味噌", "price": 900},
    {"name": "塩",   "price": 850},
    {"name": "豚骨", "price": 1000},
]

# 価格の安い順（昇順）
by_price_asc  = sorted(menu, key=lambda item: item["price"])

# 価格の高い順（降順）
by_price_desc = sorted(menu, key=lambda item: item["price"], reverse=True)

# 複合キー：価格→名前（同額のときに名前で安定整列）
by_price_then_name = sorted(menu, key=lambda item: (item["price"], item["name"]))

print(by_price_asc)
print(by_price_desc)
print(by_price_then_name)
'''

def run5():
    menu = [
        {"name": "醤油", "price": 800},
        {"name": "味噌", "price": 900},
        {"name": "塩",   "price": 850},
        {"name": "豚骨", "price": 1000},
    ]
    by_price_asc  = sorted(menu, key=lambda item: item["price"])
    by_price_desc = sorted(menu, key=lambda item: item["price"], reverse=True)
    by_price_then_name = sorted(menu, key=lambda item: (item["price"], item["name"]))
    st.write("安い順:", by_price_asc)
    st.write("高い順:", by_price_desc)
    st.write("価格→名前:", by_price_then_name)

code_showcase("#5 sorted(key=…)：価格でソート／複合キー", code5, runner=run5)

st.markdown("""
**要点**  
- `key=` には“並べ替え用の値”を返す関数を渡します（ここでは `lambda item: item["price"]`）。  
- 降順は `reverse=True`。  
- 複合ソートは `key=lambda x: (x["price"], x["name"])` のようにタプルを返す。  
- `sorted` は元リストを変更しません（安定ソート）。
""")

# ──────────────────────────────────────────────────────────
# #6 any / all：在庫チェックを簡潔に
# ──────────────────────────────────────────────────────────
code6 = '''stock = {"noodle": 5, "base_shoyu": 2, "egg": 0, "nori": 10}

def can_make(order_items):
    # すべての必要素材が 1 以上あるか？
    return all(stock.get(item, 0) >= 1 for item in order_items)

def has_shortage(order_items):
    # どれか1つでも 0 なら不足（any）
    return any(stock.get(item, 0) <= 0 for item in order_items)

ramen_shoyu = ["noodle", "base_shoyu", "nori"]
ramen_egg   = ["noodle", "base_shoyu", "egg"]

print(can_make(ramen_shoyu))      # True
print(has_shortage(ramen_shoyu))  # False

print(can_make(ramen_egg))        # False（eggが0）
print(has_shortage(ramen_egg))    # True
'''

def run6():
    stock = {"noodle": 5, "base_shoyu": 2, "egg": 0, "nori": 10}
    def can_make(order_items):
        return all(stock.get(item, 0) >= 1 for item in order_items)
    def has_shortage(order_items):
        return any(stock.get(item, 0) <= 0 for item in order_items)
    ramen_shoyu = ["noodle", "base_shoyu", "nori"]
    ramen_egg   = ["noodle", "base_shoyu", "egg"]
    st.write("醤油ラーメン 作れる？", can_make(ramen_shoyu))
    st.write("醤油ラーメン 不足ある？", has_shortage(ramen_shoyu))
    st.write("味玉ラーメン 作れる？", can_make(ramen_egg))
    st.write("味玉ラーメン 不足ある？", has_shortage(ramen_egg))

code_showcase("#6 any / all：在庫チェック（ジェネレータ式）", code6, runner=run6)

st.markdown("""
**要点**  
- `all(条件 for …)`：すべて満たすなら True（在庫OK）。  
- `any(条件 for …)`：どれか一つでも True なら True（不足あり等）。  
- `dict.get(key, 0)` で存在しない素材を 0 とみなすのが実務で安全。  
- 並列に大量チェックするときは any() の短絡評価で無駄を抑えられます。
""")

st.divider()
st.subheader("🧪 小テスト（MCQ）")

ok1 = mcq(
    "関数オブジェクトを“実行せずに渡す”正しい書き方は？",
    ["func()", "func", "print(func())"],
    answer_index=1,
    explain="括弧を付けると実行。値として渡すなら `func`。",
    key="lambda_q1",
)
ok2 = mcq(
    "条件だけが違う複数のフィルタ関数を共通化する最適解は？",
    ["if/elif を増やす", "述語関数（pred）を引数に取る高階関数にする", "同じ処理をコピペ"],
    answer_index=1,
    explain="述語（True/False を返す関数）を受け取る関数に抽象化するのが定石。",
    key="lambda_q2",
)
ok3 = mcq(
    "lambda の主な使い所として正しいのはどれ？",
    ["巨大なロジックの記述", "その場限りの小関数を key / map / filter に渡す", "I/O最適化"],
    answer_index=1,
    explain="短い無名関数としての“即席道具”が本領です。",
    key="lambda_q3",
)
ok4 = mcq(
    "sorted(key=…) の key に渡すべきものは？",
    ["比較対象のインデックス", "要素を受けて“並べ替え用の値”を返す関数", "boolを返す述語関数のみ"],
    answer_index=1,
    explain="key= は『各要素→並べ替えキー』の関数。述語は filter で使います。",
    key="lambda_q4",
)
ok5 = mcq(
    "在庫チェックで『どれか一つでも不足があれば警告』に最適なのは？",
    ["all(stock[item] <= 0 for item in items)", "any(stock.get(item,0) <= 0 for item in items)", "sum(stock.values()) == 0"],
    answer_index=1,
    explain="不足判定は any(不足条件) が簡潔で短絡的（高速）。getで未登録も0扱いに。",
    key="lambda_q5",
)

current = int(ok1) + int(ok2) + int(ok3) + int(ok4) + int(ok5)
st.success(f"スコア：{current}/5 でした。良かったですね！")
