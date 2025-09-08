import streamlit as st

st.title("📊 お店ダッシュボード（在庫・提供・売上）")
st.caption("在庫や売上を可視化しながら、ラーメン屋を回してみましょう。")

# 初期状態
if 'sim' not in st.session_state:
    st.session_state['sim'] = {
        'inventory': {
            'noodle': 10,
            'base_shoyu': 5,
            'base_miso': 5,
            'base_shio': 5,
        },
        'cash': 0,
        'served': 0,
        'complaints': 0,
        'sales_over_time': [],  # 累積提供数の推移
    }

sim = st.session_state['sim']

# レシピと価格
RECIPES = {
    '醤油': {'noodle': 1, 'base_shoyu': 1},
    '味噌': {'noodle': 1, 'base_miso': 1},
    '塩':  {'noodle': 1, 'base_shio': 1},
}
PRICES = {'醤油': 800, '味噌': 900, '塩': 850}
RESTOCK_COST = {'noodle': 100, 'base_shoyu': 150, 'base_miso': 150, 'base_shio': 150}

# メトリクス
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("売上（円）", sim['cash'])
with col2:
    st.metric("提供数", sim['served'])
with col3:
    st.metric("クレーム", sim['complaints'])

st.divider()

# 在庫の可視化（簡易バー）
st.subheader("在庫（カラム別）")
bar_data = {k: [v] for k, v in sim['inventory'].items()}  # 単一レコード
st.bar_chart(bar_data, use_container_width=True)
st.caption("補充や提供で棒の高さが変わります。")

st.divider()

# 提供UI
st.subheader("提供（注文をさばく）")
col_a, col_b = st.columns([2,1])
with col_a:
    menu = st.selectbox("メニューを選択", list(RECIPES.keys()), index=0)
    if st.button("🍜 提供する"):
        need = RECIPES[menu]
        # 在庫チェック
        if all(sim['inventory'].get(item, 0) >= qty for item, qty in need.items()):
            for item, qty in need.items():
                sim['inventory'][item] -= qty
            sim['cash'] += PRICES[menu]
            sim['served'] += 1
            sim['sales_over_time'].append(sim['served'])
            st.success(f"{menu}を提供しました。お疲れ様でございました！")
        else:
            sim['complaints'] += 1
            sim['sales_over_time'].append(sim['served'])
            st.error("在庫不足でございました。惜しかったです。")
with col_b:
    st.write("価格（円）")
    st.table({m: PRICES[m] for m in RECIPES})

st.divider()

# 補充UI
st.subheader("補充（仕入れ）")
with st.form("restock_form"):
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        add_noodle = st.number_input("麺", min_value=0, max_value=100, value=0, step=1)
    with c2:
        add_shoyu = st.number_input("醤油ベース", min_value=0, max_value=100, value=0, step=1)
    with c3:
        add_miso = st.number_input("味噌ベース", min_value=0, max_value=100, value=0, step=1)
    with c4:
        add_shio = st.number_input("塩ベース", min_value=0, max_value=100, value=0, step=1)
    submitted = st.form_submit_button("📦 仕入れる")
    if submitted:
        cost = (
            add_noodle * RESTOCK_COST['noodle'] +
            add_shoyu * RESTOCK_COST['base_shoyu'] +
            add_miso * RESTOCK_COST['base_miso'] +
            add_shio * RESTOCK_COST['base_shio']
        )
        # 仕入れコストは現金から差し引き（マイナスも許容: 借金！）
        sim['cash'] -= cost
        sim['inventory']['noodle'] += int(add_noodle)
        sim['inventory']['base_shoyu'] += int(add_shoyu)
        sim['inventory']['base_miso'] += int(add_miso)
        sim['inventory']['base_shio'] += int(add_shio)
        st.success(f"仕入れ完了（コスト: -¥{cost}）。お疲れ様でございました！")

st.caption("注: コストは麺=¥100/玉、各ベース=¥150/杯ぶんでございました。")

st.divider()

# 売上/提供推移（簡易ライン）
st.subheader("提供数の推移（累積）")
line_data = sim['sales_over_time'] if sim['sales_over_time'] else [0]
st.line_chart(line_data, use_container_width=True)

st.divider()

if st.button("全リセット（このページの状態）"):
    st.session_state.pop('sim', None)
    st.success("初期化しました。お疲れ様でございました！")
    st.experimental_rerun()

