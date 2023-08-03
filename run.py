from main import generate_clips_from_video

VIDEO_URLS = [
    ("podflow", "https://www.youtube.com/watch?v=4bWJcUxSd8U", "#cristiano #papaicris #futebol #psicopata"),
    ("podflow", "https://www.youtube.com/watch?v=ntnCRHnvI0I", "#marinasena #igao #ombrin #brinca-no-chao #love")
]

if __name__ == "__main__":
    threads = []

    for account, video_url, extra_hashtags in VIDEO_URLS:
        generate_clips_from_video(video_url, account, threads=threads, perform_upload=True, start_at=0, end_at=2)

    for t in threads:
        t.join()
