import cv2
import os


def create_and_save_video(frames_dir, result_path, prefix, img_format, fps=30):
    images = [img for img in os.listdir(frames_dir) if img.startswith(prefix) and img.endswith(img_format)]
    images.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))

    load_symbols = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]

    frames = []
    for i in range(len(images)):
        symbol = load_symbols[(i // 10) % len(load_symbols)]

        frames.append(cv2.imread(os.path.join(frames_dir, images[i])))

    max_width = 0
    max_height = 0
    for i in range(len(frames)):
        symbol = load_symbols[(i // 10) % len(load_symbols)]

        height, width, _ = frames[i].shape
        if width > max_width:
            max_width = width
        if height > max_height:
            max_height = height

    video = cv2.VideoWriter(result_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (max_width, max_height))

    for i in range(len(frames)):
        symbol = load_symbols[(i // 10) % len(load_symbols)]

        video.write(cv2.resize(frames[i], (max_width, max_height)))

    video.release()
