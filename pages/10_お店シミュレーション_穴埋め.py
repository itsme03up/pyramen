import streamlit as st
from textwrap import dedent

st.title("🧩 お店シミュレーション：穴埋めドリル")
st.caption("___1___ のような空所を正しいコードで埋めてください。printやコメントでの誤魔化しは不可でございました。")

# ページ用の進捗（このページ内だけの合格数）
if 'code_game' not in st.session_state:
    st.session_state['code_game'] = {'passed': {}}  # qkey -> bool
cg = st.session_state['code_game']

def run_q(qkey: str, skeleton: str, height: int = 320):
    """共通UI: テキストエリア + 実行＆採点 + 合否表示"""
    default = st.session_state.get(f"code_{qkey}", skeleton)
    code = st.text_area(f"以下の ___ を埋めてください（{qkey}）", default, height=height, key=f"area_{qkey}")
    colA, colB = st.columns([1,1])
    with colA:
        if st.button(f"▶ 実行＆採点（{qkey}）", key=f"run_{qkey}"):
            ns = {}
            try:
                exec(code, ns, ns)
                st.success("✅ 合格！ 良かったですね！")
                cg['passed'][qkey] = True
                st.session_state[f"code_{qkey}"] = code
            except Exception as e:
                st.error(f"❌ テスト失敗：{e}")
                st.info("テストはコード末尾の assert で判定しています。")
    with colB:
        if st.button(f"↺ リセット（{qkey}）", key=f"reset_{qkey}"):
            st.session_state.pop(f"code_{qkey}", None)
            cg['passed'].pop(qkey, None)
            st.experimental_rerun()


# スコアボード（このページ専用）
passed_count = sum(1 for v in cg['passed'].values() if v)
total_q = 8
st.metric("合格数", f"{passed_count} / {total_q}")
if st.button("Reset（このページの合否を初期化）"):
    st.session_state['code_game'] = {'passed': {}}
    st.success("このページの進捗を初期化しました。良かったですね！")
    st.experimental_rerun()

st.divider()

# ===== Q1 =====
st.subheader("Q1 クラス変数と在庫消費（基礎）")
st.caption("狙い：クラス変数の共有／安全な消費メソッド")
SKELETON_Q1 = dedent('''
# ramen_stock.py
class OutOfStockError(Exception):
    pass

class RamenShop:
    # すべての店舗で共有する在庫
    stock = {"noodle": 3, "base_shoyu": 2}

    @classmethod
    def has(cls, item: str, qty: int) -> bool:
        return ___1___  # 例: 指定個数あるか判定

    @classmethod
    def consume(cls, item: str, qty: int = 1) -> None:
        if not cls.has(item, qty):
            ___2___  # OutOfStockError を投げる
        cls.stock[item] ___3___ qty  # 在庫を減らす

# 最小テスト
assert RamenShop.has("noodle", 2) is True
RamenShop.consume("noodle", 2)
assert RamenShop.stock["noodle"] == 1
try:
    RamenShop.consume("base_shoyu", 3)
    raise AssertionError("在庫不足で例外が必要")
except OutOfStockError:
    pass
''')
with st.expander("Q1 を開く/閉じる", expanded=True):
    run_q("Q1", SKELETON_Q1)

# ===== Q2 =====
st.subheader("Q2 スコープ：global / nonlocal の違い")
st.caption("狙い：global と nonlocal の正しい使い分け")
SKELETON_Q2 = dedent('''
# scope_demo.py
x = "global"

def outer():
    x = "enclosing"
    def inner():
        ___1___ x         # nonlocal を正しく使う
        x = x + "->inner"
        return x
    inner()
    return x

def use_global():
    ___2___ x            # global を正しく宣言
    x = x + "->G"
    return x

# 最小テスト
assert outer() == "enclosing->inner"
assert use_global() == "global->G"
''')
with st.expander("Q2 を開く/閉じる", expanded=False):
    run_q("Q2", SKELETON_Q2)

# ===== Q3 =====
st.subheader("Q3 ラムダ＆高階関数：一番安い丼を選ぶ")
st.caption("狙い：sorted/min と lambda")
SKELETON_Q3 = dedent('''
# pick_cheapest.py
menu = [
    {"name": "醤油", "price": 800},
    {"name": "味噌", "price": 900},
    {"name": "塩",   "price": 850},
]

def pick_cheapest(items: list[dict]) -> dict:
    # 価格で一番安いメニューを返す
    return ___1___(items, key=___2___ i: i["price"])

# 最小テスト
c = pick_cheapest(menu)
assert c["name"] == "醤油" and c["price"] == 800
''')
with st.expander("Q3 を開く/閉じる", expanded=False):
    run_q("Q3", SKELETON_Q3)

