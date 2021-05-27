import argparse
import sys
import time
sys.path.append('./')

from engine.keyframes import KeyFrameExtractor
from api import VideosModel, PluginsModel

class EngineManager:
    def __init__(self):
        pass

    def _import(self, name):
        components = name.split('.')
        mod = __import__(components[0])
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod

    def run(self, limit):
        keyframe_extractor = KeyFrameExtractor()
        videos = VideosModel.query.filter_by(processed=False).limit(limit)
        plugins_records = PluginsModel.query.filter_by(is_enabled=True)
        videos_results = {}
        for plugin_record in plugins_records:
            print(f'plugin {plugin_record} running')

            plugin = self._import(plugin_record.executable_path)(plugin_record.plugin_configuration)
            config = plugin_record.system_configuration
            for video in videos:
                results = []
                if config.get('keyframes_enabled'):
                    key_frames_path = f'./key_frames/{video.name}/'
                    frames_data = keyframe_extractor.significant_change_detect(video.url, key_frames_path, config.get('keyframes_threshold'), True)
                    for frame in frames_data.frames_list:
                        detections = plugin.run(frame.get('path'))
                        if detections:
                            results.append({'at': frame.get('at'), 'results': detections})
                else:
                    results.append(plugin.run(video.url))
                
                print(f'plugin results {results}')
                videos_results[video] = videos_results.get(video, []) + results
        
        for video, results in videos_results.items():
            video.processed = True
            video.results = list(results)
            video.save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", help="Number of videos to be processed at a time")
    parser.add_argument("--sleeptime", help="Cronjob interval")
    args = parser.parse_args()
    engine = EngineManager()

    try:
        while True:
            engine.run(args.limit if args.limit else 2)
            import ipdb; ipdb.set_trace()
            for remaining in range(int(args.sleeptime) if args.sleeptime else 60, -1, -1):
                sys.stdout.write("\r")
                sys.stdout.write("{:2d} seconds remaining.".format(remaining))
                sys.stdout.flush()
                time.sleep(1)
            print("")
    except KeyboardInterrupt:
        print("\n===========\nEngine terminated.\nBye!")
        sys.exit()

