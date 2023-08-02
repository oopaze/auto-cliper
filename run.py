from functools import partial
from threading import Thread

from selenium_tools import upload_videos
from tools import download_video, generate_clips
from video_tools import VideoMixer

VIDEO_URLS = [
    ("podflow", "https://www.youtube.com/watch?v=hWgz_KMBmngpy"),
    ("podflow", "https://www.youtube.com/watch?v=oy96txJnAhM")
]

video_mixer = VideoMixer()

if __name__ == "__main__":
    threads = []

    for account, video_url in VIDEO_URLS:
        video = download_video(video_url)
        mixed_video = video_mixer.generate_video(video["filepath"])
        paths = generate_clips(video["instance"], mixed_video)

        uploader = Thread(target=partial(upload_videos, clips=paths, account=account))
        uploader.start()
        threads.append(uploader)

    for t in threads:
        t.join()
