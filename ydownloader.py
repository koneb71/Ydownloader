import youtube_dl
import sys

import re
from pytube import YouTube

total_argv = len(sys.argv)
cmdargs = str(sys.argv)


class Ydownloader:
    def __init__(self, link):
        self.link = link
        self.youtube_link = YouTube(link)

    def get_available_format(self):
        return self.youtube_link.get_videos()

    def print_list(self):
        for index, link in enumerate(self.get_available_format()):
            print(str(index) + ': ' + str(link))
        print('mp3: audio only')

    def download(self, info):
        video = self.youtube_link.get(info['format'], info['resolution'])
        video.download('')

    def get_format_and_resolution(self, index):
        selected = str(self.get_available_format()[index]).split(' ')
        format_re = re.compile("(\(\.?(.*))")
        resolution_re = re.compile('\d+p')

        return {'format': ''.join(filter(format_re.match, selected)).replace('(.', '').replace(')', ''),
                'resolution': ''.join(filter(resolution_re.match, selected))}

    def download_mp3(self):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.link])

    def run(self):
        running = True
        while running:
            self.print_list()
            scan = input("Select: ")
            try:
                if ''.join(scan) == 'mp3':
                    self.download_mp3()
                else:
                    get_info = self.get_format_and_resolution(int(scan))
                    self.download(get_info)
            except:
                sys.exit('Wrong Input')


if __name__ == "__main__":
    if total_argv == 2:
        yt = Ydownloader(sys.argv[1])
        yt.run()
    else:
        print("usage: %s YOUTUBELINK" % sys.argv[0])
        sys.exit(2)
