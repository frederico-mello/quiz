import io
import math
import os
from PIL import Image, ImageDraw

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
GIF_PATH = os.path.join(ASSETS_DIR, "scientist.gif")


def generate_talking_gif_bytes() -> bytes:
    """Gera um GIF animado de um cientista falando."""
    frames = []
    width, height = 200, 220
    center_x = 100
    face_y = 95

    for frame_idx in range(20):
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        hair_color = (80, 50, 30)
        face_color = (255, 224, 189)
        glass_color = (40, 40, 40)
        nose_color = (240, 190, 140)
        coat_color = (255, 255, 255)

        # === CABELO (fundo) ===
        draw.ellipse([center_x - 55, face_y - 75, center_x + 55, face_y - 25], fill=hair_color)
        draw.ellipse([center_x - 60, face_y - 60, center_x - 30, face_y - 30], fill=hair_color)
        draw.ellipse([center_x + 30, face_y - 60, center_x + 60, face_y - 30], fill=hair_color)
        draw.ellipse([center_x - 50, face_y - 80, center_x - 10, face_y - 40], fill=hair_color)
        draw.ellipse([center_x + 10, face_y - 80, center_x + 50, face_y - 40], fill=hair_color)

        # === ORELHAS ===
        draw.ellipse([center_x - 58, face_y - 10, center_x - 42, face_y + 20], fill=face_color)
        draw.ellipse([center_x + 42, face_y - 10, center_x + 58, face_y + 20], fill=face_color)

        # === ROSTO ===
        draw.ellipse([center_x - 45, face_y - 40, center_x + 45, face_y + 50], fill=face_color)

        # === OLHOS ===
        eye_y = face_y - 5
        is_blinking = (frame_idx % 10) in (8, 9)

        if is_blinking:
            draw.line([center_x - 20, eye_y, center_x - 8, eye_y], fill=(0, 0, 0), width=3)
            draw.line([center_x + 8, eye_y, center_x + 20, eye_y], fill=(0, 0, 0), width=3)
        else:
            draw.ellipse([center_x - 22, eye_y - 10, center_x - 6, eye_y + 12], fill=(255, 255, 255), outline=(0, 0, 0))
            draw.ellipse([center_x + 6, eye_y - 10, center_x + 22, eye_y + 12], fill=(255, 255, 255), outline=(0, 0, 0))
            look_x = int(2 * math.sin(frame_idx * 0.4))
            draw.ellipse([center_x - 16 + look_x, eye_y - 2, center_x - 10 + look_x, eye_y + 6], fill=(0, 0, 0))
            draw.ellipse([center_x + 12 + look_x, eye_y - 2, center_x + 18 + look_x, eye_y + 6], fill=(0, 0, 0))

        # === SOBRANCELHAS ===
        draw.line([center_x - 20, face_y - 18, center_x - 8, face_y - 22], fill=hair_color, width=3)
        draw.line([center_x + 8, face_y - 22, center_x + 20, face_y - 18], fill=hair_color, width=3)

        # === ÓCULOS ===
        draw.ellipse([center_x - 28, eye_y - 16, center_x - 2, eye_y + 16], outline=glass_color, width=3)
        draw.ellipse([center_x + 2, eye_y - 16, center_x + 28, eye_y + 16], outline=glass_color, width=3)
        draw.line([center_x - 2, eye_y, center_x + 2, eye_y], fill=glass_color, width=3)
        draw.line([center_x - 28, eye_y, center_x - 45, eye_y - 5], fill=glass_color, width=2)
        draw.line([center_x + 28, eye_y, center_x + 45, eye_y - 5], fill=glass_color, width=2)

        # === NARIZ ===
        draw.polygon([
            (center_x, face_y + 10),
            (center_x - 8, face_y + 28),
            (center_x + 8, face_y + 28),
        ], fill=nose_color)

        # === BOCA (ANIMADA) ===
        mouth_y = face_y + 40
        talk_cycle = abs(math.sin(frame_idx * math.pi / 4))

        if talk_cycle < 0.15:
            draw.arc([center_x - 20, mouth_y - 5, center_x + 20, mouth_y + 15], start=0, end=180, fill=(180, 60, 60), width=3)
        else:
            mouth_h = int(4 + 18 * talk_cycle)
            mouth_w = 28
            draw.ellipse(
                [center_x - mouth_w // 2, mouth_y, center_x + mouth_w // 2, mouth_y + mouth_h],
                fill=(80, 30, 30),
                outline=(180, 60, 60),
                width=2,
            )
            if mouth_h > 6:
                draw.ellipse(
                    [center_x - 10, mouth_y + mouth_h - 6, center_x + 10, mouth_y + mouth_h],
                    fill=(255, 100, 100),
                )

        # === CABELO (frente/franja) ===
        draw.ellipse([center_x - 50, face_y - 65, center_x - 20, face_y - 35], fill=hair_color)
        draw.ellipse([center_x + 20, face_y - 65, center_x + 50, face_y - 35], fill=hair_color)
        draw.ellipse([center_x - 30, face_y - 70, center_x + 10, face_y - 40], fill=hair_color)
        draw.ellipse([center_x - 10, face_y - 70, center_x + 30, face_y - 40], fill=hair_color)

        # === JALECO ===
        draw.polygon([
            (center_x - 50, face_y + 45),
            (center_x - 20, height - 10),
            (center_x + 20, height - 10),
            (center_x + 50, face_y + 45),
        ], fill=coat_color)
        draw.line([
            (center_x - 50, face_y + 45),
            (center_x - 20, height - 10),
            (center_x + 20, height - 10),
            (center_x + 50, face_y + 45),
        ], fill=(220, 220, 220), width=2)
        draw.ellipse([center_x - 3, face_y + 60, center_x + 3, face_y + 68], fill=(200, 200, 200), outline=(150, 150, 150))
        draw.ellipse([center_x - 3, face_y + 80, center_x + 3, face_y + 88], fill=(200, 200, 200), outline=(150, 150, 150))

        frames.append(img)

    buf = io.BytesIO()
    frames[0].save(
        buf,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0,
        disposal=2,
    )
    return buf.getvalue()


def get_talking_gif_base64() -> str:
    """Retorna o GIF em base64, gerando e salvando em disco se necessário."""
    import base64

    if not os.path.exists(GIF_PATH):
        os.makedirs(ASSETS_DIR, exist_ok=True)
        gif_bytes = generate_talking_gif_bytes()
        with open(GIF_PATH, "wb") as f:
            f.write(gif_bytes)

    with open(GIF_PATH, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def ensure_avatar_exists() -> None:
    """Garante que o arquivo GIF do avatar existe no disco."""
    if not os.path.exists(GIF_PATH):
        os.makedirs(ASSETS_DIR, exist_ok=True)
        gif_bytes = generate_talking_gif_bytes()
        with open(GIF_PATH, "wb") as f:
            f.write(gif_bytes)
