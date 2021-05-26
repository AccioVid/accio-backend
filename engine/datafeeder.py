import sys
sys.path.append('./')

import time
import glob
import os
import cv2
from api import VideosModel


class DataFeeder:
    def __init__(self, repository_path):
        if not os.path.exists(repository_path):
            raise Exception('Repository not found')
        self.repository_path = repository_path

    def __get_duration(self, url):
        cap = cv2.VideoCapture(url)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count/fps
        return duration

    def run(self):
        files = glob.glob(self.repository_path + '/*.mp4')
        new_videos = []
        for url in files:
            video = VideosModel.query.filter_by(url=url).first()
            if not video:
                VideosModel(url.split('/')[-1], self.__get_duration(url), url).save()
                new_videos.append(url)
        if new_videos:
            print(f'Added: {new_videos}')
        else:
            print(f'DB is already synced with videos repository')

"""
v = VideosModel("test", 50, "url", results={"key": "value", "test": {"key2": "value2"}})

"""

if __name__ == '__main__':
    # python python engine/datafeeder.py ./repository
    repository_path = sys.argv[1] if len(sys.argv) > 1 else './repository'
    df = DataFeeder(repository_path)
    while True:
        print("DataFeeder started execution")
        df.run()
        for remaining in range(60, -1, -1):
            sys.stdout.write("\r")
            sys.stdout.write("{:2d} seconds remaining.".format(remaining))
            sys.stdout.flush()
            time.sleep(1)
        print("")