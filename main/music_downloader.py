import urllib.request
import re
import urllib.parse
import youtube_dl

from ytmbot.main.settings import MP3_FILE_OPTIONS, MAIN_FILE_PATH, YOUTUBE_SEARCH_LINK, YOUTUBE_WATCH_LINK


def download_music_file(url: str) -> str:
    with youtube_dl.YoutubeDL(MP3_FILE_OPTIONS) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        filename = f'{MAIN_FILE_PATH}\\audio\\{info_dict.get("title", None)}.webm'
        ydl.download([url])

    return filename


def search(search_keyword: str) -> str:
    url = YOUTUBE_SEARCH_LINK + urllib.parse.quote(search_keyword)
    html = urllib.request.urlopen(url)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    url = YOUTUBE_WATCH_LINK + video_ids[0]

    return url


def prepare_search_keywords(words: tuple) -> str:
    search_keywords = '+'
    search_keywords = search_keywords.join(words)

    return search_keywords
