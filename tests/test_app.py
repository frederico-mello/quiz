import importlib
import sys
import types
from io import BytesIO


class _SessionState(dict):
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value


class _Column:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False


class _Streamlit:
    def __init__(self):
        self.session_state = _SessionState(
            questions=[
                {"id": 7, "question": "Pergunta", "correct_answer": "Resposta"}
            ],
            answered=True,
            response_text="Resposta avaliada",
            audio_file=None,
        )
        self.query_params = {"q": "7"}

    def set_page_config(self, **kwargs):
        pass

    def markdown(self, *args, **kwargs):
        pass

    def title(self, *args, **kwargs):
        pass

    def columns(self, *args, **kwargs):
        return _Column(), _Column(), _Column()

    def button(self, *args, **kwargs):
        return False

    def image(self, *args, **kwargs):
        pass

    def caption(self, *args, **kwargs):
        pass


def _load_app(monkeypatch):
    monkeypatch.setattr("dotenv.load_dotenv", lambda: None)
    config = importlib.import_module("src.config")
    importlib.reload(config)
    streamlit_module = types.ModuleType("streamlit")
    components_module = types.ModuleType("streamlit.components")
    components_v1_module = types.ModuleType("streamlit.components.v1")
    streamlit_module.components = components_module
    components_module.v1 = components_v1_module
    monkeypatch.setitem(sys.modules, "streamlit", streamlit_module)
    monkeypatch.setitem(sys.modules, "streamlit.components", components_module)
    monkeypatch.setitem(sys.modules, "streamlit.components.v1", components_v1_module)
    qrcode_service_module = types.ModuleType("src.qrcode_service")
    qrcode_service_module.generate_qr_code = lambda url: BytesIO()
    monkeypatch.setitem(sys.modules, "src.qrcode_service", qrcode_service_module)
    avatar_module = types.ModuleType("src.avatar")
    avatar_module.get_idle_gif_base64 = lambda: ""
    avatar_module.get_talking_gif_base64 = lambda: ""
    monkeypatch.setitem(sys.modules, "src.avatar", avatar_module)
    content_filter_module = types.ModuleType("src.content_filter")
    content_filter_module.check_text = lambda text: (False, None)
    content_filter_module.get_warning_level = lambda warnings: "none"
    monkeypatch.setitem(sys.modules, "src.content_filter", content_filter_module)
    llm_service_module = types.ModuleType("src.llm_service")
    llm_service_module.evaluate_answer = lambda question, correct_answer, user_answer: ""
    monkeypatch.setitem(sys.modules, "src.llm_service", llm_service_module)
    quiz_data_module = types.ModuleType("src.quiz_data")
    quiz_data_module.get_question_by_id = lambda questions, question_id: next(
        (question for question in questions if question["id"] == question_id), None
    )
    quiz_data_module.load_questions = lambda: []
    monkeypatch.setitem(sys.modules, "src.quiz_data", quiz_data_module)
    tts_service_module = types.ModuleType("src.tts_service")
    tts_service_module.generate_speech = lambda text: None
    monkeypatch.setitem(sys.modules, "src.tts_service", tts_service_module)
    app = importlib.import_module("app")
    return importlib.reload(app)


def _run_app_and_capture_qr_urls(monkeypatch):
    app = _load_app(monkeypatch)
    streamlit = _Streamlit()
    generated_urls = []

    monkeypatch.setattr(app, "st", streamlit)
    monkeypatch.setattr(
        app,
        "generate_qr_code",
        lambda url: generated_urls.append(url) or BytesIO(),
    )

    app.main()

    return generated_urls


def test_qr_link_uses_public_default_when_app_url_is_unset(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-api-key")
    monkeypatch.delenv("APP_URL", raising=False)

    generated_urls = _run_app_and_capture_qr_urls(monkeypatch)

    assert generated_urls == ["https://lappquiz.ict.unesp.br?q=7"]


def test_qr_link_uses_custom_app_url(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-api-key")
    monkeypatch.setenv("APP_URL", "https://quiz.example.com")

    generated_urls = _run_app_and_capture_qr_urls(monkeypatch)

    assert generated_urls == ["https://quiz.example.com?q=7"]
