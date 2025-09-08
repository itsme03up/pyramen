import streamlit as st
from textwrap import dedent
from difflib import unified_diff
from lib.explains import EXPLAINS

st.title("🧩 お店シミュレーション：穴埋めドリル")
st.caption("___1___ のような空所を正しいコードで埋めてください。printやコメントでの誤魔化しは不可でございました。")

# ページ用の進捗（このページ内だけの合格数）
if 'code_game' not in st.session_state:
    st.session_state['code_game'] = {'passed': {}}  # qkey -> bool
cg = st.session_state['code_game']


def show_tabs(qkey: str, title: str, explain_key: str, skeleton: str, solution: str, hints: list[str], reference_md: str, tester):
    """4タブ（解説/コード/実行/参考）+ 進捗 & 差分。"""
    st.subheader(title)
    t1, t2, t3, t4 = st.tabs(["解説", "コード（スケルトン）", "実行", "参考（落とし穴・追加練習）"])

    with t1:
        st.markdown(EXPLAINS[explain_key])

    with t2:
        default = st.session_state.get(f"code_{qkey}", skeleton)
        st.caption("スケルトンの ___ を埋めてください。")
        code = st.text_area("提出コード", default, height=320, key=f"area_{qkey}")
        with st.expander("ヒント", expanded=False):
            for h in hints:
                st.markdown(f"- {h}")
        # 差分表示
        if st.button(f"解答例との差分を表示（{qkey}）", key=f"diff_{qkey}"):
            diff = "\n".join(unified_diff(solution.splitlines(), code.splitlines(), fromfile="model", tofile="yours", lineterm=""))
            st.code(diff or "差分なし（完全一致）", language="diff")
        # 保存
        if st.button(f"保存（{qkey}）", key=f"save_{qkey}"):
            st.session_state[f"code_{qkey}"] = code
            st.success("保存しました。お疲れ様でございました！")

    with t3:
        code = st.session_state.get(f"code_{qkey}", skeleton)
        if st.button(f"▶ 実行＆採点（{qkey}）", key=f"run_{qkey}"):
            # ユーザーコードを定義部とテスト部で分割（# 最小テスト 以降は除去）
            before, _, _ = code.partition("# 最小テスト")
            ns: dict = {}
            passed, total, details = 0, 0, []
            try:
                exec(before, ns, ns)
                passed, total, details = tester(ns)
                if passed == total:
                    st.success("✅ 合格！ お疲れ様でございました！")
                    cg['passed'][qkey] = True
                else:
                    st.warning("一部のテストに未合格があります。惜しかったです。")
                    cg['passed'][qkey] = False
            except Exception as e:
                st.error(f"❌ 実行時エラー：{e}")
                cg['passed'][qkey] = False
                return
            # 進捗バー
            st.progress(passed / total if total else 0.0, text=f"{passed} / {total} テスト合格")
            # 詳細
            for ok, msg in details:
                (st.success if ok else st.error)(msg)
        # リセット
        if st.button(f"↺ リセット（{qkey}）", key=f"reset_{qkey}"):
            st.session_state.pop(f"code_{qkey}", None)
            cg['passed'].pop(qkey, None)
            st.experimental_rerun()

    with t4:
        st.markdown(reference_md)


# ===== Q1 =====
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
SOLUTION_Q1 = dedent('''
class OutOfStockError(Exception):
    pass
class RamenShop:
    stock = {"noodle": 3, "base_shoyu": 2}
    @classmethod
    def has(cls, item: str, qty: int) -> bool:
        return cls.stock.get(item, 0) >= qty
    @classmethod
    def consume(cls, item: str, qty: int = 1) -> None:
        if not cls.has(item, qty):
            raise OutOfStockError(f"在庫不足: {item}")
        cls.stock[item] -= qty
''')
HINTS_Q1 = [
    "___1___: dict.get を使って個数比較 (>=)",
    "___2___: OutOfStockError を raise",
    "___3___: 減算代入演算子（-=）",
]
REF_Q1 = dedent('''
**落とし穴**: `cls.stock[item]` 直アクセスで KeyError。例外の代わりに False 返却は非推奨。

**追加練習**: `@classmethod def add_stock(...)` を実装して補充も一元化。
''')

