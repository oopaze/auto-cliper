from functools import partial
from threading import Thread

from selenium_tools import upload_videos
from tools import clean_temp_files, download_video, generate_clips
from video_tools import VideoMixer
from youtube_tools import CLIP_START_DELAY

video_mixer = VideoMixer()


def generate_clips_from_video(
    video_url,
    account,
    threads=None,
    perform_upload=False,
    start_at=0,
    end_at=None,
    extra_hashtags="",
    start_delay=CLIP_START_DELAY,
    with_satisfying=True
):
    if perform_upload and threads is None:
        raise ValueError("You need to pass a list to store threads to perform upload")

    video = download_video(video_url)
    mixed_video = video_mixer.generate_video(video["filepath"], with_satisfying=with_satisfying)
    paths = generate_clips(
        video["instance"],
        mixed_video,
        start_at=start_at,
        end_at=end_at,
        clip_start_delay=start_delay,
        with_satisfying=with_satisfying
    )
    clean_temp_files()

    if perform_upload:
        upload_kwargs = {"clips": paths, "account": account, "start_flag": start_at, "extra_hashtags": extra_hashtags}

        if end_at:
            upload_kwargs["stop_flag"] = end_at

        uploader = Thread(target=partial(upload_videos, **upload_kwargs))
        uploader.start()
        threads.append(uploader)
