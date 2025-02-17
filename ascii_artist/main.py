import os
from concurrent.futures import ThreadPoolExecutor
from moviepy.editor import VideoFileClip

from ascii_artist.ascii_art_maker import convert_img_to_ascii_art
from ascii_artist.extract_frames import extract_frames_from_video
from ascii_artist.create_video import create_and_save_video
from ascii_artist.symbols import make_ASCII_list
from ascii_artist.symbols_packs import SymbolsPacks


def main(file_path, result_height, bg_color=(0, 0, 0), font_color=(255, 255, 255), symbols=None, true_color_mode=False):
    bg_color, font_color = tuple(bg_color), tuple(font_color)
    file_directory_name, file = os.path.split(os.path.abspath(file_path))
    file_name, file_format = file.split('.')
    resized_file_path = os.path.join(file_directory_name, f"{file_name}_resized.{file_format}")
    result_without_audio_path = os.path.join(file_directory_name, f"{file_name}_ascii_art_without_audio.{file_format}")
    result_path = os.path.join(file_directory_name, f"{file_name}_ascii_art.{file_format}")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    frames_dir = os.path.join(current_dir, "frames", file_name)
    result_frames_dir = os.path.join(current_dir, "result_frames", file_name)
    os.mkdir(os.path.join(frames_dir))
    os.mkdir(os.path.join(result_frames_dir))

    font_path, font_size = get_font_path_and_size_by_symbols(symbols)

    symbols, is_RGB = make_ASCII_list(bg_color, font_color, symbols, font_path)
    if true_color_mode:
        symbols.remove(' ')

    photo_quality = max(200 - result_height, 50)
    video_quality = photo_quality * 0.7
    if result_height <= 30:
        video_quality = 100

    if file_format == 'jpg' or file_format == 'png':
        _process_image(result_height, file_path, symbols, is_RGB, bg_color,
                       font_color, photo_quality, result_path, true_color_mode, font_path, font_size)
    else:
        _process_video(result_height, file_path, resized_file_path, frames_dir,
                       result_frames_dir, symbols, is_RGB,
                       result_without_audio_path, result_path, bg_color,
                       font_color, video_quality, true_color_mode, font_path, font_size)

    os.rmdir(frames_dir)
    os.rmdir(result_frames_dir)


def _process_image(result_height, file_path, symbols, is_RGB, bg_color, font_color, photo_quality, result_path, true_color_mode, font_path, font_size):
    result_img = convert_img_to_ascii_art(file_path, result_height, symbols, is_RGB, bg_color, font_color, photo_quality, true_color_mode, font_path, font_size)
    result_img.save(result_path, optimize=True, quality=photo_quality)


def _process_video(result_height, file_path, resized_file_path, frames_dir,
                   result_frames_dir, symbols, is_RGB,
                   result_without_audio_path, result_path, bg_color,
                   font_color, video_quality, true_color_mode, font_path, font_size):

    font_size = min(int(font_size * 0.6), 12)
    video = VideoFileClip(file_path, verbose=False)
    resized_video = video.resize(height=result_height)
    resized_video.write_videofile(resized_file_path, verbose=False, logger=None)

    frames_count, fps = extract_frames_from_video(resized_file_path, frames_dir)
    os.remove(resized_file_path)
    frames_per_group = frames_count // os.cpu_count()

    frame_groups = [range(i * frames_per_group, min((i + 1) * frames_per_group, frames_count)) for i in range((frames_count + frames_per_group - 1) // frames_per_group)]
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        for _ in executor.map(lambda group: _process_frame_group(group, frames_dir, result_frames_dir, symbols, is_RGB, result_height, bg_color, font_color, video_quality, true_color_mode, font_path, font_size), frame_groups):
            pass

    create_and_save_video(result_frames_dir, result_without_audio_path, "frame", "png", fps)

    for dir in [frames_dir, result_frames_dir]:
        for filename in os.listdir(dir):
            remove_file_path = os.path.join(dir, filename)
            os.unlink(remove_file_path)

    original_audio = video.audio
    result_without_audio = VideoFileClip(result_without_audio_path, verbose=False)
    result = result_without_audio.set_audio(original_audio)
    result.write_videofile(result_path, audio_codec='aac', verbose=False, logger=None)

    video.close()
    os.remove(result_without_audio_path)


def _process_frame_group(frame_group, frames_dir, result_frames_dir, symbols, is_RGB, result_height, bg_color, font_color, video_quality, true_color_mode, font_path, font_size):
    for i in frame_group:
        frame_path = os.path.join(frames_dir, f"frame_{i}.png")
        result_frame = convert_img_to_ascii_art(frame_path, result_height, symbols, is_RGB, bg_color, font_color, video_quality, true_color_mode, font_path, font_size)
        result_frame_path = os.path.join(result_frames_dir, f"frame_{i}.png")
        result_frame.save(result_frame_path, optimize=True, quality=video_quality)


def get_font_path_and_size_by_symbols(symbols):
    fonts_dir = os.path.join(os.getcwd(), 'fonts')
    font_path = os.path.join(fonts_dir, 'NotoSansMono-SemiBold.ttf')
    font_size = 14
    if symbols == SymbolsPacks.japanese:
        font_path = os.path.join(fonts_dir, 'NotoSansJP-SemiBold.ttf')
        font_size = 22
    elif symbols == SymbolsPacks.braille or symbols == SymbolsPacks.angles:
        font_path = os.path.join(fonts_dir, 'NotoSansSymbols2-Regular.ttf')
    elif symbols == SymbolsPacks.arabian:
        font_path = os.path.join(fonts_dir, 'NotoKufiArabic-SemiBold.ttf')
        font_size = 22
    return font_path, font_size

