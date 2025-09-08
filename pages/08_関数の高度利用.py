import streamlit as st
from lib.ui import section_title, code_showcase
from lib.quiz import mcq

st.set_page_config(page_title="⑧ 関数の高度利用（ラーメン屋）", page_icon="🍜")
section_title("⑧ 関数の高度利用", "関数は『道具』＝値。受け渡し・返却・組み合わせで厨房の手際が上がる、でした。")

# ──────────────────────────────────────────────────────────
# #1 関数は“値”（代入・参照・コレクション）
# ──────────────────────────────────────────────────────────
code1 = '''def boil():
    print("麺をゆでました。お疲れ様でございました！")

f = boil       # 関数を変数に代入（=道具の指し棒を持つイメージ）
f()            # => boil の実行

print(f)       # <function boil at 0x...>
print(type(f)) # <class 'function'>

# リストに詰めて順番に使う
tools = [boil, boil, boil]
tools[0]()     # 最初の道具（boil）を実行
'''

def run1():
    def boil():
        st.write("麺をゆでました。お疲れ様でございました！")
    f = boil
    f()
    st.code(str(f))
    st.write(type(f))
    tools = [boil, boil, boil]
    tools[0]()

code_showcase("#1 関数は“値”として扱える", code1, runner=run1)

st.markdown("""
**解説**
- 関数はオブジェクト（値）なので、**代入／引数／戻り値／コレクション**に使えます。
- 「`boil`」と「`boil()`」は別物：前者は**関数そのもの**、後者は**実行**でした。
""")
st.divider()

# ──────────────────────────────────────────────────────────
# #2 関数を“受け取る／返す”＝高階関数
# ──────────────────────────────────────────────────────────
code2 = '''def make_portions(n: int):
    # 1〜nの丼数を返す（例：n=5 → [1,2,3,4,5]）
    return [(i+1) for i in range(n)]

def power_price(n: int):
    # 価格のパワー遊び（例：n=5 → 5**5）
    return n**n

# 関数を受け取って実行（高階関数）
def hi_run(func):
    return func(5)

# 条件で関数を返す（“返り値が関数”＝高階関数）
def choose_func(menu_name: str):
    # 文字数が偶数なら make_portions、奇数なら power_price を返す
    return make_portions if (len(menu_name) % 2 == 0) else power_price

result1 = hi_run(make_portions)  # => [1,2,3,4,5]
result2 = hi_run(power_price)    # => 3125
print(result1)
print(result2)

fA = choose_func("醤油")   # len=2 → 偶数 → make_portions
fB = choose_func("味噌")   # len=2 → 偶数 → make_portions
print(fA(7))               # => [1..7]
print(fB(7))               # => [1..7]
'''

def run2():
    def make_portions(n:int): return [(i+1) for i in range(n)]
    def power_price(n:int):  return n**n
    def hi_run(func):        return func(5)
    def choose_func(menu_name:str):
        return make_portions if (len(menu_name)%2==0) else power_price
    st.write(hi_run(make_portions))
    st.write(hi_run(power_price))
    fA = choose_func("醤油")
    fB = choose_func("味噌")
    st.write(fA(7))
    st.write(fB(7))

code_showcase("#2 受け取る＆返す：高階関数の基本", code2, runner=run2)

st.markdown("""
**解説**
- **高階関数**＝「関数を **受け取る** or **返す** 関数」。
- 厨房で例えると、**レシピ（関数）を選んで渡す／条件で道具を返す**イメージ。
- `choose_func` のように **条件に応じてロジックを差し替える**のが現場で効きます。
""")
st.divider()

