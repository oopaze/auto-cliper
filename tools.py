from os import listdir, mkdir, remove
from random import choice

from pytube import YouTube
from slugify import slugify

CLIP_DURATION = 65


def normalize_filename(filename):
    return filename.replace(":", " -")


def generate_clips(video, video_mixer, start_at=0, end_at=float("inf")):
    if end_at is None:
        end_at = float("inf")

    if end_at <= start_at:
        raise ValueError("start_at should be less than end_at")

    length_in_seconds = int(video.vid_info["videoDetails"]["lengthSeconds"])
    amount_of_clips_monetized = length_in_seconds // CLIP_DURATION
    amount_of_clips = length_in_seconds / CLIP_DURATION

    if end_at < amount_of_clips_monetized:
        amount_of_clips_monetized = end_at

    if end_at < amount_of_clips:
        amount_of_clips = end_at

    path = f"{get_video_folder_name(video)}/clips"
    paths = []

    for i in range(start_at, amount_of_clips_monetized):
        clip_start_at = CLIP_DURATION * i
        clip_end_at = CLIP_DURATION * (i + 1)
        full_file_path = f"{path}/{normalize_filename(video.title)} - Parte {i + 1}.mp4"
        video_mixer.save([clip_start_at, clip_end_at], full_file_path)
        paths.append(full_file_path)

    last_clip_parcel = (amount_of_clips - amount_of_clips_monetized)
    if (last_clip_parcel > 0.2):
        full_file_path = f"{path}/{normalize_filename(video.title)} - Parte {i + 2}.mp4"
        video_mixer.save([clip_end_at, length_in_seconds - 1], full_file_path)
        paths.append(full_file_path)

    return paths


def get_video_folder_name(video):
    return f"youtube-videos/{slugify(video.title)}"


def download_video(vlink):
    video = YouTube(vlink)
    full_filepath = video.streams.get_highest_resolution().download(
        get_video_folder_name(video), filename_prefix="[ORIGINAL] - "
    )

    if "clips" not in listdir(get_video_folder_name(video)):
        mkdir(f"{get_video_folder_name(video)}/clips")

    return {"instance": video, "filepath": full_filepath}


def get_random_satisfying_video():
    satisfying_videos = listdir("satisfying-videos")
    return "satisfying-videos/" + choice(satisfying_videos)


def clean_temp_files():
    tmp_files = listdir("tmp")

    for file in tmp_files:
        remove("tmp/" + file)