def test_Q1(ns: dict):
    passed, total, details = 0, 3, []
    RamenShop = ns.get('RamenShop'); OutOfStockError = ns.get('OutOfStockError')
    ok1 = bool(RamenShop and RamenShop.has("noodle", 2) is True)
    details.append((ok1, "has('noodle',2) が True"))
    if ok1: passed += 1
    try:
        RamenShop.consume("noodle", 2)
        ok2 = (RamenShop.stock["noodle"] == 1)
    except Exception:
        ok2 = False
    details.append((ok2, "consume 後に在庫が 1"))
    if ok2: passed += 1
    try:
        RamenShop.consume("base_shoyu", 3)
        ok3 = False
    except Exception as e:
        ok3 = isinstance(e, OutOfStockError)
    details.append((ok3, "在庫不足で OutOfStockError を送出"))
    if ok3: passed += 1
    return passed, total, details


# ===== Q2 =====
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
SOLUTION_Q2 = dedent('''
x = "global"
def outer():
    x = "enclosing"
    def inner():
        nonlocal x
        x = x + "->inner"
        return x
    inner(); return x
def use_global():
    global x
    x = x + "->G"
    return x
''')
HINTS_Q2 = [
    "___1___: 直近の外側の変数を書き換えるキーワード",
    "___2___: モジュール変数を指すキーワード",
]
REF_Q2 = dedent('''
**落とし穴**: nonlocal は外側“関数”が必要。トップレベルには効きません。

**追加練習**: nonlocal と global を混在させて状態の流れを観察。
''')

def test_Q2(ns: dict):
    passed, total, details = 0, 2, []
    outer = ns.get('outer'); use_global = ns.get('use_global')
    ok1 = (outer and outer() == "enclosing->inner")
    details.append((ok1, "outer() が 'enclosing->inner'"))
    if ok1: passed += 1
    ok2 = (use_global and use_global() == "global->G")
    details.append((ok2, "use_global() が 'global->G'"))
    if ok2: passed += 1
    return passed, total, details


# ===== Q3 =====
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
SOLUTION_Q3 = dedent('''
menu = [
    {"name": "醤油", "price": 800},
    {"name": "味噌", "price": 900},
    {"name": "塩",  "price": 850},
]
def pick_cheapest(items: list[dict]) -> dict:
    return min(items, key=lambda i: i["price"])
''')
HINTS_Q3 = [
    "___1___: 目的は“最小”の要素を取る",
    "___2___: 無名関数キーワード",
]
REF_Q3 = dedent('''
**落とし穴**: キー名のタイプミスに注意。

**追加練習**: max(..., key=lambda x: len(x["toppings"])) を考える。
''')

def test_Q3(ns: dict):
    passed, total, details = 0, 1, []
    f = ns.get('pick_cheapest'); menu = ns.get('menu')
    ok = bool(f and menu and f(menu)["name"] == "醤油" and f(menu)["price"] == 800)
    details.append((ok, "最安メニューが 醤油(800)"))
    if ok: passed += 1
    return passed, total, details


# ===== Q4 =====
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
SOLUTION_Q4 = dedent('''
def serve_stream(orders: list[str]):
    for o in orders:
        yield f"提供: {o}"
''')
HINTS_Q4 = [
    "___1___: 停止位置を覚えた return",
]
REF_Q4 = dedent('''
**落とし穴**: return を使うとループが終わる。yield を使う。
''')

