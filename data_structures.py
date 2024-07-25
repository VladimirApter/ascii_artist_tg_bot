from enum import Enum


class Mode(Enum):
    regular = 0
    true_color = 1


class TutorialPhase(Enum):
    first = 0
    second = 1


class Orientation(Enum):
    horizontal = 0
    vertical = 1


class PhotoData:
    def __init__(self, file_id: int, file_path: str,
                 result_path: str, orientation: Orientation):
        self.file_id = file_id
        self.file_path = file_path
        self.result_path = result_path
        self.orientation = orientation

    @property
    def max_height(self):
        return 600 if self.orientation == Orientation.horizontal else 1000


class VideoData:
    def __init__(self, file_id: int, file_path: str,
                 result_path: str, orientation: Orientation):
        self.file_id = file_id
        self.file_path = file_path
        self.result_path = result_path
        self.orientation = orientation

    @property
    def max_height(self):
        return 100 if self.orientation == Orientation.horizontal else 200


class UserData:
    first_time: bool
    media: PhotoData | VideoData | None
    mode: Mode | None
    tutorial_phase: TutorialPhase | None
    height: int | None
    symbols: str | None
    bg_color = None
    font_color = None

    def __init__(self, first_time: bool):
        self.first_time = first_time
        self.media = None
        self.mode = None
        self.tutorial_phase = None
        self.height = None
        self.symbols = None
        self.bg_color = None
        self.font_color = None

    @property
    def russian_file_type(self):
        return 'фото' if isinstance(self.media, PhotoData) else 'видео'

    @property
    def russian_orientation(self):
        return 'горизонтального' if self.media.orientation == Orientation.horizontal else 'вертикального'
