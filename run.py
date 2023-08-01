from tools import download_video, generate_clips
from video_tools import VideoMixer

VIDEO_URLS = ["https://www.youtube.com/watch?v=RJq3dSQxtSc"]

video_mixer = VideoMixer()

if __name__ == "__main__":
    for video_url in VIDEO_URLS:
        video = download_video(video_url)
        mixed_video = video_mixer.generate_video(video["filepath"])
        generate_clips(video["instance"], mixed_video)
