from sort_ASCII import generate_sorted_ascii_list


def _make_RGB_list(ASCII_list):
    ASCII_list_RGB = [
        [ASCII_list[i] for i in range(len(ASCII_list)) if i % 9 < 3],
        [ASCII_list[i] for i in range(len(ASCII_list)) if i % 9 < 6],
        [ASCII_list[i] for i in range(len(ASCII_list)) if i % 9 < 9]
    ]
    return ASCII_list_RGB


def make_ASCII_list(symbols=None):
    is_RGB = True
    ASCII_list = generate_sorted_ascii_list(symbols)
    if len(ASCII_list) < 60:
        is_RGB = False
    else:
        ASCII_list = _make_RGB_list(ASCII_list)
    return ASCII_list, is_RGB
