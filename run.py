from main import generate_clips_from_video
from youtube_tools import YVideoStorage

video_storage = YVideoStorage()

video_storage.add_video(
    "science",
    "https://www.youtube.com/watch?v=PMWhNBDNKHk",
    "#interestelar #marte #viagem #sacani",
    start_at=1,
    end_at=4,
    clip_start_delay=0
)

video_storage.add_video(
    "podflow",
    "https://www.youtube.com/watch?v=yiPS8vlETPM",
    "#podpah #faturamento #salario #eua #forbes",
    end_at=2,
    clip_start_delay=2
)


if __name__ == "__main__":
    threads = []

    for account, video_url, extra_hashtags, start_at, end_at, clip_start_delay in video_storage:
        generate_clips_from_video(
            video_url, account,
            threads=threads,
            perform_upload=True,
            extra_hashtags=extra_hashtags,
            start_at=start_at,
            end_at=end_at,
            start_delay=clip_start_delay
        )

    for t in threads:
        t.join()