def test_Q4(ns: dict):
    passed, total, details = 0, 2, []
    gfn = ns.get('serve_stream')
    g = gfn(["醤油","味噌","塩"]) if gfn else None
    ok1 = (g is not None) and (next(g) == "提供: 醤油")
    details.append((ok1, "next(g) が '提供: 醤油'"))
    if ok1: passed += 1
    ok2 = (list(g) == ["提供: 味噌", "提供: 塩"]) if gfn else False
    details.append((ok2, "list(g) が ['提供: 味噌','提供: 塩']"))
    if ok2: passed += 1
    return passed, total, details


# ===== Q5 =====
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
SOLUTION_Q5 = dedent('''
def make_counter(start: int = 0):
    count = start
    def inc(step: int = 1) -> int:
        nonlocal count
        count += step
        return count
    return inc
''')
HINTS_Q5 = [
    "___1___: 外側の count を再束縛するキーワード",
]
REF_Q5 = dedent('''
**落とし穴**: nonlocal がないと UnboundLocalError。
''')

def test_Q5(ns: dict):
    passed, total, details = 0, 3, []
    make_counter = ns.get('make_counter')
    c = make_counter(1) if make_counter else None
    ok1 = (c() == 2) if c else False
    details.append((ok1, "初回呼び出しで 2"))
    if ok1: passed += 1
    ok2 = (c(2) == 4) if c else False
    details.append((ok2, "step=2 で 4"))
    if ok2: passed += 1
    ok3 = (c() == 5) if c else False
    details.append((ok3, "次回呼び出しで 5"))
    if ok3: passed += 1
    return passed, total, details


# ===== Q6 =====
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
SOLUTION_Q6 = dedent('''
import time
def with_log(func):
    def wrapper(*args, **kwargs):
        t0 = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        except Exception:
            raise
    return wrapper
@with_log
def serve(bowl: str) -> str:
    if bowl == "売り切れ":
        raise RuntimeError("在庫切れ")
    return f"{bowl}を提供しました"
''')
HINTS_Q6 = [
    "___1___: 直前の例外をそのまま再送出",
]
REF_Q6 = dedent('''
**落とし穴**: 例外を握りつぶして None を返さないこと。
''')

def test_Q6(ns: dict):
    passed, total, details = 0, 2, []
    serve = ns.get('serve')
    ok1 = (serve and serve("醤油") == "醤油を提供しました")
    details.append((ok1, "serve('醤油') が 正しい文言"))
    if ok1: passed += 1
    try:
        serve("売り切れ")
        ok2 = False
    except RuntimeError:
        ok2 = True
    details.append((ok2, "売り切れ で RuntimeError"))
    if ok2: passed += 1
    return passed, total, details


# ===== Q7 =====
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
SOLUTION_Q7 = dedent('''
class Ramen:
    VALID_BASES = {"shio","shoyu","miso","tonkotsu"}
    def __init__(self, base: str, price: int = 900):
        if not Ramen.is_valid_base(base):
            raise ValueError("無効なスープ")
        self.base = base; self.price = price
    @staticmethod
    def is_valid_base(base: str) -> bool:
        return base in Ramen.VALID_BASES
    @classmethod
    def from_menu(cls, name: str) -> "Ramen":
        table = {"塩":("shio",850), "醤油":("shoyu",800), "味噌":("miso",900)}
        b, p = table[name]
        return cls(b, p)
''')
HINTS_Q7 = [
    "___1___: static メソッド呼び出し（クラスに依存しない）",
    "___2___: 検証集合（クラス変数）",
    "___3___: 代替コンストラクタで使う呼び出し先",
]
REF_Q7 = dedent('''
**落とし穴**: is_valid_base を classmethod にする必要はない。
''')

def test_Q7(ns: dict):
    passed, total, details = 0, 1, []
    Ramen = ns.get('Ramen')
    r = Ramen.from_menu("醤油") if Ramen else None
    ok = bool(r and isinstance(r, Ramen) and r.base == "shoyu" and r.price == 800)
    details.append((ok, "from_menu('醤油') が shoyu/800"))
    if ok: passed += 1
    return passed, total, details


