from os import listdir, mkdir
from random import choice

from pytube import YouTube
from slugify import slugify

CLIP_DURATION = 65


def generate_clips(video, video_mixer):
    length_in_seconds = int(video.vid_info["videoDetails"]["lengthSeconds"])
    amount_of_clips_monetized = length_in_seconds // CLIP_DURATION

    path = f"{get_video_folder_name(video)}/clips"

    for i in range(0, amount_of_clips_monetized):
        clip_start_at = CLIP_DURATION * i
        clip_end_at = CLIP_DURATION * (i + 1)
        video_mixer.save([clip_start_at, clip_end_at], f"{path}/{video.title} - Parte {i + 1}.mp4")

    last_clip_parcel = (length_in_seconds / CLIP_DURATION - amount_of_clips_monetized)
    if (last_clip_parcel > 0.2):
        video_mixer.save([clip_end_at, length_in_seconds - 1], f"{path}/{video.title} - Parte {i + 2}.mp4",)

    return path


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
