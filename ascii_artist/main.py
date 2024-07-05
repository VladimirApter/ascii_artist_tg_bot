import os
from concurrent.futures import ThreadPoolExecutor
from alive_progress import alive_bar
from moviepy.editor import VideoFileClip

from ascii_artist.ascii_art_maker import convert_img_to_ascii_art
from ascii_artist.extract_frames import extract_frames_from_video
from ascii_artist.create_video import create_and_save_video
from ascii_artist.symbols import make_ASCII_list


def main(file_path, result_height, bg_color=(0, 0, 0), font_color=(255, 255, 255), symbols=None):
    file_directory_name, file = os.path.split(os.path.abspath(file_path))
    file_name, file_format = file.split('.')
    resized_file_path = os.path.join(file_directory_name, f"{file_name}_resized.{file_format}")
    result_without_audio_path = os.path.join(file_directory_name, f"{file_name}_ascii_art_without_audio.{file_format}")
    result_path = os.path.join(file_directory_name, f"{file_name}_ascii_art.{file_format}")

    current_dir = os.getcwd()
    frames_dir = os.path.join(current_dir, "frames")
    result_frames_dir = os.path.join(current_dir, "result_frames")

    symbols, is_RGB = make_ASCII_list(symbols)

    photo_quality = max(150 - result_height, 50)
    video_quality = photo_quality * 0.7

    if file_format == 'jpg' or file_format == 'png':
        process_image(result_height, file_path, symbols, is_RGB, bg_color,
                      font_color, photo_quality, result_path)
    else:
        process_video(file_path, result_height, resized_file_path, frames_dir,
                      result_frames_dir, symbols, is_RGB,
                      result_without_audio_path, result_path, bg_color,
                      font_color, video_quality)


def process_image(result_height, file_path, symbols, is_RGB, bg_color, font_color, photo_quality, result_path):
    print("Обработка картирнки началась")
    with alive_bar(result_height, title="Преобразование картинки  ") as bar:
        result_img = convert_img_to_ascii_art(file_path, result_height, symbols, is_RGB, bg_color, font_color, photo_quality, bar)
    result_img.save(result_path, optimize=True, quality=photo_quality)


def process_video(file_path, result_height, resized_file_path, frames_dir,
                  result_frames_dir, symbols, is_RGB,
                  result_without_audio_path, result_path, bg_color,
                  font_color, video_quality):
    print(f"Обработка видео началась")

    video = VideoFileClip(file_path, verbose=False)
    resized_video = video.resize(height=result_height)
    resized_video.write_videofile(resized_file_path, verbose=False, logger=None)

    frames_count, fps = extract_frames_from_video(resized_file_path, frames_dir)
    os.remove(resized_file_path)
    frames_per_group = frames_count // os.cpu_count()

    frame_groups = [range(i * frames_per_group, min((i + 1) * frames_per_group, frames_count)) for i in range((frames_count + frames_per_group - 1) // frames_per_group)]
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        with alive_bar(frames_count, title="Преобразование видео  ") as bar:
            for _ in executor.map(lambda group: process_frame_group(group, frames_dir, result_frames_dir, symbols, is_RGB, result_height, bar, bg_color, font_color, video_quality), frame_groups):
                pass

    create_and_save_video(result_frames_dir, result_without_audio_path, "frame", "png", fps)

    for dir in [frames_dir, result_frames_dir]:
        for filename in os.listdir(dir):
            remove_file_path = os.path.join(dir, filename)
            os.unlink(remove_file_path)

    original_audio = VideoFileClip(file_path, verbose=False).audio
    result_without_audio = VideoFileClip(result_without_audio_path, verbose=False)
    result = result_without_audio.set_audio(original_audio)
    result.write_videofile(result_path, audio_codec='aac', verbose=False, logger=None)

    os.remove(result_without_audio_path)


def process_frame_group(frame_group, frames_dir, result_frames_dir, symbols, is_RGB, result_height, bar, bg_color, font_color, video_quality):
    for i in frame_group:
        bar()
        frame_path = os.path.join(frames_dir, f"frame_{i}.png")
        result_frame = convert_img_to_ascii_art(frame_path, result_height, symbols, is_RGB, bg_color, font_color, video_quality)
        result_frame_path = os.path.join(result_frames_dir, f"frame_{i}.png")
        result_frame.save(result_frame_path, optimize=True, quality=video_quality)
