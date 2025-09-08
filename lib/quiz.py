import streamlit as st
from typing import List, Optional

def mcq(question: str, choices: List[str], answer_index: int, explain: str = "", key: Optional[str] = None) -> bool:
    """単一選択のMCQ。初回採点時だけスコアを集計し、以降は結果表示のみ。

    - 集計は st.session_state['quiz_state'] に保持（correct/total, graded辞書）。
    - gradedは設問キー単位で一度きり加算。Resetはトップで実装。
    """
    qkey = key or question
    st.markdown(f"**Q. {question}**")
    picked = st.radio("選択肢", choices, index=None, key=qkey)

    # 集計用のセッション状態初期化
    if 'quiz_state' not in st.session_state:
        st.session_state['quiz_state'] = {
            'correct': 0,
            'total': 0,
            'graded': {},  # qkey -> {correct: bool}
        }
    qs = st.session_state['quiz_state']

    ok = False
    if st.button("採点する", key=f"{qkey}_score"):
        if picked is None:
            st.warning("選んでから採点してください。")
        else:
            ok = (choices.index(picked) == answer_index)
            already = qkey in qs['graded']
            if not already:
                qs['total'] += 1
                if ok:
                    qs['correct'] += 1
                qs['graded'][qkey] = {'correct': ok}
            # 表示（既採点でも再表示だけ行う）
            if ok:
                st.success("✅ 正解でした。お疲れ様でございました！")
            else:
                st.error(f"❌ 惜しかったです。正解は「{choices[answer_index]}」でした。")
            if already:
                st.info("この設問は採点済みです（Resetでやり直せます）。")
            if explain:
                st.info(explain)
    return ok
