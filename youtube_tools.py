class YVideoStorage:
    def __init__(self) -> None:
        self.videos: list[YVideo] = []

    def add_video(self, channel, url, extra_hashtags="", start_at=0, end_at=float("inf")):
        self.videos.append(YVideo(channel, url, extra_hashtags, start_at, end_at))

    def __iter__(self):
        for video in self.videos:
            yield video


class YVideo:
    def __init__(self, channel, url, extra_hashtags, start_at, end_at):
        self.channel = channel
        self.url = url
        self.extra_hashtags = extra_hashtags
        self.start_at = start_at
        self.end_at = end_at

    def __iter__(self):
        list_conf = [self.channel, self.url, self.extra_hashtags, self.start_at, self.end_at]

        for item_conf in list_conf:
            yield item_conf
