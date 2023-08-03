from main import generate_clips_from_video

VIDEO_URLS = [
    ("science", "https://www.youtube.com/watch?v=rgUT9jeNl_E", "#sacani #terra #plana #xandao #cientista", 0, 3)
]

if __name__ == "__main__":
    threads = []

    for account, video_url, extra_hashtags, start_at, end_at in VIDEO_URLS:
        generate_clips_from_video(
            video_url, account,
            threads=threads,
            perform_upload=True,
            extra_hashtags=extra_hashtags,
            start_at=start_at,
            end_at=end_at
        )

    for t in threads:
        t.join()
