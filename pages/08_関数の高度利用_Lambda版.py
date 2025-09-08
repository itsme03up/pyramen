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
    st.code(str(f))
    st.write(type(f))
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
st.success(f"スコア：{int(ok1)+int(ok2)+int(ok3)}/3 でした。良かったですね！")

