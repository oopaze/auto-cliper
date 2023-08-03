from re import sub
from uuid import uuid4

from moviepy.editor import (AudioFileClip, CompositeVideoClip, TextClip,
                            VideoFileClip)
from moviepy.video.fx.all import crop
from moviepy.video.tools.subtitles import SubtitlesClip
from stable_whisper import modify_model
from whisper import load_model

from tools import CLIP_DURATION, get_random_satisfying_video


class SubtitlesGenerator:
    def __init__(self):
        self.model = load_model("small")
        modify_model(self.model)

    def generate(self, audio_clip):
        filepath = self.save_separed_audio(audio_clip)
        result_subtitles = self.model.transcribe(filepath, language="pt", vad=True)
        normalized_subtitle = self.normalize_result(result_subtitles)
        return SubtitlesClip(normalized_subtitle, self.subtitle_generator).set_position("center")

    def subtitle_generator(self, text):
        return TextClip(
            text,
            method="caption",
            font="Acherus-Grotesque-Bold",  # Geometos-Rounded or Acherus-Grotesque-Bold
            fontsize=30,
            align="center",
            color="yellow",
            size=(VideoMixer.SCREEN_WIDTH - VideoMixer.HEIGHT_DIFF, None)
        )

    def normalize_result(self, result_subtitles):
        normalized_subtitle = []

        for segment in result_subtitles.segments:
            normalized_subtitle.append(((segment.start, segment.end), segment.text))

        return normalized_subtitle

    def normalize_text(self, text):
        return sub(r'[^\w]', ' ', text).replace("  ", " ")

    def save_separed_audio(self, audio_clip: AudioFileClip):
        filepath = f"tmp/{uuid4()}.mp3"
        audio_clip.write_audiofile(filepath)
        return filepath


class VideoMixer:
    SCREEN_WIDTH = 540
    SCREEN_HEIGHT = 960
    HEIGHT_DIFF = 60

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
        subtittle_clip = self.subtitles_generator.generate(main_clip.audio)

        clips_array = [main_clip, subtittle_clip, satisfying_clip]
        size = (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        return CompositeVideoClip(clips_array, size=size).write_videofile(filename)

    def generate_video(self, full_video_filename):
        self.video_clip = VideoFileClip(full_video_filename)

        self.full_clip = self.get_normalized_video()
        return self

    def get_normalized_video(self, is_main=True, duration=CLIP_DURATION):
        height_diff = +self.HEIGHT_DIFF if is_main else -self.HEIGHT_DIFF
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
