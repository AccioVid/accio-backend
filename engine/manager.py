"""
- query one unprocessed video
- multiple plugins
    - query enabled from db
    - load from executable_path
    - extract keyframes
        - consider threshold
    - 
- update video to be processed (not scalable)
"""

import sys
sys.path.append('./')

import glob
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

    def run(self):
        keyframe_extractor = KeyFrameExtractor()
        videos = VideosModel.query.filter_by(processed=False)
        plugins_records = PluginsModel.query.filter_by(is_enabled=True)
        # plugins = [self._import(p.executable_path)(p.plugin_configuration) for p in plugins_records]
        videos_results = {}
        for plugin_record in plugins_records:
            print(f'plugin {plugin_record} running')

            plugin = self._import(plugin_record.executable_path)(plugin_record.plugin_configuration)
            config = plugin_record.system_configuration
            for video in videos:
                results = []
                if config.get('keyframes_enabled'):
                    # import ipdb; ipdb.set_trace()
                    key_frames_path = f'./key_frames/{video.name}/'
                    # frames_data = keyframe_extractor.significant_change_detect(video.url, key_frames_path, config.get('keyframes_threshold'), True)
                    frames_data = keyframe_extractor.significant_change_detect(video.url, key_frames_path, 0.7, True)
                    # import ipdb; ipdb.set_trace()
                    for frame in frames_data.frames_list:
                        detections = plugin.run(frame.get('path'))
                        if detections:
                            results.append({'at': frame.get('at'), 'results': detections})
                else:
                    results.append(plugin.run(video.url))
                
                print(f'plugin results {results}')
                # video.results.append(results)
                # video.save()
                videos_results[video] = videos_results.get(video, []) + results
        
        for video, results in videos_results.items():
            import ipdb; ipdb.set_trace()
            video.processed = True
            video.results = list(results)
            video.save()

            
        

obj = EngineManager()
obj.run()
videos = VideosModel.query.filter_by(processed=True)
# klass = obj._import('plugins.yolo_object_detection.yolo.YoloPlugin')
import ipdb; ipdb.set_trace()
# plugins[1].plugin_configuration = {"confidence" : 0.5, "threshold" : 0.3}
# plugins[0].plugin_configuration = {'encodings_path': 'plugins/facedetection/the_office.pkl'}