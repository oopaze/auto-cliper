from main import generate_clips_from_video

if __name__ == "__main__":
    VIDEO_URLS = [
        (
            "science",
            "https://www.youtube.com/watch?v=juh0Kj7N04I&t=91s",
            "#marimaria #igao #laurabrito #mitico #fica #namoro",
            0,
            2
        )
    ]
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
