import base64
import os

import streamlit as st
import streamlit.components.v1 as components

from src.avatar import (
    get_idle_gif_base64,
    get_talking_gif_base64,
)
from src.config import MODERATION_ENABLED, OPENROUTER_API_KEY
from src.content_filter import check_text, get_warning_level
from src.llm_service import evaluate_answer
from src.quiz_data import get_question, load_questions
from src.tts_service import generate_speech

QUIZ_CSS = """
<style>
:root {
    --bg-gradient-start: #f5f7fa;
    --bg-gradient-end: #c3cfe2;
    --question-bg: #f5f7fa;
    --question-text: #1a1a2e;
    --response-bg: #f0f4ff;
    --response-text: #1a1a2e;
    --progress-color: #666;
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg-gradient-start: #1a1a2e;
        --bg-gradient-end: #16213e;
        --question-bg: #1a1a2e;
        --question-text: #f5f7fa;
        --response-bg: #0f3460;
        --response-text: #e4e4e7;
        --progress-color: #a1a1aa;
    }
}

.stTextInput > div > div > input {
    font-size: 18px;
    padding: 12px;
}
.stButton > button {
    font-size: 18px;
    padding: 8px 24px;
}
.question-box {
    background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
    padding: 24px;
    border-radius: 16px;
    margin: 16px 0;
    font-size: 22px;
    font-weight: bold;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    color: var(--question-text);
}
.progress-text {
    text-align: center;
    color: var(--progress-color);
    font-size: 14px;
}
.response-text {
    background: var(--response-bg);
    padding: 16px;
    border-radius: 12px;
    margin: 12px 0;
    font-size: 16px;
    line-height: 1.6;
    color: var(--response-text);
}
</style>
"""


def main():
    st.set_page_config(
        page_title="Quiz do Professor",
        page_icon="🧑‍🔬",
        layout="centered",
    )

    st.markdown(QUIZ_CSS, unsafe_allow_html=True)

    if not OPENROUTER_API_KEY:
        st.error(
            "⚠️ OPENROUTER_API_KEY não configurada. Crie um arquivo .env com sua chave."
        )
        return

    if "questions" not in st.session_state:
        st.session_state.questions = load_questions()
        st.session_state.current_index = 0
        st.session_state.answered = False
        st.session_state.response_text = ""
        st.session_state.audio_file = None
        st.session_state.moderation_warnings = 0
        st.session_state.moderation_blocked = False

    st.title("🧑‍🔬 Quiz do Professor")
    st.markdown(
        f'<p class="progress-text">Pergunta {st.session_state.current_index + 1} de {len(st.session_state.questions)}</p>',
        unsafe_allow_html=True,
    )

    question = get_question(st.session_state.questions, st.session_state.current_index)
    if not question:
        st.success("🎉 Parabéns! Você completou todas as perguntas!")
        if st.button("Recomeçar"):
            st.session_state.current_index = 0
            st.session_state.answered = False
            st.session_state.response_text = ""
            st.session_state.audio_file = None
            st.rerun()
        return

    st.markdown(
        f'<div class="question-box">{question["question"]}</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.answered:
        user_answer = st.text_input(
            "Sua resposta:",
            key="answer_input",
            placeholder="Digite sua resposta aqui...",
        )

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit = st.button(
                "Enviar Resposta", type="primary", use_container_width=True
            )

        if submit:

            def _process_answer():
                with st.spinner("🤔 O professor está pensando..."):
                    try:
                        response_text = evaluate_answer(
                            question["question"],
                            question["correct_answer"],
                            user_answer,
                        )
                        st.session_state.response_text = response_text

                        with st.spinner("🎙️ Gerando áudio da resposta..."):
                            audio_path = generate_speech(response_text)
                            st.session_state.audio_file = audio_path

                        st.session_state.answered = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao processar: {e}")

            if not user_answer.strip():
                st.warning("Por favor, digite uma resposta antes de enviar.")
            elif st.session_state.get("moderation_blocked", False):
                st.error(
                    "⚠️ Sua sessão foi bloqueada devido a tentativas repetidas de envio de conteúdo impróprio. Recarregue a página para tentar novamente."
                )
            else:
                if MODERATION_ENABLED:
                    with st.spinner("Verificando conteúdo..."):
                        is_blocked, block_msg = check_text(user_answer)

                    if is_blocked:
                        st.session_state.moderation_warnings += 1
                        warning_level = get_warning_level(
                            st.session_state.moderation_warnings
                        )

                        if warning_level == "first":
                            st.warning(
                                f"⚠️ {block_msg} Esta é sua primeira advertência. Por favor, mantenha o respeito."
                            )
                        elif warning_level == "second":
                            st.warning(
                                f"⚠️ {block_msg} Esta é sua segunda advertência. Uma última chance antes do bloqueio."
                            )
                        else:
                            st.session_state.moderation_blocked = True
                            st.error(
                                "🚫 Você excedeu o número de tentativas com conteúdo impróprio. Sua sessão foi bloqueada."
                            )
                    else:
                        _process_answer()
                else:
                    _process_answer()
    else:
        st.markdown(
            f'<div class="response-text">{st.session_state.response_text}</div>',
            unsafe_allow_html=True,
        )

        if st.session_state.audio_file and os.path.exists(st.session_state.audio_file):
            try:
                talking_b64 = get_talking_gif_base64()
                idle_b64 = get_idle_gif_base64()

                with open(st.session_state.audio_file, "rb") as f:
                    audio_b64 = base64.b64encode(f.read()).decode("utf-8")

                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    sync_html = f"""
                    <div style="text-align:center;">
                        <img id="prof-gif" src="data:image/gif;base64,{talking_b64}"
                             width="160" style="display:block;margin:0 auto;"
                             alt="Professor Quiz">
                        <div style="color:#764ba2;font-weight:bold;margin-top:4px;font-size:14px;">Professor Quiz</div>
                        <audio id="prof-audio" autoplay controls style="margin-top:10px;width:100%;"
                            onplay="document.getElementById('prof-gif').src='data:image/gif;base64,{talking_b64}';"
                            onended="document.getElementById('prof-gif').src='data:image/gif;base64,{idle_b64}';">
                            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
                        </audio>
                    </div>
                    """
                    components.html(sync_html, height=250)

            except Exception as e:
                st.warning(f"Não foi possível reproduzir o áudio: {e}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Tentar novamente", use_container_width=True):
                st.session_state.answered = False
                st.session_state.response_text = ""
                if st.session_state.audio_file:
                    try:
                        os.remove(st.session_state.audio_file)
                    except OSError:
                        pass
                    st.session_state.audio_file = None
                st.rerun()
        with col2:
            if st.button(
                "➡️ Próxima pergunta", type="primary", use_container_width=True
            ):
                st.session_state.current_index += 1
                st.session_state.answered = False
                st.session_state.response_text = ""
                if st.session_state.audio_file:
                    try:
                        os.remove(st.session_state.audio_file)
                    except OSError:
                        pass
                    st.session_state.audio_file = None
                st.rerun()


if __name__ == "__main__":
    main()
