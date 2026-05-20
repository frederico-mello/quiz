import os
import time
import streamlit as st
from src.config import OPENROUTER_API_KEY, MODERATION_ENABLED
from src.quiz_data import load_questions, get_question
from src.llm_service import evaluate_answer
from src.tts_service import generate_speech, get_audio_duration
from src.avatar import get_talking_gif_base64
from src.content_filter import check_text, get_warning_level

GIF_BASE64 = get_talking_gif_base64()

SCIENTIST_CSS = """
<style>
.scientist-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 20px;
    margin: 20px auto;
    max-width: 200px;
}
.scientist-gif {
    width: 160px;
    height: 160px;
    border-radius: 12px;
}
.scientist-label {
    color: white;
    font-size: 14px;
    margin-top: 10px;
    font-weight: bold;
}
</style>
"""

SCIENTIST_HTML = f"""
<div class="scientist-container">
    <img class="scientist-gif" src="data:image/gif;base64,{GIF_BASE64}" alt="Professor Quiz">
    <div class="scientist-label">Professor Quiz</div>
</div>
"""

QUIZ_CSS = """
<style>
.stTextInput > div > div > input {
    font-size: 18px;
    padding: 12px;
}
.stButton > button {
    font-size: 18px;
    padding: 8px 24px;
}
.question-box {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 24px;
    border-radius: 16px;
    margin: 16px 0;
    font-size: 22px;
    font-weight: bold;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.progress-text {
    text-align: center;
    color: #666;
    font-size: 14px;
}
.response-text {
    background: #f0f4ff;
    padding: 16px;
    border-radius: 12px;
    margin: 12px 0;
    font-size: 16px;
    line-height: 1.6;
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
        st.error("⚠️ OPENROUTER_API_KEY não configurada. Crie um arquivo .env com sua chave.")
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

    st.markdown(f'<div class="question-box">{question["question"]}</div>', unsafe_allow_html=True)

    if not st.session_state.answered:
        user_answer = st.text_input("Sua resposta:", key="answer_input", placeholder="Digite sua resposta aqui...")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit = st.button("Enviar Resposta", type="primary", use_container_width=True)

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
                st.error("⚠️ Sua sessão foi bloqueada devido a tentativas repetidas de envio de conteúdo impróprio. Recarregue a página para tentar novamente.")
            else:
                if MODERATION_ENABLED:
                    with st.spinner("Verificando conteúdo..."):
                        is_blocked, block_msg = check_text(user_answer)

                    if is_blocked:
                        st.session_state.moderation_warnings += 1
                        warning_level = get_warning_level(st.session_state.moderation_warnings)

                        if warning_level == "first":
                            st.warning(f"⚠️ {block_msg} Esta é sua primeira advertência. Por favor, mantenha o respeito.")
                        elif warning_level == "second":
                            st.warning(f"⚠️ {block_msg} Esta é sua segunda advertência. Uma última chance antes do bloqueio.")
                        else:
                            st.session_state.moderation_blocked = True
                            st.error("🚫 Você excedeu o número de tentativas com conteúdo impróprio. Sua sessão foi bloqueada.")
                    else:
                        _process_answer()
                else:
                    _process_answer()
    else:
        st.markdown(f'<div class="response-text">{st.session_state.response_text}</div>', unsafe_allow_html=True)

        if st.session_state.audio_file and os.path.exists(st.session_state.audio_file):
            try:
                duration = get_audio_duration(st.session_state.audio_file)

                animation_placeholder = st.empty()
                audio_placeholder = st.empty()

                animation_placeholder.markdown(SCIENTIST_CSS + SCIENTIST_HTML, unsafe_allow_html=True)

                with open(st.session_state.audio_file, "rb") as f:
                    audio_bytes = f.read()
                audio_placeholder.audio(audio_bytes, format="audio/mp3", autoplay=True)

                time.sleep(duration)

                animation_placeholder.empty()

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
            if st.button("➡️ Próxima pergunta", type="primary", use_container_width=True):
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
