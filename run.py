from functools import partial
from threading import Thread

from selenium_tools import upload_videos
from tools import download_video, generate_clips
from video_tools import VideoMixer

VIDEO_URLS = [
    ("science", "https://www.youtube.com/watch?v=oEGwIa1KTGk"),
    ("science", "https://www.youtube.com/watch?v=jpeteuPq1-I"),
    ("podflow", "https://www.youtube.com/watch?v=QPxmjFKOcXY"),
    ("podflow", "https://www.youtube.com/watch?v=Wb1dFURkUqw")
]

video_mixer = VideoMixer()
perform_upload = True

if __name__ == "__main__":
    threads = []

    for account, video_url in VIDEO_URLS:
        video = download_video(video_url)
        mixed_video = video_mixer.generate_video(video["filepath"])
        paths = generate_clips(video["instance"], mixed_video)

        if perform_upload:
            uploader = Thread(target=partial(upload_videos, clips=paths, account=account, stop_flag=1))
            uploader.start()
            threads.append(uploader)

    for t in threads:
        t.join()
