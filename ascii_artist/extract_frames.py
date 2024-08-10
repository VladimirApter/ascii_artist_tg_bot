import cv2
import os


def extract_frames_from_video(video_path, output_folder, prefix='frame', format='png'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)

    success = True
    index = 0
    while success:
        success, frame = video.read()
        if success:
            file_name = f"{prefix}_{index}.{format}"
            full_path = os.path.join(output_folder, file_name)
            cv2.imwrite(full_path, frame)
            index += 1

    video.release()

    return index, fps
