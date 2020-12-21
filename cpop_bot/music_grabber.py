import os
import logging
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from youtube_dl import YoutubeDL
from PIL import Image
from config import DOWNLOAD_DIR

logger = logging.getLogger(__name__)


class WrongCategoryError(ValueError):
    pass


class WrongFileSizeError(ValueError):
    pass


class MusicDownloader:

    def download(self, input_url, filesize_limit):
        input_url = input_url.split('&list', 1)[0]
        ydl_opts = {
            'format': 'bestaudio[protocol^=http]',
            'logger': logger,
            'outtmpl': DOWNLOAD_DIR
            + '%(title)s - %(extractor)s-%(id)s.%(ext)s',
            'writethumbnail': True
        }
        ydl = YoutubeDL(ydl_opts)
        info = ydl.extract_info(input_url, download=False)
        webpage_info = info['extractor'] + " " + info['id']
        info_format = next((item for item in info['formats']
                            if item['format_id'] == info['format_id']),
                           None)

        if self.youtube_video_not_music(info):
            raise WrongCategoryError(webpage_info
                                     + ": not under Music category")

        audio_filesize = self.__get_filesize(info_format)
        if int(audio_filesize) > filesize_limit:
            raise WrongFileSizeError(webpage_info + ": audio file size ("
                                     + str(audio_filesize) + ") is greater"
                                     + "than the limit: ("
                                     + str(filesize_limit) + ")")

        logger.info("%s: downloading...", webpage_info)
        ydl.process_info(info)
        info = self.__add_downloads_to_info_dict(info, ydl_opts)
        if not self.__files_successfully_downloaded(info['downloads']):
            self.__delete_downloaded_files(info['downloads'])
            raise ValueError(webpage_info
                             + ": failed to download audio or thumbnail")
        return info

    def youtube_video_not_music(self, info):
        if info['extractor'] == 'youtube' and \
                'Music' not in info['categories']:
            return True
        return False

    def __get_filesize(self, info_format):
        if 'filesize' in info_format:
            audio_filesize = info_format['filesize']
        else:
            audio_url = info_format['url']
            http_headers = info_format['http_headers']
            request_head = Request(audio_url, method='HEAD',
                                   headers=http_headers)
            audio_filesize = urlopen(request_head).headers['Content-Length']
        return audio_filesize

    def __add_downloads_to_info_dict(self, info, ydl_opts):
        thumbnail_url = info['thumbnail']
        audio_file = YoutubeDL(ydl_opts).prepare_filename(info)
        thumbnail_file = audio_file.rsplit(".", 1)[-2] + "." + \
            self.__get_file_extension_from_url(thumbnail_url)
        info['downloads'] = {
            'audio': audio_file,
            'thumbnail': thumbnail_file
        }
        return info

    def __files_successfully_downloaded(self, info_downloads):
        return all(os.path.isfile(f) for f in info_downloads.values())

    def __delete_downloaded_files(self, info_downloads):
        for f in info_downloads.values():
            try:
                os.remove(f)
            except OSError:
                pass

    def __get_file_extension_from_url(self, url):
        url_path = urlparse(url).path
        basename = os.path.basename(url_path)
        return basename.split(".")[-1]


class SquarethumbMaker:

    # https://stackoverflow.com/a/52177551
    def make_squarethumb(self, thumbnail, output):
        original_thumb = Image.open(thumbnail)
        squarethumb = self.__crop_to_square(original_thumb)
        squarethumb.thumbnail((320, 320), Image.ANTIALIAS)
        squarethumb.save(output)

    def __crop_to_square(self, img):
        width, height = img.size
        length = min(width, height)
        left = (width - length) / 2
        top = (height - length) / 2
        right = (width + length) / 2
        bottom = (height + length) / 2
        return img.crop((left, top, right, bottom))
