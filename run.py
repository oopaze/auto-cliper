from main import generate_clips_from_video
from youtube_tools import YVideoStorage

video_storage = YVideoStorage()

video_storage.add_video("science", "https://youtu.be/du9gFOMaz8c", "#dinossauro #extincao #sacani #inteligencialtda")
video_storage.add_video("podflow", "https://youtu.be/r04n-PQxbWI", "#rodrygo #igao #gordofobia #academia", end_at=2)
video_storage.add_video(
    "podflow",
    "https://youtu.be/ZDEptuy7D9s",
    "#panico #silvio #carioca #ronaldo #fenomeno",
    end_at=2
)

if __name__ == "__main__":
    threads = []

    for account, video_url, extra_hashtags, start_at, end_at in video_storage:
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