# ===== Q4 =====
st.subheader("Q4 ジェネレータ：丼を順番に提供")
st.caption("狙い：yield と遅延評価")
SKELETON_Q4 = dedent('''
# bowl_queue.py
def serve_stream(orders: list[str]):
    """注文リストから1杯ずつ提供するジェネレータ"""
    for o in orders:
        ___1___ f"提供: {o}"   # yield を使って返す

# 最小テスト
g = serve_stream(["醤油","味噌","塩"])
assert next(g) == "提供: 醤油"
assert list(g) == ["提供: 味噌", "提供: 塩"]
''')
with st.expander("Q4 を開く/閉じる", expanded=False):
    run_q("Q4", SKELETON_Q4)

# ===== Q5 =====
st.subheader("Q5 クロージャ：替え玉カウンタ")
st.caption("狙い：エンクロージャ内の状態を保持")
SKELETON_Q5 = dedent('''
# counter_closure.py
def make_counter(start: int = 0):
    count = start
    def inc(step: int = 1) -> int:
        ___1___ count     # 適切なスコープ宣言
        count += step
        return count
    return inc

# 最小テスト
c = make_counter(1)
assert c() == 2
assert c(2) == 4
assert c() == 5
''')
with st.expander("Q5 を開く/閉じる", expanded=False):
    run_q("Q5", SKELETON_Q5)

# ===== Q6 =====
st.subheader("Q6 デコレータ：提供ログ＆失敗ハンドリング")
st.caption("狙い：共通処理（ログ）と例外の再送出")
SKELETON_Q6 = dedent('''
# serve_decorator.py
import time

def with_log(func):
    def wrapper(*args, **kwargs):
        t0 = time.time()
        try:
            result = func(*args, **kwargs)
            print(f"[OK] {func.__name__} took {time.time()-t0:.3f}s")
            return result
        except Exception as e:
            print(f"[NG] {func.__name__}: {e}")
            ___1___     # 例外を再送出（握りつぶさない）
    return wrapper

@with_log
def serve(bowl: str) -> str:
    if bowl == "売り切れ":
        raise RuntimeError("在庫切れ")
    return f"{bowl}を提供しました"

# 最小テスト
assert serve("醤油") == "醤油を提供しました"
try:
    serve("売り切れ")
    raise AssertionError("例外が必要")
except RuntimeError:
    pass
''')
with st.expander("Q6 を開く/閉じる", expanded=False):
    run_q("Q6", SKELETON_Q6)

# ===== Q7 =====
st.subheader("Q7 クラスメソッド／スタティックメソッド：工場とバリデータ")
st.caption("狙い：@classmethod と @staticmethod の役割分担")
SKELETON_Q7 = dedent('''
# ramen_factory.py
class Ramen:
    VALID_BASES = {"shio","shoyu","miso","tonkotsu"}

    def __init__(self, base: str, price: int = 900):
        if not ___1___(base):
            raise ValueError("無効なスープ")
        self.base = base
        self.price = price

    @staticmethod
    def is_valid_base(base: str) -> bool:
        return base in ___2___

    @classmethod
    def from_menu(cls, name: str) -> "Ramen":
        table = {"塩":("shio",850), "醤油":("shoyu",800), "味噌":("miso",900)}
        b, p = table[name]
        return ___3___(b, p)

# 最小テスト
r = Ramen.from_menu("醤油")
assert isinstance(r, Ramen) and r.base == "shoyu" and r.price == 800
''')
with st.expander("Q7 を開く/閉じる", expanded=False):
    run_q("Q7", SKELETON_Q7)

# ===== Q8 =====
st.subheader("Q8 オーバーライド＆データ隠蔽（名前マングリング）")
st.caption("狙い：super()・オーバーライド・__name の扱い")
SKELETON_Q8 = dedent('''
# premium_shop.py
class Shop:
    def __init__(self, name: str):
        self._name = name
        self.__secret_recipe = "base"  # マングリング対象

    def order(self, base: str, toppings: list[str]) -> dict:
        return {"shop": self._name, "base": base, "toppings": toppings}

class PremiumShop(Shop):
    def order(self, base: str, toppings: list[str]) -> dict:
        # 自動で味玉を追加し、親のorderを呼ぶ
        if "egg" not in toppings:
            toppings = toppings + [___1___]
        res = ___2___().order(base, toppings)
        # 秘密レシピが外から直接見えないことを確認（AttributeError期待）
        try:
            _ = self.__secret_recipe
            raise AssertionError("隠蔽されていない")
        except AttributeError:
            pass
        return res

# 最小テスト
p = PremiumShop("高級支店")
out = p.order("miso", ["nori"])
assert out["toppings"][-1] == "egg"
''')
with st.expander("Q8 を開く/閉じる", expanded=False):
    run_q("Q8", SKELETON_Q8)

