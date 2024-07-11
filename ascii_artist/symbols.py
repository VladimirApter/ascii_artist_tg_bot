from ascii_artist.sort_ASCII import generate_sorted_ascii_list


def make_ASCII_list(bg_color, font_color, symbols=None):
    is_RGB = False
    ASCII_list = generate_sorted_ascii_list(symbols)

    if not _is_color1_brightness_less_than_color2(bg_color, font_color):
        ASCII_list.reverse()

    return ASCII_list, is_RGB


def _is_color1_brightness_less_than_color2(color1, color2):
    color1_brightness = color1[0] * 0.299 + color1[1] * 0.587 + color1[2] * 0.114
    color2_brightness = color2[0] * 0.299 + color2[1] * 0.587 + color2[2] * 0.114

    return color1_brightness < color2_brightness
