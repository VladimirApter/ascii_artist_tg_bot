from PIL import Image, ImageFilter, ImageEnhance
from ascii_artist.ascii_art_draw import create_img_font_drawer, draw_line

ASCII_SYMBOLS, IS_RGB_MODE = [], True


def _process_image(img, result_size):
    img = img.filter(ImageFilter.SHARPEN)
    img = img.resize(result_size)

    enhancer = ImageEnhance.Contrast(img)
    contrast_enhanced_image = enhancer.enhance(1.5)

    return contrast_enhanced_image


def _get_pixels_line(img, line_number):
    width, _ = img.size

    line = []
    for x in range(width):
        pixel = list(img.getpixel((x, line_number)))
        line.append(pixel)

    return line


def _convert_pixel_to_ascii_symbol(pixel):
    pixel = pixel[:3]
    grey_value = _convert_rgb_to_grey(pixel)
    pixel_graduation = grey_value / 256

    if IS_RGB_MODE:
        color_index = pixel.index(max(pixel))
        symbol_index = int(pixel_graduation * len(ASCII_SYMBOLS[color_index]))
        symbol = ASCII_SYMBOLS[color_index][symbol_index]
    else:
        symbol = ASCII_SYMBOLS[int(pixel_graduation * len(ASCII_SYMBOLS))]
    return symbol


def _convert_rgb_to_grey(pixel):
    r = pixel[0]
    g = pixel[1]
    b = pixel[2]
    return r * 0.299 + g * 0.587 + b * 0.114


def convert_img_to_ascii_art(img_path, result_height, symbols, is_RGB, bg_color, font_color, quality):
    global ASCII_SYMBOLS, IS_RGB_MODE
    ASCII_SYMBOLS, IS_RGB_MODE = symbols, is_RGB

    img = Image.open(img_path)
    width, height = img.size

    result_width = int(result_height / height * width)
    result_size = (result_width, result_height)
    img = _process_image(img, result_size)

    font_size = 12
    if quality >= 90:
        font_size = 16
    result_img, font, drawer = create_img_font_drawer(result_size, font_size, bg_color)

    for line_number in range(result_height):
        line = _get_pixels_line(img, line_number)
        result_line = []
        for pixel in line:
            result_line.append(_convert_pixel_to_ascii_symbol(pixel))
        draw_line(drawer, font, result_line, line_number, font_color)

    return result_img
