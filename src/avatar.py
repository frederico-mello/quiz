import base64
import io
import math
import os

from PIL import Image, ImageDraw

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
GIF_PATH = os.path.join(ASSETS_DIR, "scientist.gif")
IDLE_GIF_PATH = os.path.join(ASSETS_DIR, "scientist_idle.gif")

WIDTH, HEIGHT = 200, 220
CENTER_X = 100
FACE_Y = 95


class TransparentGifConverter:
    def __init__(self, alpha_threshold: int = 0):
        self.alpha_threshold = alpha_threshold

    def process(self, img: Image.Image) -> Image.Image:
        rgba = img.convert("RGBA")
        palette_img = rgba.convert("P")
        palette = palette_img.getpalette()
        if palette is None:
            raise ValueError("Failed to get palette from image")
        pixels = list(palette_img.getdata())  # type: ignore[arg-type]

        used_colors = set()
        transparent_pixels = set()
        for i, p in enumerate(pixels):
            pixel = rgba.getpixel((i % rgba.width, i // rgba.width))
            if not isinstance(pixel, (tuple, list)):
                continue
            if pixel[3] <= self.alpha_threshold:
                transparent_pixels.add(i)
            else:
                used_colors.add(p)

        free_idx = 255
        for i in range(255, -1, -1):
            if i not in used_colors:
                free_idx = i
                break

        new_palette = bytearray(palette)
        if 0 in used_colors:
            old_0_color = bytes(palette[0:3])
            new_palette[free_idx * 3 : free_idx * 3 + 3] = old_0_color
            for i in range(3):
                new_palette[i] = 0
            for i, p in enumerate(pixels):
                if p == 0 and i not in transparent_pixels:
                    pixels[i] = free_idx
            for i in transparent_pixels:
                pixels[i] = 0
        else:
            for i in range(3):
                new_palette[i] = 0
            for i in transparent_pixels:
                pixels[i] = 0

        out = Image.new("P", rgba.size)
        out.putpalette(new_palette)
        out.putdata(pixels)
        out.info["transparency"] = 0
        out.info["background"] = 0
        return out


def _draw_scientist_frame(
    mouth_open_factor: float = 0.0,
    is_blinking: bool = False,
    eye_offset: float = 0.0,
) -> Image.Image:
    """Desenha um frame do avatar professor."""
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    hair_color = (80, 50, 30)
    face_color = (255, 224, 189)
    glass_color = (40, 40, 40)
    nose_color = (240, 190, 140)
    coat_color = (255, 255, 255)

    # Cabelo (topo)
    draw.ellipse(
        [CENTER_X - 55, FACE_Y - 75, CENTER_X + 55, FACE_Y - 25], fill=hair_color
    )
    draw.ellipse(
        [CENTER_X - 60, FACE_Y - 60, CENTER_X - 30, FACE_Y - 30], fill=hair_color
    )
    draw.ellipse(
        [CENTER_X + 30, FACE_Y - 60, CENTER_X + 60, FACE_Y - 30], fill=hair_color
    )
    draw.ellipse(
        [CENTER_X - 50, FACE_Y - 80, CENTER_X - 10, FACE_Y - 40], fill=hair_color
    )
    draw.ellipse(
        [CENTER_X + 10, FACE_Y - 80, CENTER_X + 50, FACE_Y - 40], fill=hair_color
    )

    # Orelhas
    draw.ellipse(
        [CENTER_X - 58, FACE_Y - 10, CENTER_X - 42, FACE_Y + 20], fill=face_color
    )
    draw.ellipse(
        [CENTER_X + 42, FACE_Y - 10, CENTER_X + 58, FACE_Y + 20], fill=face_color
    )

    # Rosto
    draw.ellipse(
        [CENTER_X - 45, FACE_Y - 40, CENTER_X + 45, FACE_Y + 50], fill=face_color
    )

    # Olhos
    eye_y = FACE_Y - 5
    if is_blinking:
        draw.line([CENTER_X - 20, eye_y, CENTER_X - 8, eye_y], fill=(0, 0, 0), width=3)
        draw.line([CENTER_X + 8, eye_y, CENTER_X + 20, eye_y], fill=(0, 0, 0), width=3)
    else:
        draw.ellipse(
            [CENTER_X - 22, eye_y - 10, CENTER_X - 6, eye_y + 12],
            fill=(255, 255, 255),
            outline=(0, 0, 0),
        )
        draw.ellipse(
            [CENTER_X + 6, eye_y - 10, CENTER_X + 22, eye_y + 12],
            fill=(255, 255, 255),
            outline=(0, 0, 0),
        )
        look_x = int(2 * math.sin(eye_offset))
        draw.ellipse(
            [CENTER_X - 16 + look_x, eye_y - 2, CENTER_X - 10 + look_x, eye_y + 6],
            fill=(0, 0, 0),
        )
        draw.ellipse(
            [CENTER_X + 12 + look_x, eye_y - 2, CENTER_X + 18 + look_x, eye_y + 6],
            fill=(0, 0, 0),
        )

    # Sobrancelhas
    draw.line(
        [CENTER_X - 20, FACE_Y - 18, CENTER_X - 8, FACE_Y - 22],
        fill=hair_color,
        width=3,
    )
    draw.line(
        [CENTER_X + 8, FACE_Y - 22, CENTER_X + 20, FACE_Y - 18],
        fill=hair_color,
        width=3,
    )

    # Óculos
    draw.ellipse(
        [CENTER_X - 28, eye_y - 16, CENTER_X - 2, eye_y + 16],
        outline=glass_color,
        width=3,
    )
    draw.ellipse(
        [CENTER_X + 2, eye_y - 16, CENTER_X + 28, eye_y + 16],
        outline=glass_color,
        width=3,
    )
    draw.line([CENTER_X - 2, eye_y, CENTER_X + 2, eye_y], fill=glass_color, width=3)
    draw.line(
        [CENTER_X - 28, eye_y, CENTER_X - 45, eye_y - 5], fill=glass_color, width=2
    )
    draw.line(
        [CENTER_X + 28, eye_y, CENTER_X + 45, eye_y - 5], fill=glass_color, width=2
    )

    # Nariz
    draw.polygon(
        [
            (CENTER_X, FACE_Y + 10),
            (CENTER_X - 8, FACE_Y + 28),
            (CENTER_X + 8, FACE_Y + 28),
        ],
        fill=nose_color,
    )

    # Boca
    mouth_y = FACE_Y + 40
    if mouth_open_factor < 0.15:
        # Boca fechada (arco de sorriso)
        draw.arc(
            [CENTER_X - 20, mouth_y - 5, CENTER_X + 20, mouth_y + 15],
            start=0,
            end=180,
            fill=(180, 60, 60),
            width=3,
        )
    else:
        # Boca aberta (falando)
        mouth_h = int(4 + 18 * mouth_open_factor)
        mouth_w = 28
        draw.ellipse(
            [
                CENTER_X - mouth_w // 2,
                mouth_y,
                CENTER_X + mouth_w // 2,
                mouth_y + mouth_h,
            ],
            fill=(80, 30, 30),
            outline=(180, 60, 60),
            width=2,
        )
        if mouth_h > 6:
            draw.ellipse(
                [
                    CENTER_X - 10,
                    mouth_y + mouth_h - 6,
                    CENTER_X + 10,
                    mouth_y + mouth_h,
                ],
                fill=(255, 100, 100),
            )

    # Franja (cabelo frontal)
    draw.ellipse(
        [CENTER_X - 50, FACE_Y - 65, CENTER_X - 20, FACE_Y - 35], fill=hair_color
    )
    draw.ellipse(
        [CENTER_X + 20, FACE_Y - 65, CENTER_X + 50, FACE_Y - 35], fill=hair_color
    )
    draw.ellipse(
        [CENTER_X - 30, FACE_Y - 70, CENTER_X + 10, FACE_Y - 40], fill=hair_color
    )
    draw.ellipse(
        [CENTER_X - 10, FACE_Y - 70, CENTER_X + 30, FACE_Y - 40], fill=hair_color
    )

    # Casaco / Corpo
    draw.polygon(
        [
            (CENTER_X - 50, FACE_Y + 45),
            (CENTER_X - 20, HEIGHT - 10),
            (CENTER_X + 20, HEIGHT - 10),
            (CENTER_X + 50, FACE_Y + 45),
        ],
        fill=coat_color,
    )
    draw.line(
        [
            (CENTER_X - 50, FACE_Y + 45),
            (CENTER_X - 20, HEIGHT - 10),
            (CENTER_X + 20, HEIGHT - 10),
            (CENTER_X + 50, FACE_Y + 45),
        ],
        fill=(220, 220, 220),
        width=2,
    )
    draw.ellipse(
        [CENTER_X - 3, FACE_Y + 60, CENTER_X + 3, FACE_Y + 68],
        fill=(200, 200, 200),
        outline=(150, 150, 150),
    )
    draw.ellipse(
        [CENTER_X - 3, FACE_Y + 80, CENTER_X + 3, FACE_Y + 88],
        fill=(200, 200, 200),
        outline=(150, 150, 150),
    )

    return img


def _frames_to_gif_bytes(
    frames: list[Image.Image], duration_ms: int, loop: int = 0
) -> bytes:
    """Converte uma lista de frames PIL em bytes GIF."""
    converter = TransparentGifConverter()
    frames_p = [converter.process(f) for f in frames]
    buf = io.BytesIO()
    frames_p[0].save(
        buf,
        format="GIF",
        save_all=True,
        optimize=False,
        append_images=frames_p[1:],
        duration=duration_ms,
        loop=loop,
        disposal=2,
    )
    return buf.getvalue()


def generate_talking_gif_bytes(audio_duration_seconds: float = 0) -> bytes:
    """Gera GIF animado do professor falando.

    Se audio_duration_seconds > 0, o GIF terá duração igual ao áudio
    e tocará apenas uma vez (loop=1), parando no último frame.
    Caso contrário, gera GIF padrão de 20 frames com loop infinito.
    """
    frame_duration_ms = 100  # 10 FPS

    if audio_duration_seconds > 0:
        num_frames = max(20, int(audio_duration_seconds * 1000 / frame_duration_ms))
        loop_count = 1  # Toca uma vez e para
    else:
        num_frames = 20
        loop_count = 0  # Loop infinito

    frames = []
    for frame_idx in range(num_frames):
        mouth_open = abs(math.sin(frame_idx * math.pi / 4))
        is_blinking = (frame_idx % 10) in (8, 9)
        eye_offset = frame_idx * 0.4
        frames.append(_draw_scientist_frame(mouth_open, is_blinking, eye_offset))

    return _frames_to_gif_bytes(frames, frame_duration_ms, loop_count)


def generate_idle_gif_bytes() -> bytes:
    """Gera GIF do professor parado, apenas piscando os olhos.

    GIF com loop infinito (loop=0), boca fechada, piscada ocasional.
    48 frames a 125ms = 6 segundos por ciclo de loop.
    """
    num_frames = 48
    frame_duration_ms = 125

    frames = []
    for frame_idx in range(num_frames):
        # Pisca 2 frames a cada ~4 segundos (frames 30-31 de 48)
        is_blinking = frame_idx in (30, 31)
        # Movimento suave dos olhos
        eye_offset = frame_idx * 0.15
        frames.append(_draw_scientist_frame(0.0, is_blinking, eye_offset))

    return _frames_to_gif_bytes(frames, frame_duration_ms, loop=0)


def get_talking_gif_base64(duration_seconds: float = 0) -> str:
    """Retorna GIF falante em base64.

    Se duration_seconds for fornecido, gera um GIF com a duração
    exata do áudio. Caso contrário, usa o GIF padrão em cache.
    """
    if duration_seconds > 0:
        gif_bytes = generate_talking_gif_bytes(duration_seconds)
        return base64.b64encode(gif_bytes).decode("utf-8")

    # GIF padrão (cache em disco)
    if not os.path.exists(GIF_PATH):
        os.makedirs(ASSETS_DIR, exist_ok=True)
        gif_bytes = generate_talking_gif_bytes()
        with open(GIF_PATH, "wb") as f:
            f.write(gif_bytes)

    with open(GIF_PATH, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def get_idle_gif_base64() -> str:
    """Retorna GIF idle (piscando) em base64, com cache em disco."""
    if not os.path.exists(IDLE_GIF_PATH):
        os.makedirs(ASSETS_DIR, exist_ok=True)
        gif_bytes = generate_idle_gif_bytes()
        with open(IDLE_GIF_PATH, "wb") as f:
            f.write(gif_bytes)

    with open(IDLE_GIF_PATH, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
