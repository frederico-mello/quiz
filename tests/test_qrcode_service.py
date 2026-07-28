import io

from src.qrcode_service import generate_qr_code

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def test_generate_qr_code_returns_bytesio_with_png_signature():
    result = generate_qr_code("https://example.com/share?id=1")

    assert isinstance(result, io.BytesIO)
    assert result.read(8) == PNG_SIGNATURE