import streamlit as st

def section_title(title: str, subtitle: str = ""):
    st.markdown(f"## {title}")
    if subtitle:
        st.caption(subtitle)

def code_block(code: str, lang: str = "python", note: str = ""):
    if note:
        st.caption(note)
    st.code(code, language=lang)

def code_showcase(title: str, code: str, runner=None, lang: str = "python"):
    t1, t2, t3 = st.tabs(["解説", "コード", "実行"])
    with t1:
        st.markdown(f"**{title}** のポイントでございました。")
        st.markdown("- 重要な引数・戻り値\n- 想定される出力\n- 試験の落とし穴 など")
    with t2:
        st.code(code, language=lang)
    with t3:
        if runner is not None:
            try:
                runner()
            except Exception as e:
                st.error(f"実行時エラーでした: {e}")
        else:
            st.info("このセクションは実行なしでございました。")
