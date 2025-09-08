import streamlit as st
from typing import List, Optional

def mcq(question: str, choices: List[str], answer_index: int, explain: str = "", key: Optional[str] = None) -> bool:
    st.markdown(f"**Q. {question}**")
    picked = st.radio("選択肢", choices, index=None, key=key)
    ok = False
    if st.button("採点する", key=f"{key or question}_score"):
        if picked is None:
            st.warning("選んでから採点してください。")
        else:
            ok = (choices.index(picked) == answer_index)
            if ok:
                st.success("✅ 正解でした。良かったですね！")
            else:
                st.error(f"❌ 残念。正解は「{choices[answer_index]}」でした。")
            if explain:
                st.info(explain)
    return ok
