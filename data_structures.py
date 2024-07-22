from enum import Enum


class PhotoData:
    def __init__(self, file_id: int, file_path: str, result_path: str):
        self.file_id = file_id
        self.file_path = file_path
        self.result_path = result_path


class VideoData:
    def __init__(self, file_id: int, file_path: str, result_path: str):
        self.file_id = file_id
        self.file_path = file_path
        self.result_path = result_path


class Mode(Enum):
    regular = 0
    true_color = 1


class TutorialPhase(Enum):
    first = 0
    second = 1


class FileType(Enum):
    photo = 0
    video = 1


class UserData:
    file_type: FileType
    first_time: bool
    media: PhotoData | VideoData | None
    mode: Mode | None
    tutorial_phase: TutorialPhase | None
    height: int | None
    symbols: str | None
    bg_color = None
    font_color = None

    def __init__(self, file_type: FileType, first_time: bool):
        self.file_type = file_type
        self.first_time = first_time
        self.media = None
        self.mode = None
        self.tutorial_phase = None
        self.height = None
        self.symbols = None
        self.bg_color = None
        self.font_color = None