# ──────────────────────────────────────────────────────────
# #3 命令型フィルタ（偶数・奇数・しきい値）→ 高階関数で共通化する前段
# ──────────────────────────────────────────────────────────
code3 = '''# まずは“よくある”重複コード（命令型）
def pick_odd(nums):
    ret = []
    for n in nums:
        if n % 2 == 1:
            ret.append(n)
    return ret

def pick_even(nums):
    ret = []
    for n in nums:
        if n % 2 == 0:
            ret.append(n)
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
    def pick_odd(nums):
        ret=[]
        for n in nums:
            if n%2==1: ret.append(n)
        return ret
    def pick_even(nums):
        ret=[]
        for n in nums:
            if n%2==0: ret.append(n)
        return ret
    def pick_over900(prices):
        ret=[]
        for p in prices:
            if p>=900: ret.append(p)
        return ret
    prices=[800,930,740,1000,880,1200,950,700,900]
    st.write("奇数:", pick_odd(prices))
    st.write("偶数:", pick_even(prices))
    st.write("900円以上:", pick_over900(prices))

code_showcase("#3 命令型フィルタ（Before）", code3, runner=run3)

st.markdown("""
**解説（Before）**
- 似た処理が **コピペ3兄弟** になってます。
- 条件だけが違うので、**条件＝関数**として外だしすれば共通化できます（次の #4）。
""")
st.divider()

# ──────────────────────────────────────────────────────────
# #4 高階関数で共通化（述語関数を渡す）＋lambda/map/filter
# ──────────────────────────────────────────────────────────
code4 = '''def is_odd(n):  return n % 2 == 1
def is_even(n): return n % 2 == 0
def is_over900(p): return p >= 900

def pick_by(pred, nums):
    # 述語（True/False を返す関数）を受け取って共通化
    return [n for n in nums if pred(n)]

prices = [800, 930, 740, 1000, 880, 1200, 950, 700, 900]

print(pick_by(is_odd, prices))       # 奇数
print(pick_by(is_even, prices))      # 偶数
print(pick_by(is_over900, prices))   # 900円以上

# lambda と標準高階関数（map / filter / sorted）
names = ["醤油", "味噌", "塩", "豚骨"]
lengths = list(map(lambda s: (s, len(s)), names))
expensive = list(filter(lambda p: p >= 900, prices))
sorted_by_price = sorted(prices, key=lambda p: p)  # もちろん key 不要だが例として

print(lengths)
print(expensive)
print(sorted_by_price)
'''

def run4():
    def is_odd(n):  return n%2==1
    def is_even(n): return n%2==0
    def is_over900(p): return p>=900
    def pick_by(pred, nums): return [n for n in nums if pred(n)]
    prices=[800,930,740,1000,880,1200,950,700,900]
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
**解説（After）**
- 「条件だけが違う」→ **述語関数（pred）を渡す**ことで **1関数に共通化**。
- `lambda` はその場で小さな関数を作る“即席道具”。
- `map` は「全件に関数適用」、`filter` は「述語を満たすものだけ通す」、`sorted(key=…)` は「並べ替え基準を渡す」でした。
- **可読性**：`list(map(...))` より **内包表記**の方が読みやすいことも多いです（チーム規約に従う）。
""")

st.divider()
st.subheader("🧪 小テスト（MCQ）")

ok1 = mcq(
    "関数オブジェクトそのものを参照するのはどれ？",
    ["boil()", "boil", "boil print"],
    answer_index=1,
    explain="括弧を付けると“実行”。値として渡すなら関数名だけ（boil）。",
    key="hof_q1",
)
ok2 = mcq(
    "条件だけが異なるフィルタ処理を共通化する最適解は？",
    ["条件分岐を増やす", "述語関数を引数に取り、内包表記やfilterで実装", "forを3回回す"],
    answer_index=1,
    explain="述語（True/False関数）を受け取る“高階関数”にすると重複が消えます。",
    key="hof_q2",
)
ok3 = mcq(
    "lambda の主な使いどころは？",
    ["巨大な業務ロジックの実装", "その場限りの小関数を即席で渡す", "I/O最適化"],
    answer_index=1,
    explain="短い一発関数を key / map / filter に渡す用途が中心です。",
    key="hof_q3",
)

st.success(f"スコア：{int(ok1)+int(ok2)+int(ok3)}/3 でした。お疲れ様でございました！")
