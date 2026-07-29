from pathlib import Path
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)


DIGITS = {
    "0": ("111", "101", "101", "101", "111"),
    "1": ("010", "110", "010", "010", "111"),
    "2": ("111", "001", "111", "100", "111"),
    "3": ("111", "001", "111", "001", "111"),
    "4": ("101", "101", "111", "001", "001"),
    "5": ("111", "100", "111", "001", "111"),
    "6": ("111", "100", "111", "101", "111"),
    "7": ("111", "001", "010", "010", "010"),
    "8": ("111", "101", "111", "101", "111"),
    "9": ("111", "101", "111", "001", "111"),
}

TILES = [
    ("2", "#45426f", "#9b96df", "#ffffff"),
    ("4", "#5a3e88", "#c685ff", "#ffffff"),
    ("8", "#963ac5", "#f584ff", "#ffffff"),
    ("16", "#d52ba1", "#ff8bdc", "#ffffff"),
    ("32", "#f33f76", "#ff9ab8", "#ffffff"),
    ("64", "#ff5e42", "#ffb195", "#ffffff"),
    ("128", "#ff9d24", "#ffe17d", "#291500"),
    ("256", "#ffd21e", "#fff49b", "#2d1b00"),
    ("512", "#82ef45", "#caff9f", "#092900"),
    ("1024", "#16e5b4", "#9bffe8", "#002a20"),
    ("2048", "#42eaff", "#c5fbff", "#00252a"),
]


def hex_rgba(value, alpha=255):
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def draw_number(draw, text, color):
    scale = 3 if len(text) <= 2 else 2
    width = (len(text) * 4 - 1) * scale
    x0 = (32 - width) // 2
    y0 = (32 - 5 * scale) // 2
    for index, char in enumerate(text):
        for y, row in enumerate(DIGITS[char]):
            for x, bit in enumerate(row):
                if bit == "1":
                    x1 = x0 + (index * 4 + x) * scale
                    y1 = y0 + y * scale
                    draw.rectangle((x1, y1, x1 + scale - 1, y1 + scale - 1), fill=color)


def make_tile_sheet():
    sheet = Image.new("RGBA", (128, 96), (0, 0, 0, 0))
    for index, (text, base, shine, ink) in enumerate(TILES):
        tile = Image.new("RGBA", (32, 32), hex_rgba(base))
        draw = ImageDraw.Draw(tile)
        draw.rectangle((0, 0, 31, 31), outline=hex_rgba(shine))
        draw.rectangle((2, 2, 29, 29), outline=hex_rgba("#17122f", 120))
        draw.line((2, 2, 28, 2), fill=hex_rgba(shine, 180), width=2)
        draw.line((2, 2, 2, 28), fill=hex_rgba(shine, 120), width=2)
        draw.rectangle((27, 27, 29, 29), fill=hex_rgba("#080516", 95))
        draw_number(draw, text, hex_rgba(ink))
        x = (index % 4) * 32
        y = (index // 4) * 32
        sheet.alpha_composite(tile, (x, y))

    super_tile = Image.new("RGBA", (32, 32), hex_rgba("#7f5cff"))
    draw = ImageDraw.Draw(super_tile)
    draw.rectangle((0, 0, 31, 31), outline=hex_rgba("#ffffff"))
    for y in range(3, 29, 4):
        for x in range(3 + (y % 8), 29, 8):
            draw.rectangle((x, y, x + 2, y + 2), fill=hex_rgba("#70f7ff"))
    sheet.alpha_composite(super_tile, (96, 64))
    sheet.save(ASSETS / "tile-sprites.png", optimize=True)


def make_nine_slice(name, fill, light, dark):
    image = Image.new("RGBA", (32, 32), hex_rgba(fill))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 31, 31), outline=hex_rgba(light))
    draw.rectangle((2, 2, 29, 29), outline=hex_rgba(dark))
    draw.line((3, 3, 27, 3), fill=hex_rgba(light, 180), width=2)
    draw.line((3, 3, 3, 27), fill=hex_rgba(light, 120), width=2)
    draw.line((4, 28, 28, 28), fill=hex_rgba(dark, 220), width=2)
    draw.line((28, 4, 28, 28), fill=hex_rgba(dark, 220), width=2)
    image.save(ASSETS / name, optimize=True)


def make_background():
    source = Image.open(ASSETS / "neon-city-bg-source.png").convert("RGB")
    source.thumbnail((512, 512), Image.Resampling.NEAREST)
    canvas = Image.new("RGB", (512, 512), "#030619")
    canvas.paste(source, ((512 - source.width) // 2, (512 - source.height) // 2))
    canvas.save(ASSETS / "neon-city-bg.png", optimize=True)


make_background()
make_tile_sheet()
make_nine_slice("panel.png", "#0d0b25", "#5c4b95", "#03030c")
make_nine_slice("cell.png", "#17142f", "#39315f", "#090817")
make_nine_slice("button.png", "#563dc5", "#70f7ff", "#24136d")
