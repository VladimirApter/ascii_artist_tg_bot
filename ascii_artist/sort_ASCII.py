from PIL import Image, ImageDraw, ImageFont

ASCII = [
    ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_',
    '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
]


def generate_sorted_ascii_list(symbols=None):
    if symbols is None or len(symbols) == 0:
        symbols = ASCII
    ASCII_list = "".join(set(symbols))
    font = ImageFont.truetype('msjhl.ttc', 36)
    #font = ImageFont.truetype('arial.ttf', 36)
    images = {}
    for symbol in ASCII_list:
        img_width, img_height = 45, 45
        img = Image.new('RGB', (img_width, img_height), (255, 255, 255))

        drawer = ImageDraw.Draw(img)
        drawer.text((3, 0), symbol, font=font, fill=(0, 0, 0))

        images[symbol] = img

    counts = {}
    for symbol, img in images.items():
        count = 0
        for x in range(img.width):
            for y in range(img.height):
                r, g, b = img.getpixel((x, y))
                if not (r == 255 and g == 255 and b == 255):
                    count += 1
        counts[symbol] = count

    ASCII_list = sorted(ASCII_list, key=lambda symbol: counts[symbol])

    return ASCII_list
