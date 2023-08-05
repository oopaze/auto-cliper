from re import sub
from uuid import uuid4

from moviepy.editor import (AudioFileClip, CompositeVideoClip, TextClip,
                            VideoFileClip)
from moviepy.video.fx.all import crop, resize
from moviepy.video.tools.subtitles import SubtitlesClip
from stable_whisper import modify_model
from whisper import load_model

from tools import CLIP_DURATION, get_random_satisfying_video


class SubtitlesGenerator:
    MAX_CHARS_PER_SEGMENT = 35
    MAX_WORDS_PER_SEGMENT = 7

    def __init__(self):
        self.model = load_model("small")
        modify_model(self.model)

    def generate(self, audio_clip, with_satisfying=True):
        filepath = self.save_separed_audio(audio_clip)
        result_subtitles = self.model.transcribe(filepath, language="pt", vad=True)
        result_subtitles = result_subtitles.split_by_length(
            max_chars=self.MAX_CHARS_PER_SEGMENT,
            max_words=self.MAX_WORDS_PER_SEGMENT
        )
        normalized_subtitle = self.normalize_result(result_subtitles)

        y_pos = VideoMixer.SCREEN_HEIGHT // 2 if with_satisfying else VideoMixer.SCREEN_HEIGHT - 200
        return SubtitlesClip(normalized_subtitle, self.subtitle_generator) \
            .set_position(("center", y_pos))

    def subtitle_generator(self, text):
        default_params = {
            "txt": text,
            "method": "caption",
            "font": "Acherus-Grotesque-Bold",  # Geometos-Rounded or Acherus-Grotesque-Bold
            "fontsize": 30,
            "align": "center",
            "size": (VideoMixer.SCREEN_WIDTH - VideoMixer.HEIGHT_DIFF, None)
        }

        outerTextClip = TextClip(**default_params, color="black", stroke_color="black", stroke_width=2)
        innerTextClip = TextClip(**default_params, color="yellow")
        return CompositeVideoClip([outerTextClip, innerTextClip])

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

    def save(self, clip_range, filename, with_satisfying=True):
        if self.full_clip is None:
            raise ValueError("You need to generate video before save")

        main_clip = self.full_clip.subclip(*clip_range)
        subtittle_clip = self.subtitles_generator.generate(main_clip.audio, with_satisfying)
        clips_array = [main_clip, subtittle_clip]

        if with_satisfying:
            satisfying_clip = self.get_satisfying_clip(main_clip.duration)
            clips_array.insert(0, satisfying_clip)

        size = (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        return CompositeVideoClip(clips_array, size=size).write_videofile(filename)

    def generate_video(self, full_video_filename, with_satisfying=True):
        self.video_clip = VideoFileClip(full_video_filename)
        self.full_clip = self.get_normalized_video(with_satisfying=with_satisfying)
        return self

    def get_normalized_video(self, with_satisfying=True):
        video_clip = self.video_clip

        height = video_clip.size[1]
        width = (video_clip.size[1] / 16) * 9

        if with_satisfying:
            height = (self.SCREEN_HEIGHT / 2) + self.HEIGHT_DIFF
            width = self.SCREEN_WIDTH

        clip = crop(
            video_clip,
            width=width,
            height=height,
            x_center=video_clip.size[0] / 2,
            y_center=video_clip.size[1] / 2
        )

        if not with_satisfying:
            size = (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
            clip = resize(clip, size)

        return clip.set_position("top" if with_satisfying else "center")

    def get_satisfying_clip(self, duration=CLIP_DURATION):
        video_clip = VideoFileClip(get_random_satisfying_video())

        return crop(
            video_clip,
            width=self.SCREEN_WIDTH,
            height=(self.SCREEN_HEIGHT / 2) - self.HEIGHT_DIFF,
            x_center=video_clip.size[0] / 2,
            y_center=video_clip.size[1] / 2,
        ).set_position("bottom").without_audio().set_duration(duration)
