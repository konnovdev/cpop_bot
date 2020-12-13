import os
import logging
from youtube_dl import YoutubeDL
from urllib.parse import urlparse
from urllib.request import Request
from urllib.request import urlopen
from PIL import Image
import config

DOWNLOAD_DIR = config.DOWNLOAD_DIR

logger = logging.getLogger(__name__)


class WrongCategoryError(ValueError):
    pass


class WrongFileSizeError(ValueError):
    pass


class MusicDownloader:

    def download(self, input_url, filesize_limit):
        ydl_opts = {
                'format': 'bestaudio[protocol^=http]',
                'outtmpl': DOWNLOAD_DIR + '%(extractor)s_%(id)s.%(ext)s',
                'writethumbnail': True
        }
        ydl = YoutubeDL(ydl_opts)
        info = ydl.extract_info(input_url, download=False)
        webpage_info = info['extractor'] + " " + info['id']
        info_format = next((item for item in info['formats']
                            if item['format_id'] == info['format_id']),
                           None)

        if self.__youtubeVideoNotMusic(info):
            raise WrongCategoryError(webpage_info +
                                     ": not under Music category")

        audio_filesize = self.__getFileSize(info_format)
        if int(audio_filesize) < filesize_limit:
            logger.info(webpage_info + ": downloading...")
            ydl.process_info(info)
            info = self.__addDownloadsToInfoDict(info)
            if self.__filesSuccessfullyDownloaded(info['downloads']):
                return info
            else:
                self.__deleteDownloadedFiles(info['downloads'])
                raise ValueError(webpage_info +
                                 ": failed to download audio or thumbnail")
        else:
            raise WrongFileSizeError(webpage_info + ": audio file size (" +
                                     str(audio_filesize) + ") is greater" +
                                     "than the limit: (" +
                                     str(filesize_limit) + ")")

    def __youtubeVideoNotMusic(self, info):
        if info['extractor'] == 'youtube' and \
                'Music' not in info['categories']:
            return True
        else:
            return False

    def __getFileSize(self, info_format):
        if 'filesize' in info_format:
            audio_filesize = info_format['filesize']
        else:
            audio_url = info_format['url']
            http_headers = info_format['http_headers']
            request_head = Request(audio_url, method='HEAD',
                                   headers=http_headers)
            audio_filesize = urlopen(request_head).headers['Content-Length']
        return audio_filesize

    def __addDownloadsToInfoDict(self, info):
        webpage_id = info['id']
        extractor = info['extractor']
        thumbnail_url = info['thumbnail']
        basename = DOWNLOAD_DIR + extractor + '_' + webpage_id
        thumbnail_file = basename + "." + \
            self.__getFileExtensionFromUrl(thumbnail_url)
        audio_file = basename + '.' + info['ext']
        info['downloads'] = {
                'audio': audio_file,
                'thumbnail': thumbnail_file
        }
        return info

    def __filesSuccessfullyDownloaded(self, info_downloads):
        return all(os.path.isfile(f) for f in info_downloads.values())

    def __deleteDownloadedFiles(self, info_downloads):
        for f in info_downloads.values():
            try:
                os.remove(f)
            except OSError:
                pass

    def __getFileExtensionFromUrl(self, url):
        url_path = urlparse(url).path
        basename = os.path.basename(url_path)
        ext = basename.split(".")[-1]
        return ext


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
        left = (width - length)/2
        top = (height - length)/2
        right = (width + length)/2
        bottom = (height + length)/2
        return img.crop((left, top, right, bottom))