# ===== Q8 =====
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
SOLUTION_Q8 = dedent('''
class Shop:
    def __init__(self, name: str):
        self._name = name
        self.__secret_recipe = "base"
    def order(self, base: str, toppings: list[str]) -> dict:
        return {"shop": self._name, "base": base, "toppings": toppings}
class PremiumShop(Shop):
    def order(self, base: str, toppings: list[str]) -> dict:
        if "egg" not in toppings:
            toppings = toppings + ["egg"]
        return super().order(base, toppings)
''')
HINTS_Q8 = [
    "___1___: 自動で加えるトッピング名",
    "___2___: 親メソッド参照のためのビルトイン",
]
REF_Q8 = dedent('''
**落とし穴**: in-place append は副作用に注意。新しいリストを返すのが安全。
''')

def test_Q8(ns: dict):
    passed, total, details = 0, 2, []
    PremiumShop = ns.get('PremiumShop')
    p = PremiumShop("高級支店") if PremiumShop else None
    out = p.order("miso", ["nori"]) if p else None
    ok1 = bool(out and out["toppings"][-1] == "egg")
    details.append((ok1, "自動で 'egg' を追加"))
    if ok1: passed += 1
    try:
        _ = p.__secret_recipe  # noqa: F841
        ok2 = False
    except AttributeError:
        ok2 = True
    details.append((ok2, "__secret_recipe は直接参照不可（AttributeError）"))
    if ok2: passed += 1
    return passed, total, details


# ===== UI 構築（各Qに4タブを提供） =====
st.divider()
show_tabs("Q1", "Q1 クラス変数と在庫消費（基礎）", "Q1", SKELETON_Q1, SOLUTION_Q1, HINTS_Q1, REF_Q1, test_Q1)
st.divider()
show_tabs("Q2", "Q2 スコープ：global / nonlocal の違い", "Q2", SKELETON_Q2, SOLUTION_Q2, HINTS_Q2, REF_Q2, test_Q2)
st.divider()
show_tabs("Q3", "Q3 ラムダ＆高階関数：一番安い丼を選ぶ", "Q3", SKELETON_Q3, SOLUTION_Q3, HINTS_Q3, REF_Q3, test_Q3)
st.divider()
show_tabs("Q4", "Q4 ジェネレータ：丼を順番に提供", "Q4", SKELETON_Q4, SOLUTION_Q4, HINTS_Q4, REF_Q4, test_Q4)
st.divider()
show_tabs("Q5", "Q5 クロージャ：替え玉カウンタ", "Q5", SKELETON_Q5, SOLUTION_Q5, HINTS_Q5, REF_Q5, test_Q5)
st.divider()
show_tabs("Q6", "Q6 デコレータ：提供ログ＆失敗ハンドリング", "Q6", SKELETON_Q6, SOLUTION_Q6, HINTS_Q6, REF_Q6, test_Q6)
st.divider()
show_tabs("Q7", "Q7 クラスメソッド／スタティックメソッド：工場とバリデータ", "Q7", SKELETON_Q7, SOLUTION_Q7, HINTS_Q7, REF_Q7, test_Q7)
st.divider()
show_tabs("Q8", "Q8 オーバーライド＆データ隠蔽（名前マングリング）", "Q8", SKELETON_Q8, SOLUTION_Q8, HINTS_Q8, REF_Q8, test_Q8)

st.divider()
# スコアボード（このページ専用）
passed_count = sum(1 for v in cg['passed'].values() if v)
total_q = 8
st.metric("合格数", f"{passed_count} / {total_q}")
if st.button("Reset（このページの合否を初期化）"):
    st.session_state['code_game'] = {'passed': {}}
    st.success("このページの進捗を初期化しました。お疲れ様でございました！")
    st.experimental_rerun()

