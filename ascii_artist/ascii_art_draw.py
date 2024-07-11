from PIL import Image, ImageDraw, ImageFont


def create_img_font_drawer(original_img_size, font_size, bg_color=(0, 0, 0)):
    font = ImageFont.truetype('ebrima.ttf', font_size)
    #font = ImageFont.truetype('arial.ttf', font_size)

    img_width = original_img_size[0] * font_size
    img_height = original_img_size[1] * font_size

    img = Image.new('RGB', (img_width, img_height), bg_color)
    drawer = ImageDraw.Draw(img)

    return img, font, drawer


def draw_line(drawer, font, line, line_number, font_color=(255, 255, 255)):
    for x, symbol in enumerate(line):
        drawer.text((x * font.size, line_number * font.size), symbol, font=font, fill=font_color)
