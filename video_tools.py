from moviepy.editor import CompositeVideoClip, VideoFileClip
from moviepy.video.fx.all import crop

from tools import CLIP_DURATION, get_random_satisfying_video


class SubtitlesGenerator:
    ...


class VideoMixer:
    SCREEN_WIDTH = 540
    SCREEN_HEIGHT = 960

    subtitles_generator = SubtitlesGenerator()

    def __init__(self):
        self.video_clip = None
        self.full_clip = None
        self.subtitles_clip = None

    @property
    def satisfying_clip(self):
        return VideoFileClip(get_random_satisfying_video())

    def save(self, clip_range, filename):
        if self.full_clip is None:
            raise ValueError("You need to generate video before save")

        main_clip = self.full_clip.subclip(*clip_range)
        satisfying_clip = self.get_normalized_video(False, duration=main_clip.duration)

        clips_array = [main_clip, satisfying_clip]
        size = (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        return CompositeVideoClip(clips_array, size=size).write_videofile(filename)

    def generate_video(self, full_video_filename):
        self.video_clip = VideoFileClip(full_video_filename)

        self.full_clip = self.get_normalized_video()
        return self

    def get_normalized_video(self, is_main=True, duration=CLIP_DURATION):
        height_diff = +60 if is_main else -60
        position = "top" if is_main else "bottom"
        video_clip = self.video_clip if is_main else self.satisfying_clip

        clip = crop(
            video_clip,
            width=self.SCREEN_WIDTH,
            height=(self.SCREEN_HEIGHT / 2) + height_diff,
            x_center=video_clip.size[0] / 2,
            y_center=video_clip.size[1] / 2,
        ).set_position(position)

        if not is_main:
            clip = clip.without_audio().set_duration(duration)

        return clip
